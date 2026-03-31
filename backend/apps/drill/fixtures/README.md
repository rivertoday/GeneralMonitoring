# 演练模块 Fixtures 使用说明

## 文件说明

本目录包含演练模块的初始化数据文件，用于演示数据初始化。

### 文件列表

1. **`initial_drill_events.json`** - 演练事件数据
   - 包含5个演练事件
   - 覆盖不同事故类型（危化品泄漏、防汛抢险、危化品火灾、建筑施工坍塌、森林火灾）
   - 包含不同演练状态（已完成、进行中、未开始）
   - 关联预案、组织等数据

2. **`initial_drill_evaluations.json`** - 演练评价数据
   - 包含12条演练评价记录
   - 覆盖不同节点类型（信息收集、决策指挥、资源调配、现场处置、其他）
   - 包含不同评价等级（优秀、良好）
   - 关联演练事件、评价人等数据

3. **`initial_drill_summaries.json`** - 演练总结数据
   - 包含3条演练总结记录
   - 对应已完成的演练事件
   - 包含完整的评价维度（内部沟通、预案熟悉程度、预案可操作性、职责定位、应急指挥、应急处置）
   - 包含总体评分和等级

4. **`initial_drill_analyses.json`** - 演练分析统计数据
   - 包含6条统计分析记录
   - 包含日报、月报等统计类型
   - 包含按单位、按事故类型的统计分析
   - 包含演练次数、完成次数、优秀/良好/合格/不合格次数、平均分等统计指标

## 数据加载顺序

**重要**：必须按照以下顺序加载fixtures，确保数据关联关系正确：

```bash
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

## 数据特点

### 演练事件
- **事件编码**: DRILL001-DRILL005
- **事故类型**: 危化品泄漏、防汛抢险、危化品火灾、建筑施工坍塌、森林火灾
- **演练状态**: 已完成（2个）、进行中（1个）、未开始（1个）
- **地理位置**: 所有事件均位于马鞍山市范围内
- **时间分布**: 2024年10月至12月

### 演练评价
- **节点类型**: 信息收集、决策指挥、资源调配、现场处置、其他
- **评价等级**: 优秀、良好
- **评价得分**: 85-93分
- **评价人**: 关联用户ID 3（监测预警用户）

### 演练总结
- **总体等级**: 优秀（1个）、良好（2个）
- **总体得分**: 88.60-91.50分
- **评价维度**: 包含6个维度的详细评价
- **总结人**: 关联用户ID 3

### 演练分析
- **统计类型**: 日报、月报
- **统计维度**: 全部单位、按单位、按事故类型
- **统计指标**: 演练次数、完成次数、优秀/良好/合格/不合格次数、平均分、完成率

## 数据关联关系

- **演练事件** → 关联组织（organization_id）、预案（related_plan_id）
- **演练评价** → 关联演练事件（event_id）、评价人（evaluator_id）
- **演练总结** → 关联演练事件（event_id，唯一）、总结人（summary_user_id）
- **演练分析** → 基于演练事件、评价、总结生成统计数据

## 注意事项

1. **外键关联**: 确保关联的组织、用户、预案等数据已加载
2. **唯一性约束**: 演练总结的event_id必须唯一，一个事件只能有一个总结
3. **时间逻辑**: 演练评价和总结的时间应在演练事件时间之后
4. **统计数据**: 演练分析数据基于已完成的演练事件生成，确保数据一致性

## 验证数据

加载完成后，可以通过以下方式验证数据：

```bash
# 进入Django shell
python manage.py shell

# 检查演练事件数量
from apps.drill.models import DrillEvent
print(DrillEvent.objects.count())

# 检查演练评价数量
from apps.drill.models import DrillEvaluation
print(DrillEvaluation.objects.count())

# 检查演练总结数量
from apps.drill.models import DrillSummary
print(DrillSummary.objects.count())

# 检查演练分析数量
from apps.drill.models import DrillAnalysis
print(DrillAnalysis.objects.count())
```

