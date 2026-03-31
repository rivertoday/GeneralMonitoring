# 系统管理模块演示数据初始化说明

本目录包含系统管理模块的演示数据初始化文件（Django Fixtures）。

## 文件说明

### 数据源（5个数据源）
- `initial_data_sources.json` - 外部数据源配置（5个）
  - DS001：马鞍山市气象局API（气象）
  - DS002：危化品监测数据库（危化）
  - DS003：防汛监测API（防汛）
  - DS004：交通运输监测数据文件（交通运输）
  - DS005：森林火灾监测API（森林火灾）

### 消息模板（15个模板）
- `initial_message_templates.json` - 消息模板（15个）
  - 风险预警通知：系统消息、短信、邮件（3个）
  - 报警通知：系统消息、短信（2个）
  - 简报推送通知：系统消息、邮件（2个）
  - 叫应通知：系统消息、短信（2个）
  - 政策下发通知：系统消息、邮件（2个）
  - 其他通知：预警发布、隐患整改、演练开始、预案启动（4个）

## 使用方法

### 加载fixtures

```bash
cd backend
python manage.py loaddata apps/system/fixtures/initial_data_sources.json
python manage.py loaddata apps/system/fixtures/initial_message_templates.json
```

### 验证数据

```bash
python manage.py shell
```

```python
from apps.system.models import DataSource, MessageTemplate

# 检查数据源数量
print(f"数据源数量: {DataSource.objects.filter(deleted_at__isnull=True).count()}")

# 检查消息模板数量
print(f"消息模板数量: {MessageTemplate.objects.filter(deleted_at__isnull=True).count()}")
```

## 注意事项

1. **数据源密码**：数据库类型的数据源密码字段为加密存储，实际使用中需要正确配置
2. **API地址**：示例API地址为演示用，实际使用中需要配置真实地址
3. **变量占位符**：消息模板中的变量占位符格式为 `{变量名}`，使用时需要替换为实际值

