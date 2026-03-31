# Vue 3 前端应用生产化部署方案

## 概述

本文档描述将 Vue 3 前端应用（管理后台 frontend/admin 和大屏展示 frontend/screen）部署到生产环境的完整方案。部署环境为虚拟机服务器（IP: 192.168.11.162），采用 Nginx 静态文件服务方式，后端 API 地址为 `http://192.168.11.162:8888/`。

**重要说明**：
- 本文档假设后端服务已按照 `backend/DEPLOY_PROD.md` 完成部署，Nginx 已配置并运行在 8888 端口
- 我们将复用同一个 Nginx 实例，在现有配置文件中添加两个新的 server 块来服务前端应用
- **管理后台（admin）**：监听 5173 端口，部署在 `/opt/risk-monitoring/frontend/admin/dist`
- **大屏展示（screen）**：监听 5174 端口，部署在 `/opt/risk-monitoring/frontend/screen/dist`

## 部署架构

```
┌─────────────────────────────────────────┐
│         虚拟机服务器 (192.168.11.162)      │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │         Nginx (复用)              │  │
│  │                                  │  │
│  │  ┌──────────┐ ┌──────┐ ┌──────┐│  │
│  │  │ Backend  │ │Admin │ │Screen││  │
│  │  │ Port:8888│ │Port: │ │Port: ││  │
│  │  │(反向代理) │ │5173  │ │5174  ││  │
│  │  │          │ │(静态) │ │(静态)││  │
│  │  └──────────┘ └──────┘ └──────┘│  │
│  └──────────────────────────────────┘  │
│         │          │          │         │
│         │          │          │         │
│         └──────────┼──────────┼─────────┼──▶ 后端 API (Gunicorn)
│                    │          │         │    http://127.0.0.1:8000
│                    │          │         │
│  部署目录:          │          │         │
│  - /opt/risk-monitoring/      │         │
│    ├── backend/               │         │
│    └── frontend/              │         │
│        ├── admin/dist/        │         │
│        │   (管理后台静态文件)  │         │
│        └── screen/dist/       │         │
│            (大屏展示静态文件)  │         │
└─────────────────────────────────────────┘
```

## 技术选型

### 管理后台（Admin）
- **前端框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **UI 框架**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP 客户端**: Axios

### 大屏展示（Screen）
- **前端框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **地图库**: Cesium（三维地图）
- **图表库**: ECharts（数据可视化）
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP 客户端**: Axios

### 公共技术
- **Web 服务器**: Nginx（静态文件服务）
- **后端 API**: Django REST Framework（`http://192.168.11.162:8888/`）

## 需要创建的文件

### 1. 环境变量文件

#### 管理后台（Admin）的 .env.prod
在 `frontend/admin/` 目录创建 `.env.prod` 文件，包含：
- `VITE_API_BASE_URL`: 后端 API 基础地址

#### 大屏展示（Screen）的 .env.prod（如需要）
在 `frontend/screen/` 目录创建 `.env.prod` 文件（如果 screen 项目需要环境变量），包含：
- `VITE_API_BASE_URL`: 后端 API 基础地址

### 2. Nginx 配置文件更新
在现有的 Nginx 配置文件（`/etc/nginx/sites-available/risk-monitoring`）中添加两个新的 server 块，包含：
- 管理后台（Admin）静态文件服务（5173 端口）
- 大屏展示（Screen）静态文件服务（5174 端口）
- SPA 路由支持（history 模式）
- 与后端配置共存于同一文件

## 部署步骤

### 阶段一：准备阶段（在开发环境）

本阶段需要为管理后台（admin）和大屏展示（screen）分别创建生产环境配置文件。

#### 1.1 创建管理后台（Admin）的生产环境配置

1. **创建生产环境配置文件**

   在管理后台项目根目录创建 `.env.prod` 文件：

   ```bash
   cd frontend/admin
   nano .env.prod
   ```

   内容如下：

   ```env
   # 后端 API 基础地址
   # 注意：应该访问 Nginx 的对外端口（8888），而不是 Gunicorn 的内部端口（8000）
   # Gunicorn 监听 127.0.0.1:8000（仅内部访问）
   # Nginx 监听 8888（对外服务，包含反向代理和静态文件服务）
   VITE_API_BASE_URL=http://192.168.11.162:8888
   ```

#### 1.2 创建大屏展示（Screen）的生产环境配置（如需要）

1. **创建生产环境配置文件**

   如果大屏展示项目需要环境变量，在大屏展示项目根目录创建 `.env.prod` 文件：

   ```bash
   cd frontend/screen
   nano .env.prod
   ```

   内容如下：

   ```env
   # 后端 API 基础地址
   VITE_API_BASE_URL=http://192.168.11.162:8888
   ```

   **注意**：如果 screen 项目不需要环境变量或使用其他方式配置 API 地址，可以跳过此步骤。

**重要说明**：
- 环境变量必须以 `VITE_` 开头才能在构建时被 Vite 识别
- 不要包含末尾的斜杠
- **必须使用 Nginx 的对外端口（8888）**，不要使用 Gunicorn 的内部端口（8000）
- Gunicorn 的 8000 端口通常只监听 `127.0.0.1`，外部无法访问
- Nginx 作为反向代理，负责处理所有外部请求

2. **验证环境变量配置**

   可以在 `vite.config.ts` 中验证环境变量是否正确加载：

   ```typescript
   // vite.config.ts
   export default defineConfig({
     // ... 其他配置
     define: {
       'import.meta.env.VITE_API_BASE_URL': JSON.stringify(process.env.VITE_API_BASE_URL || 'http://192.168.11.162:8888'),
     },
   })
   ```

### 阶段二：构建项目（在开发环境）

本阶段需要分别构建管理后台（admin）和大屏展示（screen）两个前端应用。

#### 2.1 构建管理后台（Admin）

1. **安装依赖（如果还没有）**

   ```bash
   cd frontend/admin
   npm install
   ```

2. **构建生产版本**

   ```bash
   # 使用 prod 模式构建（会加载 .env.prod 文件）
   npm run build:prod
   ```

   **注意**：如果 `package.json` 中没有 `build:prod` 脚本，可以使用：

   ```bash
   # 使用 --mode prod 参数指定模式
   vite build --mode prod
   ```

   构建完成后，会在 `frontend/admin/dist/` 目录下生成生产环境的静态文件。

3. **验证构建结果**

   ```bash
   # 检查构建输出
   ls -la frontend/admin/dist/
   # 应该能看到 index.html 和 assets/ 目录
   
   # 检查构建文件大小（可选）
   du -sh frontend/admin/dist/
   ```

#### 2.2 构建大屏展示（Screen）

1. **安装依赖（如果还没有）**

   ```bash
   cd frontend/screen
   npm install
   ```

2. **构建生产版本**

   ```bash
   # 使用 prod 模式构建（如果有 build:prod 脚本）
   npm run build:prod
   
   # 或使用标准构建命令
   npm run build
   ```

   构建完成后，会在 `frontend/screen/dist/` 目录下生成生产环境的静态文件。

3. **验证构建结果**

   ```bash
   # 检查构建输出
   ls -la frontend/screen/dist/
   # 应该能看到 index.html 和 assets/ 目录
   
   # 检查构建文件大小（可选）
   du -sh frontend/screen/dist/
   ```

#### 2.3 本地预览（可选）

   ```bash
   # 预览管理后台构建结果
   cd frontend/admin
   npm run preview
   # 访问 http://localhost:4173 查看效果
   
   # 预览大屏展示构建结果
   cd frontend/screen
   npm run preview
   # 访问 http://localhost:4173 查看效果（注意：如果同时运行，需要修改端口）
   ```

### 阶段三：部署到服务器

本阶段将部署两个前端应用：管理后台（admin）和大屏展示（screen）。

#### 3.1 准备服务器目录

1. **创建部署目录**

   ```bash
   # 在服务器上创建前端部署目录结构
   sudo mkdir -p /opt/risk-monitoring/frontend/{admin,screen}
   sudo chown -R $USER:$USER /opt/risk-monitoring/frontend
   ```

   **目录结构**：
   ```
   /opt/risk-monitoring/
   ├── backend/              # 后端服务（已部署）
   └── frontend/             # 前端应用目录
       ├── admin/           # 管理后台目录
       │   └── dist/        # 管理后台构建文件（待上传）
       └── screen/          # 大屏展示目录
           └── dist/        # 大屏展示构建文件（待上传）
   ```

#### 3.2 上传构建文件

**注意**：管理后台（admin）和大屏展示（screen）需要分别构建和上传。

##### 3.2.1 部署管理后台（Admin）

1. **在开发环境构建管理后台**

   ```bash
   cd frontend/admin
   npm run build:prod
   ```

2. **上传管理后台构建文件到服务器**

   ```bash
   # 在开发环境执行（示例）
   # 方式一：使用 scp
   scp -r frontend/admin/dist/ user@192.168.11.162:/opt/risk-monitoring/frontend/admin/
   
   # 方式二：使用 rsync（推荐，支持增量同步）
   rsync -avz --delete frontend/admin/dist/ user@192.168.11.162:/opt/risk-monitoring/frontend/admin/dist/
   ```

3. **验证管理后台文件上传**

   ```bash
   # 在服务器上检查
   ls -la /opt/risk-monitoring/frontend/admin/dist/
   # 应该能看到 index.html 和 assets/ 目录
   ```

##### 3.2.2 部署大屏展示（Screen）

1. **在开发环境构建大屏展示**

   ```bash
   cd frontend/screen
   npm run build:prod
   # 注意：如果 screen 项目没有 build:prod 脚本，使用 npm run build
   ```

2. **上传大屏展示构建文件到服务器**

   ```bash
   # 在开发环境执行（示例）
   # 方式一：使用 scp
   scp -r frontend/screen/dist/ user@192.168.11.162:/opt/risk-monitoring/frontend/screen/
   
   # 方式二：使用 rsync（推荐，支持增量同步）
   rsync -avz --delete frontend/screen/dist/ user@192.168.11.162:/opt/risk-monitoring/frontend/screen/dist/
   ```

3. **验证大屏展示文件上传**

   ```bash
   # 在服务器上检查
   ls -la /opt/risk-monitoring/frontend/screen/dist/
   # 应该能看到 index.html 和 assets/ 目录
   ```

**注意**：
- 使用 `rsync` 时，`--delete` 选项会删除目标目录中不存在于源目录的文件
- 确保上传的是 `dist/` 目录的内容，而不是 `dist/` 目录本身
- 两个前端应用需要分别构建和上传

#### 3.3 配置 Nginx（复用现有配置）

**重要**：我们将修改现有的 Nginx 配置文件（`/etc/nginx/sites-available/risk-monitoring`），在其中添加两个新的 server 块来服务前端应用，而不是创建独立的配置文件。这样可以复用同一个 Nginx 实例。

1. **编辑现有的 Nginx 配置文件**

   ```bash
   sudo nano /etc/nginx/sites-available/risk-monitoring
   ```

2. **在文件末尾添加两个前端应用的 server 块**

   在现有的 backend server 块（监听 8888 端口）之后，添加以下内容：

   ```nginx
   # 前端管理后台（Admin）服务配置
   server {
       listen 5173;
       server_name 192.168.11.162;
       
       root /opt/risk-monitoring/frontend/admin/dist;
       index index.html;
       
       client_max_body_size 100M;
       
       # 启用 gzip 压缩
       gzip on;
       gzip_vary on;
       gzip_min_length 1024;
       gzip_types text/plain text/css text/xml text/javascript 
                  application/json application/javascript application/xml+rss 
                  application/rss+xml font/truetype font/opentype 
                  application/vnd.ms-fontobject image/svg+xml;
       
       # 静态资源缓存
       location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
           expires 1y;
           add_header Cache-Control "public, immutable";
           access_log off;
       }
       
       # SPA 路由支持（history 模式）
       # 所有非静态文件请求都返回 index.html，由 Vue Router 处理路由
       location / {
           try_files $uri $uri/ /index.html;
       }
       
       # 禁止访问隐藏文件
       location ~ /\. {
           deny all;
           access_log off;
           log_not_found off;
       }
   }
   
   # 前端大屏展示（Screen）服务配置
   server {
       listen 5174;
       server_name 192.168.11.162;
       
       root /opt/risk-monitoring/frontend/screen/dist;
       index index.html;
       
       client_max_body_size 100M;
       
       # 启用 gzip 压缩
       gzip on;
       gzip_vary on;
       gzip_min_length 1024;
       gzip_types text/plain text/css text/xml text/javascript 
                  application/json application/javascript application/xml+rss 
                  application/rss+xml font/truetype font/opentype 
                  application/vnd.ms-fontobject image/svg+xml;
       
       # 静态资源缓存
       location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
           expires 1y;
           add_header Cache-Control "public, immutable";
           access_log off;
       }
       
       # SPA 路由支持（history 模式）
       # 所有非静态文件请求都返回 index.html，由 Vue Router 处理路由
       location / {
           try_files $uri $uri/ /index.html;
       }
       
       # 禁止访问隐藏文件
       location ~ /\. {
           deny all;
           access_log off;
           log_not_found off;
       }
   }
   ```

   **完整配置文件示例**（包含 backend、admin 和 screen 三个 server 块）：

   ```nginx
   # Backend 服务配置（已存在，保持不变）
   upstream django_backend {
       server 127.0.0.1:8000;
   }
   
   server {
       listen 8888;
       server_name 192.168.11.162;
       
       client_max_body_size 100M;
       
       # 静态文件服务
       location /static/ {
           alias /opt/risk-monitoring/backend/backend/staticfiles/;
           expires 30d;
           add_header Cache-Control "public, immutable";
           access_log /var/log/nginx/static_access.log;
           include /etc/nginx/mime.types;
           default_type application/octet-stream;
           try_files $uri =404;
       }
       
       # 媒体文件服务
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
           
           proxy_connect_timeout 60s;
           proxy_send_timeout 60s;
           proxy_read_timeout 60s;
       }
   }
   
   # 前端管理后台（Admin）服务配置（新增）
   server {
       listen 5173;
       server_name 192.168.11.162;
       
       root /opt/risk-monitoring/frontend/admin/dist;
       index index.html;
       
       client_max_body_size 100M;
       
       # 启用 gzip 压缩
       gzip on;
       gzip_vary on;
       gzip_min_length 1024;
       gzip_types text/plain text/css text/xml text/javascript 
                  application/json application/javascript application/xml+rss 
                  application/rss+xml font/truetype font/opentype 
                  application/vnd.ms-fontobject image/svg+xml;
       
       # 静态资源缓存
       location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
           expires 1y;
           add_header Cache-Control "public, immutable";
           access_log off;
       }
       
       # SPA 路由支持（history 模式）
       location / {
           try_files $uri $uri/ /index.html;
       }
       
       # 禁止访问隐藏文件
       location ~ /\. {
           deny all;
           access_log off;
           log_not_found off;
       }
   }
   
   # 前端大屏展示（Screen）服务配置（新增）
   server {
       listen 5174;
       server_name 192.168.11.162;
       
       root /opt/risk-monitoring/frontend/screen/dist;
       index index.html;
       
       client_max_body_size 100M;
       
       # 启用 gzip 压缩
       gzip on;
       gzip_vary on;
       gzip_min_length 1024;
       gzip_types text/plain text/css text/xml text/javascript 
                  application/json application/javascript application/xml+rss 
                  application/rss+xml font/truetype font/opentype 
                  application/vnd.ms-fontobject image/svg+xml;
       
       # 静态资源缓存
       location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
           expires 1y;
           add_header Cache-Control "public, immutable";
           access_log off;
       }
       
       # SPA 路由支持（history 模式）
       location / {
           try_files $uri $uri/ /index.html;
       }
       
       # 禁止访问隐藏文件
       location ~ /\. {
           deny all;
           access_log off;
           log_not_found off;
       }
   }
   ```

   **配置说明**：
   - **管理后台（Admin）**：监听 **5173 端口**，`root` 指向 `/opt/risk-monitoring/frontend/admin/dist`
   - **大屏展示（Screen）**：监听 **5174 端口**，`root` 指向 `/opt/risk-monitoring/frontend/screen/dist`
   - `index`: 默认文件为 `index.html`
   - `location /`: 使用 `try_files` 支持 Vue Router 的 history 模式
   - 静态资源缓存：设置长期缓存以提高性能
   - **注意**：前端直接访问后端 API（`http://192.168.11.162:8888`），不需要通过 Nginx 代理

3. **测试并重新加载 Nginx 配置**

   ```bash
   # 测试 Nginx 配置语法
   sudo nginx -t
   
   # 如果测试通过，重新加载 Nginx（不会中断服务）
   sudo systemctl reload nginx
   
   # 如果 reload 失败，可以尝试重启（会短暂中断服务）
   # sudo systemctl restart nginx
   ```

4. **检查 Nginx 状态和端口监听**

   ```bash
   # 检查 Nginx 服务状态
   sudo systemctl status nginx
   
   # 检查端口监听情况（应该看到 8888、5173 和 5174）
   sudo netstat -tlnp | grep -E '8888|5173|5174'
   # 或使用 ss 命令
   sudo ss -tlnp | grep -E '8888|5173|5174'
   ```

### 阶段四：验证和测试

1. **检查服务状态**

   ```bash
   # 检查 Nginx 服务
   sudo systemctl status nginx
   
   # 检查端口监听（应该看到 8888、5173 和 5174）
   sudo netstat -tlnp | grep -E '8888|5173|5174'
   # 或使用 ss 命令
   sudo ss -tlnp | grep -E '8888|5173|5174'
   ```

2. **测试前端访问**

   ```bash
   # 测试管理后台首页（使用 5173 端口）
   curl -I http://192.168.11.162:5173/
   
   # 测试大屏展示首页（使用 5174 端口）
   curl -I http://192.168.11.162:5174/

   # 或使用浏览器访问
   # 管理后台：http://192.168.11.162:5173/
   # 大屏展示：http://192.168.11.162:5174/
   ```

3. **测试 API 连接**

   在浏览器中打开开发者工具（F12），查看 Network 标签：
   - **管理后台（5173）**：
     - 登录页面应该能正常加载
     - 尝试登录，检查 API 请求是否正常
     - 确认 API 请求地址为 `http://192.168.11.162:8888/api/v1/...`
   - **大屏展示（5174）**：
     - 页面应该能正常加载
     - 检查数据请求是否正常
     - 确认 API 请求地址为 `http://192.168.11.162:8888/api/v1/...`

4. **检查控制台错误**

   在浏览器控制台（Console）中检查是否有错误：
   - CORS 错误
   - API 连接错误
   - 资源加载错误
   - 分别检查管理后台（5173）和大屏展示（5174）的控制台

## 环境变量配置

### .env.prod 示例

```env
# 后端 API 基础地址
# 注意：必须使用 Nginx 的对外端口（8888），不要使用 Gunicorn 的内部端口（8000）
# 架构说明：
# - Gunicorn 监听 127.0.0.1:8000（仅内部访问，由 Nginx 反向代理）
# - Nginx 监听 8888（对外服务，处理所有外部请求）
VITE_API_BASE_URL=http://192.168.11.162:8888
```

### 环境变量说明

- `VITE_API_BASE_URL`: 后端 API 的基础地址
  - **开发环境**：`http://127.0.0.1:8000`（Django 开发服务器或 Gunicorn）
  - **生产环境**：`http://192.168.11.162:8888`（**必须使用 Nginx 的对外端口**）
  - 必须以 `VITE_` 开头才能在构建时被 Vite 识别
  - 构建时会被内联到代码中，构建后无法修改
  
  **重要**：
  - 生产环境**必须使用 Nginx 的 8888 端口**，不要使用 Gunicorn 的 8000 端口
  - Gunicorn 监听 `127.0.0.1:8000`（仅内部访问，由 Nginx 反向代理）
  - Nginx 监听 `8888`（对外服务，处理所有外部请求，包括 API 和静态文件）
  - 如果使用 8000 端口，可能会遇到连接失败或 CORS 错误

## 日常维护和更新

### 代码更新流程

**注意**：管理后台（admin）和大屏展示（screen）需要分别更新。

#### 更新管理后台（Admin）

1. **在开发环境更新代码并构建**

   ```bash
   cd frontend/admin
   
   # 更新代码（使用 git pull 或其他方式）
   # git pull origin main
   
   # 安装新依赖（如果有）
   npm install
   
   # 构建生产版本
   npm run build:prod
   ```

2. **上传新的构建文件到服务器**

   ```bash
   # 使用 rsync 上传（推荐）
   rsync -avz --delete frontend/admin/dist/ user@192.168.11.162:/opt/risk-monitoring/frontend/admin/dist/
   
   # 或使用 scp
   scp -r frontend/admin/dist/* user@192.168.11.162:/opt/risk-monitoring/frontend/admin/dist/
   ```

#### 更新大屏展示（Screen）

1. **在开发环境更新代码并构建**

   ```bash
   cd frontend/screen
   
   # 更新代码（使用 git pull 或其他方式）
   # git pull origin main
   
   # 安装新依赖（如果有）
   npm install
   
   # 构建生产版本
   npm run build:prod
   # 或 npm run build（如果没有 build:prod 脚本）
   ```

2. **上传新的构建文件到服务器**

   ```bash
   # 使用 rsync 上传（推荐）
   rsync -avz --delete frontend/screen/dist/ user@192.168.11.162:/opt/risk-monitoring/frontend/screen/dist/
   
   # 或使用 scp
   scp -r frontend/screen/dist/* user@192.168.11.162:/opt/risk-monitoring/frontend/screen/dist/
   ```

3. **清除浏览器缓存（可选）**

   由于静态资源设置了长期缓存，更新后可能需要清除浏览器缓存才能看到最新版本。

   **方法一**：在构建时添加版本号或哈希值（Vite 默认已启用）
   
   **方法二**：强制刷新浏览器（Ctrl+F5 或 Cmd+Shift+R）

### 回滚方案

如果新版本出现问题，可以快速回滚：

1. **恢复旧版本的构建文件**

   ```bash
   # 恢复管理后台（如果有备份）
   cp -r /opt/risk-monitoring/frontend/admin/dist.backup /opt/risk-monitoring/frontend/admin/dist
   
   # 恢复大屏展示（如果有备份）
   cp -r /opt/risk-monitoring/frontend/screen/dist.backup /opt/risk-monitoring/frontend/screen/dist
   
   # 或从版本控制系统恢复
   # git checkout <previous-commit-hash>
   # npm run build:prod
   # 重新上传
   ```

**建议**：在更新前备份当前版本：

```bash
# 备份管理后台当前版本
cp -r /opt/risk-monitoring/frontend/admin/dist /opt/risk-monitoring/frontend/admin/dist.backup.$(date +%Y%m%d)

# 备份大屏展示当前版本
cp -r /opt/risk-monitoring/frontend/screen/dist /opt/risk-monitoring/frontend/screen/dist.backup.$(date +%Y%m%d)
```

## 故障排查

### 常见问题

1. **页面显示空白**
   - 检查浏览器控制台是否有错误
   - 检查 Nginx 错误日志：`sudo tail -f /var/log/nginx/error.log`
   - 检查文件权限：
     ```bash
     # 检查管理后台文件
     ls -la /opt/risk-monitoring/frontend/admin/dist/
     # 检查大屏展示文件
     ls -la /opt/risk-monitoring/frontend/screen/dist/
     ```
   - 确认 `index.html` 文件存在

2. **API 请求失败（CORS 错误或连接失败）**
   - **确认使用的是 Nginx 端口（8888），而不是 Gunicorn 端口（8000）**
   - 检查 `.env.prod` 中的 `VITE_API_BASE_URL` 配置是否正确
   - 检查后端 API 的 CORS 配置（`settings.py` 中的 `CORS_ALLOWED_ORIGINS`）
   - 在浏览器开发者工具中查看网络请求，确认请求地址是否正确
   - 如果使用 Nginx 代理，检查代理配置
   - 测试 API 连接：`curl http://192.168.11.162:8888/api/v1/auth/login/`

3. **路由刷新后 404**
   - 确认 Nginx 配置中有 `try_files $uri $uri/ /index.html;`
   - 检查 Nginx 配置是否正确加载：`sudo nginx -t`

4. **静态资源加载失败（404）**
   - 检查 `dist/assets/` 目录是否存在
   - 检查文件权限：
     ```bash
     # 修复管理后台文件权限
     sudo chmod -R 755 /opt/risk-monitoring/frontend/admin/dist/
     # 修复大屏展示文件权限
     sudo chmod -R 755 /opt/risk-monitoring/frontend/screen/dist/
     ```
   - 检查 Nginx 配置中的 `root` 路径是否正确（管理后台：`/opt/risk-monitoring/frontend/admin/dist`，大屏展示：`/opt/risk-monitoring/frontend/screen/dist`）

5. **构建后 API 地址不正确**
   - 确认 `.env.prod` 文件存在且配置正确
   - 确认环境变量以 `VITE_` 开头
   - 重新构建：`npm run build`

6. **Nginx 无法启动或配置错误**
   - 测试 Nginx 配置：`sudo nginx -t`
   - 查看 Nginx 错误日志：`sudo tail -f /var/log/nginx/error.log`
   - 检查端口是否被占用：
     ```bash
     # 检查 5173 端口（管理后台）
     sudo netstat -tlnp | grep 5173
     # 检查 5174 端口（大屏展示）
     sudo netstat -tlnp | grep 5174
     # 或使用 ss 命令
     sudo ss -tlnp | grep -E '5173|5174'
     ```
   - 确认配置文件语法正确，特别是新添加的两个 server 块
   - 检查是否有重复的 server_name 或端口配置冲突

## 性能优化建议

1. **启用 Gzip 压缩**
   - Nginx 配置中已包含 gzip 配置
   - 可以进一步调整压缩级别和类型

2. **静态资源缓存**
   - 已配置长期缓存（1年）
   - Vite 构建时会自动添加文件哈希，确保更新后能获取新版本

3. **CDN 加速（可选）**
   - 对于大型项目，可以考虑使用 CDN 加速静态资源
   - 将 `assets/` 目录部署到 CDN

4. **代码分割**
   - Vite 默认启用代码分割
   - 可以进一步优化路由级别的代码分割

## 安全考虑

1. **HTTPS（推荐）**
   - 生产环境建议配置 HTTPS
   - 需要 SSL 证书（可以使用 Let's Encrypt 免费证书）

2. **CORS 配置**
   - 确保后端 API 的 CORS 配置正确
   - 不要使用 `Access-Control-Allow-Origin: *`（生产环境）

3. **隐藏文件保护**
   - Nginx 配置中已禁止访问隐藏文件（`location ~ /\.`）

4. **API 密钥保护**
   - 不要在代码中硬编码 API 密钥
   - 使用环境变量管理敏感信息

## 部署检查清单

在开始部署前，请确认：

- [ ] 后端服务已按照 `backend/DEPLOY_PROD.md` 完成部署
- [ ] Nginx 已配置并运行在 8888 端口（后端服务）
- [ ] 已创建管理后台的 `.env.prod` 文件并配置正确的 API 地址（`http://192.168.11.162:8888`）
- [ ] 已创建大屏展示的 `.env.prod` 文件并配置正确的 API 地址（`http://192.168.11.162:8888`）
- [ ] 已在开发环境成功构建管理后台（`cd frontend/admin && npm run build:prod`）
- [ ] 已在开发环境成功构建大屏展示（`cd frontend/screen && npm run build:prod`）
- [ ] 已创建服务器部署目录（`/opt/risk-monitoring/frontend/admin` 和 `/opt/risk-monitoring/frontend/screen`）
- [ ] 已上传管理后台构建文件到服务器（`frontend/admin/dist/` 目录内容）
- [ ] 已上传大屏展示构建文件到服务器（`frontend/screen/dist/` 目录内容）
- [ ] 已在现有 Nginx 配置文件（`/etc/nginx/sites-available/risk-monitoring`）中添加两个前端 server 块（5173 和 5174）
- [ ] 已测试 Nginx 配置语法（`sudo nginx -t`）
- [ ] 已重新加载 Nginx 配置（`sudo systemctl reload nginx`）
- [ ] 已检查端口监听（8888、5173 和 5174 端口）
- [ ] 已测试管理后台页面访问（`http://192.168.11.162:5173/`）
- [ ] 已测试大屏展示页面访问（`http://192.168.11.162:5174/`）
- [ ] 已测试 API 连接（浏览器开发者工具中检查 API 请求）
- [ ] 已检查浏览器控制台无错误

## 相关文件位置

### 管理后台（Admin）
- 项目源码: `frontend/admin/`
- 构建输出: `frontend/admin/dist/`
- 生产环境变量: `frontend/admin/.env.prod`
- 服务器部署目录: `/opt/risk-monitoring/frontend/admin/dist`
- 访问地址: `http://192.168.11.162:5173/`

### 大屏展示（Screen）
- 项目源码: `frontend/screen/`
- 构建输出: `frontend/screen/dist/`
- 生产环境变量: `frontend/screen/.env.prod`（如需要）
- 服务器部署目录: `/opt/risk-monitoring/frontend/screen/dist`
- 访问地址: `http://192.168.11.162:5174/`

### 公共配置
- Nginx 配置: `/etc/nginx/sites-available/risk-monitoring`（与后端共用，添加了两个前端 server 块）
- Nginx 日志: `/var/log/nginx/access.log` 和 `/var/log/nginx/error.log`
- 后端 API: `http://192.168.11.162:8888/`（后端服务）

## 注意事项

1. **环境变量**: 必须在构建时设置，构建后无法修改。如果需要修改 API 地址，需要重新构建。
2. **路由模式**: 项目使用 Vue Router 的 history 模式，需要 Nginx 配置支持。
3. **浏览器缓存**: 静态资源设置了长期缓存，更新后可能需要清除浏览器缓存。
4. **文件权限**: 确保 Nginx 用户（通常是 `www-data`）有权限读取部署目录。
5. **端口冲突**: 
   - 如果 5173 端口（管理后台）已被占用，可以修改 Nginx 配置使用其他端口（如 8080、8081 等）
   - 如果 5174 端口（大屏展示）已被占用，可以修改 Nginx 配置使用其他端口（如 8082、8083 等）
6. **Nginx 配置复用**: 后端和两个前端应用共用同一个 Nginx 配置文件（`/etc/nginx/sites-available/risk-monitoring`），通过不同的 server 块和端口区分服务。
7. **两个前端应用**: 管理后台（admin）和大屏展示（screen）需要分别构建和部署，但使用相同的 Nginx 实例和配置文件。

## 下一步

确认此方案后，按照步骤执行部署。如果遇到问题，参考"故障排查"部分或查看相关日志文件。

