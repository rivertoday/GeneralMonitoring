# 风险监测预警系统 - 部署文档

## 项目简介

风险监测预警系统后端服务，基于Django 5.2.8和Django REST Framework构建，提供RESTful API接口。

## 技术栈

- **Web框架**: Django 5.2.8
- **API框架**: Django REST Framework 3.15.2
- **数据库**: MySQL 8.0
- **认证**: JWT (djangorestframework-simplejwt)
- **API文档**: drf-yasg (Swagger/OpenAPI)
- **Python版本**: Python 3.11
- **操作系统**: Windows 11 (开发环境)

## 项目结构

```
backend/
├── apps/                    # 应用模块
│   ├── common/             # 公共模块（异常处理、响应格式、分页等）
│   ├── users/              # 用户权限管理
│   ├── risk/               # 风险监测预警
│   ├── brief/              # 平急两用简报
│   ├── call/               # 平急两用叫应
│   ├── plan/               # 应急预案数智化
│   ├── safety/             # 安全态势展示
│   ├── drill/              # 应急演练监督
│   └── system/             # 系统管理
├── config/                 # Django项目配置
│   ├── settings.py         # 主配置文件
│   ├── urls.py             # 主URL配置
│   ├── wsgi.py             # WSGI配置
│   └── asgi.py             # ASGI配置
├── api/                    # API路由配置
│   └── urls.py             # API统一路由
├── manage.py               # Django管理脚本
├── requirements.txt        # Python依赖包
├── .env.local.example     # 环境变量示例
├── .gitignore             # Git忽略文件
└── README.md              # 项目说明文档
```

## 环境要求

- Python 3.11
- MySQL 8.0
- pip (Python包管理器)

## 安装步骤

### 1. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.local.example` 为 `.env.local`，并修改相关配置：

```bash
# Windows
copy .env.local.example .env.local

# Linux/Mac
cp .env.local.example .env.local
```

**注意**：使用 `.env.local` 作为环境变量文件名，避免与Python虚拟环境目录 `.env` 冲突。

#### 3.1 生成SECRET_KEY

SECRET_KEY是Django项目的安全密钥，用于加密会话、CSRF令牌等。生成方法如下：

**方法一：使用Django命令（推荐）**

```bash
python manage.py shell
```

在Django shell中执行：

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

**方法二：使用Python命令行（无需Django）**

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

或者：

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 3.2 编辑.env.local文件

将生成的SECRET_KEY复制到 `.env.local` 文件中，并设置其他配置：

```env
SECRET_KEY=生成的密钥字符串（例如：django-insecure-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx）
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=risk_monitoring
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
```

**重要提示**：
- SECRET_KEY必须保密，不要提交到版本控制系统
- 生产环境必须使用强随机生成的SECRET_KEY
- 不同环境（开发、测试、生产）应使用不同的SECRET_KEY
- 使用 `.env.local` 文件名避免与虚拟环境目录 `.env` 冲突

### 4. 创建数据库

在MySQL中创建数据库：

```sql
CREATE DATABASE risk_monitoring CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 数据库迁移

**重要说明**：
- `makemigrations`：检测模型变化，生成迁移文件（不修改数据库）
- `migrate`：将迁移文件应用到数据库，创建或更新表结构
- **必须先执行 `makemigrations`，再执行 `migrate`**

```bash
# 第一步：生成迁移文件（为所有app生成）
# 这会检测所有模型的变化，并生成相应的迁移文件
python manage.py makemigrations

# 如果输出 "No changes detected"，说明所有迁移文件已是最新
# 如果输出了新的迁移文件，说明有模型变化需要迁移

# 或者为特定app生成迁移文件
python manage.py makemigrations users
python manage.py makemigrations risk
python manage.py makemigrations system
python manage.py makemigrations brief
python manage.py makemigrations call
python manage.py makemigrations plan
python manage.py makemigrations safety
python manage.py makemigrations drill

# 第二步：执行迁移（将迁移文件应用到数据库）
# 这会根据迁移文件创建或更新数据库表结构
python manage.py migrate
```

**迁移流程说明**：
1. 首次部署：先执行 `makemigrations` 生成所有迁移文件，再执行 `migrate` 创建数据库表
2. 模型更新后：先执行 `makemigrations` 生成新的迁移文件，再执行 `migrate` 更新数据库
3. 如果模型没有变化：`makemigrations` 会输出 "No changes detected"，可以直接执行 `migrate` 确保所有迁移已应用

### 6. 演示数据初始化

#### 第一步：基础数据初始化（系统管理模块）

**已创建的Fixtures文件**：

1. `backend/apps/users/fixtures/initial_organizations.json` - 组织架构数据
2. `backend/apps/users/fixtures/initial_roles.json` - 角色数据
3. `backend/apps/users/fixtures/initial_permissions.json` - 权限树数据
4. `backend/apps/users/fixtures/initial_users.json` - 用户数据
5. `backend/apps/users/fixtures/initial_user_roles.json` - 用户角色关联数据
6. `backend/apps/users/fixtures/initial_role_permissions.json` - 角色权限关联数据
7. `backend/apps/system/fixtures/initial_data_sources.json` - 数据源数据
8. `backend/apps/system/fixtures/initial_message_templates.json` - 消息模板数据

**加载命令**：

```bash
# 按依赖顺序加载fixtures
cd backend
python manage.py loaddata apps/users/fixtures/initial_organizations.json
python manage.py loaddata apps/users/fixtures/initial_roles.json
python manage.py loaddata apps/users/fixtures/initial_permissions.json
python manage.py loaddata apps/users/fixtures/initial_users.json
python manage.py loaddata apps/users/fixtures/initial_role_permissions.json
python manage.py loaddata apps/users/fixtures/initial_user_roles.json
python manage.py loaddata apps/system/fixtures/initial_data_sources.json
python manage.py loaddata apps/system/fixtures/initial_message_templates.json

# 修复用户密码（默认密码：123456）
python manage.py fix_user_passwords
```

#### 第二步：资源数据初始化（安全态势模块）

**已创建的Fixtures文件**：

1. `backend/apps/safety/fixtures/initial_safety_resources.json` - 安全资源数据
2. `backend/apps/safety/fixtures/initial_safety_targets.json` - 防护目标数据
3. `backend/apps/safety/fixtures/initial_shelters.json` - 避难场所数据
4. `backend/apps/safety/fixtures/initial_hazard_sources.json` - 危险源数据
5. `backend/apps/safety/fixtures/initial_video_monitors.json` - 视频监控数据
6. `backend/apps/safety/fixtures/initial_industry_status.json` - 行业态势数据
7. `backend/apps/safety/fixtures/initial_region_status.json` - 区域态势数据（四色风险图）

**加载命令**：

```bash
# 按依赖顺序加载fixtures
cd backend
python manage.py loaddata apps/safety/fixtures/initial_safety_resources.json
python manage.py loaddata apps/safety/fixtures/initial_safety_targets.json
python manage.py loaddata apps/safety/fixtures/initial_shelters.json
python manage.py loaddata apps/safety/fixtures/initial_hazard_sources.json
python manage.py loaddata apps/safety/fixtures/initial_video_monitors.json
python manage.py loaddata apps/safety/fixtures/initial_industry_status.json
python manage.py loaddata apps/safety/fixtures/initial_region_status.json
```

**重要说明**：
- `loaddata` 命令的行为：
  - 如果 fixtures 中指定的 `pk`（主键）已存在，会**更新**该记录
  - 如果 fixtures 中指定的 `pk` 不存在，会**创建**新记录
  - **不会删除**数据库中已存在但 fixtures 中没有的记录
- 如果之前已经加载过相同 `pk` 的数据，再次执行 `loaddata` 会更新这些记录
- 如果需要完全替换数据，建议先清除旧数据再加载

#### 第三步：预警体系初始化（风险监测预警模块）

**已创建的Fixtures文件**：

1. `backend/apps/risk/fixtures/initial_warning_levels.json` - 预警级别数据
2. `backend/apps/risk/fixtures/initial_warning_rules.json` - 预警规则数据
3. `backend/apps/risk/fixtures/initial_risk_monitors.json` - 风险监测点数据
4. `backend/apps/risk/fixtures/initial_risk_warnings.json` - 风险预警数据
5. `backend/apps/risk/fixtures/initial_alarm_records.json` - 报警记录数据
6. `backend/apps/risk/fixtures/initial_risk_hidden_dangers.json` - 隐患排查数据
7. `backend/apps/risk/fixtures/initial_risk_rectifications.json` - 隐患整改数据

**加载命令**：

```bash
# 1. 基础数据（如果还未加载）
python manage.py loaddata apps/users/fixtures/initial_organizations.json
python manage.py loaddata apps/users/fixtures/initial_users.json
python manage.py loaddata apps/system/fixtures/initial_data_sources.json

# 2. 预警级别
python manage.py loaddata apps/risk/fixtures/initial_warning_levels.json

# 3. 预警规则
python manage.py loaddata apps/risk/fixtures/initial_warning_rules.json

# 4. 风险监测点
python manage.py loaddata apps/risk/fixtures/initial_risk_monitors.json

# 5. 风险预警
python manage.py loaddata apps/risk/fixtures/initial_risk_warnings.json

# 6. 报警记录
python manage.py loaddata apps/risk/fixtures/initial_alarm_records.json

# 7. 隐患排查
python manage.py loaddata apps/risk/fixtures/initial_risk_hidden_dangers.json

# 8. 隐患整改
python manage.py loaddata apps/risk/fixtures/initial_risk_rectifications.json
```

#### 第四步：预案体系初始化（预案模块）

**已创建的Fixtures文件**：

1. `backend/apps/plan/fixtures/initial_emergency_plans.json` - 应急预案数据
2. `backend/apps/plan/fixtures/initial_plan_structures.json` - 预案结构数据
3. `backend/apps/plan/fixtures/initial_plan_flows.json` - 预案流程数据
4. `backend/apps/plan/fixtures/initial_plan_tasks.json` - 预案任务数据
5. `backend/apps/plan/fixtures/initial_plan_executions.json` - 预案执行记录数据

**加载命令**：

```bash
# 1. 基础数据（如果还未加载）
python manage.py loaddata apps/users/fixtures/initial_organizations.json
python manage.py loaddata apps/users/fixtures/initial_users.json
python manage.py loaddata apps/users/fixtures/initial_roles.json

# 2. 预警数据（如果需要关联预警）- 如果还未加载
python manage.py loaddata apps/risk/fixtures/initial_risk_warnings.json

# 3. 应急预案
python manage.py loaddata apps/plan/fixtures/initial_emergency_plans.json

# 4. 预案结构
python manage.py loaddata apps/plan/fixtures/initial_plan_structures.json

# 5. 预案流程
python manage.py loaddata apps/plan/fixtures/initial_plan_flows.json

# 6. 预案任务
python manage.py loaddata apps/plan/fixtures/initial_plan_tasks.json

# 7. 预案执行记录
python manage.py loaddata apps/plan/fixtures/initial_plan_executions.json
```

#### 第五步：叫应体系初始化（叫应模块）

**已创建的Fixtures文件**：

1. `backend/apps/call/fixtures/initial_call_groups.json` - 叫应分组数据
2. `backend/apps/call/fixtures/initial_call_targets.json` - 叫应对象数据
3. `backend/apps/call/fixtures/initial_call_persons.json` - 叫应人员数据
4. `backend/apps/call/fixtures/initial_policy_files.json` - 政策文件数据
5. `backend/apps/call/fixtures/initial_policy_distributions.json` - 政策文件下发数据
6. `backend/apps/call/fixtures/initial_call_records.json` - 叫应记录数据

**加载命令**：

```bash
# 1. 基础数据（如果还未加载）
python manage.py loaddata apps/users/fixtures/initial_organizations.json
python manage.py loaddata apps/users/fixtures/initial_users.json

# 2. 预警数据（预警触发叫应）- 如果还未加载
python manage.py loaddata apps/risk/fixtures/initial_risk_warnings.json

# 3. 叫应分组
python manage.py loaddata apps/call/fixtures/initial_call_groups.json

# 4. 叫应对象
python manage.py loaddata apps/call/fixtures/initial_call_targets.json

# 5. 叫应人员
python manage.py loaddata apps/call/fixtures/initial_call_persons.json

# 6. 政策文件
python manage.py loaddata apps/call/fixtures/initial_policy_files.json

# 7. 政策文件下发
python manage.py loaddata apps/call/fixtures/initial_policy_distributions.json

# 8. 叫应记录
python manage.py loaddata apps/call/fixtures/initial_call_records.json
```

#### 第六步：简报体系初始化（简报模块）

**已创建的Fixtures文件**：

1. `backend/apps/brief/fixtures/initial_brief_templates.json` - 简报模板数据
2. `backend/apps/brief/fixtures/initial_brief_strategies.json` - 简报策略数据
3. `backend/apps/brief/fixtures/initial_brief_data.json` - 简报数据
4. `backend/apps/brief/fixtures/initial_brief_pushes.json` - 简报推送记录数据

**加载命令**：

```bash
# 1. 基础数据（如果还未加载）
python manage.py loaddata apps/users/fixtures/initial_organizations.json
python manage.py loaddata apps/users/fixtures/initial_users.json
python manage.py loaddata apps/users/fixtures/initial_roles.json
python manage.py loaddata apps/system/fixtures/initial_message_templates.json

# 2. 简报模板
python manage.py loaddata apps/brief/fixtures/initial_brief_templates.json

# 3. 简报策略（依赖模板、消息模板）
python manage.py loaddata apps/brief/fixtures/initial_brief_strategies.json

# 4. 简报数据（依赖模板、策略、用户）
python manage.py loaddata apps/brief/fixtures/initial_brief_data.json

# 5. 简报推送记录（依赖简报数据、用户、角色、组织）
python manage.py loaddata apps/brief/fixtures/initial_brief_pushes.json
```

#### 第七步：演练体系初始化（演练模块）

**已创建的Fixtures文件**：

1. `backend/apps/drill/fixtures/initial_drill_events.json` - 演练事件数据
2. `backend/apps/drill/fixtures/initial_drill_evaluations.json` - 演练评价数据
3. `backend/apps/drill/fixtures/initial_drill_summaries.json` - 演练总结数据
4. `backend/apps/drill/fixtures/initial_drill_analyses.json` - 演练分析统计数据

**加载命令**：

```bash
# 按依赖顺序加载fixtures
cd backend

# 1. 基础数据（如果还未加载）
python manage.py loaddata apps/users/fixtures/initial_organizations.json
python manage.py loaddata apps/users/fixtures/initial_users.json

# 2. 预案数据（演练事件关联预案）- 如果还未加载
python manage.py loaddata apps/plan/fixtures/initial_emergency_plans.json

# 3. 演练事件
python manage.py loaddata apps/drill/fixtures/initial_drill_events.json

# 4. 演练评价（依赖演练事件）
python manage.py loaddata apps/drill/fixtures/initial_drill_evaluations.json

# 5. 演练总结（依赖演练事件）
python manage.py loaddata apps/drill/fixtures/initial_drill_summaries.json

# 6. 演练分析（依赖演练事件、评价、总结）
python manage.py loaddata apps/drill/fixtures/initial_drill_analyses.json
```

#### 第八步：数据验证（可选）

已创建数据验证脚本：`backend/scripts/validate_data.py`

**使用方法**：

```bash
# 在虚拟环境中执行
cd backend
python scripts/validate_data.py
```

**验证内容**：
1. 数据关联关系完整性
2. 地理数据分布合理性
3. 时间数据逻辑性
4. 数据质量和真实性
5. 业务流程完整性

### 7. 创建超级用户

```bash
python manage.py createsuperuser
```

### 8. 运行开发服务器

```bash
python manage.py runserver
```

服务器将在 `http://127.0.0.1:8000` 启动。

## API文档

系统集成了Swagger UI和ReDoc，提供交互式API文档。

### 访问地址

- **Swagger UI**: `http://127.0.0.1:8000/swagger/` 或 `http://127.0.0.1:8000/docs/`
- **ReDoc**: `http://127.0.0.1:8000/redoc/`
- **OpenAPI JSON**: `http://127.0.0.1:8000/swagger.json`
- **OpenAPI YAML**: `http://127.0.0.1:8000/swagger.yaml`

### 使用说明

1. 在Swagger UI中可以：
   - 查看所有API接口的详细说明
   - 在线测试API接口
   - 查看请求/响应示例
   - 直接在界面中输入JWT Token进行认证

2. 获取JWT Token：
   - 在Swagger UI中找到 `/api/v1/auth/login/` 接口
   - 点击"Try it out"，输入用户名和密码
   - 执行后获取 `access` token
   - 点击页面右上角的"Authorize"按钮
   - 输入 `Bearer <your-access-token>`，点击"Authorize"
   - 之后就可以测试需要认证的接口了

## 常用开发命令

```bash
# 创建迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 运行开发服务器
python manage.py runserver

# 收集静态文件（生产环境）
python manage.py collectstatic

# 进入Django Shell
python manage.py shell

# 修复用户密码（演示数据）
python manage.py fix_user_passwords
```

## 注意事项

1. **数据库连接**: 确保MySQL服务已启动，数据库已创建
2. **环境变量**: 开发环境使用 `.env.local` 文件，生产环境使用系统环境变量
3. **静态文件**: 
   - 开发环境：静态文件从 `backend/static/` 目录自动提供
   - 生产环境：需要运行 `python manage.py collectstatic` 收集到 `backend/staticfiles/` 目录
4. **媒体文件**: 上传的媒体文件存储在 `backend/media/` 目录
5. **日志文件**: 日志文件存储在 `backend/logs/` 目录，需要确保目录存在

