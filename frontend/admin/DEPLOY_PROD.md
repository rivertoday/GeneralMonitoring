# Vue 3 管理后台生产化部署方案

## 概述

本文档描述将 Vue 3 管理后台（frontend/admin）部署到生产环境的完整方案。部署环境为虚拟机服务器（IP: 192.168.11.162），采用 Nginx 静态文件服务方式，后端 API 地址为 `http://192.168.11.162:8888/`。

## 部署架构

```
┌─────────────────────────────────────────┐
│         虚拟机服务器 (192.168.11.162)      │
│                                         │
│  ┌──────────────┐                       │
│  │   Nginx      │                       │
│  │  (静态文件)   │                       │
│  │   Port: 80   │                       │
│  └──────────────┘                       │
│         │                                │
│         │                                │
│         └──────────────────────────────┼──▶ 后端 API
│                                         │    http://192.168.11.162:8888/
│                                         │
│  部署目录:                               │
│  - /opt/risk-monitoring/admin/dist      │
│    (构建后的静态文件)                     │
└─────────────────────────────────────────┘
```

## 技术选型

- **前端框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **UI 框架**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP 客户端**: Axios
- **Web 服务器**: Nginx（静态文件服务）
- **后端 API**: Django REST Framework（`http://192.168.11.162:8888/`）

## 需要创建的文件

### 1. .env.prod
生产环境环境变量文件，包含：
- `VITE_API_BASE_URL`: 后端 API 基础地址

### 2. Nginx 配置文件
Nginx 站点配置文件（`/etc/nginx/sites-available/risk-monitoring-admin`），包含：
- 静态文件服务
- SPA 路由支持（history 模式）
- API 代理配置（可选）

## 部署步骤

### 阶段一：准备阶段（在开发环境）

1. **创建生产环境配置文件**

   在项目根目录创建 `.env.prod` 文件：

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

   或者修改 `package.json` 添加 `build:prod` 脚本（见下方说明）。

   构建完成后，会在 `dist/` 目录下生成生产环境的静态文件。

3. **验证构建结果**

   ```bash
   # 检查构建输出
   ls -la dist/
   # 应该能看到 index.html 和 assets/ 目录
   
   # 检查构建文件大小（可选）
   du -sh dist/
   ```

4. **本地预览（可选）**

   ```bash
   # 使用 Vite 预览构建结果
   npm run preview
   # 访问 http://localhost:4173 查看效果
   ```

### 阶段三：部署到服务器

#### 3.1 准备服务器目录

1. **创建部署目录**

   ```bash
   # 在服务器上创建部署目录
   sudo mkdir -p /opt/risk-monitoring/admin
   sudo chown -R $USER:$USER /opt/risk-monitoring/admin
   ```

#### 3.2 上传构建文件

1. **上传 dist 目录到服务器**

   将构建好的 `dist/` 目录上传到服务器，可以使用 `scp`、`rsync` 或其他方式：

   ```bash
   # 在开发环境执行（示例）
   # 方式一：使用 scp
   scp -r dist/ user@192.168.11.162:/opt/risk-monitoring/admin/
   
   # 方式二：使用 rsync（推荐，支持增量同步）
   rsync -avz --delete dist/ user@192.168.11.162:/opt/risk-monitoring/admin/dist/
   ```

   **注意**：
   - 使用 `rsync` 时，`--delete` 选项会删除目标目录中不存在于源目录的文件
   - 确保上传的是 `dist/` 目录的内容，而不是 `dist/` 目录本身

2. **验证文件上传**

   ```bash
   # 在服务器上检查
   ls -la /opt/risk-monitoring/admin/dist/
   # 应该能看到 index.html 和 assets/ 目录
   ```

#### 3.3 配置 Nginx

1. **创建 Nginx 配置文件**

   ```bash
   sudo nano /etc/nginx/sites-available/risk-monitoring-admin
   ```

   内容如下：

   ```nginx
   server {
       listen 80;
       server_name 192.168.11.162;
       
       root /opt/risk-monitoring/admin/dist;
       index index.html;
       
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
       
       # API 代理（可选，如果需要通过 Nginx 代理 API 请求）
       # 如果前端直接访问后端 API，可以跳过此配置
       location /api/ {
           proxy_pass http://127.0.0.1:8888;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_redirect off;
           
           # CORS 配置（如果需要）
           add_header Access-Control-Allow-Origin *;
           add_header Access-Control-Allow-Methods 'GET, POST, PUT, DELETE, PATCH, OPTIONS';
           add_header Access-Control-Allow-Headers 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization';
           
           # 处理预检请求
           if ($request_method = 'OPTIONS') {
               return 204;
           }
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

   **配置说明**：
   - `root`: 指向构建后的静态文件目录
   - `index`: 默认文件为 `index.html`
   - `location /`: 使用 `try_files` 支持 Vue Router 的 history 模式
   - `location /api/`: 可选，如果需要通过 Nginx 代理 API 请求
   - 静态资源缓存：设置长期缓存以提高性能

2. **启用 Nginx 配置**

   ```bash
   # 创建符号链接
   sudo ln -s /etc/nginx/sites-available/risk-monitoring-admin /etc/nginx/sites-enabled/
   
   # 测试 Nginx 配置
   sudo nginx -t
   
   # 如果测试通过，重新加载 Nginx
   sudo systemctl reload nginx
   ```

3. **检查 Nginx 状态**

   ```bash
   sudo systemctl status nginx
   ```

### 阶段四：验证和测试

1. **检查服务状态**

   ```bash
   # 检查 Nginx 服务
   sudo systemctl status nginx
   
   # 检查端口监听
   sudo netstat -tlnp | grep :80
   ```

2. **测试前端访问**

   ```bash
   # 测试首页
   curl -I http://192.168.11.162/
   
   # 或使用浏览器访问
   # http://192.168.11.162/
   ```

3. **测试 API 连接**

   在浏览器中打开开发者工具（F12），查看 Network 标签：
   - 登录页面应该能正常加载
   - 尝试登录，检查 API 请求是否正常
   - 确认 API 请求地址为 `http://192.168.11.162:8888/api/v1/...`

4. **检查控制台错误**

   在浏览器控制台（Console）中检查是否有错误：
   - CORS 错误
   - API 连接错误
   - 资源加载错误

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

1. **在开发环境更新代码并构建**

   ```bash
   cd frontend/admin
   
   # 更新代码（使用 git pull 或其他方式）
   # git pull origin main
   
   # 安装新依赖（如果有）
   npm install
   
   # 构建生产版本
   npm run build
   ```

2. **上传新的构建文件到服务器**

   ```bash
   # 使用 rsync 上传（推荐）
   rsync -avz --delete dist/ user@192.168.11.162:/opt/risk-monitoring/admin/dist/
   
   # 或使用 scp
   scp -r dist/* user@192.168.11.162:/opt/risk-monitoring/admin/dist/
   ```

3. **清除浏览器缓存（可选）**

   由于静态资源设置了长期缓存，更新后可能需要清除浏览器缓存才能看到最新版本。

   **方法一**：在构建时添加版本号或哈希值（Vite 默认已启用）
   
   **方法二**：强制刷新浏览器（Ctrl+F5 或 Cmd+Shift+R）

### 回滚方案

如果新版本出现问题，可以快速回滚：

1. **恢复旧版本的构建文件**

   ```bash
   # 如果有备份，恢复备份
   cp -r /opt/risk-monitoring/admin/dist.backup /opt/risk-monitoring/admin/dist
   
   # 或从版本控制系统恢复
   # git checkout <previous-commit-hash>
   # npm run build
   # 重新上传
   ```

**建议**：在更新前备份当前版本：

```bash
# 备份当前版本
cp -r /opt/risk-monitoring/admin/dist /opt/risk-monitoring/admin/dist.backup.$(date +%Y%m%d)
```

## 故障排查

### 常见问题

1. **页面显示空白**
   - 检查浏览器控制台是否有错误
   - 检查 Nginx 错误日志：`sudo tail -f /var/log/nginx/error.log`
   - 检查文件权限：`ls -la /opt/risk-monitoring/admin/dist/`
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
   - 检查文件权限：`sudo chmod -R 755 /opt/risk-monitoring/admin/dist/`
   - 检查 Nginx 配置中的 `root` 路径是否正确

5. **构建后 API 地址不正确**
   - 确认 `.env.prod` 文件存在且配置正确
   - 确认环境变量以 `VITE_` 开头
   - 重新构建：`npm run build`

6. **Nginx 无法启动或配置错误**
   - 测试 Nginx 配置：`sudo nginx -t`
   - 查看 Nginx 错误日志：`sudo tail -f /var/log/nginx/error.log`
   - 检查端口是否被占用：`sudo netstat -tlnp | grep :80`

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

- [ ] 已创建 `.env.prod` 文件并配置正确的 API 地址
- [ ] 已在开发环境成功构建项目（`npm run build`）
- [ ] 已创建服务器部署目录
- [ ] 已上传构建文件到服务器
- [ ] 已配置 Nginx 站点文件
- [ ] 已启用 Nginx 配置并重新加载
- [ ] 已测试前端页面访问
- [ ] 已测试 API 连接
- [ ] 已检查浏览器控制台无错误

## 相关文件位置

- 项目源码: `frontend/admin/`
- 构建输出: `frontend/admin/dist/`
- 生产环境变量: `frontend/admin/.env.prod`
- 服务器部署目录: `/opt/risk-monitoring/admin/dist`
- Nginx 配置: `/etc/nginx/sites-available/risk-monitoring-admin`
- Nginx 日志: `/var/log/nginx/access.log` 和 `/var/log/nginx/error.log`

## 注意事项

1. **环境变量**: 必须在构建时设置，构建后无法修改。如果需要修改 API 地址，需要重新构建。
2. **路由模式**: 项目使用 Vue Router 的 history 模式，需要 Nginx 配置支持。
3. **浏览器缓存**: 静态资源设置了长期缓存，更新后可能需要清除浏览器缓存。
4. **文件权限**: 确保 Nginx 用户（通常是 `www-data`）有权限读取部署目录。
5. **端口冲突**: 如果 80 端口已被占用，可以修改 Nginx 配置使用其他端口（如 8080）。

## 下一步

确认此方案后，按照步骤执行部署。如果遇到问题，参考"故障排查"部分或查看相关日志文件。

