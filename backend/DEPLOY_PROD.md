# Django 后端服务生产化部署方案

## 概述

本文档描述将 Django 后端服务部署到生产环境的完整方案。部署环境为虚拟机服务器（IP: 192.168.11.162），采用宿主机直接部署方式（Nginx + Gunicorn），MySQL 8.0 通过 Docker 运行在端口 3308。

## 部署架构

```
┌─────────────────────────────────────────┐
│         虚拟机服务器 (192.168.11.162)      │
│                                         │
│  ┌──────────────┐    ┌──────────────┐  │
│  │   Nginx      │───▶│  Django App  │  │
│  │  (反向代理)   │    │  (Gunicorn)  │  │
│  │   Port: 80   │    │  Port: 8000  │  │
│  └──────────────┘    └──────────────┘  │
│         │                    │          │
│         │                    └──────────┼──▶ MySQL 8.0
│         │                              │    (Docker)
│         │                              │    Port: 3308
│         └──────────────────────────────┘
│
│  数据持久化:                              │
│  - /opt/risk-monitoring/backend/backend/media (媒体文件) │
│  - /opt/risk-monitoring/backend/backend/logs (日志文件) │
│  - /opt/risk-monitoring/backend/backend/staticfiles (静态文件) │
└─────────────────────────────────────────┘
```

## 技术选型

- **部署方式**: 宿主机直接部署（非容器化）
- **WSGI 服务器**: Gunicorn（生产环境推荐）
- **进程管理**: Systemd
- **反向代理**: Nginx（用于静态文件服务和反向代理）
- **数据库**: MySQL 8.0（通过 Docker 运行）
- **Python 版本**: 3.11
- **Django 版本**: 5.2.8

## 需要创建的文件

### 1. .env.prod
生产环境环境变量文件，包含：
- SECRET_KEY
- DEBUG=False
- ALLOWED_HOSTS
- 数据库连接配置（指向 192.168.11.162:3308）
- 其他生产环境配置

### 2. gunicorn_config.py
Gunicorn 配置文件，包含：
- 工作进程数
- 绑定地址和端口
- 日志配置
- 超时设置

### 3. Nginx 配置文件
Nginx 站点配置文件（`/etc/nginx/sites-available/risk-monitoring`），包含：
- 反向代理配置
- 静态文件服务
- 媒体文件服务

### 4. Systemd 服务文件
Systemd 服务配置文件（`/etc/systemd/system/risk-monitoring-backend.service`），用于管理 Gunicorn 进程

## 部署步骤

### 阶段零：MySQL 数据库服务（在服务器上）

**注意**：如果 MySQL 容器已经在运行，可以跳过此步骤。

1. **启动 MySQL 8.0 容器**

   在服务器上执行以下命令启动 MySQL 容器：

   ```bash
   docker run -d \
     --name riskmon-mysql \
     --restart unless-stopped \
     -e MYSQL_ROOT_PASSWORD=YourPass123! \
     -p 3308:3306 \
     -v /home/ubuntu/jeremy/riskmon/mysql8/data:/var/lib/mysql \
     -v /home/ubuntu/jeremy/riskmon/mysql8/conf.d:/etc/mysql/conf.d:ro \
     mysql:8.0.25
   ```

   **参数说明**：
   - `--name riskmon-mysql`: 容器名称
   - `--restart unless-stopped`: 容器自动重启策略
   - `-e MYSQL_ROOT_PASSWORD=YourPass123!`: MySQL root 用户密码（请修改为您的实际密码）
   - `-p 3308:3306`: 将容器内的 3306 端口映射到宿主机的 3308 端口
   - `-v /home/ubuntu/jeremy/riskmon/mysql8/data:/var/lib/mysql`: 数据目录挂载（持久化数据）
   - `-v /home/ubuntu/jeremy/riskmon/mysql8/conf.d:/etc/mysql/conf.d:ro`: MySQL 配置文件目录（只读）

2. **验证 MySQL 容器运行状态**

   ```bash
   docker ps | grep riskmon-mysql
   docker logs riskmon-mysql
   ```

3. **测试数据库连接**

   ```bash
   # 从宿主机测试连接
   mysql -h 127.0.0.1 -P 3308 -u root -p
   # 输入密码后，如果成功连接，说明 MySQL 服务正常
   ```

### 阶段一：准备阶段（在开发环境）

1. **生成生产环境 SECRET_KEY**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   output:1$^ti0hei7a!f-@j+_h$4s(do&rqdwb*j()8l=lj#bjzg%mr6z

2. **创建生产环境配置文件**
   - 创建 `.env.prod` 文件
   - 配置数据库连接（指向 192.168.11.162:3308）
   - 设置 `DEBUG=False`
   - 配置 `ALLOWED_HOSTS`

3. **准备部署相关文件**
   - 创建 `gunicorn_config.py`（Gunicorn 配置文件，已在项目中）
   - 创建 `.env.prod`（生产环境环境变量文件）
   - Nginx 和 Systemd 配置文件将在服务器上创建

### 阶段二：宿主机部署（在服务器上）

本阶段将在服务器上直接部署 Django 应用，使用 Nginx + Gunicorn 架构，不构建 Docker 应用镜像。

#### 2.1 安装 Python 3.11 和系统依赖

1. **检查 Python 版本**

   ```bash
   python3 --version
   # 如果版本低于 3.11，需要安装 Python 3.11
   ```

2. **安装 Python 3.11（如果未安装）**

   ```bash
   # Ubuntu/Debian 系统
   sudo apt update
   sudo apt install -y software-properties-common
   sudo add-apt-repository ppa:deadsnakes/ppa
   sudo apt update
   sudo apt install -y python3.11 python3.11-venv python3.11-dev
   
   # 安装系统依赖（MySQL 客户端库等）
   sudo apt install -y build-essential libmysqlclient-dev pkg-config
   ```

3. **安装 Nginx**

   ```bash
   sudo apt install -y nginx
   ```

#### 2.2 准备项目目录和代码

1. **创建项目目录**

   ```bash
   # 创建项目根目录
   sudo mkdir -p /opt/risk-monitoring
   sudo chown -R $USER:$USER /opt/risk-monitoring
   
   # 创建数据目录（静态文件、媒体文件、日志文件）
   # 数据目录位于 /opt/risk-monitoring/backend/backend
   sudo mkdir -p /opt/risk-monitoring/backend/backend/{media,logs,staticfiles}
   sudo chown -R $USER:$USER /opt/risk-monitoring/backend
   ```

2. **上传项目代码到服务器**

   从开发目录 `/home/ubuntu/jeremy/riskmon/backend` 拷贝整个 `backend` 目录到服务器的 `/opt/risk-monitoring/backend`：

   ```bash
   # 在服务器上执行（从开发目录拷贝）
   cp -r /home/ubuntu/jeremy/riskmon/backend /opt/risk-monitoring/
   
   # 或使用 rsync（推荐，支持增量同步，排除不需要的文件）
   rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude '*.pyc' \
     --exclude '.env' --exclude 'logs' \
     /home/ubuntu/jeremy/riskmon/backend/ /opt/risk-monitoring/backend/
   
   # 或从开发环境使用 scp（在开发环境执行）
   # scp -r backend/ user@192.168.11.162:/opt/risk-monitoring/
   ```

3. **进入项目目录**

   ```bash
   cd /opt/risk-monitoring/backend
   ```

#### 2.3 创建虚拟环境并安装依赖

1. **创建虚拟环境**

   ```bash
   python3.11 -m venv venv
   ```

2. **激活虚拟环境**

   ```bash
   source venv/bin/activate
   ```

3. **升级 pip**

   ```bash
   pip install --upgrade pip
   ```

4. **安装项目依赖**

   ```bash
   pip install -r requirements.txt
   ```

#### 2.4 配置环境变量

1. **创建生产环境配置文件**

   将 `.env.prod` 文件上传到服务器，或直接在服务器上创建：

   ```bash
   # 在服务器上创建 .env.prod
   cd /opt/risk-monitoring/backend
   nano .env.prod
   ```

   内容示例（根据实际情况修改）：

   ```env
   # Django 核心配置
   SECRET_KEY=1$^ti0hei7a!f-@j+_h$4s(do&rqdwb*j()8l=lj#bjzg%mr6z
   DEBUG=False
   ALLOWED_HOSTS=192.168.11.162,localhost,127.0.0.1
   
   # 数据库配置（连接到 MySQL Docker 容器）
   DB_NAME=risk_monitoring
   DB_USER=root
   DB_PASSWORD=YourPass123!
   DB_HOST=127.0.0.1
   DB_PORT=3308
   
   # Gunicorn 配置
   GUNICORN_WORKERS=4
   GUNICORN_BIND=127.0.0.1:8000
   GUNICORN_TIMEOUT=120
   
   # CORS 跨域配置（必须配置，否则前端无法访问后端 API）
   # 多个来源用逗号分隔，不要有空格
   CORS_ALLOWED_ORIGINS=http://192.168.11.162:5173,http://192.168.11.162:5174
   
   # CSRF 信任的来源（必须配置）
   # 多个来源用逗号分隔，不要有空格
   CSRF_TRUSTED_ORIGINS=http://192.168.11.162:8888,http://192.168.11.162:5173,http://192.168.11.162:5174
   
   # 日志配置
   LOG_LEVEL=INFO
   ```
   
   **重要提示**：
   - 生产环境必须配置 `CORS_ALLOWED_ORIGINS` 和 `CSRF_TRUSTED_ORIGINS`，否则前端无法访问后端 API
   - 如果前端地址有变化，需要更新这两个配置并重启后端服务
   - 可以参考项目根目录下的 `.env.prod.example` 文件（如果存在）
   
   **注意**：CORS 配置已在 `settings.py` 中硬编码了生产环境的前端地址（`http://192.168.11.162:5173` 和 `http://192.168.11.162:5174`），通常不需要在环境变量中额外配置。如果需要添加其他来源，可以通过环境变量 `CORS_ALLOWED_ORIGINS` 和 `CSRF_TRUSTED_ORIGINS` 配置。

2. **验证环境变量加载**

   ```bash
   # 确保虚拟环境已激活
   source venv/bin/activate
   
   # 测试环境变量是否加载
   python manage.py shell
   # 在 shell 中执行：
   # >>> from django.conf import settings
   # >>> print(settings.DEBUG)
   # >>> print(settings.DATABASES)
   # 应该显示 False 和正确的数据库配置
   ```

#### 2.5 数据库迁移和初始化

1. **执行数据库迁移**

   ```bash
   # 确保虚拟环境已激活
   source venv/bin/activate
   
   # 执行迁移
   python manage.py migrate
   ```

2. **创建超级用户（如需要）**

   ```bash
   python manage.py createsuperuser
   ```

3. **加载演示数据（如需要）**

   ```bash
   python manage.py loaddata apps/users/fixtures/initial_organizations.json
   python manage.py loaddata apps/safety/fixtures/initial_industry_status.json
   python manage.py loaddata apps/safety/fixtures/initial_region_status.json
   # ... 其他 fixtures
   ```

#### 2.6 收集静态文件

```bash
# 确保虚拟环境已激活
source venv/bin/activate

# 收集静态文件到 STATIC_ROOT 目录
# 根据 settings.py: STATIC_ROOT = BASE_DIR / 'backend' / 'staticfiles'
# BASE_DIR = /opt/risk-monitoring/backend
# 实际路径: /opt/risk-monitoring/backend/backend/staticfiles
python manage.py collectstatic --noinput

# 验证静态文件是否已收集
ls -la /opt/risk-monitoring/backend/backend/staticfiles/
# 应该能看到 admin/ 目录和其他静态文件

# 检查 admin 静态文件
ls -la /opt/risk-monitoring/backend/backend/staticfiles/admin/
# 应该能看到 css/, js/, img/ 等目录
```

#### 2.7 配置 Gunicorn

1. **验证 gunicorn_config.py 存在**

   确保 `gunicorn_config.py` 文件在项目根目录，内容应该类似：

   确保 `gunicorn_config.py` 文件在项目根目录（`/opt/risk-monitoring/backend/gunicorn_config.py`），日志路径已配置为 `/opt/risk-monitoring/backend/backend/logs/`。
   
   **重要**：worker 数量已设置上限（最多16个），避免启动过多进程导致资源耗尽。如果您的服务器 CPU 核心数较多，可以通过环境变量 `GUNICORN_WORKERS` 手动设置（建议不超过32）。

2. **测试 Gunicorn 启动**

   ```bash
   # 确保虚拟环境已激活
   source venv/bin/activate
   
   # 确保在项目根目录（backend 目录）
   cd /opt/risk-monitoring/backend
   
   # 测试启动（前台运行，用于测试）
   # 注意：WSGI 应用路径是 config.wsgi:application（不是 risk_monitoring.wsgi:application）
   gunicorn config.wsgi:application -c gunicorn_config.py
   
   # 如果启动成功，按 Ctrl+C 停止，然后继续下一步
   ```

#### 2.8 配置 Systemd 服务（Gunicorn）

1. **创建 Systemd 服务文件**

   ```bash
   sudo nano /etc/systemd/system/risk-monitoring-backend.service
   ```

   内容如下：

   ```ini
   [Unit]
   Description=Risk Monitoring Backend (Gunicorn)
   After=network.target mysql.service
   
   [Service]
   Type=notify
   User=ubuntu
   Group=ubuntu
   WorkingDirectory=/opt/risk-monitoring/backend
   Environment="PATH=/opt/risk-monitoring/backend/venv/bin"
   EnvironmentFile=/opt/risk-monitoring/backend/.env.prod
   ExecStart=/opt/risk-monitoring/backend/venv/bin/gunicorn \
       config.wsgi:application \
       -c gunicorn_config.py
   ExecReload=/bin/kill -s HUP $MAINPID
   Restart=always
   RestartSec=3
   
   [Install]
   WantedBy=multi-user.target
   ```

   **重要说明**：
   - 请将 `User` 和 `Group` 修改为实际的用户名和组名（如 `ubuntu`）
   - `WorkingDirectory`: `/opt/risk-monitoring/backend`（项目根目录）
   - `Environment`: `/opt/risk-monitoring/backend/venv/bin`（虚拟环境路径）
   - `EnvironmentFile`: `/opt/risk-monitoring/backend/.env.prod`（环境变量文件）
   - `ExecStart`: 使用虚拟环境中的 gunicorn
   - **WSGI 应用路径必须是 `config.wsgi:application`**（不是 `risk_monitoring.wsgi:application`）

2. **启动并启用服务**

   ```bash
   # 重新加载 systemd 配置
   sudo systemctl daemon-reload
   
   # 启动服务
   sudo systemctl start risk-monitoring-backend
   
   # 设置开机自启
   sudo systemctl enable risk-monitoring-backend
   
   # 检查服务状态
   sudo systemctl status risk-monitoring-backend
   
   # 查看日志
   sudo journalctl -u risk-monitoring-backend -f
   ```

#### 2.9 配置 Nginx

1. **创建 Nginx 配置文件**

   ```bash
   sudo nano /etc/nginx/sites-available/risk-monitoring
   ```

   内容如下：

   ```nginx
   upstream django_backend {
       server 127.0.0.1:8000;
   }
   
   server {
       listen 8888;
       server_name 192.168.11.162;
       
       client_max_body_size 100M;
       
       # 静态文件服务
       # 根据 settings.py: STATIC_ROOT = BASE_DIR / 'backend' / 'staticfiles'
       # BASE_DIR = /opt/risk-monitoring/backend
       # 实际路径: /opt/risk-monitoring/backend/backend/staticfiles
       location /static/ {
           alias /opt/risk-monitoring/backend/backend/staticfiles/;
           expires 30d;
           add_header Cache-Control "public, immutable";
           # 启用访问日志以便调试
           access_log /var/log/nginx/static_access.log;
           # 确保正确的 MIME 类型
           include /etc/nginx/mime.types;
           default_type application/octet-stream;
           # 如果文件不存在，返回 404 而不是代理到 Django
           try_files $uri =404;
       }
       
       # 媒体文件服务
       # 根据 settings.py: MEDIA_ROOT = BASE_DIR / 'backend' / 'media'
       # BASE_DIR = /opt/risk-monitoring/backend
       # 实际路径: /opt/risk-monitoring/backend/backend/media
       location /media/ {
           alias /opt/risk-monitoring/backend/backend/media/;
           expires 7d;
           add_header Cache-Control "public";
           access_log off;
       }
       
       # API 请求转发到 Gunicorn
       location / {
           proxy_pass http://django_backend;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_redirect off;
           
           # 超时设置
           proxy_connect_timeout 60s;
           proxy_send_timeout 60s;
           proxy_read_timeout 60s;
       }
   }
   ```
   
   **路径说明**：
   - 静态文件路径：`/opt/risk-monitoring/backend/backend/staticfiles/`
   - 媒体文件路径：`/opt/risk-monitoring/backend/backend/media/`
   - 这些路径与 `settings.py` 中的 `STATIC_ROOT` 和 `MEDIA_ROOT` 配置一致
   - 确认路径的方法：
     ```bash
     # 检查静态文件目录（collectstatic 后的实际位置）
     ls -la /opt/risk-monitoring/backend/backend/staticfiles/
     
     # 检查媒体文件目录
     ls -la /opt/risk-monitoring/backend/backend/media/
     ```
   - **注意**：确保在部署前已执行 `python manage.py collectstatic` 收集静态文件

2. **启用 Nginx 配置**

   ```bash
   # 创建符号链接
   sudo ln -s /etc/nginx/sites-available/risk-monitoring /etc/nginx/sites-enabled/
   
   # 测试 Nginx 配置
   sudo nginx -t
   
   # 如果测试通过，重新加载 Nginx
   sudo systemctl reload nginx
   ```

3. **检查 Nginx 状态**

   ```bash
   sudo systemctl status nginx
   ```

### 阶段三：验证和测试

1. **检查服务状态**

   ```bash
   # 检查 Gunicorn 服务
   sudo systemctl status risk-monitoring-backend
   
   # 检查 Nginx 服务
   sudo systemctl status nginx
   
   # 检查端口监听
   sudo netstat -tlnp | grep -E '8000|3308'
   ```

2. **测试 API 接口**

   ```bash
   # 测试健康检查接口（如果有）
   curl http://192.168.11.162:8000/api/v1/auth/login/
   
   # 或使用浏览器访问
   # http://192.168.11.162:8000/api/v1/auth/login/
   ```

3. **检查日志**

   ```bash
   # Gunicorn 日志
   tail -f /opt/risk-monitoring/backend/backend/logs/gunicorn_access.log
   tail -f /opt/risk-monitoring/backend/backend/logs/gunicorn_error.log
   
   # Django 应用日志（如果配置了）
   tail -f /opt/risk-monitoring/backend/backend/logs/django.log
   
   # Systemd 服务日志
   sudo journalctl -u risk-monitoring-backend -f
   
   # Nginx 日志
   sudo tail -f /var/log/nginx/access.log
   sudo tail -f /var/log/nginx/error.log
   ```

### 阶段四：日常维护和监控

1. **服务管理命令**

   ```bash
   # 启动服务
   sudo systemctl start risk-monitoring-backend
   
   # 停止服务
   sudo systemctl stop risk-monitoring-backend
   
   # 重启服务
   sudo systemctl restart risk-monitoring-backend
   
   # 查看服务状态
   sudo systemctl status risk-monitoring-backend
   
   # 查看服务日志
   sudo journalctl -u risk-monitoring-backend -f
   ```

2. **代码更新流程**

   ```bash
   # 1. 停止服务
   sudo systemctl stop risk-monitoring-backend
   
   # 2. 更新代码（从开发目录拷贝到生产目录）
   # 方式一：使用 rsync（推荐，支持增量同步）
   rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude '*.pyc' \
     --exclude '.env' --exclude 'logs' --exclude 'backend/logs' \
     --exclude 'backend/media' --exclude 'backend/staticfiles' \
     /home/ubuntu/jeremy/riskmon/backend/ /opt/risk-monitoring/backend/
   
   # 方式二：使用 cp（完整拷贝）
   # cp -r /home/ubuntu/jeremy/riskmon/backend/* /opt/risk-monitoring/backend/
   
   # 3. 激活虚拟环境
   cd /opt/risk-monitoring/backend
   source venv/bin/activate
   
   # 4. 更新依赖（如需要）
   pip install -r requirements.txt
   
   # 5. 执行数据库迁移（如需要）
   python manage.py migrate
   
   # 6. 收集静态文件（如需要）
   python manage.py collectstatic --noinput
   
   # 7. 重启服务
   sudo systemctl start risk-monitoring-backend
   
   # 8. 检查服务状态
   sudo systemctl status risk-monitoring-backend
   ```

## 环境变量配置

### .env.prod 示例

```env
# Django 核心配置
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=192.168.11.162,localhost,127.0.0.1

# 数据库配置（连接到已运行的 MySQL Docker 容器）
DB_NAME=risk_monitoring
DB_USER=root
DB_PASSWORD=YourPass123!
DB_HOST=127.0.0.1
DB_PORT=3308

# Gunicorn 配置
GUNICORN_WORKERS=4
GUNICORN_BIND=127.0.0.1:8000
GUNICORN_TIMEOUT=120

# CORS 跨域配置（必须配置，否则前端无法访问后端 API）
# 多个来源用逗号分隔，不要有空格
CORS_ALLOWED_ORIGINS=http://192.168.11.162:5173,http://192.168.11.162:5174

# CSRF 信任的来源（必须配置）
# 多个来源用逗号分隔，不要有空格
CSRF_TRUSTED_ORIGINS=http://192.168.11.162:8888,http://192.168.11.162:5173,http://192.168.11.162:5174

# 日志配置
LOG_LEVEL=INFO
```

**注意**：
- 生产环境必须配置 `CORS_ALLOWED_ORIGINS` 和 `CSRF_TRUSTED_ORIGINS`，否则前端无法访问后端 API
- 如果前端地址有变化，需要更新这两个配置并重启后端服务
- 可以参考项目根目录下的 `.env.prod.example` 文件获取完整配置示例

## 数据持久化

以下目录用于数据持久化：

- `/opt/risk-monitoring/backend/backend/media` - 用户上传的媒体文件
- `/opt/risk-monitoring/backend/backend/logs` - 应用日志文件
- `/opt/risk-monitoring/backend/backend/staticfiles` - 收集的静态文件

## 安全考虑

1. **SECRET_KEY**: 必须使用强随机生成的密钥，不要使用默认值
2. **DEBUG**: 生产环境必须设置为 `False`
3. **ALLOWED_HOSTS**: 必须包含服务器的 IP 地址和域名
4. **数据库密码**: 使用强密码，不要使用默认密码
5. **防火墙**: 确保只开放必要的端口（80, 443）
6. **HTTPS**: 生产环境建议配置 HTTPS（需要 SSL 证书）

## 性能优化

1. **Gunicorn 工作进程数**: 
   - 建议设置为 `(2 × CPU核心数) + 1`，但不超过 16 个（配置文件已设置上限）
   - 对于小型服务器（2-4核），建议设置为 4-8 个 worker
   - 对于中型服务器（4-8核），建议设置为 8-16 个 worker
   - 可以通过环境变量 `GUNICORN_WORKERS` 手动设置（建议不超过32）
   - **注意**：worker 数量过多会导致内存消耗增加和日志快速增长
2. **数据库连接池**: 考虑使用连接池优化数据库连接
3. **静态文件**: 使用 Nginx 直接服务静态文件，减轻 Django 负担
4. **缓存**: 考虑使用 Redis 进行缓存（如需要）
5. **CDN**: 对于媒体文件，考虑使用 CDN（如需要）

## 监控和维护

1. **日志监控**: 
   - Gunicorn 访问日志: `/opt/risk-monitoring/backend/backend/logs/gunicorn_access.log`
   - Gunicorn 错误日志: `/opt/risk-monitoring/backend/backend/logs/gunicorn_error.log`
   - Django 应用日志（如果配置了）: `/opt/risk-monitoring/backend/backend/logs/django.log`
   - Systemd 服务日志: `sudo journalctl -u risk-monitoring-backend`
   - Nginx 访问日志: `/var/log/nginx/access.log`
   - Nginx 错误日志: `/var/log/nginx/error.log`

2. **服务健康检查**: 
   - 定期检查服务状态: `sudo systemctl status risk-monitoring-backend`
   - 监控端口监听: `sudo netstat -tlnp | grep 8000`
   - 定期测试 API 接口: `curl http://192.168.11.162:8000/api/v1/auth/login/`

3. **备份策略**: 
   - 定期备份数据库（建议每天）
   - 定期备份媒体文件（建议每周）
   - 定期备份代码（建议每次更新前）

4. **更新流程**: 见"阶段四：日常维护和监控"中的代码更新流程

## 故障排查

### 常见问题

1. **Gunicorn 服务无法启动**
   - 检查服务状态: `sudo systemctl status risk-monitoring-backend`
   - 查看服务日志: `sudo journalctl -u risk-monitoring-backend -n 50`
   - 检查 Gunicorn 错误日志: `tail -f /opt/risk-monitoring/backend/backend/logs/gunicorn_error.log`
   - 检查环境变量配置（`.env.prod` 文件）
   - 检查虚拟环境是否正确激活
   - 检查数据库连接

2. **数据库连接失败**
   - 确认 MySQL 容器正在运行: `docker ps | grep riskmon-mysql`
   - 检查数据库连接配置（IP、端口、用户名、密码）
   - 测试数据库连接: `mysql -h 127.0.0.1 -P 3308 -u root -p`
   - 确认防火墙规则允许连接

3. **静态文件无法访问（404 错误或样式丢失）**
   - **确认已执行 collectstatic**:
     ```bash
     # 检查静态文件目录是否存在且有内容
     ls -la /opt/risk-monitoring/backend/backend/staticfiles/
     # 应该能看到 admin/ 目录
     ls -la /opt/risk-monitoring/backend/backend/staticfiles/admin/
     # 应该能看到 css/, js/, img/ 等目录
     ```
   - **如果目录为空或不存在，重新收集静态文件**:
     ```bash
     cd /opt/risk-monitoring/backend
     source venv/bin/activate
     python manage.py collectstatic --noinput
     ```
   - **检查 Nginx 配置中的静态文件路径**:
     ```bash
     # 确认路径与 STATIC_ROOT 一致
     grep -A 5 "location /static/" /etc/nginx/sites-available/risk-monitoring
     # 应该显示: alias /opt/risk-monitoring/backend/backend/staticfiles/;
     ```
   - **检查文件权限**:
     ```bash
     # 确保 Nginx 可以读取文件
     ls -la /opt/risk-monitoring/backend/backend/staticfiles/
     # 如果权限不对，修复权限
     sudo chown -R ubuntu:ubuntu /opt/risk-monitoring/backend/backend/staticfiles/
     sudo chmod -R 755 /opt/risk-monitoring/backend/backend/staticfiles/
     ```
   - **检查 Nginx 错误日志**:
     ```bash
     sudo tail -f /var/log/nginx/error.log
     # 查看是否有权限错误或路径错误
     ```
   - **测试静态文件访问**:
     ```bash
     # 直接测试静态文件路径
     curl -I http://192.168.11.162:8000/static/admin/css/base.css
     # 应该返回 200 状态码，Content-Type: text/css
     ```
   - **验证 Nginx 配置并重新加载**:
     ```bash
     sudo nginx -t
     sudo systemctl reload nginx
     ```

4. **API 返回 500 错误**
   - 检查 Gunicorn 错误日志: `tail -f /opt/risk-monitoring/backend/backend/logs/gunicorn_error.log`
   - 检查 Django 应用日志（如果配置了）: `tail -f /opt/risk-monitoring/backend/backend/logs/django.log`
   - 检查数据库连接
   - 检查环境变量配置
   - 检查 Django 设置: `python manage.py check --deploy`

5. **Nginx 无法启动或配置错误**
   - 测试 Nginx 配置: `sudo nginx -t`
   - 查看 Nginx 错误日志: `sudo tail -f /var/log/nginx/error.log`
   - 检查端口是否被占用: `sudo netstat -tlnp | grep 8000`
   - 检查 Nginx 服务状态: `sudo systemctl status nginx`

6. **Gunicorn 启动过多 Worker 进程**
   - **症状**：启动时看到大量 worker 进程（超过20个），日志快速增长
   - **原因**：环境变量 `GUNICORN_WORKERS` 被设置为过大的值，或 `multiprocessing.cpu_count()` 返回异常值
   - **解决方法**：
     ```bash
     # 1. 检查环境变量
     echo $GUNICORN_WORKERS
     
     # 2. 如果设置了过大的值，取消设置或设置为合理值（建议4-16）
     unset GUNICORN_WORKERS
     # 或
     export GUNICORN_WORKERS=4
     
     # 3. 检查 CPU 核心数
     python3 -c "import multiprocessing; print(multiprocessing.cpu_count())"
     
     # 4. 重新启动 Gunicorn（使用更新后的配置文件，已设置上限）
     ```
   - **预防**：配置文件已设置 worker 数量上限（最多16个），避免资源耗尽

## 回滚方案

如果新版本出现问题，可以快速回滚：

1. **停止当前服务**
   ```bash
   sudo systemctl stop risk-monitoring-backend
   ```

2. **恢复代码到旧版本**
   ```bash
   cd /opt/risk-monitoring/backend
   # 使用 git 回滚到上一个版本
   git checkout <previous-commit-hash>
   # 或恢复备份的代码
   ```

3. **重新启动服务**
   ```bash
   sudo systemctl start risk-monitoring-backend
   sudo systemctl status risk-monitoring-backend
   ```

**建议**：在更新代码前，先备份当前代码和数据库：

```bash
# 备份代码
cp -r /opt/risk-monitoring/backend /opt/risk-monitoring/backend.backup.$(date +%Y%m%d)

# 备份数据库
mysqldump -h 127.0.0.1 -P 3308 -u root -p risk_monitoring > /opt/risk-monitoring/risk_monitoring_backup_$(date +%Y%m%d).sql
```

## 后续优化建议

1. **CI/CD 集成**: 配置自动化构建和部署流程
2. **容器编排**: 如需要多实例部署，考虑使用 Kubernetes
3. **监控告警**: 集成 Prometheus + Grafana 进行监控
4. **日志聚合**: 使用 ELK 或 Loki 进行日志聚合和分析
5. **自动备份**: 配置数据库和文件的自动备份脚本

## 注意事项

1. **首次部署**: 需要手动执行数据库迁移和初始化数据
2. **数据迁移**: 如果从开发环境迁移数据，需要导出并导入数据库
3. **文件权限**: 确保应用用户对项目目录和数据目录有正确的读写权限
4. **网络配置**: 确保 Django 应用可以访问宿主机上的 MySQL（使用 `127.0.0.1:3308`）
5. **时区设置**: 确保服务器时区正确（Asia/Shanghai）
6. **虚拟环境**: 确保使用正确的 Python 版本（3.11）创建虚拟环境
7. **环境变量**: 确保 `.env.prod` 文件中的配置正确，特别是数据库连接信息
8. **防火墙**: 确保防火墙允许 8000 端口的访问（如需要）
9. **资源限制**: 根据服务器资源调整 Gunicorn 工作进程数
10. **日志轮转**: 建议配置日志轮转，避免日志文件过大

## 部署检查清单

在开始部署前，请确认：

- [ ] MySQL 容器已启动并正常运行
- [ ] 服务器已安装 Python 3.11
- [ ] 服务器已安装 Nginx
- [ ] 已创建 `.env.prod` 文件并配置正确
- [ ] 已创建 `gunicorn_config.py` 文件
- [ ] 项目代码已上传到服务器
- [ ] 已创建必要的目录（`/opt/risk-monitoring/backend/backend/{media,logs,staticfiles}`）
- [ ] 已配置 Systemd 服务文件
- [ ] 已配置 Nginx 站点文件
- [ ] 已执行数据库迁移
- [ ] 已收集静态文件
- [ ] 已测试服务启动

## 相关文件位置

- 项目代码: `/opt/risk-monitoring/backend`
- 环境变量: `/opt/risk-monitoring/backend/.env.prod`
- Gunicorn 配置: `/opt/risk-monitoring/backend/gunicorn_config.py`
- Systemd 服务: `/etc/systemd/system/risk-monitoring-backend.service`
- Nginx 配置: `/etc/nginx/sites-available/risk-monitoring`
- 数据目录: `/opt/risk-monitoring/backend/backend/{media,logs,staticfiles}`
- MySQL 数据: `/home/ubuntu/jeremy/riskmon/mysql8/data`（MySQL 容器数据目录，保持不变）

