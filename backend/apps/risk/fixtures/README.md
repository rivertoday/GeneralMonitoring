# 风险监测预警模块 - 演示数据初始化

本目录包含风险监测预警模块的初始演示数据，用于系统演示和功能测试。

## 文件说明

### 1. `initial_warning_levels.json` - 预警级别数据
- **数量**: 4个固定级别
- **内容**: 红色I级、橙色Ⅱ级、黄色Ⅲ级、蓝色Ⅳ级预警级别配置
- **依赖**: 无

### 2. `initial_warning_rules.json` - 预警规则数据
- **数量**: 5条规则
- **内容**: 
  - 3条预警生成规则（危化品、防汛、森林火灾）
  - 2条预警处置规则（红色I级、橙色Ⅱ级）
- **依赖**: `initial_warning_levels.json`

### 3. `initial_risk_monitors.json` - 风险监测点数据
- **数量**: 6个监测点
- **内容**: 
  - 危化品监测点：3个（焦化厂、油库、化工厂）
  - 防汛监测点：1个（水位监测）
  - 森林火灾监测点：1个（火险等级）
  - 交通运输监测点：1个（交通流量）
- **依赖**: `initial_data_sources.json` (system模块)
- **地理位置**: 马鞍山市花山区、雨山区

### 4. `initial_risk_warnings.json` - 风险预警数据
- **数量**: 3条预警记录
- **内容**: 
  - 1条红色I级预警（危化品泄漏）
  - 1条橙色Ⅱ级预警（水位预警）
  - 1条黄色Ⅲ级预警（森林火险）
- **依赖**: 
  - `initial_warning_levels.json`
  - `initial_warning_rules.json`
  - `initial_risk_monitors.json`
  - `initial_organizations.json` (users模块)
  - `initial_users.json` (users模块)

### 5. `initial_alarm_records.json` - 报警记录数据
- **数量**: 4条报警记录
- **内容**: 不同行业类型、不同状态的报警记录
- **依赖**: 
  - `initial_risk_monitors.json`
  - `initial_users.json` (users模块)

### 6. `initial_risk_hidden_dangers.json` - 隐患排查数据
- **数量**: 3条隐患记录
- **内容**: 危化品行业的隐患记录（不同等级、不同状态）
- **依赖**: 
  - `initial_risk_monitors.json`
  - `initial_organizations.json` (users模块)
  - `initial_users.json` (users模块)

### 7. `initial_risk_rectifications.json` - 隐患整改数据
- **数量**: 3条整改记录
- **内容**: 对应隐患排查的整改方案和执行记录
- **依赖**: 
  - `initial_risk_hidden_dangers.json`
  - `initial_organizations.json` (users模块)
  - `initial_users.json` (users模块)

## 数据加载顺序

由于存在外键依赖关系，请按照以下顺序加载fixtures：

```bash
# 1. 基础数据（用户、组织、数据源）- 如果还未加载
python manage.py loaddata apps/users/fixtures/initial_organizations.json
python manage.py loaddata apps/users/fixtures/initial_users.json
python manage.py loaddata apps/system/fixtures/initial_data_sources.json

# 2. 预警级别
python manage.py loaddata apps/risk/fixtures/initial_warning_levels.json

# 3. 预警规则（依赖预警级别）
python manage.py loaddata apps/risk/fixtures/initial_warning_rules.json

# 4. 风险监测点（依赖数据源）
python manage.py loaddata apps/risk/fixtures/initial_risk_monitors.json

# 5. 风险预警（依赖预警级别、预警规则、监测点、组织、用户）
python manage.py loaddata apps/risk/fixtures/initial_risk_warnings.json

# 6. 报警记录（依赖监测点、用户）
python manage.py loaddata apps/risk/fixtures/initial_alarm_records.json

# 7. 隐患排查（依赖监测点、组织、用户）
python manage.py loaddata apps/risk/fixtures/initial_risk_hidden_dangers.json

# 8. 隐患整改（依赖隐患排查、组织、用户）
python manage.py loaddata apps/risk/fixtures/initial_risk_rectifications.json
```

## 数据说明

### 预警级别（固定4个）
- **红色I级**: 特别严重，响应时间30分钟
- **橙色Ⅱ级**: 严重，响应时间60分钟
- **黄色Ⅲ级**: 较重，响应时间120分钟
- **蓝色Ⅳ级**: 一般，响应时间240分钟

### 监测点覆盖
- **危化品**: 3个监测点（焦化厂、油库、化工厂）
- **防汛**: 1个监测点（水位监测）
- **森林火灾**: 1个监测点（火险等级）
- **交通运输**: 1个监测点（交通流量）

### 预警记录状态
- **红色I级**: 已发布，已响应，待处置
- **橙色Ⅱ级**: 已发布，处理中
- **黄色Ⅲ级**: 已发布，待响应

### 隐患整改状态
- **整改中**: 1条（马钢焦化厂）
- **待开始**: 1条（中石化油库）
- **已完成**: 1条（液氨储罐，已验收通过）

## 注意事项

1. 所有数据的时间戳设置为2024年1月，确保数据的时间一致性
2. 地理位置统一使用马鞍山市花山区、雨山区
3. 关联的用户和组织ID需要与实际加载的基础数据一致
4. 如果基础数据（用户、组织、数据源）的ID发生变化，需要相应调整这些fixtures中的外键ID

