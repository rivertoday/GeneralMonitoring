# 演示数据初始化说明

本目录包含系统管理模块的基础数据初始化文件（Django Fixtures）。

## 文件说明

### 加载顺序

按照依赖关系，请按以下顺序加载fixtures：

1. `initial_organizations.json` - 组织架构（12个组织，三级结构）
2. `initial_roles.json` - 角色定义（8个业务角色）
3. `initial_permissions.json` - 权限树（50个权限节点）
4. `initial_users.json` - 用户数据（8个演示用户）
5. `initial_role_permissions.json` - 角色权限关联
6. `initial_user_roles.json` - 用户角色关联

### 数据说明

#### 组织架构（12个组织）
- 市级组织：马鞍山市应急管理局
- 区级组织：雨山区、花山区应急管理局
- 街道级组织：佳山街道、平湖街道、雨山街道、解放路街道应急办
- 其他组织：马钢、人民医院、消防救援支队、气象局、环保局

#### 角色（8个角色）
- 系统管理员（admin）
- 应急指挥（emergency_command）
- 监测预警（monitor_warning）
- 预案管理（plan_manager）
- 叫应调度（call_dispatcher）
- 简报管理（brief_manager）
- 安全态势管理（safety_manager）
- 演练管理（drill_manager）

#### 用户（8个用户）
- admin - 系统管理员（超级用户）
- zhangweimin - 张伟民（应急指挥）
- lihua - 李华（监测预警）
- wangqiang - 王强（预案管理）
- zhaomei - 赵梅（叫应调度）
- sunli - 孙丽（简报管理）
- zhoujun - 周军（安全态势管理）
- wudong - 吴东（演练管理）

**默认密码**：所有用户的默认密码为 `123456`

#### 权限树（50个权限节点）
包含系统所有主要菜单权限，涵盖：
- 仪表盘
- 风险监测预警模块（9个子菜单）
- 平急两用简报模块（4个子菜单）
- 平急两用叫应模块（7个子菜单）
- 应急预案数智化模块（5个子菜单）
- 安全态势模块（5个子菜单）
- 应急演练监督模块（4个子菜单）
- 系统管理模块（6个子菜单）
- 大屏展示模块（1个子菜单）
- 部分API接口权限

## 使用方法

### 1. 加载所有fixtures

```bash
cd backend
python manage.py loaddata apps/users/fixtures/initial_organizations.json
python manage.py loaddata apps/users/fixtures/initial_roles.json
python manage.py loaddata apps/users/fixtures/initial_permissions.json
python manage.py loaddata apps/users/fixtures/initial_users.json
python manage.py loaddata apps/users/fixtures/initial_role_permissions.json
python manage.py loaddata apps/users/fixtures/initial_user_roles.json
```

### 2. 修复用户密码

由于Django的密码哈希机制，fixtures中的密码可能无法直接使用。请在加载fixtures后运行：

```bash
python manage.py fix_user_passwords
```

这将为所有用户设置默认密码 `123456`。如果需要设置其他密码，可以使用：

```bash
python manage.py fix_user_passwords --password your_password
```

### 3. 验证数据

加载完成后，可以使用Django shell验证数据：

```bash
python manage.py shell
```

```python
from apps.users.models import User, Organization, Role, Permission

# 检查组织数量
print(f"组织数量: {Organization.objects.filter(deleted_at__isnull=True).count()}")

# 检查角色数量
print(f"角色数量: {Role.objects.filter(deleted_at__isnull=True).count()}")

# 检查权限数量
print(f"权限数量: {Permission.objects.filter(deleted_at__isnull=True).count()}")

# 检查用户数量
print(f"用户数量: {User.objects.filter(deleted_at__isnull=True).count()}")

# 测试登录
user = User.objects.get(username='admin')
user.check_password('123456')  # 应该返回 True
```

## 注意事项

1. **密码安全**：演示环境的默认密码为 `123456`，生产环境必须修改
2. **数据覆盖**：如果数据库中已存在相同ID的记录，loaddata会更新现有记录
3. **外键依赖**：必须按照依赖顺序加载，否则会报外键约束错误
4. **权限完整性**：当前权限树包含主要菜单权限，后续可根据需要扩展

## 后续步骤

加载完基础数据后，继续加载其他模块的fixtures：
- 系统管理模块的其他数据（数据源、消息模板）
- 安全态势模块数据
- 风险监测预警模块数据
- 其他业务模块数据

