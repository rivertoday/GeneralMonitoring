# Postman 测试指南 - 登录接口

## 接口信息

- **接口路径**: `POST /api/v1/auth/login/`
- **完整URL**: `http://127.0.0.1:8000/api/v1/auth/login/`
- **请求方式**: POST
- **Content-Type**: `application/json`
- **权限要求**: 无需认证（AllowAny）

## 请求格式

### 请求头（Headers）

```
Content-Type: application/json
```

### 请求体（Body）

选择 **raw** 格式，类型选择 **JSON**，内容如下：

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

## Postman 详细操作步骤

### 步骤 1: 创建新请求

1. 打开 Postman
2. 点击左上角的 **"New"** 按钮
3. 选择 **"HTTP Request"**
4. 或者点击 **"+"** 号创建新标签页

### 步骤 2: 配置请求方法

1. 在请求方法下拉菜单中选择 **POST**

### 步骤 3: 输入请求URL

1. 在地址栏输入：
   ```
   http://127.0.0.1:8000/api/v1/auth/login/
   ```

### 步骤 4: 配置请求头

1. 点击 **"Headers"** 标签
2. 添加以下请求头：
   - **Key**: `Content-Type`
   - **Value**: `application/json`
   - 点击 **"Add"** 或直接按回车

### 步骤 5: 配置请求体

1. 点击 **"Body"** 标签
2. 选择 **"raw"** 选项
3. 在右侧下拉菜单中选择 **"JSON"**
4. 在文本框中输入请求体（替换为你的实际用户名和密码）：

```json
{
    "username": "admin",
    "password": "your_password"
}
```

### 步骤 6: 发送请求

1. 点击右上角的 **"Send"** 按钮
2. 等待响应结果

## 预期响应

### 成功响应（200 OK）

```json
{
    "code": 200,
    "message": "登录成功",
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user": {
            "id": 1,
            "username": "admin",
            "real_name": "管理员",
            "email": "admin@example.com",
            "phone": "13800138000",
            "organization_id": 1,
            "status": 1,
            "is_staff": true,
            "is_superuser": true,
            "roles": [],
            "permissions": []
        }
    }
}
```

### 失败响应（401 Unauthorized）

**情况1：用户名或密码错误**
```json
{
    "code": 401,
    "message": "用户名或密码错误",
    "data": null
}
```

**情况2：用户被禁用**
```json
{
    "code": 403,
    "message": "用户已被禁用",
    "data": null
}
```

## 测试用例

### 测试用例 1: 正确登录

**请求**:
```json
{
    "username": "admin",
    "password": "your_correct_password"
}
```

**预期**: 返回200状态码，包含 `access_token` 和 `refresh_token`

### 测试用例 2: 错误密码

**请求**:
```json
{
    "username": "admin",
    "password": "wrong_password"
}
```

**预期**: 返回401状态码，错误信息："用户名或密码错误"

### 测试用例 3: 不存在的用户

**请求**:
```json
{
    "username": "nonexistent_user",
    "password": "any_password"
}
```

**预期**: 返回401状态码，错误信息："用户名或密码错误"

### 测试用例 4: 缺少参数

**请求**:
```json
{
    "username": "admin"
}
```

**预期**: 返回400状态码，错误信息提示缺少 `password` 字段

## 使用返回的 Token

登录成功后，你会获得 `access_token`，可以用于后续需要认证的接口：

1. 在 Postman 中，点击 **"Authorization"** 标签
2. 选择 **"Bearer Token"** 类型
3. 将 `access_token` 的值粘贴到 **"Token"** 输入框中
4. 或者手动在请求头中添加：
   ```
   Authorization: Bearer <your_access_token>
   ```

## 常见问题

### 1. 连接被拒绝

**问题**: 无法连接到服务器

**解决**:
- 确保后端服务已启动：`python manage.py runserver`
- 检查URL是否正确：`http://127.0.0.1:8000`
- 检查防火墙设置

### 2. 401 未授权错误

**问题**: 返回401错误

**解决**:
- 检查用户名和密码是否正确
- 检查用户状态是否为启用（status=1）
- 检查用户是否被软删除（deleted_at为null）

### 3. CORS 错误

**问题**: 浏览器中可能出现CORS错误，但Postman不受影响

**说明**: Postman不受CORS限制，可以直接测试

### 4. 500 服务器错误

**问题**: 返回500错误

**解决**:
- 检查后端日志查看详细错误信息
- 确保数据库连接正常
- 确保所有依赖已安装

## 验证用户是否存在

如果不知道用户名或密码，可以通过Django shell查询：

```bash
cd backend
python manage.py shell
```

然后在shell中执行：

```python
from apps.users.models import User

# 查询所有用户
users = User.objects.filter(deleted_at__isnull=True)
for user in users:
    print(f"用户名: {user.username}, 状态: {user.status}, 是否启用: {user.is_active}")

# 查询特定用户
user = User.objects.filter(username='admin', deleted_at__isnull=True).first()
if user:
    print(f"用户存在: {user.username}, 状态: {user.status}")
else:
    print("用户不存在")
```

## 重置用户密码

如果需要重置用户密码，可以在Django shell中执行：

```python
from apps.users.models import User

user = User.objects.get(username='admin')
user.set_password('new_password')
user.save()
print(f"用户 {user.username} 的密码已重置")
```

## 后续接口测试

登录成功后，可以使用返回的 `access_token` 测试其他需要认证的接口，例如：

- **获取用户信息**: `GET /api/v1/auth/user-info/`
  - 需要添加 Header: `Authorization: Bearer <access_token>`

- **刷新Token**: `POST /api/v1/auth/refresh/`
  - Body: `{"refresh": "<refresh_token>"}`

- **登出**: `POST /api/v1/auth/logout/`
  - 需要添加 Header: `Authorization: Bearer <access_token>`
  - Body: `{"refresh": "<refresh_token>"}`

