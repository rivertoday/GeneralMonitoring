# 预案模块 - 演示数据初始化

本目录包含预案模块的初始演示数据，用于系统演示和功能测试。

## 文件说明

### 1. `initial_emergency_plans.json` - 应急预案数据
- **数量**: 3个预案
- **内容**: 
  - 1个综合应急预案（危化品事故应急预案）
  - 1个综合应急预案（防汛应急预案）
  - 1个现场处置方案（马钢焦化厂危化品泄漏现场处置方案）
- **依赖**: 
  - `initial_organizations.json` (users模块)
  - `initial_users.json` (users模块)

### 2. `initial_plan_structures.json` - 预案结构数据
- **数量**: 7个结构节点
- **内容**: 
  - 预案1（危化品）: 5个节点（总则、组织体系、预警与信息报告、应急响应）
  - 预案2（防汛）: 2个节点（总则、汛情监测与预警）
- **依赖**: `initial_emergency_plans.json`
- **树形结构**: 支持多级树形结构（章节->条款->子条款）

### 3. `initial_plan_flows.json` - 预案流程数据
- **数量**: 6个流程节点
- **内容**: 
  - 预案1（危化品）: 3个主流程 + 1个子流程节点
    - 事故信息接报与响应启动
    - 现场处置与救援（含人员疏散子节点）
    - 应急结束与总结评估
  - 预案2（防汛）: 2个主流程
    - 汛情监测与预警发布
    - 防汛抢险与人员转移
- **依赖**: `initial_emergency_plans.json`
- **树形结构**: 支持多级树形结构（主流程->子流程->任务节点）

### 4. `initial_plan_tasks.json` - 预案任务数据
- **数量**: 7个任务
- **内容**: 
  - 预案1（危化品）: 5个任务（信息接报、启动响应、人员疏散、泄漏控制、环境监测）
  - 预案2（防汛）: 2个任务（水位监测预警、堤防巡查抢险）
- **依赖**: 
  - `initial_emergency_plans.json`
  - `initial_plan_flows.json`
  - `initial_organizations.json` (users模块)
  - `initial_roles.json` (users模块)

### 5. `initial_plan_executions.json` - 预案执行记录数据
- **数量**: 3条执行记录
- **内容**: 
  - 1条实战执行（进行中）- 危化品事故应急预案
  - 1条实战执行（已完成）- 防汛应急预案
  - 1条演练执行（已完成）- 现场处置方案
- **依赖**: 
  - `initial_emergency_plans.json`
  - `initial_risk_warnings.json` (risk模块，可选)
  - `initial_users.json` (users模块)
  - `initial_plan_flows.json`

## 数据加载顺序

由于存在外键依赖关系，请按照以下顺序加载fixtures：

```bash
# 1. 基础数据（用户、组织、角色）- 如果还未加载
python manage.py loaddata apps/users/fixtures/initial_organizations.json
python manage.py loaddata apps/users/fixtures/initial_users.json
python manage.py loaddata apps/users/fixtures/initial_roles.json

# 2. 预警数据（如果需要关联预警）- 如果还未加载
python manage.py loaddata apps/risk/fixtures/initial_risk_warnings.json

# 3. 应急预案
python manage.py loaddata apps/plan/fixtures/initial_emergency_plans.json

# 4. 预案结构（依赖应急预案）
python manage.py loaddata apps/plan/fixtures/initial_plan_structures.json

# 5. 预案流程（依赖应急预案）
python manage.py loaddata apps/plan/fixtures/initial_plan_flows.json

# 6. 预案任务（依赖应急预案、流程、组织、角色）
python manage.py loaddata apps/plan/fixtures/initial_plan_tasks.json

# 7. 预案执行记录（依赖应急预案、预警、用户、流程）
python manage.py loaddata apps/plan/fixtures/initial_plan_executions.json
```

## 数据说明

### 预案类型分布
- **综合应急预案**: 2个（危化品、防汛）
- **现场处置方案**: 1个（企业级）

### 预案状态分布
- **已发布**: 3个

### 流程结构
- **主流程**: 5个（3个危化品预案流程 + 2个防汛预案流程）
- **子流程/任务节点**: 1个（人员疏散）

### 任务类型分布
- **信息收集**: 2个
- **决策指挥**: 1个
- **资源调配**: 0个
- **现场处置**: 4个
- **其他**: 0个

### 执行记录状态
- **进行中**: 1条（危化品实战执行）
- **已完成**: 2条（防汛实战执行、现场处置演练）

## 业务流程示例

### 危化品事故应急预案执行流程
1. **接报与启动**: 接报事故信息 -> 核实信息 -> 启动应急响应
2. **现场处置**: 人员疏散 -> 泄漏控制 -> 环境监测与污染处置
3. **应急结束**: 事故评估 -> 应急结束

### 防汛应急预案执行流程
1. **监测预警**: 水位监测 -> 预警发布
2. **抢险转移**: 堤防巡查 -> 抢险加固 -> 人员转移

## 注意事项

1. 预案执行记录中关联的预警ID（warning_id）需要与实际加载的预警数据一致
2. 任务的assign_role_id需要与实际加载的角色数据一致
3. 预案的组织ID和用户ID需要与实际加载的基础数据一致
4. 如果基础数据（用户、组织、角色）的ID发生变化，需要相应调整这些fixtures中的外键ID
5. 预案结构的树形结构通过parent_id关联，确保parent_id指向正确的父节点
6. 预案流程的树形结构通过parent_id关联，next_flow_ids为JSON数组格式

