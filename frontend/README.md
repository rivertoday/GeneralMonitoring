# 风险监测预警系统 - 前端开发文档

## 1. 项目概述

### 1.1 项目定位
风险监测预警系统前端部分包含两个独立的应用：
- **业务管理后台**：提供系统业务功能的管理界面
- **大屏展示系统**：提供三个一张图的大屏可视化展示

### 1.2 技术栈

#### 1.2.1 业务管理后台
- **框架**: Vue 3.0
- **语言**: TypeScript
- **UI组件库**: Element Plus / Ant Design Vue
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP客户端**: Axios
- **构建工具**: Vite
- **Node版本**: Node.js 22.12

#### 1.2.2 大屏展示系统
- **框架**: Vue 3.0
- **语言**: TypeScript
- **可视化**: ECharts
- **大屏组件**: DataV
- **地图引擎**: Cesium 1.108.0
- **地图服务**: 天地图（Tianditu）
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP客户端**: Axios
- **构建工具**: Vite
- **Node版本**: Node.js 22.12

### 1.3 项目结构

```
frontend/
├── admin/                    # 业务管理后台
│   ├── src/
│   │   ├── api/             # API接口封装
│   │   ├── assets/          # 静态资源
│   │   ├── components/      # 公共组件
│   │   ├── views/           # 页面组件
│   │   ├── router/          # 路由配置
│   │   ├── store/           # 状态管理（Pinia）
│   │   ├── utils/           # 工具函数
│   │   ├── styles/          # 样式文件
│   │   └── main.ts          # 入口文件
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
└── screen/                  # 大屏展示系统
    ├── src/
    │   ├── api/             # API接口封装
    │   ├── assets/          # 静态资源
    │   ├── components/      # 公共组件
    │   │   ├── charts/      # 图表组件
    │   │   ├── map/         # 地图组件
    │   │   └── widgets/     # 大屏组件
    │   ├── views/           # 页面组件
    │   ├── router/          # 路由配置
    │   ├── store/           # 状态管理
    │   ├── utils/           # 工具函数
    │   ├── styles/          # 样式文件（大屏专用样式）
    │   └── main.ts          # 入口文件
    ├── public/
    ├── package.json
    └── vite.config.ts
```

---

## 2. 业务管理后台设计

### 2.1 项目初始化

#### 2.1.1 创建项目
```bash
cd frontend
npm create vite@latest admin -- --template vue-ts
cd admin
npm install
```

#### 2.1.2 安装核心依赖
```bash
# UI组件库（选择其一）
npm install element-plus @element-plus/icons-vue
# 或
npm install ant-design-vue @ant-design/icons-vue

# 状态管理
npm install pinia

# 路由
npm install vue-router@4

# HTTP客户端
npm install axios

# 工具库
npm install dayjs
npm install lodash-es
npm install @types/lodash-es
```

#### 2.1.3 安装开发依赖
```bash
npm install -D @types/node
npm install -D sass
npm install -D @vitejs/plugin-vue
```

### 2.2 目录结构设计

```
admin/src/
├── api/                      # API接口封装
│   ├── index.ts              # Axios实例配置
│   ├── request.ts            # 请求拦截器、响应拦截器
│   ├── types.ts              # API类型定义
│   ├── modules/              # 按模块划分的API
│   │   ├── auth.ts           # 认证相关API
│   │   ├── user.ts           # 用户管理API
│   │   ├── risk.ts           # 风险监测预警API
│   │   ├── brief.ts          # 简报API
│   │   ├── call.ts           # 叫应API
│   │   ├── plan.ts           # 预案API
│   │   ├── safety.ts         # 安全态势API
│   │   ├── drill.ts          # 演练API
│   │   └── system.ts         # 系统管理API
│   └── constants.ts          # API常量
│
├── assets/                   # 静态资源
│   ├── images/              # 图片资源
│   ├── icons/                # 图标资源
│   └── fonts/                # 字体资源
│
├── components/               # 公共组件
│   ├── common/               # 通用组件
│   │   ├── PageHeader.vue    # 页面头部
│   │   ├── PageTable.vue     # 表格组件（封装分页、搜索等）
│   │   ├── PageForm.vue       # 表单组件
│   │   ├── PageDialog.vue    # 对话框组件
│   │   ├── PageDrawer.vue    # 抽屉组件
│   │   ├── UploadImage.vue   # 图片上传组件
│   │   ├── UploadFile.vue    # 文件上传组件
│   │   └── RichTextEditor.vue # 富文本编辑器
│   ├── layout/                # 布局组件
│   │   ├── AppLayout.vue     # 主布局
│   │   ├── AppHeader.vue     # 顶部导航
│   │   ├── AppSidebar.vue    # 侧边栏
│   │   └── AppBreadcrumb.vue # 面包屑导航
│   └── business/             # 业务组件
│       ├── MapPicker.vue     # 地图选点组件
│       ├── MapViewer.vue     # 地图查看组件
│       ├── StatusTag.vue     # 状态标签组件
│       └── LevelTag.vue      # 级别标签组件（四色预警）
│
├── views/                    # 页面组件
│   ├── login/                # 登录页面
│   │   └── Login.vue
│   ├── dashboard/            # 仪表盘
│   │   └── Dashboard.vue
│   ├── risk/                 # 风险监测预警模块
│   │   ├── monitor/          # 风险监测
│   │   │   ├── MonitorList.vue      # 监测点列表
│   │   │   ├── MonitorDetail.vue    # 监测点详情
│   │   │   └── MonitorForm.vue      # 监测点表单
│   │   ├── warning/          # 风险预警
│   │   │   ├── WarningList.vue      # 预警列表
│   │   │   ├── WarningDetail.vue    # 预警详情
│   │   │   ├── WarningForm.vue      # 预警表单
│   │   │   └── WarningPublish.vue   # 预警发布
│   │   ├── alarm/            # 报警管理
│   │   │   ├── AlarmList.vue        # 报警列表
│   │   │   ├── AlarmDetail.vue      # 报警详情
│   │   │   └── AlarmHandle.vue      # 报警处理
│   │   ├── rule/             # 预警规则
│   │   │   ├── RuleList.vue         # 规则列表
│   │   │   ├── RuleForm.vue         # 规则表单
│   │   │   └── RuleConfig.vue      # 规则配置
│   │   ├── level/            # 预警级别
│   │   │   ├── LevelList.vue        # 级别列表
│   │   │   └── LevelForm.vue        # 级别表单
│   │   ├── danger/           # 隐患排查
│   │   │   ├── DangerList.vue       # 隐患列表
│   │   │   ├── DangerDetail.vue     # 隐患详情
│   │   │   └── DangerForm.vue      # 隐患表单
│   │   ├── rectification/    # 隐患整改
│   │   │   ├── RectificationList.vue    # 整改列表
│   │   │   ├── RectificationDetail.vue  # 整改详情
│   │   │   ├── RectificationForm.vue   # 整改表单
│   │   │   └── RectificationVerify.vue  # 整改验收
│   │   └── statistics/       # 统计分析
│   │       └── Statistics.vue
│   ├── brief/                # 简报模块
│   │   ├── template/         # 简报模板
│   │   │   ├── TemplateList.vue
│   │   │   ├── TemplateForm.vue
│   │   │   └── TemplateEditor.vue
│   │   ├── strategy/         # 简报策略
│   │   │   ├── StrategyList.vue
│   │   │   ├── StrategyForm.vue
│   │   │   └── StrategyConfig.vue
│   │   ├── data/             # 简报数据
│   │   │   ├── DataList.vue
│   │   │   ├── DataDetail.vue
│   │   │   └── DataGenerate.vue
│   │   └── push/             # 简报推送
│   │       ├── PushList.vue
│   │       └── PushDetail.vue
│   ├── call/                 # 叫应模块
│   │   ├── target/           # 叫应对象
│   │   │   ├── TargetList.vue
│   │   │   └── TargetForm.vue
│   │   ├── person/           # 叫应人员
│   │   │   ├── PersonList.vue
│   │   │   └── PersonForm.vue
│   │   ├── group/            # 叫应分组
│   │   │   ├── GroupList.vue
│   │   │   └── GroupForm.vue
│   │   ├── policy/           # 政策文件
│   │   │   ├── PolicyList.vue
│   │   │   ├── PolicyForm.vue
│   │   │   ├── PolicyUpload.vue
│   │   │   └── PolicyPublish.vue
│   │   ├── distribution/     # 政策下发
│   │   │   ├── DistributionList.vue
│   │   │   ├── DistributionDetail.vue
│   │   │   └── DistributionFeedback.vue
│   │   ├── record/           # 叫应记录
│   │   │   ├── RecordList.vue
│   │   │   └── RecordDetail.vue
│   │   └── emergency/        # 一键叫应
│   │       └── EmergencyCall.vue
│   ├── plan/                 # 预案模块
│   │   ├── plan/             # 应急预案
│   │   │   ├── PlanList.vue
│   │   │   ├── PlanDetail.vue
│   │   │   ├── PlanForm.vue
│   │   │   └── PlanPublish.vue
│   │   ├── structure/        # 预案结构
│   │   │   ├── StructureTree.vue
│   │   │   └── StructureEditor.vue
│   │   ├── flow/             # 预案流程
│   │   │   ├── FlowList.vue
│   │   │   ├── FlowEditor.vue
│   │   │   └── FlowViewer.vue
│   │   ├── task/             # 预案任务
│   │   │   ├── TaskList.vue
│   │   │   └── TaskForm.vue
│   │   └── execution/        # 预案执行
│   │       ├── ExecutionList.vue
│   │       ├── ExecutionDetail.vue
│   │       └── ExecutionMonitor.vue
│   ├── safety/               # 安全态势模块
│   │   ├── resource/          # 安全资源
│   │   │   ├── ResourceList.vue
│   │   │   └── ResourceForm.vue
│   │   ├── target/           # 防护目标
│   │   │   ├── TargetList.vue
│   │   │   └── TargetForm.vue
│   │   ├── shelter/           # 避难场所
│   │   │   ├── ShelterList.vue
│   │   │   └── ShelterForm.vue
│   │   ├── hazard/           # 危险源
│   │   │   ├── HazardList.vue
│   │   │   └── HazardForm.vue
│   │   └── video/             # 视频监控
│   │       ├── VideoList.vue
│   │       └── VideoForm.vue
│   ├── drill/                # 演练模块
│   │   ├── event/            # 演练事件
│   │   │   ├── EventList.vue
│   │   │   ├── EventDetail.vue
│   │   │   └── EventForm.vue
│   │   ├── evaluation/       # 演练评价
│   │   │   ├── EvaluationList.vue
│   │   │   └── EvaluationForm.vue
│   │   ├── summary/          # 演练总结
│   │   │   ├── SummaryList.vue
│   │   │   ├── SummaryDetail.vue
│   │   │   └── SummaryForm.vue
│   │   └── analysis/         # 演练分析
│   │       └── Analysis.vue
│   ├── system/               # 系统管理模块
│   │   ├── user/             # 用户管理
│   │   │   ├── UserList.vue
│   │   │   └── UserForm.vue
│   │   ├── role/             # 角色管理
│   │   │   ├── RoleList.vue
│   │   │   └── RoleForm.vue
│   │   ├── permission/        # 权限管理
│   │   │   ├── PermissionTree.vue
│   │   │   └── PermissionForm.vue
│   │   ├── organization/     # 组织管理
│   │   │   ├── OrganizationTree.vue
│   │   │   └── OrganizationForm.vue
│   │   ├── datasource/       # 数据源管理
│   │   │   ├── DatasourceList.vue
│   │   │   └── DatasourceForm.vue
│   │   └── template/         # 消息模板
│   │       ├── TemplateList.vue
│   │       └── TemplateForm.vue
│   └── screen/               # 大屏入口
│       └── ScreenOverview.vue
│
├── router/                   # 路由配置
│   ├── index.ts              # 路由主文件
│   ├── modules/              # 路由模块
│   │   ├── risk.ts           # 风险监测预警路由
│   │   ├── brief.ts          # 简报路由
│   │   ├── call.ts           # 叫应路由
│   │   ├── plan.ts           # 预案路由
│   │   ├── safety.ts         # 安全态势路由
│   │   ├── drill.ts          # 演练路由
│   │   └── system.ts         # 系统管理路由
│   └── guards.ts             # 路由守卫
│
├── store/                    # 状态管理（Pinia）
│   ├── index.ts              # Store入口
│   ├── modules/              # Store模块
│   │   ├── auth.ts           # 认证状态
│   │   ├── user.ts           # 用户信息
│   │   ├── app.ts            # 应用状态（主题、布局等）
│   │   └── permission.ts    # 权限状态
│   └── types.ts              # Store类型定义
│
├── utils/                    # 工具函数
│   ├── request.ts            # HTTP请求封装
│   ├── auth.ts               # 认证工具
│   ├── storage.ts            # 本地存储工具
│   ├── format.ts             # 格式化工具
│   ├── validate.ts           # 验证工具
│   ├── constants.ts          # 常量定义
│   └── helpers.ts            # 辅助函数
│
├── styles/                   # 样式文件
│   ├── variables.scss        # 变量定义
│   ├── mixins.scss           # Mixin定义
│   ├── common.scss           # 通用样式
│   └── element-plus.scss     # Element Plus样式覆盖
│
├── types/                    # TypeScript类型定义
│   ├── api.ts                # API类型
│   ├── common.ts             # 通用类型
│   └── modules/              # 模块类型
│       ├── risk.ts
│       ├── brief.ts
│       ├── call.ts
│       ├── plan.ts
│       ├── safety.ts
│       ├── drill.ts
│       └── system.ts
│
├── App.vue                   # 根组件
└── main.ts                   # 入口文件
```

### 2.3 核心功能模块设计

#### 2.3.1 风险监测预警模块

**功能页面**:
- **风险监测**: 监测点列表、监测点详情、监测点配置、实时数据展示
- **风险预警**: 预警列表、预警详情、预警发布、预警处置
- **报警管理**: 报警列表、报警处理、报警统计
- **预警规则**: 规则列表、规则配置、规则测试
- **预警级别**: 级别管理（四色预警：红、橙、黄、蓝）
- **隐患排查**: 隐患列表、隐患详情、隐患录入
- **隐患整改**: 整改列表、整改详情、整改验收
- **统计分析**: 报警统计、预警统计、趋势分析

**关键组件**:
- `MapPicker.vue`: 地图选点组件（用于选择监测点位置）
- `MapViewer.vue`: 地图查看组件（展示监测点、预警位置）
- `LevelTag.vue`: 预警级别标签（四色显示）
- `StatusTag.vue`: 状态标签（预警状态、报警状态等）
- `RealTimeMonitor.vue`: 实时监测数据展示组件

#### 2.3.2 简报模块

**功能页面**:
- **简报模板**: 模板列表、模板编辑、变量配置
- **简报策略**: 策略列表、策略配置、触发条件设置
- **简报数据**: 简报列表、简报详情、简报生成
- **简报推送**: 推送记录、推送状态、推送渠道管理

**关键组件**:
- `TemplateEditor.vue`: 模板编辑器（支持变量占位符）
- `StrategyConfig.vue`: 策略配置组件（定时触发、事件触发）
- `BriefViewer.vue`: 简报查看组件（支持PDF预览）

#### 2.3.3 叫应模块

**功能页面**:
- **叫应对象**: 对象列表、对象管理（政府部门、企业单位、事业单位）
- **叫应人员**: 人员列表、人员管理、人员分组
- **叫应分组**: 分组列表、分组管理（常态化分组、非常态化分组）
- **政策文件**: 文件列表、文件上传、文件发布
- **政策下发**: 下发列表、下发管理、反馈跟踪、督办管理
- **叫应记录**: 记录列表、记录详情、叫应统计
- **一键叫应**: 一键叫应界面（支持选择人员/分组、选择渠道）

**关键组件**:
- `FileUpload.vue`: 文件上传组件（政策文件上传）
- `CallConfig.vue`: 叫应配置组件（选择人员、分组、渠道）
- `FeedbackForm.vue`: 反馈表单组件

#### 2.3.4 预案模块

**功能页面**:
- **应急预案**: 预案列表、预案详情、预案发布、预案版本管理
- **预案结构**: 结构树、结构编辑（章节、条款）
- **预案流程**: 流程列表、流程编辑（流程图编辑）
- **预案任务**: 任务列表、任务配置、任务分配
- **预案执行**: 执行列表、执行监控、执行记录

**关键组件**:
- `StructureTree.vue`: 预案结构树组件
- `FlowEditor.vue`: 流程图编辑器（基于流程图库）
- `TaskAssign.vue`: 任务分配组件

#### 2.3.5 安全态势模块

**功能页面**:
- **安全资源**: 资源列表、资源管理（救援队伍、应急专家、物资装备）
- **防护目标**: 目标列表、目标管理（学校、居民区等）
- **避难场所**: 场所列表、场所管理
- **危险源**: 危险源列表、危险源管理（重大危险源、一般危险源）
- **视频监控**: 监控设施列表、监控设施管理

**关键组件**:
- `ResourceForm.vue`: 资源表单组件（支持不同类型资源）
- `MapResourceViewer.vue`: 地图资源查看组件

#### 2.3.6 演练模块

**功能页面**:
- **演练事件**: 事件列表、事件详情、事件录入
- **演练评价**: 评价列表、评价录入（节点评价）
- **演练总结**: 总结列表、总结详情、总结录入
- **演练分析**: 统计分析（按单位、类型、事故类型统计）

**关键组件**:
- `EvaluationForm.vue`: 评价表单组件（支持多节点评价）
- `SummaryForm.vue`: 总结表单组件（包含多个评价维度）

#### 2.3.7 系统管理模块

**功能页面**:
- **用户管理**: 用户列表、用户表单、用户权限分配
- **角色管理**: 角色列表、角色表单、角色权限分配
- **权限管理**: 权限树、权限表单（菜单、按钮、接口）
- **组织管理**: 组织树、组织表单
- **数据源管理**: 数据源列表、数据源配置（API、数据库、文件）
- **消息模板**: 模板列表、模板编辑（系统消息、短信、邮件）

**关键组件**:
- `PermissionTree.vue`: 权限树组件
- `OrganizationTree.vue`: 组织树组件
- `DatasourceConfig.vue`: 数据源配置组件（支持多种类型）

### 2.4 路由设计

#### 2.4.1 路由结构
```
/login                          # 登录页
/dashboard                      # 仪表盘
/risk                           # 风险监测预警
  /risk/monitor                 # 风险监测
  /risk/warning                 # 风险预警
  /risk/alarm                   # 报警管理
  /risk/rule                    # 预警规则
  /risk/level                   # 预警级别
  /risk/danger                  # 隐患排查
  /risk/rectification           # 隐患整改
  /risk/statistics              # 统计分析
/brief                          # 简报
  /brief/template               # 简报模板
  /brief/strategy               # 简报策略
  /brief/data                   # 简报数据
  /brief/push                   # 简报推送
/call                           # 叫应
  /call/target                  # 叫应对象
  /call/person                  # 叫应人员
  /call/group                   # 叫应分组
  /call/policy                  # 政策文件
  /call/distribution            # 政策下发
  /call/record                  # 叫应记录
  /call/emergency               # 一键叫应
/plan                           # 预案
  /plan/plan                    # 应急预案
  /plan/structure                # 预案结构
  /plan/flow                    # 预案流程
  /plan/task                    # 预案任务
  /plan/execution               # 预案执行
/safety                         # 安全态势
  /safety/resource              # 安全资源
  /safety/target                # 防护目标
  /safety/shelter               # 避难场所
  /safety/hazard                # 危险源
  /safety/video                 # 视频监控
/drill                          # 演练
  /drill/event                  # 演练事件
  /drill/evaluation             # 演练评价
  /drill/summary                # 演练总结
  /drill/analysis               # 演练分析
/system                         # 系统管理
  /system/user                  # 用户管理
  /system/role                  # 角色管理
  /system/permission            # 权限管理
  /system/organization          # 组织管理
  /system/datasource            # 数据源管理
  /system/template              # 消息模板
/screen                         # 大屏入口
  /screen/overview              # 大屏总览
```

#### 2.4.2 路由守卫
- 登录验证：未登录用户重定向到登录页
- 权限验证：根据用户权限动态加载路由
- 页面标题：根据路由自动设置页面标题

### 2.5 状态管理设计

#### 2.5.1 Auth Store
```typescript
interface AuthState {
  token: string | null
  refreshToken: string | null
  user: UserInfo | null
  permissions: string[]
  roles: string[]
}
```

#### 2.5.2 User Store
```typescript
interface UserState {
  currentUser: UserInfo | null
  userList: UserInfo[]
}
```

#### 2.5.3 App Store
```typescript
interface AppState {
  theme: 'light' | 'dark'
  sidebarCollapsed: boolean
  screenSize: 'desktop' | 'tablet' | 'mobile'
}
```

#### 2.5.4 Permission Store
```typescript
interface PermissionState {
  routes: RouteRecordRaw[]
  permissions: string[]
  roles: string[]
}
```

### 2.6 API接口封装

#### 2.6.1 Axios配置
- 基础URL配置
- 请求拦截器（添加Token）
- 响应拦截器（统一错误处理、Token刷新）
- 请求超时设置

#### 2.6.2 API模块划分
- `auth.ts`: 认证相关API（登录、登出、刷新Token）
- `user.ts`: 用户管理API
- `risk.ts`: 风险监测预警API
- `brief.ts`: 简报API
- `call.ts`: 叫应API
- `plan.ts`: 预案API
- `safety.ts`: 安全态势API
- `drill.ts`: 演练API
- `system.ts`: 系统管理API

### 2.7 公共组件设计

#### 2.7.1 PageTable组件
- 支持分页
- 支持搜索
- 支持排序
- 支持批量操作
- 支持自定义列

#### 2.7.2 PageForm组件
- 支持表单验证
- 支持动态表单
- 支持表单布局
- 支持表单重置

#### 2.7.3 MapPicker组件
- 基于百度地图
- 支持选点
- 支持搜索地址
- 支持坐标转换

#### 2.7.4 MapViewer组件
- 基于百度地图
- 支持标记点展示
- 支持区域展示
- 支持信息窗口

---

## 3. 大屏展示系统设计

### 3.1 项目初始化

#### 3.1.1 创建项目
```bash
cd frontend
npm create vite@latest screen -- --template vue-ts
cd screen
npm install
```

#### 3.1.2 安装核心依赖
```bash
# 可视化
npm install echarts
npm install @dataview/datav-vue3

# 3D地图引擎
npm install cesium@1.108.0        # Cesium（与天地图官方支持版本一致）
npm install -D vite-plugin-cesium # Vite插件（处理Cesium静态资源）

# 状态管理
npm install pinia

# 路由
npm install vue-router@4

# HTTP客户端
npm install axios

# 工具库
npm install dayjs
npm install lodash-es
npm install @types/lodash-es
```

**注意**：
- Cesium版本需与天地图官方支持版本一致（当前使用1.108.0）
- 天地图扩展插件（Cesium_ext_min.js等）通过CDN动态加载，无需npm安装
- 需要在`.env`文件中配置`VITE_TIANDITU_APP_KEY`（天地图密钥）

#### 3.1.3 安装开发依赖
```bash
npm install -D @types/node
npm install -D sass
npm install -D @vitejs/plugin-vue
```

### 3.2 目录结构设计

```
screen/src/
├── api/                      # API接口封装
│   ├── index.ts              # Axios实例配置
│   ├── request.ts            # 请求拦截器、响应拦截器
│   ├── modules/              # 按模块划分的API
│   │   ├── safety.ts         # 安全态势API
│   │   └── monitor.ts        # 监测预警API
│   └── constants.ts          # API常量
│
├── assets/                   # 静态资源
│   ├── images/              # 图片资源
│   ├── icons/               # 图标资源
│   └── fonts/               # 字体资源
│
├── components/              # 公共组件
│   ├── charts/              # 图表组件
│   │   ├── LineChart.vue    # 折线图
│   │   ├── BarChart.vue     # 柱状图
│   │   ├── PieChart.vue     # 饼图
│   │   ├── MapChart.vue     # 地图图表
│   │   └── GaugeChart.vue   # 仪表盘
│   ├── map/                 # 地图组件
│   │   └── CesiumMap.vue    # Cesium地图组件（集成天地图底图）
│   └── widgets/             # 大屏组件
│       ├── NumberCard.vue   # 数字卡片
│       ├── ProgressBar.vue  # 进度条
│       ├── StatusIndicator.vue # 状态指示器
│       └── DataTable.vue    # 数据表格
│
├── views/                   # 页面组件
│   ├── overview/            # 大屏总览
│   │   └── Overview.vue
│   ├── safety-run/          # 安全运行一张图
│   │   └── SafetyRun.vue
│   ├── safety-status/       # 安全态势一张图
│   │   └── SafetyStatus.vue
│   └── monitor-warn/        # 监测预警一张图
│       └── MonitorWarn.vue
│
├── router/                  # 路由配置
│   └── index.ts
│
├── store/                   # 状态管理
│   ├── index.ts
│   └── modules/
│       ├── safety.ts        # 安全态势数据
│       └── monitor.ts       # 监测预警数据
│
├── utils/                   # 工具函数
│   ├── request.ts           # HTTP请求封装
│   ├── tianditu.ts          # 天地图工具（扩展插件加载、图层创建等）
│   ├── cesium-entity.ts     # Cesium实体工具（标记点、多边形等）
│   ├── marker-icons.ts      # 标记图标工具（生成SVG图标）
│   ├── chart.ts             # 图表工具
│   ├── format.ts            # 格式化工具
│   └── constants.ts         # 常量定义
│
├── styles/                  # 样式文件
│   ├── variables.scss       # 变量定义（大屏专用）
│   ├── mixins.scss          # Mixin定义
│   ├── common.scss          # 通用样式
│   └── screen.scss          # 大屏样式
│
├── types/                   # TypeScript类型定义
│   ├── api.ts               # API类型
│   ├── map.ts               # 地图类型
│   └── chart.ts             # 图表类型
│
├── App.vue                  # 根组件
└── main.ts                  # 入口文件
```

### 3.3 大屏功能设计

#### 3.3.1 安全运行一张图

**功能模块**:
- **GIS地图展示**: Cesium Viewer + 天地图矢量底图（球面墨卡托投影）
- **安全基础数据**: 危险源、防护目标、物资装备、救援队伍等资源上图
- **统计面板**:
  - 救援队伍统计（按类型：危化品、消防、应急抢险、医疗、社会救援）
  - 应急专家统计（按类型：行业专家、救援专家、技术专家）
  - 物资装备统计（按类型：个人防护、抢险救援、食品、药品、饮用水、人员庇护）
  - 防护目标统计（按类型：学校、居民区、医院、商场等）
  - 避难场所统计（按类型：公园、广场、体育场等，汇总容纳能力）
- **地图交互**:
  - 点击标记点显示详细信息
  - 支持地图缩放、平移
  - 支持场景模式切换（2D/3D/哥伦布视图）
  - 支持地图样式切换（矢量/影像/地形）
  - 支持根据风险位置进行资源分析

**技术实现**:
- Cesium Viewer提供地图引擎（支持2D/3D场景模式）
- 天地图矢量底图提供底图服务（2D模式使用vec_w+cva_w，球面墨卡托投影）
- Cesium Entity API渲染业务图层（标记点、区域等）
- 使用WebSocket或轮询获取实时数据
- 数据自动刷新（每30秒或1分钟）

#### 3.3.2 安全态势一张图

**功能模块**:
- **区域四色风险图**: 根据风险评估结果对区域进行四色图渲染（红、橙、黄、蓝）
- **行业态势展示**: 
  - 危险化学品行业态势
  - 防汛行业态势
  - 交通运输行业态势
  - 森林防火行业态势
- **区域态势展示**: 基于辖区内的街道，对安全态势数据进行分析和综合展示
- **统计图表**:
  - 风险等级分布（饼图）
  - 行业态势对比（柱状图）
  - 区域态势对比（柱状图）
  - 趋势分析（折线图）

**技术实现**:
- Cesium Entity API渲染四色风险区域（使用Polygon组件）
- ECharts展示统计图表
- 数据自动刷新

#### 3.3.3 监测预警一张图

**功能模块**:
- **实时监测数据展示**: 
  - 监测点在线状态统计
  - 监测数据分类统计
  - 监测数据趋势图表
- **预警事件地图标注**: 
  - 预警事件位置标注（不同级别不同颜色）
  - 预警事件列表
  - 预警事件详情弹窗
- **预警级别分布**: 预警级别统计（饼图、柱状图）
- **监测点在线状态**: 在线/离线监测点统计
- **预警处置进度**: 预警处置状态统计
- **视频监控点位展示**: 
  - 根据事发地定位或指定位置，自动标示出一定范围内的所有视频监控设施的位置
  - 支持视频流播放

**技术实现**:
- Cesium Viewer + 天地图矢量底图（2D模式，球面墨卡托投影）
- 预警事件使用Entity标记点展示（不同级别不同图标和颜色）
- 监测点使用Entity标记点展示（在线/离线不同状态）
- 视频监控设施使用Entity标记点展示
- 支持点击标记点显示详细信息
- 支持视频流播放（RTSP转HLS或WebRTC）

### 3.4 地图集成方案

#### 3.4.1 技术方案
- **3D地图引擎**: Cesium 1.108.0（支持2D、2.5D、3D场景模式）
- **底图服务**: 天地图（Tianditu）
  - 2D模式: 天地图矢量底图（vec_w）+ 矢量注记（cva_w），球面墨卡托投影
  - 3D模式: 天地图影像底图（img_w）+ 国界图层（ibo_w）
  - 地形模式: 天地图地形服务（swdx）+ 三维地名服务（GetTiles）
- **业务图层**: Cesium Entity API（标记点、多边形、标签等）

#### 3.4.2 实现步骤
1. 初始化Cesium Viewer（配置场景模式、相机参数等）
2. 将Cesium挂载到window对象上（天地图扩展插件需要）
3. 动态加载天地图扩展插件（long.min.js、bytebuffer.min.js、protobuf.min.js、Cesium_ext_min.js）
4. 根据场景模式加载对应的天地图底图图层（矢量/影像/地形）
5. 使用Cesium Entity API渲染业务数据（标记点、区域等）
6. 实现地图交互（点击、缩放、平移、场景切换等）

#### 3.4.3 关键组件
- `CesiumMap.vue`: Cesium地图组件（提供基础地图展示和交互功能）
- `cesium-entity.ts`: 业务实体工具函数（创建标记点、多边形等）
- `tianditu.ts`: 天地图工具函数（加载扩展插件、创建图层、地形服务等）
- `marker-icons.ts`: 标记图标工具（生成SVG图标）

### 3.5 数据刷新机制

#### 3.5.1 刷新策略
- **实时数据**: 每30秒刷新一次（监测数据、预警事件）
- **统计数据**: 每1分钟刷新一次（统计图表）
- **基础数据**: 每5分钟刷新一次（安全资源、危险源等）

#### 3.5.2 实现方式
- 使用`setInterval`定时刷新
- 或使用WebSocket实时推送（可选，演示系统可先使用轮询）

### 3.6 响应式布局

#### 3.6.1 适配方案
- 使用`vw`、`vh`单位进行布局
- 使用`scale`进行整体缩放
- 支持不同分辨率大屏（1920x1080、2560x1440等）

#### 3.6.2 布局组件
- 使用Grid布局或Flex布局
- 使用DataV的布局组件

---

## 4. 开发规范

### 4.1 代码规范

#### 4.1.1 TypeScript规范
- 使用TypeScript进行开发
- 定义清晰的类型接口
- 避免使用`any`类型

#### 4.1.2 Vue组件规范
- 使用Composition API
- 组件命名使用PascalCase
- Props和Emits定义类型
- 使用`<script setup>`语法

#### 4.1.3 文件命名规范
- 组件文件使用PascalCase：`UserList.vue`
- 工具文件使用camelCase：`formatDate.ts`
- 常量文件使用UPPER_SNAKE_CASE：`API_CONSTANTS.ts`

### 4.2 Git提交规范

使用Conventional Commits规范：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

### 4.3 组件开发规范

#### 4.3.1 组件结构
```vue
<template>
  <!-- 模板 -->
</template>

<script setup lang="ts">
// 导入
import { ref, computed, onMounted } from 'vue'
import type { ComponentProps } from './types'

// Props定义
interface Props {
  // ...
}
const props = defineProps<Props>()

// Emits定义
const emit = defineEmits<{
  // ...
}>()

// 状态
const state = ref()

// 计算属性
const computedValue = computed(() => {
  // ...
})

// 方法
const handleClick = () => {
  // ...
}

// 生命周期
onMounted(() => {
  // ...
})
</script>

<style scoped lang="scss">
// 样式
</style>
```

### 4.4 API调用规范

#### 4.4.1 API封装
- 所有API调用统一通过`api`目录下的模块
- 使用TypeScript定义请求和响应类型
- 统一错误处理

#### 4.4.2 请求示例
```typescript
// api/modules/risk.ts
import request from '@/api/request'
import type { RiskWarning, RiskWarningListParams } from '@/types/modules/risk'

export const getRiskWarningList = (params: RiskWarningListParams) => {
  return request.get<RiskWarning[]>('/api/v1/risk/warning/', { params })
}

export const createRiskWarning = (data: Partial<RiskWarning>) => {
  return request.post<RiskWarning>('/api/v1/risk/warning/', data)
}
```

---

## 5. 开发计划

### 5.1 第一阶段：基础框架搭建

#### 5.1.1 业务管理后台
- [x] 项目初始化（Vue 3 + TypeScript + Vite）
- [x] 安装核心依赖（Element Plus、Pinia、Vue Router、Axios）
- [x] 配置Axios（请求拦截器、响应拦截器）
- [x] 配置路由（路由结构、路由守卫）
- [x] 配置状态管理（Auth Store、User Store、App Store）
- [x] 搭建基础布局（顶部导航、侧边栏、面包屑）
- [x] 实现登录功能
- [x] 实现权限控制

#### 5.1.2 大屏展示系统
- [x] 项目初始化（Vue 3 + TypeScript + Vite）
- [x] 安装核心依赖（ECharts、DataV、Cesium 1.108.0）
  - 注：天地图扩展插件通过CDN动态加载，无需npm安装
- [x] 配置Axios
- [x] 配置路由
- [x] 搭建大屏基础布局
- [x] 集成Cesium地图引擎
- [x] 集成天地图底图服务（矢量图层、影像图层、地形服务）
- [x] 配置天地图扩展插件动态加载

### 5.2 第二阶段：核心功能开发

#### 5.2.1 业务管理后台
- [x] 风险监测预警模块
  - [x] 风险监测页面
  - [x] 风险预警页面
  - [x] 报警管理页面
  - [x] 预警规则页面
  - [x] 预警级别页面
  - [x] 隐患排查页面
  - [x] 隐患整改页面
  - [x] 统计分析页面
- [x] 简报模块
  - [x] 简报模板页面
  - [x] 简报策略页面
  - [x] 简报数据页面
  - [x] 简报推送页面
- [x] 叫应模块
  - [x] 叫应对象页面
  - [x] 叫应人员页面
  - [x] 叫应分组页面
  - [x] 政策文件页面
  - [x] 政策下发页面
  - [x] 叫应记录页面
  - [x] 一键叫应页面

#### 5.2.2 大屏展示系统
- [ ] 安全运行一张图
  - [x] 地图展示
  - [x] 资源标记
  - [x] 统计面板
- [x] 安全态势一张图
  - [x] 四色风险图
  - [x] 行业态势展示
  - [x] 区域态势展示
- [x] 监测预警一张图
  - [x] 实时监测数据
  - [x] 预警事件标注
  - [x] 视频监控展示

### 5.3 第三阶段：扩展功能开发

#### 5.3.1 业务管理后台
- [ ] 仪表盘模块
  - [x] **关键指标卡片**
    - [x] 预警事件统计（总数、按级别分布：红色I级、橙色Ⅱ级、黄色Ⅲ级、蓝色Ⅳ级）
    - [x] 报警记录统计（总数、按状态分布：待处理、处理中、已处理、已忽略）
    - [x] 预案统计（总数、按状态分布：已发布、已修订、已废止）
    - [x] 演练统计（总数、按状态分布：已完成、进行中、未开始）
    - [x] 安全资源统计（总数、按类型分布：救援队伍、应急专家、物资装备）
    - [x] 视频监控统计（总数、在线数、离线数）
    - [x] 数据源统计（总数、按状态分布：正常、异常）
    - [x] 叫应记录统计（总数、按状态分布：已响应、未响应）
  - [x] **数据图表展示**
    - [x] 预警事件趋势图（近7天/近30天预警数量趋势，折线图）
    - [x] 报警记录趋势图（近7天/近30天报警数量趋势，折线图）
    - [x] 预警级别分布图（饼图，展示各级别预警占比）
    - [x] 报警状态分布图（饼图，展示各状态报警占比）
    - [x] 预案类型分布图（柱状图，展示各类型预案数量）
    - [x] 演练完成情况图（柱状图，展示演练完成率）
    - [x] 行业态势对比图（柱状图，展示各行业预警/报警数量对比）
  - [x] **最近活动/通知**
    - [x] 最近预警事件列表（显示最近5-10条预警事件，包含级别、时间、状态）
    - [x] 最近报警记录列表（显示最近5-10条报警记录，包含状态、时间、处理人）
    - [x] 最近预案执行记录（显示最近5-10条预案执行记录，包含预案名称、状态、时间）
    - [x] 最近演练事件（显示最近5-10条演练事件，包含演练类型、状态、时间）
    - [x] 系统通知/消息（显示系统重要通知，如数据源异常、预警发布等）
  - [x] **快捷操作入口**
    - [x] 快速创建预警事件
    - [x] 快速创建报警记录
    - [x] 快速启动预案执行
    - [x] 快速创建演练事件
    - [x] 跳转到大屏展示（安全运行、安全态势、监测预警）
  - [x] **数据刷新机制**
    - [x] 实现数据自动刷新（每5分钟刷新一次统计数据、图表数据、最近活动）
    - [x] 支持手动刷新按钮（刷新所有数据：统计数据、图表、最近活动）
    - [x] 显示最后更新时间
    - [x] 页面可见性检测（页面不可见时暂停刷新，页面重新可见时立即刷新）
- [x] 预案模块
  - [x] 应急预案管理（列表、新增、编辑、查看、发布、修订、废止、删除）
  - [x] 预案结构管理（树形结构、新增、编辑、删除）
  - [x] 预案流程管理（树形流程、新增、编辑、删除、配置查看）
  - [x] 预案任务管理（列表、新增、编辑、查看、删除）
  - [x] 预案执行管理（列表、新增、编辑、查看、启动、更新状态、完成、终止、删除）
- [x] 安全态势模块
  - [x] 安全资源管理（列表、新增、编辑、查看、删除，支持三种资源类型）
  - [x] 防护目标管理（列表、新增、编辑、查看、删除）
  - [x] 避难场所管理（列表、新增、编辑、查看、删除）
  - [x] 危险源管理（列表、新增、编辑、查看、删除）
  - [x] 视频监控管理（列表、新增、编辑、查看、预览、删除）
- [x] 演练模块
  - [x] 演练事件（列表、新增、编辑、查看、删除）
  - [x] 演练评价（列表、新增、编辑、查看、删除）
  - [x] 演练总结（列表、新增、编辑、查看、删除）
  - [x] 演练分析（统计分析）
- [ ] 系统管理模块
  - [x] 用户管理（列表、新增、编辑、查看、删除、权限分配）
  - [x] 角色管理（列表、新增、编辑、查看、删除、权限分配）
  - [x] 权限管理（权限树、新增、编辑、查看、删除）
  - [x] 组织管理（组织树、新增、编辑、查看、删除）
  - [x] 数据源管理（列表、新增、编辑、查看、删除、同步）
  - [x] 消息模板（列表、新增、编辑、查看、删除）

#### 5.3.2 大屏展示系统

**目标**：让三个大屏能够正确展示后端导入的演示数据集并正常交互。

**当前状态**：
- ✅ 基础框架已搭建（Cesium地图、天地图集成、基础组件）
- ✅ 三个大屏页面已创建（安全运行、安全态势、监测预警）
- ✅ API接口已封装（safety.ts）
- ⚠️ 目前使用模拟数据（MOCK_DATA），需要改为从后端API获取真实数据
- ⚠️ 数据自动刷新机制未实现
- ⚠️ 部分交互功能需要优化

**开发计划**：

##### 5.3.2.1 安全运行一张图（SafetyRun.vue）

**任务清单**：
- [x] **连接后端API，移除模拟数据**
  - [x] 修改 `useResourceMarkers.ts`，移除MOCK_DATA，确保从API获取真实数据
  - [x] 修改 `StatisticsPanel.vue`，确保统计数据从API获取（已完成，之前已连接API）
  - [x] 测试数据加载和错误处理（API失败时的降级方案）
  
- [x] **完善资源标记点展示**
  - [x] 确保所有安全资源（救援队伍、应急专家、物资装备）正确标记
  - [x] 确保所有防护目标正确标记
  - [x] 确保所有避难场所正确标记
  - [x] 验证标记点图标、颜色、标签显示正确
  - [x] 增强坐标验证和错误处理
  - [x] 添加详细的统计信息和日志输出
  
- [x] **完善统计面板**
  - [x] 验证统计数据准确性（救援队伍数、专家数、物资数等）
  - [x] 统计数据从API获取并正确显示
  - [x] 统计面板数据通过事件传递给父组件
  
- [x] **地图交互优化**
  - [x] 点击标记点显示详细信息弹窗（已优化，点击标记点会平滑飞行到该位置并显示详情对话框）
  - [x] 支持图层控制（显示/隐藏不同类型资源，已实现资源分类显示/隐藏功能）
  - [x] 支持地图样式切换（矢量/影像/地形，已实现标准/卫星/地形三种样式）
  - [x] 支持场景模式切换（2D/3D/哥伦布视图，已在MapToolbar中添加场景模式切换功能）
  - [x] 支持地图缩放、平移、复位视图（已优化fitBounds算法和重置视图功能，使用平滑动画过渡）

**后端API依赖**：
- `GET /api/v1/safety/resources/` - 获取安全资源列表
- `GET /api/v1/safety/resources/statistics/` - 获取安全资源统计
- `GET /api/v1/safety/targets/` - 获取防护目标列表
- `GET /api/v1/safety/targets/statistics/` - 获取防护目标统计
- `GET /api/v1/safety/shelters/` - 获取避难场所列表
- `GET /api/v1/safety/shelters/statistics/` - 获取避难场所统计

**数据验证要点**：
- 验证所有资源、目标、避难场所都有正确的经纬度坐标
- 验证统计数据与列表数据一致
- 验证标记点在地图上正确显示

##### 5.3.2.2 安全态势一张图（SafetyStatus.vue）

**任务清单**：
- [x] **连接后端API，获取四色风险图数据**
  - [x] 修改 `useColorMapRegions.ts`，从API获取区域态势数据（已移除模拟数据，确保从API获取真实数据）
  - [x] 实现区域四色风险图渲染（根据risk_color字段，已实现）
  - [x] 验证区域多边形在地图上正确显示（已实现，通过 `convertToPolygons` 函数转换并渲染）
  - [x] 优化风险区域数据：区域态势数据按照实际风险区域设定，不严格按照行政区域边界（已修改后端演示数据，区域名称改为"马钢工业园区风险区域"等实际风险区域名称）
  - [x] 实现风险等级图层控制：右上角图例框标题改为"区域风险等级"，每个颜色等级增加勾选框，支持图层显示/隐藏控制（默认全部显示）
  
- [x] **完善行业态势展示**
  - [x] 修改 `IndustryStatusPanel.vue`，从API获取行业态势数据（已移除模拟数据，确保从API获取真实数据）
  - [x] 展示四个行业的态势数据（危险化学品、防汛、交通运输、森林火灾，已实现按行业类型排序和去重逻辑）
  - [x] 优化行业态势面板样式和布局（样式已优化，包含悬停效果和不同行业的颜色区分）
  
- [x] **完善区域态势对比**
  - [x] 修改 `RegionComparisonChart.vue`，从API获取区域态势数据（已移除props，改为直接从API获取数据，使用 `getColorMapData` API）
  - [x] 实现区域态势对比图表（柱状图，已实现四个标签切换：报警数量、预警数量、风险数量、风险等级总数）
  - [x] 添加加载状态和空数据提示（已实现loading状态和空数据提示）
  - [x] 实现数据自动刷新（每5分钟自动刷新一次数据）
  - [x] 验证图表数据准确性（已实现完整的数据验证逻辑，包括：数据类型验证、字段完整性验证、X轴Y轴数据一致性验证、区域名称唯一性验证、各个标签数据映射验证、图表渲染后数据一致性验证，所有验证结果会输出到控制台）
  
- [x] **地图交互优化**
  - [x] 鼠标悬停显示区域信息（已实现，鼠标悬停在风险区域上会显示区域名称和风险等级）
  - [x] 点击区域显示区域详情弹窗（已实现，点击风险区域会显示详情对话框）
  - [x] 支持区域筛选（按风险等级、按街道）（已实现：风险等级筛选通过右上角图例框的复选框控制，街道筛选通过右侧街道筛选面板控制，支持多选和全部/清除操作）
  - [x] 支持地图样式切换（已实现，支持标准/卫星/地形三种样式切换，通过右侧地图样式选择器控制）

**后端API依赖**：
- `GET /api/v1/safety/region-status/color_map/` - 获取四色图数据
- `GET /api/v1/safety/industry-status/` - 获取行业态势列表
- `GET /api/v1/safety/region-status/` - 获取区域态势列表（用于对比图表）

**数据验证要点**：
- 验证区域态势数据包含risk_color字段（red/orange/yellow/blue）
- 验证区域多边形坐标正确
- 验证行业态势数据包含四个行业的数据
- 验证区域态势对比图表数据正确

##### 5.3.2.3 监测预警一张图（MonitorWarn.vue）

**布局说明**：
- **左侧面板**（MonitorDataPanel）：
  - 监测点状态统计（总体统计：监测点总数、在线监测点、离线监测点）
  - Tab 切换：报警记录统计（饼图）/ 预警级别分布（饼图）
  - 面板宽度：20vw（min-width: 280px, max-width: 360px）
- **右侧面板**（list-panel）：
  - Tab 切换：报警记录列表 / 预警事件列表
  - 面板宽度：18.7vw（min-width: 267px, max-width: 333px）
- **右下角**：图层控制和地图样式面板（支持 Tab 切换：图层控制 / 地图样式）
  - 图层控制：支持显示/隐藏报警记录、预警事件、视频监控
  - 地图样式：支持标准地图、卫星地图、地形地图三种样式切换

**任务清单**：
- [x] **连接后端API，获取监测数据**
  - [x] 修改 `MonitorDataPanel.vue`，从API获取监测数据统计
  - [x] 实现监测点在线状态统计展示
  - [x] 实现监测数据分类统计展示
  - [ ] 实现监测数据趋势图表（可选）
  
- [x] **连接后端API，获取预警事件数据**
  - [x] 修改 `useWarningMarkers.ts`，移除MOCK_DATA，确保从API获取真实数据
  - [x] 确保预警事件标记点正确显示（不同级别不同颜色）
  - [x] 实现预警事件列表展示
  - [x] 实现预警事件详情弹窗
  
- [x] **连接后端API，获取视频监控数据**
  - [x] 修改 `useVideoMonitors.ts`，从API获取视频监控设施列表
  - [x] 实现视频监控点位标记（根据预警事件位置自动查找附近监控）
  - [x] 实现视频监控详情弹窗
  - [x] 实现视频流播放功能（支持实际视频流和模拟播放）
  
- [x] **完善预警级别分布统计**
  - [x] 在左侧监测数据面板中实现 Tab 切换功能（报警记录统计 / 预警级别分布）
  - [x] 实现报警记录统计饼图（按报警状态：未处理、处理中、已处理、已忽略）
  - [x] 实现预警级别分布饼图（按预警级别：红色I级、橙色Ⅱ级、黄色Ⅲ级、蓝色Ⅳ级）
  - [x] 两个饼图均支持鼠标悬停动态效果（放大、阴影效果）
  - [x] 饼图大小和样式适配面板宽度，确保在一行内显示两个 Tab 按钮
  - [x] 从右侧面板移除预警级别分布统计（已整合到左侧面板）
  
- [x] **地图交互优化**
  - [x] 点击预警事件标记点显示详情（已实现，点击标记点会显示预警事件详情对话框）
  - [x] 点击视频监控标记点显示视频流（已实现，点击标记点会显示视频监控详情对话框并播放视频流）
  - [x] 点击报警记录标记点显示详情（已实现，点击标记点会显示报警记录详情对话框）
  - [x] 实现报警记录和预警事件 Tab 切换（右侧面板支持报警记录/预警事件列表切换）
  - [x] 实现图层控制功能（右下角图层控制面板，支持显示/隐藏报警记录、预警事件、视频监控）
  - [x] 支持地图样式切换（已实现，右下角面板支持 Tab 切换：图层控制 / 地图样式，地图样式支持标准地图、卫星地图、地形地图三种模式）

**后端API依赖**：
- `GET /api/v1/safety/monitor-data/statistics/` - 获取监测数据统计
- `GET /api/v1/safety/monitor-data/` - 获取监测数据列表
- `GET /api/v1/risk/alarm-records/` - 获取报警记录列表（用于报警记录统计和列表展示）
- `GET /api/v1/safety/warning-events/` - 获取预警事件列表（用于预警级别分布统计和列表展示）
- `GET /api/v1/safety/video-monitors/` - 获取视频监控设施列表
- `GET /api/v1/safety/video-monitors/nearby/` - 获取附近的视频监控设施

**数据验证要点**：
- 验证预警事件数据包含正确的经纬度坐标
- 验证预警级别ID与后端预警级别表对应
- 验证报警记录数据包含正确的经纬度坐标和报警状态
- 验证视频监控设施数据包含正确的经纬度坐标
- 验证监测数据统计准确性
- 验证报警记录统计和预警级别分布统计数据准确性

##### 5.3.2.4 数据自动刷新机制

**任务清单**：
- [x] **实现定时刷新机制**
  - [x] 为每个大屏页面添加数据刷新定时器（已实现，所有大屏页面都已添加定时刷新机制）
  - [x] 安全运行一张图：每5分钟刷新一次（基础数据变化较慢）（已实现，`SafetyRun.vue` 中每5分钟刷新资源数据）
  - [x] 安全态势一张图：每1分钟刷新一次（态势数据需要实时更新）（已实现，`SafetyStatus.vue` 中每1分钟刷新四色图数据）
  - [x] 监测预警一张图：每30秒刷新一次（监测数据和预警事件需要实时更新）（已实现，`MonitorWarn.vue` 中每30秒刷新报警记录、预警事件和视频监控数据，`MonitorDataPanel.vue` 中每30秒刷新统计数据）
  - [x] 使用`setInterval`实现定时刷新（已实现，所有页面都使用 `setInterval` 实现）
  - [x] 在组件卸载时清理定时器（已实现，所有页面都在 `onUnmounted` 中清理定时器）
  
- [x] **优化刷新策略**
  - [x] 区分实时数据和基础数据，采用不同的刷新频率（已实现，基础数据5分钟刷新，实时数据30秒-1分钟刷新）
  - [x] 实现智能刷新（页面可见时刷新，不可见时暂停）（已实现，使用 Page Visibility API 检测页面可见性）
  - [x] 实现错误重试机制（API失败时自动重试）（已实现，支持最多3次重试，支持指数退避）
  - [x] 添加刷新状态提示（可选，显示最后更新时间）（已实现，StatisticsPanel 和 MonitorDataPanel 显示最后更新时间）

**实现示例**：
```typescript
// 在组件中使用
onMounted(() => {
  loadData() // 初始加载
  refreshTimer = setInterval(() => {
    loadData() // 定时刷新
  }, 30000) // 30秒刷新一次
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
```

##### 5.3.2.5 交互优化（留待生产环境执行）

**说明**：以下任务为生产环境优化项，演示系统当前状态已满足需求，留待准备上生产环境时再执行。

**任务清单**：
- [ ] **地图交互优化**
  - [ ] 优化标记点点击响应速度
  - [ ] 优化弹窗显示动画和样式
  - [ ] 添加标记点聚合功能（当标记点过多时）
  - [ ] 优化地图缩放时的标记点显示
  
- [ ] **数据展示优化**
  - [ ] 优化统计面板数据加载状态（loading状态）
  - [ ] 优化图表数据加载状态
  - [ ] 添加数据为空时的提示信息
  - [ ] 优化错误提示信息（API失败时的友好提示）
  
- [ ] **用户体验优化**
  - [ ] 添加键盘快捷键支持（可选）
  - [ ] 优化大屏响应式布局（适配不同分辨率）
  - [ ] 添加全屏切换功能（可选）
  - [ ] 优化页面切换动画

##### 5.3.2.6 性能优化（留待生产环境执行）

**说明**：以下任务为生产环境优化项，演示系统当前状态已满足需求，留待准备上生产环境时再执行。

**任务清单**：
- [ ] **数据加载优化**
  - [ ] 实现数据分页加载（当数据量很大时）
  - [ ] 实现数据缓存机制（避免重复请求）
  - [ ] 优化API请求并发（使用Promise.all并行请求）
  - [ ] 实现请求防抖（避免频繁请求）
  
- [ ] **地图渲染优化**
  - [ ] 优化标记点渲染性能（大量标记点时）
  - [ ] 实现标记点按需加载（只加载可视区域内的标记点）
  - [ ] 优化多边形渲染性能
  - [ ] 优化地图瓦片加载
  
- [ ] **组件性能优化**
  - [ ] 使用`v-memo`优化列表渲染
  - [ ] 使用`computed`缓存计算结果
  - [ ] 避免不必要的响应式数据
  - [ ] 优化图表渲染性能（ECharts配置优化）

**实施顺序**：
1. **第一步**：连接后端API，移除模拟数据（5.3.2.1、5.3.2.2、5.3.2.3）✅ 已完成
2. **第二步**：实现数据自动刷新机制（5.3.2.4）✅ 已完成
3. **第三步**：交互优化（5.3.2.5）⏸️ 留待生产环境执行
4. **第四步**：性能优化（5.3.2.6）⏸️ 留待生产环境执行

**验收标准**：
- ✅ 三个大屏都能正确展示后端演示数据
- ✅ 所有标记点、多边形、图表数据都从后端API获取
- ✅ 数据能够自动刷新，保持最新状态
- ✅ 地图交互流畅，无明显卡顿
- ✅ 页面性能良好，无明显延迟

### 5.4 第四阶段：测试与优化

- [ ] 功能测试
- [ ] 性能优化
- [ ] 兼容性测试
- [ ] 用户体验优化




---

## 6. 技术难点与解决方案

### 6.1 Cesium与天地图集成

**难点**: 使用Cesium作为3D地图引擎，集成天地图作为底图服务，支持多种场景模式和地图样式

**解决方案**:
1. **Cesium引擎初始化**:
   - 使用Cesium 1.108.0（与天地图官方支持的版本一致）
   - 通过npm包安装，确保TypeScript类型支持
   - 创建Cesium Viewer，配置场景模式（2D/3D/COLUMBUS_VIEW）

2. **天地图底图集成**:
   - **2D模式（SCENE2D/COLUMBUS_VIEW）**: 使用天地图矢量图层
     - 矢量底图（vec_w）: 使用`UrlTemplateImageryProvider`加载，URL格式为`DataServer?T=vec_w&x={x}&y={y}&l={z}&tk=token`
     - 矢量注记（cva_w）: 使用`UrlTemplateImageryProvider`加载，URL格式为`DataServer?T=cva_w&x={x}&y={y}&l={z}&tk=token`
     - **投影方式**: 球面墨卡托投影（Web Mercator，EPSG:3857），使用`WebMercatorTilingScheme`
   - **3D模式（SCENE3D）**: 使用天地图影像图层
     - 影像底图（img_w）: URL格式为`DataServer?T=img_w&x={x}&y={y}&l={z}&tk=token`
     - 国界图层（ibo_w）: URL格式为`DataServer?T=ibo_w&x={x}&y={y}&l={z}&tk=token`
   - **地形模式**: 使用天地图地形服务
     - 地形服务（swdx）: URL格式为`mapservice/swdx?T=elv_c&tk=token`
     - 使用`GeoTerrainProvider`类（需要天地图扩展插件）

3. **天地图扩展插件加载**:
   - 将Cesium挂载到`window.Cesium`对象上（天地图扩展插件依赖）
   - 动态加载天地图扩展插件（按顺序）:
     - `long.min.js`
     - `bytebuffer.min.js`
     - `protobuf.min.js`
     - `Cesium_ext_min.js`（核心扩展，最后加载）
   - 扩展插件提供`GeoWTFS`类（三维地名服务）和`GeoTerrainProvider`类（地形服务）

4. **业务图层渲染**:
   - 使用Cesium的Entity API渲染业务数据
   - 标记点: 使用`Billboard`、`Point`、`Label`组件
   - 多边形: 使用`Polygon`组件，支持填充和描边
   - 坐标系统: 使用WGS84经纬度坐标（Cesium默认坐标系）

5. **关键技术要点**:
   - 矢量图层必须使用球面墨卡托投影（`WebMercatorTilingScheme`），确保瓦片正确加载
   - 天地图服务URL中的`_w`后缀表示球面墨卡托投影（Web Mercator）
   - Cesium版本需与天地图官方支持版本一致（当前使用1.108.0）
   - 扩展插件加载顺序至关重要，必须在Cesium Viewer创建后加载

### 6.2 MySQL空间数据类型处理

**难点**: 后端返回的空间数据（POINT、GEOMETRY）需要在前端处理

**解决方案**:
1. 后端API返回时，将空间数据转换为JSON格式（包含经纬度）
2. 前端直接使用经纬度进行地图展示
3. 如需空间查询，通过API传递经纬度参数

### 6.3 大屏响应式布局

**难点**: 适配不同分辨率大屏

**解决方案**:
1. 使用`vw`、`vh`单位
2. 使用`scale`进行整体缩放
3. 使用媒体查询适配不同分辨率

### 6.4 实时数据更新

**难点**: 大屏需要实时展示最新数据

**解决方案**:
1. 使用`setInterval`定时刷新（演示系统）
2. 或使用WebSocket实时推送（生产环境）
3. 合理设置刷新频率，避免过度请求

---

## 7. 部署说明

### 7.1 开发环境

#### 7.1.1 启动开发服务器
```bash
# 业务管理后台
cd frontend/admin
npm run dev

# 大屏展示系统
cd frontend/screen
npm run dev
```

### 7.2 生产环境

#### 7.2.1 构建项目
```bash
# 业务管理后台
cd frontend/admin
npm run build

# 大屏展示系统
cd frontend/screen
npm run build
```

#### 7.2.2 部署
- 将构建后的`dist`目录部署到Nginx
- 配置Nginx反向代理到后端API
- 配置静态资源缓存

---

## 8. 总结

本文档详细规划了风险监测预警系统前端部分的开发工作，包括业务管理后台和大屏展示系统的架构设计、功能模块、技术方案等。开发过程中应严格按照本文档进行，确保代码质量和项目进度。

