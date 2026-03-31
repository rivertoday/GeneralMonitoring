# 简报模块 - 演示数据初始化

本目录包含简报模块的初始演示数据，用于系统演示和功能测试。

## 文件说明

### 1. `initial_brief_templates.json` - 简报模板数据
- **数量**: 3个模板
- **内容**: 
  - 1个常态化运行报告模板（危化品安全运行日报）
  - 1个常态化运行报告模板（防汛安全运行周报）
  - 1个非常态化突发预警简报模板
- **特点**: 
  - 支持变量占位符（如：{report_date}、{alarm_count}等）
  - 包含数据配置（定义需要统计的数据项）
  - 支持行业维度、区域维度、时间维度配置
- **依赖**: 无

### 2. `initial_brief_strategies.json` - 简报策略数据
- **数量**: 4个策略
- **内容**: 
  - 2个常态化策略（定时触发：日报、周报）
  - 2个非常态化策略（事件触发：红色I级、橙色Ⅱ级预警）
- **特点**: 
  - 支持定时触发（配置触发时间、触发周期）
  - 支持事件触发（配置触发条件、预警级别过滤）
  - 支持多种推送目标类型（用户、角色、组织）
  - 支持多种推送渠道（系统消息、短信、邮件）
  - 关联消息模板（用于推送通知）
- **依赖**: 
  - `initial_brief_templates.json`
  - `initial_message_templates.json` (system模块，可选)

### 3. `initial_brief_data.json` - 简报数据
- **数量**: 4条简报数据
- **内容**: 
  - 2条常态化运行报告（危化品日报、防汛周报）
  - 2条非常态化突发预警简报（红色I级、橙色Ⅱ级）
- **特点**: 
  - 包含完整的简报内容（标题、正文）
  - 包含数据摘要（JSON格式：报警次数、预警次数、风险隐患数量等）
  - 包含行业维度数据、区域维度数据、时间维度数据（JSON格式）
  - 支持附件（PDF文件）
  - 关联策略和模板
- **依赖**: 
  - `initial_brief_templates.json`
  - `initial_brief_strategies.json`
  - `initial_users.json` (users模块，可选，生成人)

### 4. `initial_brief_pushes.json` - 简报推送记录数据
- **数量**: 10条推送记录
- **内容**: 
  - 覆盖不同推送目标类型（用户、角色、组织）
  - 覆盖不同推送渠道（系统消息、短信、邮件）
  - 包含不同推送状态和阅读状态
- **特点**: 
  - 支持多种推送渠道（system-系统消息、sms-短信、email-邮件）
  - 支持推送状态跟踪（待推送、推送中、推送成功、推送失败）
  - 支持阅读状态跟踪（未读、已读）
  - 包含消息ID（系统消息或短信平台返回的ID）
- **依赖**: 
  - `initial_brief_data.json`
  - `initial_users.json` (users模块，推送目标用户)
  - `initial_roles.json` (users模块，推送目标角色)
  - `initial_organizations.json` (users模块，推送目标组织)

## 数据加载顺序

由于存在外键依赖关系，请按照以下顺序加载fixtures：

```bash
# 1. 基础数据（用户、角色、组织、消息模板）- 如果还未加载
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

## 数据说明

### 简报模板类型分布
- **常态化运行报告**: 2个（日报、周报）
- **非常态化突发预警简报**: 1个

### 简报策略类型分布
- **常态化策略**: 2个（定时触发：日报、周报）
- **非常态化策略**: 2个（事件触发：红色I级、橙色Ⅱ级预警）

### 简报数据类型分布
- **常态化运行报告**: 2条（危化品日报、防汛周报）
- **非常态化突发预警简报**: 2条（红色I级、橙色Ⅱ级）

### 简报推送渠道分布
- **系统消息**: 5条
- **短信**: 2条
- **邮件**: 3条

### 简报推送目标类型分布
- **用户**: 4条
- **角色**: 4条
- **组织**: 2条

## 业务流程示例

### 常态化简报流程
1. **策略配置**: 配置定时触发策略（如每日8:00生成日报）
2. **自动生成**: 系统按策略自动生成简报数据
3. **数据填充**: 根据模板和数据配置，填充报警次数、预警次数、风险隐患数量等数据
4. **自动推送**: 根据策略配置的推送目标和渠道，自动推送简报
5. **阅读跟踪**: 跟踪推送状态和阅读状态

### 非常态化简报流程（预警触发）
1. **预警触发**: 系统检测到预警事件
2. **策略匹配**: 根据预警级别匹配对应的简报策略
3. **自动生成**: 系统自动生成突发预警简报
4. **多渠道推送**: 根据策略配置，通过系统消息、短信、邮件等多种渠道推送
5. **响应跟踪**: 跟踪推送状态和阅读状态

## 注意事项

1. 简报策略关联的模板ID需要与实际加载的模板数据一致
2. 简报策略关联的消息模板ID需要与实际加载的消息模板数据一致（如果使用）
3. 简报数据关联的模板ID、策略ID需要与实际加载的数据一致
4. 简报推送记录关联的简报ID需要与实际加载的简报数据一致
5. 简报推送记录的目标ID需要与实际加载的用户、角色、组织数据一致
6. 简报模板中的变量占位符需要与实际数据匹配
7. 简报策略中的触发配置（JSON格式）需要符合系统要求
8. 简报数据中的JSON字段（data_summary、industry_data、region_data、time_data）需要是有效的JSON格式
9. 简报推送的推送时间需要晚于简报数据的生成时间
10. 简报推送的阅读时间需要晚于推送时间（如果已读）

