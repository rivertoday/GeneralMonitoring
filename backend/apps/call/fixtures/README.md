# 叫应模块 - 演示数据初始化

本目录包含叫应模块的初始演示数据，用于系统演示和功能测试。

## 文件说明

### 1. `initial_call_groups.json` - 叫应分组数据
- **数量**: 3个分组
- **内容**: 
  - 1个常态化分组（日常政策传达组）
  - 2个非常态化分组（红色I级、橙色Ⅱ级应急响应组）
- **依赖**: 无

### 2. `initial_call_targets.json` - 叫应对象数据
- **数量**: 5个对象
- **内容**: 
  - 2个政府部门（雨山区、花山区应急管理局）
  - 2个企业单位（马钢焦化厂、中石化油库）
  - 1个事业单位（马鞍山市第一人民医院）
- **依赖**: 
  - `initial_organizations.json` (users模块，可选)

### 3. `initial_call_persons.json` - 叫应人员数据
- **数量**: 5个人员
- **内容**: 
  - 2个红色I级应急响应组人员（张指挥、李副指挥）
  - 2个橙色Ⅱ级应急响应组人员（王主任、刘队长）
  - 1个日常政策传达组人员（赵科长）
- **依赖**: 
  - `initial_call_groups.json`
  - `initial_organizations.json` (users模块，可选)

### 4. `initial_policy_files.json` - 政策文件数据
- **数量**: 3个文件
- **内容**: 
  - 2个已发布文件（危化品安全管理通知、防汛应急预案修订版通知）
  - 1个未发布文件（应急演练工作实施方案）
- **依赖**: 
  - `initial_users.json` (users模块)

### 5. `initial_policy_distributions.json` - 政策文件下发数据
- **数量**: 4条下发记录
- **内容**: 
  - 2条危化品安全管理通知下发（马钢焦化厂、中石化油库）
  - 2条防汛应急预案修订版下发（雨山区、花山区应急管理局）
  - 包含不同反馈状态（未反馈、已反馈、超时未反馈）
  - 包含督办状态（无需督办、待督办）
- **依赖**: 
  - `initial_policy_files.json`
  - `initial_call_targets.json`
  - `initial_users.json` (users模块)

### 6. `initial_call_records.json` - 叫应记录数据
- **数量**: 5条叫应记录
- **内容**: 
  - 2条常态化叫应（政策文件下发，系统消息、短信）
  - 3条非常态化叫应（预警触发、一键叫应，电话、短信）
  - 包含不同叫应状态、接收状态、响应状态
- **依赖**: 
  - `initial_policy_distributions.json` (常态化叫应)
  - `initial_risk_warnings.json` (risk模块，预警触发)
  - `initial_call_targets.json`
  - `initial_call_persons.json`
  - `initial_call_groups.json`

## 数据加载顺序

由于存在外键依赖关系，请按照以下顺序加载fixtures：

```bash
# 1. 基础数据（用户、组织）- 如果还未加载
python manage.py loaddata apps/users/fixtures/initial_organizations.json
python manage.py loaddata apps/users/fixtures/initial_users.json

# 2. 预警数据（预警触发叫应）- 如果还未加载
python manage.py loaddata apps/risk/fixtures/initial_risk_warnings.json

# 3. 叫应分组
python manage.py loaddata apps/call/fixtures/initial_call_groups.json

# 4. 叫应对象
python manage.py loaddata apps/call/fixtures/initial_call_targets.json

# 5. 叫应人员（依赖分组）
python manage.py loaddata apps/call/fixtures/initial_call_persons.json

# 6. 政策文件（依赖用户）
python manage.py loaddata apps/call/fixtures/initial_policy_files.json

# 7. 政策文件下发（依赖文件、对象、用户）
python manage.py loaddata apps/call/fixtures/initial_policy_distributions.json

# 8. 叫应记录（依赖下发、预警、对象、人员、分组）
python manage.py loaddata apps/call/fixtures/initial_call_records.json
```

## 数据说明

### 叫应分组类型分布
- **常态化分组**: 1个（日常政策传达组）
- **非常态化分组**: 2个（红色I级、橙色Ⅱ级应急响应组）

### 叫应对象类型分布
- **政府部门**: 2个
- **企业单位**: 2个
- **事业单位**: 1个

### 政策文件状态分布
- **已发布**: 2个
- **未发布**: 1个

### 政策下发反馈状态
- **未反馈**: 1条（马钢焦化厂）
- **已反馈**: 2条（中石化油库、雨山区应急管理局）
- **超时未反馈**: 1条（花山区应急管理局，已督办）

### 叫应记录类型分布
- **常态化叫应**: 2条（政策文件下发）
- **非常态化叫应**: 3条（预警触发2条、一键叫应1条）

### 叫应渠道分布
- **系统消息**: 1条
- **短信**: 2条
- **电话**: 2条

## 业务流程示例

### 常态化叫应流程
1. **政策文件上传**: 上传政策文件
2. **政策文件发布**: 发布政策文件
3. **政策文件下发**: 向叫应对象下发政策文件
4. **叫应通知**: 通过系统消息或短信向对象发送叫应通知
5. **反馈跟踪**: 跟踪对象反馈情况，必要时进行督办

### 非常态化叫应流程（预警触发）
1. **预警触发**: 系统检测到预警事件
2. **自动叫应**: 根据预警级别，自动向对应应急响应组进行叫应
3. **多渠道通知**: 通过电话、短信等方式通知相关人员
4. **响应确认**: 接收人员确认收到并响应

### 一键叫应流程
1. **选择对象**: 选择叫应人员或分组
2. **选择渠道**: 选择叫应渠道（电话、短信、系统消息）
3. **发送叫应**: 发送叫应通知
4. **响应跟踪**: 跟踪响应状态

## 注意事项

1. 叫应人员关联的分组ID需要与实际加载的分组数据一致
2. 政策文件下发关联的文件ID、对象ID需要与实际加载的数据一致
3. 叫应记录关联的预警ID需要与实际加载的预警数据一致
4. 如果基础数据（用户、组织）的ID发生变化，需要相应调整这些fixtures中的外键ID
5. 叫应记录的叫应时间、接收时间、响应时间需要符合逻辑顺序
6. 政策文件下发的反馈截止时间需要在下发时间之后

