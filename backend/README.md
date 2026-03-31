# 风险监测预警系统 - 后端服务

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

**方法二：使用Python脚本**

创建临时脚本 `generate_secret_key.py`：

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

然后运行：

```bash
python generate_secret_key.py
```

**方法三：使用Python命令行（无需Django）**

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

### 6 演示数据初始化

#### 6.1 初始化数据目标

为系统的六大核心业务模块灌入完整的初始化数据，构建一套完整、连贯、真实的演示数据集，以支持：
- 系统功能演示和流程验证
- 大屏可视化展示（三个一张图）
- 业务场景模拟和测试
- 用户体验优化

#### 6.2 数据依赖关系

数据初始化需遵循以下依赖顺序，确保数据间的关联关系正确建立：

```
系统管理模块（基础数据）
  └── 组织管理（组织架构）
      └── 用户管理（系统用户）
          └── 角色管理（角色权限）
              └── 权限管理（权限树）
                  └── 数据源管理（外部数据源）
                      └── 消息模板（消息模板）
                          │
                          ├── 安全态势模块（基础资源）
                          │   ├── 安全资源（救援队伍、专家、物资）
                          │   ├── 防护目标
                          │   ├── 避难场所
                          │   ├── 危险源
                          │   └── 视频监控
                          │       │
                          ├── 风险监测预警模块
                          │   ├── 预警级别（四色预警）
                          │   ├── 预警规则
                          │   ├── 风险监测点（关联数据源）
                          │   ├── 风险预警（关联监测点、预警级别）
                          │   ├── 报警管理（关联预警）
                          │   ├── 隐患排查
                          │   └── 隐患整改（关联隐患）
                          │
                          ├── 预案模块
                          │   ├── 应急预案
                          │   ├── 预案结构（关联预案）
                          │   ├── 预案流程（关联预案）
                          │   ├── 预案任务（关联预案、流程）
                          │   └── 预案执行（关联预案、任务）
                          │
                          ├── 叫应模块
                          │   ├── 叫应对象（关联组织）
                          │   ├── 叫应人员
                          │   ├── 叫应分组（关联人员）
                          │   ├── 政策文件
                          │   ├── 政策下发（关联文件、对象）
                          │   └── 叫应记录（关联人员、分组）
                          │
                          ├── 简报模块
                          │   ├── 简报模板（关联消息模板）
                          │   ├── 简报策略（关联模板、预警级别）
                          │   ├── 简报数据（关联策略、预警）
                          │   └── 简报推送（关联数据、人员、组织）
                          │
                          └── 演练模块
                              ├── 演练事件（关联预案、组织）
                              ├── 演练评价（关联事件）
                              ├── 演练总结（关联事件、评价）
                              └── 演练分析（统计分析，依赖以上数据）
```

#### 6.3 各模块初始化数据规划

##### 6.3.1 系统管理模块（基础数据，优先初始化）

**组织管理**:
- 创建三级组织架构（市-区/县-街道）
- 示例：马鞍山市应急管理局 → 雨山区应急管理局 → 佳山街道应急办
- 组织数量：10-15个
- 组织类型：政府部门、企业单位、事业单位

**用户管理**:
- 创建5-8个演示用户
- 角色分配：系统管理员、应急指挥、监测预警、预案管理、叫应调度等
- 用户信息：真实姓名、手机号、邮箱、所属组织

**角色管理**:
- 创建5-8个业务角色
- 角色权限：完整的权限分配（菜单、按钮、接口）

**权限管理**:
- 完整的权限树（菜单权限、按钮权限、接口权限）
- 与系统路由结构对应

**数据源管理**:
- 创建3-5个外部数据源
- 数据源类型：API接口、数据库、文件
- 行业类型：气象、危化、防汛、交通运输、森林火灾
- 配置同步间隔和连接信息

**消息模板**:
- 创建10-15个消息模板
- 模板类型：系统消息、短信、邮件
- 消息类型：预警通知、报警通知、简报推送、叫应通知
- 包含变量占位符（如：{warning_title}、{warning_level}等）

##### 6.3.2 安全态势模块（基础资源数据）

**安全资源**:
- **救援队伍**（20-30支）:
  - 类型：危化品救援队、消防队、应急抢险队、医疗救援队、社会救援队
  - 信息：队伍名称、组织、联系人、联系电话、装备信息、位置坐标
  - 位置分布：覆盖主要街道和重点区域
  
- **应急专家**（15-20名）:
  - 类型：行业专家、救援专家、技术专家
  - 信息：姓名、专业领域、技术等级、联系方式、所属组织
  
- **物资装备**（30-40项）:
  - 类型：个人防护、抢险救援、食品、药品、饮用水、人员庇护
  - 信息：物资名称、数量、单位、存放位置、联系人、位置坐标

**防护目标**（15-20个）:
- 类型：学校、居民区、医院、商场、其他人员密集场所
- 信息：目标名称、类型、位置、容纳人数、联系人、位置坐标
- 位置分布：覆盖主要街道

**避难场所**（10-15个）:
- 类型：公园、广场、体育场、学校、其他
- 信息：场所名称、类型、位置、容纳能力、设施情况、位置坐标

**危险源**（10-15个）:
- 类型：重大危险源、一般危险源
- 行业：危险化学品、防汛、交通运输、森林火灾
- 信息：危险源名称、类型、风险等级、位置、管理单位、位置坐标

**视频监控**（20-30个）:
- 信息：监控名称、位置、在线状态、视频流地址、位置坐标
- 状态分布：在线/离线混合，覆盖主要区域

##### 6.3.3 风险监测预警模块（核心业务数据）

**预警级别**（4个，固定）:
- 红色I级、橙色Ⅱ级、黄色Ⅲ级、蓝色Ⅳ级
- 配置响应组织、响应时间、严重程度

**预警规则**（5-8条）:
- 规则名称、触发条件、预警级别、处置措施
- 关联监测点和预警级别

**风险监测点**（30-40个）:
- 监测类型：实时监测、全域监测、重点监测
- 行业类型：森林火灾、防汛、交通运输、危险化学品
- 信息：监测点名称、类型、位置、阈值设置、数据源、在线状态、位置坐标
- 状态分布：在线/离线混合，覆盖不同行业和区域

**风险预警**（20-30条，近期数据）:
- 关联监测点、预警级别、预警规则
- 预警状态：待发布、已发布、处置中、已处置、已关闭
- 时间分布：过去7天内，包含不同级别的预警
- 信息：预警标题、内容、级别、状态、发布时间、处置信息

**报警管理**（15-20条）:
- 关联风险预警
- 报警状态：待处理、处理中、已处理
- 时间分布：与预警时间对应

**隐患排查**（10-15条）:
- 隐患类型：不同行业和类型
- 隐患状态：待整改、整改中、待验收、已验收
- 信息：隐患名称、类型、位置、发现时间、严重程度、整改责任人

**隐患整改**（与隐患排查对应）:
- 关联隐患排查
- 整改状态：整改中、待验收、已验收、验收不合格
- 信息：整改措施、整改时间、验收意见

##### 6.3.4 预案模块（预案体系数据）

**应急预案**（5-8个）:
- 预案类型：不同行业和场景的应急预案
- 预案状态：已发布、已修订、已废止
- 信息：预案名称、类型、版本、发布单位、发布时间

**预案结构**（每个预案20-50个节点）:
- 树形结构：章节、条款、子条款
- 信息：节点名称、类型、层级、内容

**预案流程**（每个预案3-8个流程）:
- 树形流程：流程节点、分支、决策点
- 信息：流程名称、节点配置、流转条件

**预案任务**（每个预案10-20个任务）:
- 关联预案和流程节点
- 信息：任务名称、类型、执行人、截止时间、状态

**预案执行**（5-10条执行记录）:
- 关联预案和任务
- 执行状态：待启动、执行中、已完成、已终止
- 时间分布：近期执行记录

##### 6.3.5 叫应模块（叫应体系数据）

**叫应对象**（15-20个）:
- 类型：政府部门、企业单位、事业单位
- 关联组织
- 信息：对象名称、类型、安全责任人、联系电话、地址

**叫应人员**（30-40名）:
- 信息：姓名、职务、手机号、办公电话、地址
- 关联叫应分组（部分人员）

**叫应分组**（5-8组）:
- 类型：常态化分组、非常态化分组
- 信息：分组名称、类型、成员列表

**政策文件**（10-15份）:
- 文件类型：政策文件、通知文件、法规文件
- 信息：文件名称、类型、发布单位、发布时间、文件内容

**政策下发**（15-20条）:
- 关联政策文件和叫应对象
- 下发状态：待下发、已下发、已反馈、已督办
- 信息：下发时间、接收对象、反馈情况、督办情况

**叫应记录**（20-30条）:
- 关联叫应人员或分组
- 叫应类型：电话、短信、邮件、一键叫应
- 信息：叫应时间、被叫应人、叫应内容、响应情况

##### 6.3.6 简报模块（简报体系数据）

**简报模板**（5-8个）:
- 关联消息模板
- 信息：模板名称、内容、变量配置
- 模板类型：日报、周报、月报、专项报告

**简报策略**（5-8条）:
- 关联简报模板和预警级别
- 触发条件：定时触发（每日、每周、每月）、事件触发（预警级别）
- 信息：策略名称、触发条件、模板、推送对象

**简报数据**（30-40条，近期数据）:
- 关联简报策略和风险预警
- 时间分布：过去30天内，包含日报、周报、月报
- 信息：简报标题、内容、生成时间、数据来源

**简报推送**（与简报数据对应）:
- 关联简报数据、推送人员、推送组织
- 推送状态：待推送、推送中、已推送、推送失败
- 推送渠道：系统消息、短信、邮件
- 信息：推送时间、接收人、推送状态

##### 6.3.7 演练模块（演练体系数据）

**演练事件**（10-15个）:
- 演练类型：桌面演练、功能演练、全面演练
- 事故类型：不同行业和场景
- 演练状态：待启动、进行中、已完成
- 信息：事件编号、名称、类型、组织、时间、参演人数

**演练评价**（每个事件10-20条评价）:
- 关联演练事件
- 节点类型：不同演练节点
- 评价等级：优秀、良好、合格、不合格
- 信息：节点名称、评价项、评分、等级、评价人、时间

**演练总结**（与演练事件对应）:
- 关联演练事件
- 整体等级：优秀、良好、合格、不合格
- 信息：总结标题、整体评分、各维度评价、总结时间、总结人

**演练分析**（统计数据）:
- 基于演练事件、评价、总结生成
- 统计维度：按单位、按类型、按事故类型、按时间段
- 包含：演练次数、完成次数、优秀/良好/合格/不合格次数、平均分、完成率

#### 6.4 数据关联流程示例

为构建完整的业务流程演示，需确保数据间的关联关系完整：

**预警发布流程**:
```
风险监测点（实时监测） 
  → 触发预警规则 
  → 生成风险预警（关联预警级别、监测点）
  → 触发报警管理（关联预警）
  → 触发简报策略（事件触发）
  → 生成简报数据（关联预警、策略）
  → 推送简报（关联人员、组织、消息模板）
```

**隐患整改流程**:
```
隐患排查（发现隐患）
  → 隐患整改（关联隐患）
  → 整改验收（关联整改）
  → 关闭隐患
```

**预案执行流程**:
```
应急预案（已发布）
  → 预案执行（启动预案）
  → 执行预案任务（关联任务）
  → 更新执行状态
  → 完成预案执行
```

**叫应流程**:
```
政策文件（已发布）
  → 政策下发（关联文件、对象）
  → 接收反馈（关联下发）
  → 督办管理（如未反馈）
```

**演练流程**:
```
演练事件（创建事件）
  → 启动演练
  → 演练评价（各节点评价）
  → 演练总结（关联事件、评价）
  → 演练分析（统计分析）
```

#### 6.5 数据量规划

| 模块 | 实体类型 | 数据量 | 说明 |
|------|---------|--------|------|
| 系统管理 | 组织 | 10-15个 | 三级组织架构 |
|  | 用户 | 5-8个 | 演示用户 |
|  | 角色 | 5-8个 | 业务角色 |
|  | 权限 | 完整权限树 | 与系统路由对应 |
|  | 数据源 | 3-5个 | 外部数据源 |
|  | 消息模板 | 10-15个 | 各种消息类型 |
| 安全态势 | 安全资源 | 65-90个 | 救援队伍、专家、物资 |
|  | 防护目标 | 15-20个 | 各类防护目标 |
|  | 避难场所 | 10-15个 | 各类避难场所 |
|  | 危险源 | 10-15个 | 重大/一般危险源 |
|  | 视频监控 | 20-30个 | 监控设施 |
| 风险监测预警 | 预警级别 | 4个 | 四色预警 |
|  | 预警规则 | 5-8条 | 预警规则 |
|  | 风险监测点 | 30-40个 | 各类监测点 |
|  | 风险预警 | 20-30条 | 近期预警 |
|  | 报警管理 | 15-20条 | 报警记录 |
|  | 隐患排查 | 10-15条 | 隐患记录 |
|  | 隐患整改 | 10-15条 | 整改记录 |
| 预案 | 应急预案 | 5-8个 | 各类预案 |
|  | 预案结构 | 100-400个节点 | 每个预案20-50个节点 |
|  | 预案流程 | 15-64个流程 | 每个预案3-8个流程 |
|  | 预案任务 | 50-160个任务 | 每个预案10-20个任务 |
|  | 预案执行 | 5-10条 | 执行记录 |
| 叫应 | 叫应对象 | 15-20个 | 各类对象 |
|  | 叫应人员 | 30-40名 | 叫应人员 |
|  | 叫应分组 | 5-8组 | 分组 |
|  | 政策文件 | 10-15份 | 政策文件 |
|  | 政策下发 | 15-20条 | 下发记录 |
|  | 叫应记录 | 20-30条 | 叫应记录 |
| 简报 | 简报模板 | 5-8个 | 各类模板 |
|  | 简报策略 | 5-8条 | 策略配置 |
|  | 简报数据 | 30-40条 | 近期简报 |
|  | 简报推送 | 30-40条 | 推送记录 |
| 演练 | 演练事件 | 10-15个 | 演练事件 |
|  | 演练评价 | 100-300条 | 每个事件10-20条 |
|  | 演练总结 | 10-15条 | 总结记录 |
|  | 演练分析 | 统计数据 | 基于以上数据 |

**总数据量**: 约 **1000-2000条** 核心业务数据记录（不含预案结构、流程等详细节点数据）

#### 6.6 地理数据规划

为支持大屏可视化展示，需确保地理数据的完整性和准确性：

**坐标系统**: WGS84（经纬度）

**重点区域**: 以马鞍山市雨山区为例（参考慈湖站位置：118.521577, 31.742368）

**数据分布**:
- 安全资源、防护目标、避难场所、危险源、视频监控：分布在主要街道和重点区域
- 风险监测点：覆盖不同行业和区域，形成监测网络
- 风险预警：关联监测点位置，分布在不同区域
- 位置数据需确保在同一区域范围内，便于地图展示

**街道分布**: 
- 主要街道：佳山街道、平湖街道、雨山街道等
- 确保数据在各街道均匀分布

#### 6.7 时间数据规划

为构建真实的业务场景，时间数据需遵循以下规则：

**基础数据**: 
- 创建时间：系统初始化时统一设置（如：2024-01-01）
- 更新时间：系统初始化时统一设置

**业务数据时间分布**:
- **风险预警、报警管理**: 过去7天内（2024-12-15至2024-12-22）
- **简报数据、简报推送**: 过去30天内（2024-11-23至2024-12-22）
- **预案执行**: 过去30天内
- **政策下发、叫应记录**: 过去30天内
- **演练事件、评价、总结**: 过去90天内（2024-09-23至2024-12-22）
- **隐患排查、整改**: 过去60天内（2024-10-23至2024-12-22）

**时间关联**:
- 预警发布时间 → 报警时间（关联）
- 简报生成时间 → 预警时间（关联）
- 预案执行时间 → 任务完成时间（关联）
- 演练事件时间 → 评价时间 → 总结时间（时间顺序）

#### 6.8 实施步骤

**第一步：基础数据初始化**（系统管理模块）
1. 创建组织架构（三级结构）
2. 创建用户和角色
3. 配置权限树
4. 创建数据源
5. 创建消息模板

**✅ 已完成工作**：

已创建Django Fixtures文件，位于以下目录：
- `backend/apps/users/fixtures/` - 用户权限管理模块fixtures
- `backend/apps/system/fixtures/` - 系统管理模块fixtures

**已创建的Fixtures文件**：

1. **`backend/apps/users/fixtures/initial_organizations.json`** - 组织架构数据
   - 包含12个组织（三级结构：市级-区级-街道级）
   - 组织类型：政府部门、企业单位、事业单位

2. **`backend/apps/users/fixtures/initial_roles.json`** - 角色数据
   - 包含8个业务角色：系统管理员、应急指挥、监测预警、预案管理、叫应调度、简报管理、安全态势管理、演练管理

3. **`backend/apps/users/fixtures/initial_permissions.json`** - 权限树数据
   - 包含50个权限节点
   - 涵盖所有主要模块的菜单权限和部分API接口权限

4. **`backend/apps/users/fixtures/initial_users.json`** - 用户数据
   - 包含8个演示用户
   - 关联组织、角色等数据

5. **`backend/apps/users/fixtures/initial_user_roles.json`** - 用户角色关联数据
   - 关联用户和角色

6. **`backend/apps/users/fixtures/initial_role_permissions.json`** - 角色权限关联数据
   - 关联角色和权限

7. **`backend/apps/system/fixtures/initial_data_sources.json`** - 数据源数据
   - 包含5个外部数据源
   - 覆盖气象、危化、防汛、交通运输、森林火灾五个行业

8. **`backend/apps/system/fixtures/initial_message_templates.json`** - 消息模板数据
   - 包含15个消息模板
   - 涵盖所有消息类型和模板类型

**辅助文件**：
- `backend/apps/users/fixtures/README.md` - 用户模块fixtures使用说明
- `backend/apps/system/fixtures/README.md` - 系统模块fixtures使用说明
- `backend/apps/users/management/commands/fix_user_passwords.py` - 用户密码修复管理命令

**使用方法**：
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

**第二步：资源数据初始化**（安全态势模块）
1. 创建安全资源（救援队伍、专家、物资）
2. 创建防护目标
3. 创建避难场所
4. 创建危险源
5. 创建视频监控
6. 确保地理坐标分布合理

**✅ 已完成工作**：

已创建Django Fixtures文件，位于以下目录：
- `backend/apps/safety/fixtures/` - 安全态势模块fixtures

**已创建的Fixtures文件**：

1. **`backend/apps/safety/fixtures/initial_safety_resources.json`** - 安全资源数据
   - 救援队伍：9支（危化品救援队、消防队、应急抢险队、医疗救援队、社会救援队）
   - 应急专家：5名（行业专家、救援专家、技术专家）
   - 物资装备：9项（个人防护、抢险救援、食品、药品、饮用水、人员庇护）
   - 总计：23个安全资源

2. **`backend/apps/safety/fixtures/initial_safety_targets.json`** - 防护目标数据
   - 包含10个防护目标（学校2个、居民区2个、医院2个、商场2个、其他2个）
   - 覆盖不同风险等级（高、中、低）

3. **`backend/apps/safety/fixtures/initial_shelters.json`** - 避难场所数据
   - 包含6个避难场所（公园2个、广场2个、体育场1个、学校1个）
   - 总容纳能力约25000人

4. **`backend/apps/safety/fixtures/initial_hazard_sources.json`** - 危险源数据
   - 重大危险源：4个（马钢焦化厂、中石化油库、高炉煤气柜、液氨储罐）
   - 一般危险源：3个（加油站、盐酸储罐、长江堤防险工险段）
   - 涵盖危化品和防汛行业

5. **`backend/apps/safety/fixtures/initial_video_monitors.json`** - 视频监控数据
   - 固定监控：7个
   - 无人机监控：1个
   - 覆盖主要危险源、人员密集场所、交通枢纽等

**辅助文件**：
- `backend/apps/safety/fixtures/README.md` - 安全态势模块fixtures使用说明

**使用方法**：

### 加载数据

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

### 清除数据

如果需要清除区域态势或行业态势数据，可以使用以下方法：

**方法一：使用Django管理命令（推荐）**

```bash
# 清除区域态势数据（会提示确认）
python manage.py clear_region_status

# 清除行业态势数据（会提示确认）
python manage.py clear_industry_status

# 跳过确认提示（谨慎使用）
python manage.py clear_region_status --confirm
python manage.py clear_industry_status --confirm
```

**方法二：使用Django Shell**

```bash
python manage.py shell
```

在Django shell中执行：

```python
# 清除区域态势数据
from apps.safety.models import RegionStatus
RegionStatus.objects.all().delete()

# 清除行业态势数据
from apps.safety.models import IndustryStatus
IndustryStatus.objects.all().delete()
```

**方法三：使用SQL命令（直接操作数据库）**

```sql
-- 清除区域态势数据
DELETE FROM region_status;

-- 清除行业态势数据
DELETE FROM industry_status;
```

### 重新加载数据流程

如果需要完全替换数据，建议按以下流程操作：

```bash
# 1. 清除旧数据（可选，如果pk相同会自动更新）
python manage.py clear_region_status --confirm
python manage.py clear_industry_status --confirm

# 2. 加载新数据
python manage.py loaddata apps/safety/fixtures/initial_region_status.json
python manage.py loaddata apps/safety/fixtures/initial_industry_status.json
```

**数据特点**：
- 所有地理坐标均位于马鞍山市范围内（约118.3-118.7, 31.6-31.9）
- 数据分布在主要街道：佳山街道、平湖街道、雨山街道、解放路街道
- 数据覆盖所有主要资源类型，满足演示需求

6. **`backend/apps/safety/fixtures/initial_industry_status.json`** - 行业态势数据
   - 包含4条记录，覆盖所有四个行业类型（森林火灾、防汛、交通运输、危险化学品）
   - 统计日期：2024-12-22（最新日期）
   - 每个行业包含报警数量、预警数量、风险隐患数量、各风险等级数量等统计数据
   - 数据用于安全态势一张图的行业态势面板展示

7. **`backend/apps/safety/fixtures/initial_region_status.json`** - 区域态势数据（四色风险图）
   - 包含7条记录，覆盖7个风险区域（马钢工业园区、雨山湖周边、市中心商业区、东部新区、长江沿岸、南部山区、西部工业区）
   - **重要说明**：区域态势数据按照**实际风险区域**来设定，不严格按照行政区域边界。`street` 字段表示风险区域名称，用于标识风险区域，不要求与行政区域完全对应
   - 统计日期：2024-12-22（最新日期）
   - 每个区域包含 `risk_color` 字段（red/orange/yellow/blue），用于四色风险图渲染
   - 风险颜色分布：红色I级1个、橙色Ⅱ级1个、黄色Ⅲ级2个、蓝色Ⅳ级3个
   - 数据用于安全态势一张图的四色风险图展示，前端会根据区域名称匹配对应的中心坐标和半径，在地图上绘制风险区域

**✅ 第三步：预警体系初始化**（风险监测预警模块）
1. 创建预警级别（4个固定）
2. 创建预警规则
3. 创建风险监测点（关联数据源）
4. 创建风险预警（关联监测点、规则、级别）
5. 创建报警管理（关联预警）
6. 创建隐患排查和整改

**✅ 已完成工作**：

已创建Django Fixtures文件，位于以下目录：
- `backend/apps/risk/fixtures/` - 风险监测预警模块fixtures

**已创建的Fixtures文件**：

1. **`backend/apps/risk/fixtures/initial_warning_levels.json`** - 预警级别数据
   - 4个固定预警级别：红色I级、橙色Ⅱ级、黄色Ⅲ级、蓝色Ⅳ级
   - 每个级别包含响应组织要求、响应时间、严重程度等配置

2. **`backend/apps/risk/fixtures/initial_warning_rules.json`** - 预警规则数据
   - 5条规则：3条预警生成规则（危化品、防汛、森林火灾）+ 2条预警处置规则
   - 规则包含条件配置和动作配置（JSON格式）

3. **`backend/apps/risk/fixtures/initial_risk_monitors.json`** - 风险监测点数据
   - 6个监测点：3个危化品、1个防汛、1个森林火灾、1个交通运输
   - 监测点包含实时监测数值、阈值、在线状态、地理位置等信息
   - 关联数据源ID（2、3、4等，对应system模块的数据源）

4. **`backend/apps/risk/fixtures/initial_risk_warnings.json`** - 风险预警数据
   - 3条预警记录：1条红色I级（危化品泄漏）、1条橙色Ⅱ级（水位预警）、1条黄色Ⅲ级（森林火险）
   - 关联预警级别、预警规则、监测点、响应组织和用户

5. **`backend/apps/risk/fixtures/initial_alarm_records.json`** - 报警记录数据
   - 4条报警记录：不同行业类型、不同处理状态
   - 关联监测点、处理用户，包含报警值、阈值、处理结果等信息

6. **`backend/apps/risk/fixtures/initial_risk_hidden_dangers.json`** - 隐患排查数据
   - 3条隐患记录：不同等级（重大、较大）、不同状态（待整改、整改中、已完成）
   - 关联监测点、企业组织、发现用户

7. **`backend/apps/risk/fixtures/initial_risk_rectifications.json`** - 隐患整改数据
   - 3条整改记录：对应隐患排查的整改方案和执行记录
   - 包含整改计划、整改措施、责任人、时间节点、验收状态等信息

**数据加载顺序**（需要先加载基础数据）：

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

**数据特点**：
- 预警级别固定为4个，符合四色预警标准
- 监测点覆盖4个行业类型（危化品、防汛、森林火灾、交通运输）
- 预警记录包含不同级别、不同状态，形成完整的预警流程数据
- 隐患排查和整改形成完整的隐患管理流程数据
- 所有地理坐标均位于马鞍山市范围内

**✅ 第四步：预案体系初始化**（预案模块）
1. 创建应急预案
2. 创建预案结构（树形）
3. 创建预案流程（树形）
4. 创建预案任务（关联预案、流程）
5. 创建预案执行记录

**✅ 已完成工作**：

已创建Django Fixtures文件，位于以下目录：
- `backend/apps/plan/fixtures/` - 预案模块fixtures

**已创建的Fixtures文件**：

1. **`backend/apps/plan/fixtures/initial_emergency_plans.json`** - 应急预案数据
   - 3个预案：2个综合应急预案（危化品、防汛）+ 1个现场处置方案（企业级）
   - 每个预案包含版本号、文件路径、摘要、状态等信息
   - 关联组织、创建用户、审批用户

2. **`backend/apps/plan/fixtures/initial_plan_structures.json`** - 预案结构数据
   - 7个结构节点：形成树形结构（章节->条款->子条款）
   - 预案1（危化品）：5个节点（总则、组织体系、预警与信息报告、应急响应等）
   - 预案2（防汛）：2个节点（总则、汛情监测与预警）
   - 节点包含内容文本、是否重点信息等字段

3. **`backend/apps/plan/fixtures/initial_plan_flows.json`** - 预案流程数据
   - 6个流程节点：形成树形结构（主流程->子流程->任务节点）
   - 预案1（危化品）：3个主流程 + 1个子流程节点
   - 预案2（防汛）：2个主流程
   - 流程包含配置信息（JSON格式）、下一流程ID、条件配置等

4. **`backend/apps/plan/fixtures/initial_plan_tasks.json`** - 预案任务数据
   - 7个任务：覆盖5种任务类型（信息收集、决策指挥、资源调配、现场处置、其他）
   - 预案1（危化品）：5个任务（信息接报、启动响应、人员疏散、泄漏控制、环境监测）
   - 预案2（防汛）：2个任务（水位监测预警、堤防巡查抢险）
   - 任务关联流程、组织、用户/角色，包含优先级、预计时间等

5. **`backend/apps/plan/fixtures/initial_plan_executions.json`** - 预案执行记录数据
   - 3条执行记录：1条实战执行（进行中）+ 1条实战执行（已完成）+ 1条演练执行（已完成）
   - 关联预案、预警（可选）、指挥用户、当前流程
   - 包含执行结果、执行总结等信息

**数据加载顺序**（需要先加载基础数据和预警数据）：

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

**数据特点**：
- 预案类型覆盖综合应急预案和现场处置方案
- 预案结构形成完整的树形层次（章节->条款->子条款）
- 预案流程形成完整的执行流程链（主流程->子流程->任务节点）
- 任务覆盖所有任务类型，包含优先级和时间要求
- 执行记录包含实战执行和演练执行两种类型
- 预案与预警关联，形成预警->预案执行的完整业务流程

**✅ 第五步：叫应体系初始化**（叫应模块）
1. 创建叫应对象（关联组织）
2. 创建叫应人员
3. 创建叫应分组（关联人员）
4. 创建政策文件
5. 创建政策下发（关联文件、对象）
6. 创建叫应记录

**✅ 已完成工作**：

已创建Django Fixtures文件，位于以下目录：
- `backend/apps/call/fixtures/` - 叫应模块fixtures

**已创建的Fixtures文件**：

1. **`backend/apps/call/fixtures/initial_call_groups.json`** - 叫应分组数据
   - 3个分组：1个常态化分组（日常政策传达组）+ 2个非常态化分组（红色I级、橙色Ⅱ级应急响应组）
   - 分组包含分组类型、负责应急事件级别等信息

2. **`backend/apps/call/fixtures/initial_call_targets.json`** - 叫应对象数据
   - 5个对象：2个政府部门 + 2个企业单位 + 1个事业单位
   - 对象包含安全责任人、联系电话、联系地址等信息
   - 企业单位包含企业名称、企业信息等字段

3. **`backend/apps/call/fixtures/initial_call_persons.json`** - 叫应人员数据
   - 5个人员：覆盖红色I级、橙色Ⅱ级应急响应组和日常政策传达组
   - 人员包含职级、手机号码、办公电话、负责应急事件级别等信息
   - 关联分组和组织

4. **`backend/apps/call/fixtures/initial_policy_files.json`** - 政策文件数据
   - 3个文件：2个已发布文件 + 1个未发布文件
   - 文件包含文件路径、文件大小、政策标题、政策内容、政策要求等信息
   - 关联上传用户

5. **`backend/apps/call/fixtures/initial_policy_distributions.json`** - 政策文件下发数据
   - 4条下发记录：覆盖不同反馈状态（未反馈、已反馈、超时未反馈）和督办状态
   - 下发包含反馈内容要求、反馈截止时间、反馈内容等信息
   - 关联政策文件、叫应对象、下发用户、督办用户

6. **`backend/apps/call/fixtures/initial_call_records.json`** - 叫应记录数据
   - 5条叫应记录：2条常态化叫应（政策文件下发）+ 3条非常态化叫应（预警触发、一键叫应）
   - 记录包含叫应类型、叫应来源、叫应渠道、叫应状态、接收状态、响应状态等信息
   - 支持多种叫应渠道（system-系统消息、sms-短信、phone-电话）
   - 关联政策下发、预警、对象、人员、分组

**数据加载顺序**（需要先加载基础数据和预警数据）：

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

**数据特点**：
- 叫应分组覆盖常态化分组和非常态化分组（按应急事件级别）
- 叫应对象覆盖政府部门、企业单位、事业单位三种类型
- 叫应人员按应急事件级别分组，支持应急响应和日常传达两种场景
- 政策文件包含完整的政策内容、政策要求等信息
- 政策下发形成完整的反馈跟踪和督办管理流程
- 叫应记录支持常态化叫应和非常态化叫应两种类型，支持多种叫应渠道
- 叫应记录与预警、预案执行关联，形成完整的应急响应业务流程

**✅ 第六步：简报体系初始化**（简报模块）
1. 创建简报模板（关联消息模板）
2. 创建简报策略（关联模板、预警级别）
3. 创建简报数据（关联策略、预警）
4. 创建简报推送（关联数据、人员、组织）

**✅ 已完成工作**：

已创建Django Fixtures文件，位于以下目录：
- `backend/apps/brief/fixtures/` - 简报模块fixtures

**已创建的Fixtures文件**：

1. **`backend/apps/brief/fixtures/initial_brief_templates.json`** - 简报模板数据
   - 3个模板：2个常态化运行报告模板（危化品日报、防汛周报）+ 1个非常态化突发预警简报模板
   - 模板包含模板内容（支持变量占位符）、变量说明、数据配置等信息
   - 支持行业维度、区域维度、时间维度配置（JSON格式）

2. **`backend/apps/brief/fixtures/initial_brief_strategies.json`** - 简报策略数据
   - 4个策略：2个常态化策略（定时触发：日报、周报）+ 2个非常态化策略（事件触发：红色I级、橙色Ⅱ级预警）
   - 策略包含触发配置（定时触发时间、事件触发条件）、预警级别过滤、行业过滤、区域过滤等信息
   - 支持多种推送目标类型（用户、角色、组织）和推送渠道（系统消息、短信、邮件）
   - 关联消息模板（用于推送通知）

3. **`backend/apps/brief/fixtures/initial_brief_data.json`** - 简报数据
   - 4条简报数据：2条常态化运行报告（危化品日报、防汛周报）+ 2条非常态化突发预警简报（红色I级、橙色Ⅱ级）
   - 简报包含完整的简报内容（标题、正文）、数据摘要、行业维度数据、区域维度数据、时间维度数据（JSON格式）
   - 支持附件（PDF文件）
   - 关联策略和模板

4. **`backend/apps/brief/fixtures/initial_brief_pushes.json`** - 简报推送记录数据
   - 10条推送记录：覆盖不同推送目标类型（用户、角色、组织）和推送渠道（系统消息、短信、邮件）
   - 推送包含推送状态、推送时间、阅读状态、阅读时间等信息
   - 包含消息ID（系统消息或短信平台返回的ID）

**数据加载顺序**（需要先加载基础数据和消息模板）：

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

**数据特点**：
- 简报模板支持变量占位符，支持行业、区域、时间等多维度配置
- 简报策略支持定时触发和事件触发两种方式，支持多种推送目标和渠道
- 简报数据包含完整的数据摘要和多维度分析数据（JSON格式）
- 简报推送支持多种推送渠道，支持推送状态和阅读状态跟踪
- 常态化简报和非常态化简报形成完整的业务流程

**第七步：演练体系初始化**（演练模块）
1. 创建演练事件（关联预案、组织）
2. 创建演练评价（关联事件）
3. 创建演练总结（关联事件、评价）
4. 生成演练分析统计数据

**✅ 已完成工作**：

已创建Django Fixtures文件，位于以下目录：
- `backend/apps/drill/fixtures/` - 演练模块fixtures

**已创建的Fixtures文件**：

1. **`backend/apps/drill/fixtures/initial_drill_events.json`** - 演练事件数据
   - 包含5个演练事件
   - 覆盖不同事故类型（危化品泄漏、防汛抢险、危化品火灾、建筑施工坍塌、森林火灾）
   - 包含不同演练状态（已完成2个、进行中1个、未开始1个）
   - 关联预案、组织等数据
   - 地理位置均位于马鞍山市范围内

2. **`backend/apps/drill/fixtures/initial_drill_evaluations.json`** - 演练评价数据
   - 包含12条演练评价记录
   - 覆盖不同节点类型（信息收集、决策指挥、资源调配、现场处置、其他）
   - 包含不同评价等级（优秀、良好）
   - 评价得分：85-93分
   - 关联演练事件、评价人等数据

3. **`backend/apps/drill/fixtures/initial_drill_summaries.json`** - 演练总结数据
   - 包含3条演练总结记录
   - 对应已完成的演练事件
   - 包含完整的评价维度（内部沟通、预案熟悉程度、预案可操作性、职责定位、应急指挥、应急处置）
   - 总体等级：优秀1个、良好2个
   - 总体得分：88.60-91.50分

4. **`backend/apps/drill/fixtures/initial_drill_analyses.json`** - 演练分析统计数据
   - 包含6条统计分析记录
   - 包含日报、月报等统计类型
   - 包含按单位、按事故类型的统计分析
   - 包含演练次数、完成次数、优秀/良好/合格/不合格次数、平均分等统计指标

**辅助文件**：
- `backend/apps/drill/fixtures/README.md` - 演练模块fixtures使用说明

**使用方法**：
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

**数据特点**：
- 演练事件覆盖不同事故类型和演练状态，形成完整的演练流程数据
- 演练评价覆盖所有节点类型，包含详细的评价内容和评分
- 演练总结包含完整的评价维度和改进建议
- 演练分析提供多维度统计数据，支持统计分析功能
- 所有地理坐标均位于马鞍山市范围内
- 时间数据分布在2024年10月至12月，符合业务场景

**第八步：数据验证和优化**
1. 验证数据关联关系完整性
2. 验证地理数据分布合理性
3. 验证时间数据逻辑性
4. 优化数据质量和真实性
5. 测试业务流程完整性

**✅ 已完成工作**：

已创建数据验证脚本：`backend/scripts/validate_data.py`

**使用方法**：
```bash
# 在虚拟环境中执行
cd backend
python scripts/validate_data.py
```

**验证内容**：
1. **数据关联关系完整性**：
   - 验证所有外键关联是否正确（用户-组织、演练事件-预案、演练评价-演练事件等）
   - 检查引用的ID是否在对应表中存在

2. **地理数据分布合理性**：
   - 验证所有包含坐标的数据是否在马鞍山市范围内
   - 马鞍山市范围：经度 118.3-118.7，纬度 31.5-31.9

3. **时间数据逻辑性**：
   - 验证创建时间 <= 更新时间
   - 验证审批时间 <= 发布时间
   - 验证生效时间 <= 失效时间
   - 验证开始时间 <= 结束时间

4. **数据质量和真实性**：
   - 验证编码唯一性（由数据库约束保证）
   - 验证必填字段完整性
   - 验证手机号格式
   - 验证坐标精度（小数点后6位）
   - 统计状态分布情况

5. **业务流程完整性**：
   - 测试演练业务流程（已完成演练是否有评价和总结）
   - 测试预案业务流程（已发布预案是否有结构、流程、任务）
   - 测试安全资源业务流程（是否有完整地理信息）

**执行结果**：
脚本会输出详细的验证结果，包括：
- ✅ 通过项
- ⚠️  警告项（需要关注但不影响使用）
- ❌ 错误项（需要修复）

**验证执行记录**：

**第一次执行（2024-01-XX）**：
- 发现3个警告：
  1. 已发布的预案"马钢焦化厂危化品泄漏现场处置方案" (ID: 3) 没有结构数据
  2. 已发布的预案"马钢焦化厂危化品泄漏现场处置方案" (ID: 3) 没有流程数据
  3. 已发布的预案"马钢焦化厂危化品泄漏现场处置方案" (ID: 3) 没有任务数据

**问题修复**：
- ✅ 已为预案ID 3补充结构数据（3个结构节点）
- ✅ 已为预案ID 3补充流程数据（3个流程）
- ✅ 已为预案ID 3补充任务数据（7个任务）

**修复内容**：
1. **结构数据**（`initial_plan_structures.json`）：
   - 添加了"事故发现与报告"章节（pk: 8）
   - 添加了"现场处置措施"章节（pk: 9）
   - 添加了"环境监测与安全防护"章节（pk: 10）

2. **流程数据**（`initial_plan_flows.json`）：
   - 添加了"事故发现与报告"流程（pk: 7, flow_code: FLOW006）
   - 添加了"现场处置与泄漏控制"流程（pk: 8, flow_code: FLOW007）
   - 添加了"环境监测与处置完成"流程（pk: 9, flow_code: FLOW008）

3. **任务数据**（`initial_plan_tasks.json`）：
   - 添加了"事故发现与停止作业"任务（pk: 8, task_code: TASK008）
   - 添加了"事故报告与方案启动"任务（pk: 9, task_code: TASK009）
   - 添加了"组织人员疏散"任务（pk: 10, task_code: TASK010）
   - 添加了"泄漏源控制"任务（pk: 11, task_code: TASK011）
   - 添加了"污染物处置"任务（pk: 12, task_code: TASK012）
   - 添加了"环境监测"任务（pk: 13, task_code: TASK013）
   - 添加了"安全评估与处置完成"任务（pk: 14, task_code: TASK014）

**注意事项**：
- 执行前请确保已加载所有fixtures数据
- 如果发现错误，请根据提示修复对应的fixtures文件
- 警告项可以根据实际情况决定是否修复
- 修复后需要重新加载对应的fixtures文件：
  ```bash
  python manage.py loaddata apps/plan/fixtures/initial_plan_structures.json
  python manage.py loaddata apps/plan/fixtures/initial_plan_flows.json
  python manage.py loaddata apps/plan/fixtures/initial_plan_tasks.json
  ```

#### 6.9 数据格式规范

**数据编码规范**:
- 统一编码规则：模块前缀 + 序号（如：MON001、WAR001）
- 编码唯一性：确保各实体编码唯一

**数据命名规范**:
- 名称真实化：使用真实的地名、组织名、人名（脱敏处理）
- 名称规范：符合行业规范和习惯

**数据内容规范**:
- 描述信息：完整、真实、有意义的描述
- 联系信息：符合格式规范（手机号、邮箱等）
- 坐标信息：精确到小数点后6位

**数据状态规范**:
- 状态分布：不同状态的数据合理分布（如：在线/离线、已发布/待发布等）
- 状态逻辑：确保状态转换符合业务逻辑

#### 6.10 质量要求

- **完整性**: 确保各模块核心数据完整，关键字段不缺失
- **一致性**: 确保数据关联关系正确，外键关联有效
- **真实性**: 数据内容真实合理，符合实际业务场景
- **关联性**: 确保业务流程数据关联完整，形成闭环
- **可演示性**: 数据足以支撑完整的业务流程演示
- **可视化性**: 地理数据分布合理，支持大屏可视化展示

#### 6.11 技术实现方案

根据项目使用的Django框架和MySQL数据库，提供以下技术实现方案，可按实际需求选择：

##### 方案一：Django Fixtures（推荐）

**优点**:
- 与Django ORM集成良好，自动处理外键关联
- 支持数据序列化和反序列化
- 可以追踪版本变更
- 便于维护和更新

**实现步骤**:
1. 在Django应用中创建`fixtures`目录（如：`backend/apps/system/fixtures/`）
2. 使用Django的`dumpdata`命令导出初始数据：
   ```bash
   python manage.py dumpdata system.organization --indent 2 > backend/apps/system/fixtures/initial_organizations.json
   python manage.py dumpdata system.user --indent 2 > backend/apps/system/fixtures/initial_users.json
   ```
3. 编辑生成的JSON文件，填充演示数据（注意外键使用自然键或主键）
4. 使用`loaddata`命令加载数据：
   ```bash
   python manage.py loaddata initial_organizations.json
   python manage.py loaddata initial_users.json
   ```

**Fixtures文件结构**:
```
backend/
├── apps/
│   ├── system/
│   │   └── fixtures/
│   │       ├── initial_organizations.json
│   │       ├── initial_users.json
│   │       ├── initial_roles.json
│   │       └── initial_permissions.json
│   ├── safety/
│   │   └── fixtures/
│   │       ├── initial_resources.json
│   │       ├── initial_targets.json
│   │       └── initial_shelters.json
│   └── ...
```

**注意事项**:
- 确保数据加载顺序符合依赖关系（先加载被引用的数据）
- 外键可以使用自然键（`natural_key`）或主键ID
- 日期时间字段需使用ISO格式：`"2024-12-15T10:00:00Z"`

##### 方案二：Django Management Command（自定义管理命令）

**优点**:
- 灵活性高，可以使用Python代码处理复杂逻辑
- 支持数据验证和错误处理
- 可以生成随机数据或基于模板生成
- 便于自动化执行

**实现步骤**:
1. 创建管理命令目录结构：
   ```bash
   backend/apps/system/management/
   ├── __init__.py
   └── commands/
       ├── __init__.py
       └── init_demo_data.py
   ```

2. 编写管理命令脚本（示例）：
   ```python
   # backend/apps/system/management/commands/init_demo_data.py
   from django.core.management.base import BaseCommand
   from apps.system.models import Organization, User
   
   class Command(BaseCommand):
       help = '初始化演示数据'
       
       def handle(self, *args, **options):
           # 创建组织
           org = Organization.objects.create(
               org_code='ORG001',
               org_name='马鞍山市应急管理局',
               # ... 其他字段
           )
           
           # 创建用户
           User.objects.create(
               username='admin',
               organization=org,
               # ... 其他字段
           )
           
           self.stdout.write(self.style.SUCCESS('演示数据初始化完成'))
   ```

3. 执行命令：
   ```bash
   python manage.py init_demo_data
   ```

**优点**:
- 可以使用Django ORM的所有功能
- 支持事务处理，确保数据一致性
- 可以添加进度提示和错误处理

##### 方案三：SQL脚本直接导入

**优点**:
- 执行速度快，适合大量数据
- 可以直接使用MySQL的批量插入功能
- 不受Django ORM限制

**实现步骤**:
1. 创建SQL脚本文件（如：`backend/data/init_demo_data.sql`）
2. 编写INSERT语句：
   ```sql
   -- 注意：需按依赖顺序插入，先插入被引用的表
   INSERT INTO `system_organization` (`org_code`, `org_name`, `created_at`, `updated_at`) 
   VALUES 
       ('ORG001', '马鞍山市应急管理局', NOW(), NOW()),
       ('ORG002', '雨山区应急管理局', NOW(), NOW());
   
   -- 插入用户（使用上面插入的组织ID）
   INSERT INTO `system_user` (`username`, `organization_id`, `created_at`, `updated_at`)
   VALUES
       ('admin', 1, NOW(), NOW());
   ```

3. 执行SQL脚本：
   ```bash
   # 方式1：使用mysql命令行
   mysql -u root -p risk_monitoring < backend/data/init_demo_data.sql
   
   # 方式2：使用Django dbshell
   python manage.py dbshell < backend/data/init_demo_data.sql
   ```

**注意事项**:
- 需要手动处理外键关联（使用ID）
- 需要处理自增ID的问题（可以使用固定ID或先查询再插入）
- 需要确保表名和字段名正确（Django模型名可能不同）
- 需要注意字符编码（UTF-8）

##### 方案四：API接口批量创建

**优点**:
- 可以复用现有的API接口和验证逻辑
- 可以模拟真实的创建流程
- 便于测试API功能

**实现步骤**:
1. 创建Python脚本调用API接口：
   ```python
   # backend/scripts/init_demo_data_via_api.py
   import requests
   import json
   
   BASE_URL = 'http://127.0.0.1:8000/api/v1'
   TOKEN = 'your-auth-token'
   
   headers = {
       'Authorization': f'Bearer {TOKEN}',
       'Content-Type': 'application/json'
   }
   
   # 创建组织
   org_data = {
       'org_code': 'ORG001',
       'org_name': '马鞍山市应急管理局',
       # ... 其他字段
   }
   response = requests.post(f'{BASE_URL}/system/organizations/', 
                           json=org_data, headers=headers)
   org_id = response.json()['id']
   
   # 创建用户（使用上面的组织ID）
   user_data = {
       'username': 'admin',
       'organization_id': org_id,
       # ... 其他字段
   }
   requests.post(f'{BASE_URL}/system/users/', 
                json=user_data, headers=headers)
   ```

2. 执行脚本：
   ```bash
   python backend/scripts/init_demo_data_via_api.py
   ```

**适用场景**:
- 需要测试API功能
- 需要模拟真实用户操作
- 数据量较小的情况

##### 方案五：混合方案（推荐用于大规模数据）

结合多种方案的优点：
1. **基础数据**（组织、用户、角色等）: 使用Django Fixtures或Management Command
2. **业务数据**（监测点、预警、预案等）: 使用Django Management Command（便于处理复杂关联）
3. **大量数据**（预案结构、流程节点等）: 使用SQL脚本批量插入

##### 推荐实施方案

**第一阶段：准备数据文件**
1. 使用Excel或CSV准备原始数据（便于编辑和维护）
2. 转换为JSON格式（用于Fixtures）或SQL格式（用于SQL脚本）

**第二阶段：实现数据导入脚本**
1. 创建Django Management Command：`init_demo_data`
2. 按模块划分，分别创建导入函数
3. 按依赖顺序执行导入

**第三阶段：执行数据导入**
```bash
# 方式1：使用Fixtures（适合基础数据）
python manage.py loaddata initial_organizations.json
python manage.py loaddata initial_users.json

# 方式2：使用管理命令（适合复杂业务数据）
python manage.py init_demo_data

# 方式3：使用SQL脚本（适合大量数据）
mysql -u root -p risk_monitoring < init_demo_data.sql
```

**第四阶段：验证数据**
1. 检查数据完整性
2. 验证外键关联
3. 测试业务流程

##### 技术实现注意事项

1. **外键处理**:
   - Fixtures: 使用自然键或主键ID
   - Management Command: 使用Django ORM对象引用
   - SQL脚本: 使用固定的主键ID或先查询再插入

2. **日期时间处理**:
   - 统一使用ISO格式：`"2024-12-15T10:00:00Z"`
   - 或使用Django的`timezone.now()`动态生成

3. **坐标数据**:
   - 确保经纬度格式正确（WGS84，小数点后6位）
   - 验证坐标范围（马鞍山市区域：约118.3-118.7, 31.6-31.9）

4. **数据编码**:
   - 统一使用UTF-8编码
   - 确保数据库字符集为utf8mb4

5. **事务处理**:
   - 使用Django的`transaction.atomic()`确保数据一致性
   - 导入失败时回滚，避免部分数据导入

6. **性能优化**:
   - 大量数据使用批量插入（`bulk_create`）
   - SQL脚本使用`INSERT INTO ... VALUES (...), (...), (...)`批量插入
   - 禁用信号和触发器（如需要）


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

## API接口

### 认证接口

- `POST /api/v1/auth/login/` - 用户登录（获取JWT Token）
- `POST /api/v1/auth/refresh/` - 刷新Token

### 接口规范

所有API接口遵循RESTful设计规范，统一响应格式：

**成功响应**:
```json
{
    "code": 200,
    "message": "success",
    "data": {...}
}
```

**错误响应**:
```json
{
    "code": 400,
    "message": "错误信息",
    "data": null,
    "errors": {...}
}
```

### 认证方式

使用JWT Token进行认证，在请求头中添加：

```
Authorization: Bearer <your-access-token>
```

## 开发规范

### 代码结构

- 每个功能模块独立为一个Django App
- 使用Django REST Framework的ViewSet和Serializer
- 统一使用自定义的APIResponse响应格式
- 统一异常处理

### 数据库模型

- 所有模型继承自 `django.db.models.Model`
- 使用软删除（`deleted_at`字段）
- 统一时间戳字段（`created_at`, `updated_at`）
- 使用MySQL空间数据类型支持GIS功能

### 权限控制

- 使用RBAC（基于角色的访问控制）
- 通过Django Permissions和自定义权限类实现
- API接口默认需要认证

## 待开发功能

### 第一阶段：基础框架
- [x] 项目结构搭建
- [x] 基础配置
- [x] 用户权限管理模块
  - [x] 用户、角色、权限、组织模型
  - [x] RBAC权限控制
  - [x] JWT认证
  - [x] API接口（用户、角色、权限、组织管理）
  - [x] Django Admin配置
- [x] 数据库模型定义（其他模块）
  - [x] risk模块：预警级别、预警规则、监测点、报警记录、风险预警、报警统计、隐患排查、隐患整改
  - [x] system模块：数据源、消息模板
  - [x] brief模块：简报模板、简报策略、简报数据、简报推送
  - [x] call模块：叫应分组、叫应对象、叫应人员、政策文件、政策下发、叫应记录
  - [x] plan模块：应急预案、预案结构、预案流程、预案任务、预案执行、任务执行记录
  - [x] safety模块：安全资源、防护目标、避难场所、行业态势、区域态势、监测数据、预警事件、危险源、视频监控
  - [x] drill模块：演练事件、演练评价、演练总结、演练分析

### 第二阶段：核心功能
- [x] 风险监测预警模块
  - [x] 预警级别管理API（CRUD）
  - [x] 预警规则管理API（CRUD）
  - [x] 风险监测点管理API（CRUD、状态更新）
  - [x] 报警记录管理API（CRUD、处理报警）
  - [x] 风险预警管理API（CRUD、发布预警、处置预警）
  - [x] 报警统计API（查询统计）
  - [x] 隐患排查管理API（CRUD）
  - [x] 隐患整改管理API（CRUD、验收整改）
- [x] 简报模块
  - [x] 简报模板管理API（CRUD）
  - [x] 简报策略管理API（CRUD、执行策略）
  - [x] 简报数据管理API（CRUD、生成简报）
  - [x] 简报推送管理API（CRUD、推送简报、标记已读）
- [x] 叫应模块
  - [x] 叫应分组管理API（CRUD）
  - [x] 叫应对象管理API（CRUD）
  - [x] 叫应人员管理API（CRUD）
  - [x] 政策文件管理API（CRUD、发布政策文件）
  - [x] 政策文件下发管理API（CRUD、反馈下发、督办下发）
  - [x] 叫应记录管理API（CRUD、响应叫应、重试叫应、叫应统计）
  - [x] 一键叫应API（支持常态化叫应和非常态化叫应）

### 第三阶段：扩展功能
- [x] 预案模块
  - [x] 应急预案管理API（CRUD、发布预案、审批预案、修订预案、废止预案、预案统计）
  - [x] 预案结构管理API（CRUD、获取树形结构）
  - [x] 预案流程管理API（CRUD、获取树形流程）
  - [x] 预案任务管理API（CRUD）
  - [x] 预案执行记录管理API（CRUD、启动执行、更新执行状态、完成执行）
  - [x] 预案任务执行记录管理API（CRUD、接受任务、开始执行任务、完成任务）
- [x] 安全态势展示模块
  - [x] 安全资源管理API（CRUD、资源统计）
  - [x] 防护目标管理API（CRUD、防护目标统计）
  - [x] 避难场所管理API（CRUD、避难场所统计）
  - [x] 行业态势管理API（CRUD）
  - [x] 区域态势管理API（CRUD、四色图数据）
  - [x] 监测数据管理API（CRUD、监测数据统计）
  - [x] 预警事件管理API（CRUD）
  - [x] 危险源管理API（CRUD、危险源统计）
  - [x] 视频监控设施管理API（CRUD、附近监控设施、视频监控统计）
- [x] 演练监督模块
  - [x] 演练事件管理API（CRUD、更新演练状态、演练事件统计）
  - [x] 演练评价管理API（CRUD、演练评价统计）
  - [x] 演练总结管理API（CRUD、演练总结统计）
  - [x] 演练分析管理API（CRUD、演练分析统计）

## 注意事项

1. **数据库连接**: 确保MySQL服务已启动，数据库已创建
2. **环境变量**: 开发环境使用 `.env.local` 文件，生产环境使用系统环境变量
3. **静态文件**: 
   - 开发环境：静态文件从 `backend/static/` 目录自动提供
   - 生产环境：需要运行 `python manage.py collectstatic` 收集到 `backend/staticfiles/` 目录
4. **媒体文件**: 上传的媒体文件存储在 `backend/media/` 目录
5. **日志文件**: 日志文件存储在 `backend/logs/` 目录，需要确保目录存在

## 开发命令

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

# 生成API文档Schema（可选，通常自动生成）
python manage.py generate_swagger --format openapi-json --file swagger.json
```

## 相关文档

- [系统设计文档](../01_sys_design.md)
- [数据库设计文档](../02_database_design.md)
- [产品功能设计文档](../00_prod_design.md)

## 许可证

内部项目，仅供开发使用。

