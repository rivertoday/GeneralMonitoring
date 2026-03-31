# 风险监测预警系统 - 数据库设计文档

## 1. 数据库设计说明

### 1.1 数据库基本信息
- **数据库类型**: MySQL 8.0
- **字符集**: utf8mb4
- **排序规则**: utf8mb4_unicode_ci
- **存储引擎**: InnoDB
- **空间数据支持**: 使用MySQL空间数据类型（GEOMETRY、POINT等）

### 1.2 设计规范
- 表名使用小写字母和下划线，采用复数形式（如：users, roles）
- 字段名使用小写字母和下划线（如：user_name, created_at）
- 主键统一使用 `id`，类型为 `BIGINT UNSIGNED AUTO_INCREMENT`
- 所有表必须包含 `created_at` 和 `updated_at` 字段，类型为 `DATETIME`
- 软删除使用 `deleted_at` 字段，类型为 `DATETIME`，允许NULL
- 状态字段使用 `TINYINT` 类型，0表示禁用/删除，1表示启用/正常
- 文本字段根据实际需求选择 `VARCHAR` 或 `TEXT` 类型
- 金额字段使用 `DECIMAL(10,2)` 类型
- 空间数据使用 `GEOMETRY` 或 `POINT` 类型

---

## 2. 基础数据表设计（4.1.7）

### 2.1 基础数据表设计说明

#### 2.1.1 用户权限体系
- 采用RBAC（基于角色的访问控制）模型
- 用户通过 `user_roles` 表关联角色
- 角色通过 `role_permissions` 表关联权限
- 权限支持树形结构，通过 `parent_id` 字段实现层级关系
- 权限类型包括：菜单权限、按钮权限、接口权限

#### 2.1.2 组织架构
- 组织表支持树形结构，通过 `parent_id` 字段实现层级关系
- 组织类型包括：政府部门、企业单位、事业单位
- 用户通过 `organization_id` 字段关联所属组织

#### 2.1.3 数据源管理
- 支持多种数据源类型：API接口、数据库、文件
- 支持多个行业类型：气象、危化、防汛、交通运输、森林火灾
- 数据库密码采用加密存储
- 支持定时同步配置

#### 2.1.4 消息模板
- 支持多种模板类型：系统消息、短信、邮件
- 支持多种消息类型：预警通知、报警通知、简报推送、叫应通知等
- 消息内容支持变量占位符，通过 `variables` 字段说明可用变量

---

### 2.2 用户表 (users)

**表名**: `users`  
**表说明**: 系统用户信息表，存储用户基本信息和认证信息

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 用户ID，主键 |
| username | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 用户名，唯一索引 |
| password | VARCHAR | 255 | NOT NULL | - | - | - | 密码（加密存储） |
| real_name | VARCHAR | 50 | NULL | - | - | - | 真实姓名 |
| email | VARCHAR | 100 | NULL | - | - | INDEX | 邮箱地址 |
| phone | VARCHAR | 20 | NULL | - | - | INDEX | 手机号码 |
| avatar | VARCHAR | 255 | NULL | - | - | - | 头像URL |
| gender | TINYINT | - | NULL | 0 | - | - | 性别：0-未知，1-男，2-女 |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| last_login_at | DATETIME | - | NULL | - | - | - | 最后登录时间 |
| last_login_ip | VARCHAR | 50 | NULL | - | - | - | 最后登录IP |
| organization_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 所属组织ID，外键关联organizations表 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_username` (`username`)
- KEY `idx_email` (`email`)
- KEY `idx_phone` (`phone`)
- KEY `idx_status` (`status`)
- KEY `idx_organization_id` (`organization_id`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 2.3 角色表 (roles)

**表名**: `roles`  
**表说明**: 系统角色表，定义系统中的各种角色

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 角色ID，主键 |
| role_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 角色编码，唯一索引 |
| role_name | VARCHAR | 50 | NOT NULL | - | - | - | 角色名称 |
| description | VARCHAR | 255 | NULL | - | - | - | 角色描述 |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| sort_order | INT | - | NULL | 0 | - | - | 排序顺序 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_role_code` (`role_code`)
- KEY `idx_status` (`status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 2.4 权限表 (permissions)

**表名**: `permissions`  
**表说明**: 系统权限表，定义系统中的各种权限

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 权限ID，主键 |
| permission_code | VARCHAR | 100 | NOT NULL | - | - | UNIQUE | 权限编码，唯一索引 |
| permission_name | VARCHAR | 100 | NOT NULL | - | - | - | 权限名称 |
| permission_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 权限类型：1-菜单，2-按钮，3-接口 |
| parent_id | BIGINT UNSIGNED | - | NULL | 0 | - | INDEX | 父权限ID，0表示顶级权限 |
| path | VARCHAR | 255 | NULL | - | - | - | 路由路径（菜单类型） |
| component | VARCHAR | 255 | NULL | - | - | - | 组件路径（菜单类型） |
| icon | VARCHAR | 100 | NULL | - | - | - | 图标（菜单类型） |
| api_path | VARCHAR | 255 | NULL | - | - | - | API路径（接口类型） |
| http_method | VARCHAR | 10 | NULL | - | - | - | HTTP方法：GET, POST, PUT, DELETE等 |
| description | VARCHAR | 255 | NULL | - | - | - | 权限描述 |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| sort_order | INT | - | NULL | 0 | - | - | 排序顺序 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_permission_code` (`permission_code`)
- KEY `idx_permission_type` (`permission_type`)
- KEY `idx_parent_id` (`parent_id`)
- KEY `idx_status` (`status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 2.5 用户角色关联表 (user_roles)

**表名**: `user_roles`  
**表说明**: 用户和角色的多对多关联表

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 关联ID，主键 |
| user_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 用户ID，外键关联users表 |
| role_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 角色ID，外键关联roles表 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | - | 创建时间 |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_user_role` (`user_id`, `role_id`)
- KEY `idx_user_id` (`user_id`)
- KEY `idx_role_id` (`role_id`)

---

### 2.6 角色权限关联表 (role_permissions)

**表名**: `role_permissions`  
**表说明**: 角色和权限的多对多关联表

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 关联ID，主键 |
| role_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 角色ID，外键关联roles表 |
| permission_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 权限ID，外键关联permissions表 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | - | 创建时间 |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_role_permission` (`role_id`, `permission_id`)
- KEY `idx_role_id` (`role_id`)
- KEY `idx_permission_id` (`permission_id`)

---

### 2.7 组织表 (organizations)

**表名**: `organizations`  
**表说明**: 组织架构表，支持树形结构

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 组织ID，主键 |
| org_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 组织编码，唯一索引 |
| org_name | VARCHAR | 100 | NOT NULL | - | - | - | 组织名称 |
| parent_id | BIGINT UNSIGNED | - | NULL | 0 | - | INDEX | 父组织ID，0表示顶级组织 |
| org_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 组织类型：1-政府部门，2-企业单位，3-事业单位 |
| level | INT | - | NULL | 1 | - | - | 组织层级 |
| leader | VARCHAR | 50 | NULL | - | - | - | 负责人 |
| phone | VARCHAR | 20 | NULL | - | - | - | 联系电话 |
| address | VARCHAR | 255 | NULL | - | - | - | 地址 |
| description | VARCHAR | 255 | NULL | - | - | - | 组织描述 |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| sort_order | INT | - | NULL | 0 | - | - | 排序顺序 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_org_code` (`org_code`)
- KEY `idx_parent_id` (`parent_id`)
- KEY `idx_org_type` (`org_type`)
- KEY `idx_status` (`status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 2.8 数据源表 (data_sources)

**表名**: `data_sources`  
**表说明**: 外部数据源配置表，用于管理接入的外部数据源

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 数据源ID，主键 |
| source_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 数据源编码，唯一索引 |
| source_name | VARCHAR | 100 | NOT NULL | - | - | - | 数据源名称 |
| source_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 数据源类型：1-API接口，2-数据库，3-文件 |
| industry_type | TINYINT | - | NOT NULL | - | - | INDEX | 行业类型：1-气象，2-危化，3-防汛，4-交通运输，5-森林火灾 |
| api_url | VARCHAR | 500 | NULL | - | - | - | API接口地址（API类型） |
| api_method | VARCHAR | 10 | NULL | GET | - | - | HTTP方法：GET, POST等 |
| api_params | TEXT | - | NULL | - | - | - | API请求参数（JSON格式） |
| api_headers | TEXT | - | NULL | - | - | - | API请求头（JSON格式） |
| db_type | VARCHAR | 20 | NULL | - | - | - | 数据库类型（数据库类型） |
| db_host | VARCHAR | 100 | NULL | - | - | - | 数据库主机 |
| db_port | INT | - | NULL | 3306 | - | - | 数据库端口 |
| db_name | VARCHAR | 100 | NULL | - | - | - | 数据库名称 |
| db_username | VARCHAR | 100 | NULL | - | - | - | 数据库用户名 |
| db_password | VARCHAR | 255 | NULL | - | - | - | 数据库密码（加密存储） |
| db_table | VARCHAR | 100 | NULL | - | - | - | 数据表名 |
| sync_interval | INT | - | NULL | 60 | - | - | 同步间隔（分钟） |
| last_sync_at | DATETIME | - | NULL | - | - | - | 最后同步时间 |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| description | VARCHAR | 255 | NULL | - | - | - | 数据源描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_source_code` (`source_code`)
- KEY `idx_source_type` (`source_type`)
- KEY `idx_industry_type` (`industry_type`)
- KEY `idx_status` (`status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 2.9 消息模板表 (message_templates)

**表名**: `message_templates`  
**表说明**: 消息推送模板表，用于管理短信、系统消息等模板

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 模板ID，主键 |
| template_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 模板编码，唯一索引 |
| template_name | VARCHAR | 100 | NOT NULL | - | - | - | 模板名称 |
| template_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 模板类型：1-系统消息，2-短信，3-邮件 |
| message_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 消息类型：1-预警通知，2-报警通知，3-简报推送，4-叫应通知，5-其他 |
| subject | VARCHAR | 200 | NULL | - | - | - | 消息主题（邮件类型） |
| content | TEXT | - | NOT NULL | - | - | - | 消息内容，支持变量占位符 |
| variables | TEXT | - | NULL | - | - | - | 变量说明（JSON格式） |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| description | VARCHAR | 255 | NULL | - | - | - | 模板描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_template_code` (`template_code`)
- KEY `idx_template_type` (`template_type`)
- KEY `idx_message_type` (`message_type`)
- KEY `idx_status` (`status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

**说明**: 以上为基础数据表（4.1.7）的详细设计，请确认后继续设计其他部分。

---

## 3. 风险监测预警相关表设计（4.1.1）

### 3.1 风险监测预警相关表设计说明

#### 3.1.1 预警级别体系
- 采用四色预警体系：红色I级（特别严重）、橙色Ⅱ级（严重）、黄色Ⅲ级（较重）、蓝色Ⅳ级（一般）
- 每个预警级别定义响应组织要求和响应时间要求
- 预警级别与预警规则关联，用于自动生成预警

#### 3.1.2 预警规则管理
- 预警生成规则：基于报警数据分析，通过报警频率、报警时长等条件自动生成预警
- 预警处置规则：定义预警的响应时间、处置时间、反馈时间等要求
- 规则支持按行业类型配置，不同行业可配置不同的规则

#### 3.1.3 风险监测
- 支持三种监测类型：实时监测、全域监测、重点监测
  - **实时监测**：汇聚森林火灾、防汛、交通运输、危险化学品领域实时感知监测数据和预警信息
  - **全域监测**：对危化企业、重大危险源、两客一危车辆、河流、水库等要素进行全面监控，按照街道进行空间划分
  - **重点监测**：对本区具有重大风险隐患点的危险化学品企业进行监测，展示企业隐患排查信息及整改信息，本次项目实现20个重大风险隐患点的信息展示
- 监测点支持空间数据类型，便于GIS地图展示
- 监测点可设置阈值，超过阈值自动触发报警
- 支持监测点在线状态监控

#### 3.1.4 报警与预警流程
- 监测数据超过阈值 → 生成报警记录
- 报警记录通过预警规则分析 → 生成风险预警
- 风险预警关联预警级别，确定响应组织
- 支持预警发布、处置、反馈的完整流程

#### 3.1.5 预警分析类型
- **突出预警**：根据风险因素和风险事故的突出特征进行预警
- **同比预警**：与去年同期数据进行对比分析，识别异常情况
- **环比预警**：与上一周期数据进行对比分析，识别趋势变化
- 预警关联预案主题库，进行分级响应和处理

#### 3.1.6 统计分析
- 支持按时间维度（日、周、月、年）统计
- 支持按空间维度（街道）统计
- 支持按行业类型统计
- 统计表采用唯一索引防止重复统计

---

### 3.2 预警级别表 (warning_levels)

**表名**: `warning_levels`  
**表说明**: 预警级别配置表，定义四色预警级别（红色I级、橙色Ⅱ级、黄色Ⅲ级、蓝色Ⅳ级）

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 预警级别ID，主键 |
| level_code | VARCHAR | 20 | NOT NULL | - | - | UNIQUE | 预警级别编码：I-红色，II-橙色，III-黄色，IV-蓝色 |
| level_name | VARCHAR | 50 | NOT NULL | - | - | - | 预警级别名称 |
| level_color | VARCHAR | 20 | NOT NULL | - | - | - | 预警颜色：red-红色，orange-橙色，yellow-黄色，blue-蓝色 |
| severity | TINYINT | - | NOT NULL | - | - | INDEX | 严重程度：1-特别严重，2-严重，3-较重，4-一般 |
| response_org | VARCHAR | 255 | NULL | - | - | - | 响应组织要求 |
| response_time | INT | - | NULL | - | - | - | 响应时间要求（分钟） |
| description | VARCHAR | 255 | NULL | - | - | - | 级别描述 |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| sort_order | INT | - | NULL | 0 | - | - | 排序顺序 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_level_code` (`level_code`)
- KEY `idx_severity` (`severity`)
- KEY `idx_status` (`status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 3.3 预警规则表 (warning_rules)

**表名**: `warning_rules`  
**表说明**: 预警规则配置表，包括预警生成规则和预警处置规则

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 规则ID，主键 |
| rule_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 规则编码，唯一索引 |
| rule_name | VARCHAR | 100 | NOT NULL | - | - | - | 规则名称 |
| rule_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 规则类型：1-预警生成规则，2-预警处置规则 |
| industry_type | TINYINT | - | NOT NULL | - | - | INDEX | 行业类型：1-森林火灾，2-防汛，3-交通运输，4-危险化学品 |
| warning_level_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 预警级别ID，外键关联warning_levels表 |
| condition_config | TEXT | - | NOT NULL | - | - | - | 规则条件配置（JSON格式），包含报警频率、报警时长、报警设备等条件 |
| action_config | TEXT | - | NULL | - | - | - | 规则动作配置（JSON格式），包含响应时间、处置时间、反馈时间等要求 |
| response_time | INT | - | NULL | - | - | - | 响应时间要求（分钟，处置规则） |
| handle_time | INT | - | NULL | - | - | - | 处置时间要求（分钟，处置规则） |
| feedback_time | INT | - | NULL | - | - | - | 反馈时间要求（分钟，处置规则） |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| description | VARCHAR | 255 | NULL | - | - | - | 规则描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_rule_code` (`rule_code`)
- KEY `idx_rule_type` (`rule_type`)
- KEY `idx_industry_type` (`industry_type`)
- KEY `idx_warning_level_id` (`warning_level_id`)
- KEY `idx_status` (`status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 3.4 风险监测数据表 (risk_monitors)

**表名**: `risk_monitors`  
**表说明**: 风险监测数据表，存储实时监测、全域监测、重点监测的风险数据

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 监测数据ID，主键 |
| monitor_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 监测点编码，唯一索引 |
| monitor_name | VARCHAR | 100 | NOT NULL | - | - | - | 监测点名称 |
| monitor_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 监测类型：1-实时监测，2-全域监测，3-重点监测 |
| industry_type | TINYINT | - | NOT NULL | - | - | INDEX | 行业类型：1-森林火灾，2-防汛，3-交通运输，4-危险化学品 |
| data_source_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 数据源ID，外键关联data_sources表 |
| location | POINT | - | NULL | - | - | SPATIAL | 地理位置（空间数据类型） |
| longitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 经度 |
| latitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 纬度 |
| street | VARCHAR | 100 | NULL | - | - | INDEX | 所属街道 |
| address | VARCHAR | 255 | NULL | - | - | - | 详细地址 |
| monitor_value | DECIMAL(10,2) | - | NULL | - | - | - | 监测数值 |
| monitor_unit | VARCHAR | 20 | NULL | - | - | - | 监测单位 |
| threshold_min | DECIMAL(10,2) | - | NULL | - | - | - | 阈值下限 |
| threshold_max | DECIMAL(10,2) | - | NULL | - | - | - | 阈值上限 |
| online_status | TINYINT | - | NOT NULL | 1 | - | INDEX | 在线状态：0-离线，1-在线 |
| last_data_time | DATETIME | - | NULL | - | - | INDEX | 最后数据时间 |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| description | VARCHAR | 255 | NULL | - | - | - | 监测点描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_monitor_code` (`monitor_code`)
- KEY `idx_monitor_type` (`monitor_type`)
- KEY `idx_industry_type` (`industry_type`)
- KEY `idx_data_source_id` (`data_source_id`)
- KEY `idx_longitude` (`longitude`)
- KEY `idx_latitude` (`latitude`)
- KEY `idx_street` (`street`)
- KEY `idx_online_status` (`online_status`)
- KEY `idx_last_data_time` (`last_data_time`)
- KEY `idx_status` (`status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)
- SPATIAL KEY `idx_location` (`location`)

---

### 3.5 报警记录表 (alarm_records)

**表名**: `alarm_records`  
**表说明**: 报警记录表，存储各类报警信息

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 报警记录ID，主键 |
| alarm_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 报警编码，唯一索引 |
| monitor_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 监测点ID，外键关联risk_monitors表 |
| industry_type | TINYINT | - | NOT NULL | - | - | INDEX | 行业类型：1-森林火灾，2-防汛，3-交通运输，4-危险化学品 |
| alarm_type | VARCHAR | 50 | NOT NULL | - | - | INDEX | 报警类型 |
| alarm_value | DECIMAL(10,2) | - | NULL | - | - | - | 报警数值 |
| threshold_value | DECIMAL(10,2) | - | NULL | - | - | - | 阈值数值 |
| location | POINT | - | NULL | - | - | SPATIAL | 报警位置（空间数据类型） |
| longitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 经度 |
| latitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 纬度 |
| street | VARCHAR | 100 | NULL | - | - | INDEX | 所属街道 |
| address | VARCHAR | 255 | NULL | - | - | - | 详细地址 |
| alarm_time | DATETIME | - | NOT NULL | - | - | INDEX | 报警时间 |
| alarm_duration | INT | - | NULL | - | - | - | 报警持续时间（分钟） |
| alarm_status | TINYINT | - | NOT NULL | 0 | - | INDEX | 报警状态：0-未处理，1-处理中，2-已处理，3-已忽略 |
| handle_user_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 处理人ID，外键关联users表 |
| handle_time | DATETIME | - | NULL | - | - | - | 处理时间 |
| handle_result | TEXT | - | NULL | - | - | - | 处理结果 |
| feedback_time | DATETIME | - | NULL | - | - | - | 反馈时间 |
| description | VARCHAR | 255 | NULL | - | - | - | 报警描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_alarm_code` (`alarm_code`)
- KEY `idx_monitor_id` (`monitor_id`)
- KEY `idx_industry_type` (`industry_type`)
- KEY `idx_alarm_type` (`alarm_type`)
- KEY `idx_longitude` (`longitude`)
- KEY `idx_latitude` (`latitude`)
- KEY `idx_street` (`street`)
- KEY `idx_alarm_time` (`alarm_time`)
- KEY `idx_alarm_status` (`alarm_status`)
- KEY `idx_handle_user_id` (`handle_user_id`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)
- SPATIAL KEY `idx_location` (`location`)

---

### 3.6 风险预警表 (risk_warnings)

**表名**: `risk_warnings`  
**表说明**: 风险预警表，存储风险预警信息

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 预警ID，主键 |
| warning_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 预警编码，唯一索引 |
| warning_level_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 预警级别ID，外键关联warning_levels表 |
| warning_rule_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 预警规则ID，外键关联warning_rules表 |
| industry_type | TINYINT | - | NOT NULL | - | - | INDEX | 行业类型：1-森林火灾，2-防汛，3-交通运输，4-危险化学品 |
| warning_type | VARCHAR | 50 | NOT NULL | - | - | INDEX | 预警类型（如：火灾预警、泄漏预警等） |
| warning_analysis_type | TINYINT | - | NULL | - | - | INDEX | 预警分析类型：1-突出预警，2-同比预警，3-环比预警 |
| warning_title | VARCHAR | 200 | NOT NULL | - | - | - | 预警标题 |
| warning_content | TEXT | - | NOT NULL | - | - | - | 预警内容 |
| location | POINT | - | NULL | - | - | SPATIAL | 预警位置（空间数据类型） |
| longitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 经度 |
| latitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 纬度 |
| street | VARCHAR | 100 | NULL | - | - | INDEX | 所属街道 |
| address | VARCHAR | 255 | NULL | - | - | - | 详细地址 |
| warning_time | DATETIME | - | NOT NULL | - | - | INDEX | 预警时间 |
| warning_source | TINYINT | - | NOT NULL | 1 | - | INDEX | 预警来源：1-自动生成，2-手动创建 |
| warning_status | TINYINT | - | NOT NULL | 0 | - | INDEX | 预警状态：0-未发布，1-已发布，2-处理中，3-已处置，4-已关闭 |
| response_org_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 响应组织ID，外键关联organizations表 |
| response_user_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 响应人ID，外键关联users表 |
| response_time | DATETIME | - | NULL | - | - | - | 响应时间 |
| handle_time | DATETIME | - | NULL | - | - | - | 处置时间 |
| handle_result | TEXT | - | NULL | - | - | - | 处置结果 |
| feedback_time | DATETIME | - | NULL | - | - | - | 反馈时间 |
| publish_time | DATETIME | - | NULL | - | - | INDEX | 发布时间 |
| related_alarm_ids | TEXT | - | NULL | - | - | - | 关联报警记录ID（JSON数组） |
| related_plan_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 关联预案ID（预案主题库），外键关联emergency_plans表 |
| description | VARCHAR | 255 | NULL | - | - | - | 预警描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_warning_code` (`warning_code`)
- KEY `idx_warning_level_id` (`warning_level_id`)
- KEY `idx_warning_rule_id` (`warning_rule_id`)
- KEY `idx_industry_type` (`industry_type`)
- KEY `idx_warning_type` (`warning_type`)
- KEY `idx_warning_analysis_type` (`warning_analysis_type`)
- KEY `idx_longitude` (`longitude`)
- KEY `idx_latitude` (`latitude`)
- KEY `idx_street` (`street`)
- KEY `idx_warning_time` (`warning_time`)
- KEY `idx_warning_source` (`warning_source`)
- KEY `idx_warning_status` (`warning_status`)
- KEY `idx_response_org_id` (`response_org_id`)
- KEY `idx_response_user_id` (`response_user_id`)
- KEY `idx_publish_time` (`publish_time`)
- KEY `idx_related_plan_id` (`related_plan_id`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)
- SPATIAL KEY `idx_location` (`location`)

---

### 3.7 报警统计表 (alarm_statistics)

**表名**: `alarm_statistics`  
**表说明**: 报警统计表，按时间、空间、行业等维度统计报警数据

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 统计ID，主键 |
| stat_date | DATE | - | NOT NULL | - | - | INDEX | 统计日期 |
| stat_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 统计类型：1-日报，2-周报，3-月报，4-年报 |
| industry_type | TINYINT | - | NULL | - | - | INDEX | 行业类型：1-森林火灾，2-防汛，3-交通运输，4-危险化学品，NULL-全部 |
| street | VARCHAR | 100 | NULL | - | - | INDEX | 所属街道，NULL-全部 |
| alarm_count | INT | - | NOT NULL | 0 | - | - | 报警总数 |
| unhandled_count | INT | - | NOT NULL | 0 | - | - | 未处理数量 |
| handling_count | INT | - | NOT NULL | 0 | - | - | 处理中数量 |
| handled_count | INT | - | NOT NULL | 0 | - | - | 已处理数量 |
| ignored_count | INT | - | NOT NULL | 0 | - | - | 已忽略数量 |
| avg_handle_time | INT | - | NULL | - | - | - | 平均处理时间（分钟） |
| stat_data | TEXT | - | NULL | - | - | - | 详细统计数据（JSON格式） |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_stat_unique` (`stat_date`, `stat_type`, `industry_type`, `street`)
- KEY `idx_stat_date` (`stat_date`)
- KEY `idx_stat_type` (`stat_type`)
- KEY `idx_industry_type` (`industry_type`)
- KEY `idx_street` (`street`)
- KEY `idx_created_at` (`created_at`)

---

### 3.8 隐患排查表 (risk_hidden_dangers)

**表名**: `risk_hidden_dangers`  
**表说明**: 隐患排查表，存储重大风险隐患点的隐患排查信息

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 隐患ID，主键 |
| danger_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 隐患编码，唯一索引 |
| danger_name | VARCHAR | 200 | NOT NULL | - | - | - | 隐患名称 |
| monitor_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 监测点ID，外键关联risk_monitors表（重点监测类型） |
| organization_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 企业ID，外键关联organizations表 |
| industry_type | TINYINT | - | NOT NULL | 4 | - | INDEX | 行业类型：4-危险化学品 |
| location | POINT | - | NULL | - | - | SPATIAL | 隐患位置（空间数据类型） |
| longitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 经度 |
| latitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 纬度 |
| street | VARCHAR | 100 | NULL | - | - | INDEX | 所属街道 |
| address | VARCHAR | 255 | NULL | - | - | - | 详细地址 |
| danger_level | TINYINT | - | NOT NULL | 1 | - | INDEX | 隐患等级：1-重大，2-较大，3-一般 |
| danger_category | VARCHAR | 100 | NULL | - | - | INDEX | 隐患类别 |
| danger_description | TEXT | - | NOT NULL | - | - | - | 隐患描述 |
| discover_time | DATETIME | - | NOT NULL | - | - | INDEX | 发现时间 |
| discover_user_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 发现人ID，外键关联users表 |
| status | TINYINT | - | NOT NULL | 0 | - | INDEX | 状态：0-待整改，1-整改中，2-已完成，3-已关闭 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_danger_code` (`danger_code`)
- KEY `idx_monitor_id` (`monitor_id`)
- KEY `idx_organization_id` (`organization_id`)
- KEY `idx_industry_type` (`industry_type`)
- KEY `idx_longitude` (`longitude`)
- KEY `idx_latitude` (`latitude`)
- KEY `idx_street` (`street`)
- KEY `idx_danger_level` (`danger_level`)
- KEY `idx_danger_category` (`danger_category`)
- KEY `idx_discover_time` (`discover_time`)
- KEY `idx_discover_user_id` (`discover_user_id`)
- KEY `idx_status` (`status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)
- SPATIAL KEY `idx_location` (`location`)

---

### 3.9 隐患整改表 (risk_rectifications)

**表名**: `risk_rectifications`  
**表说明**: 隐患整改表，存储隐患整改信息

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 整改ID，主键 |
| rectification_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 整改编码，唯一索引 |
| danger_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 隐患ID，外键关联risk_hidden_dangers表 |
| rectification_plan | TEXT | - | NOT NULL | - | - | - | 整改方案 |
| rectification_measures | TEXT | - | NOT NULL | - | - | - | 整改措施 |
| responsible_user_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 责任人ID，外键关联users表 |
| responsible_org_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 责任组织ID，外键关联organizations表 |
| plan_start_time | DATETIME | - | NOT NULL | - | - | INDEX | 计划开始时间 |
| plan_end_time | DATETIME | - | NOT NULL | - | - | INDEX | 计划完成时间 |
| actual_start_time | DATETIME | - | NULL | - | - | - | 实际开始时间 |
| actual_end_time | DATETIME | - | NULL | - | - | INDEX | 实际完成时间 |
| rectification_status | TINYINT | - | NOT NULL | 0 | - | INDEX | 整改状态：0-待开始，1-进行中，2-已完成，3-已延期 |
| rectification_result | TEXT | - | NULL | - | - | - | 整改结果 |
| verification_status | TINYINT | - | NOT NULL | 0 | - | INDEX | 验收状态：0-待验收，1-验收通过，2-验收不通过 |
| verification_time | DATETIME | - | NULL | - | - | - | 验收时间 |
| verification_user_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 验收人ID，外键关联users表 |
| verification_opinion | TEXT | - | NULL | - | - | - | 验收意见 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_rectification_code` (`rectification_code`)
- KEY `idx_danger_id` (`danger_id`)
- KEY `idx_responsible_user_id` (`responsible_user_id`)
- KEY `idx_responsible_org_id` (`responsible_org_id`)
- KEY `idx_plan_start_time` (`plan_start_time`)
- KEY `idx_plan_end_time` (`plan_end_time`)
- KEY `idx_actual_end_time` (`actual_end_time`)
- KEY `idx_rectification_status` (`rectification_status`)
- KEY `idx_verification_status` (`verification_status`)
- KEY `idx_verification_user_id` (`verification_user_id`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

**说明**: 以上为风险监测预警相关表（4.1.1）的详细设计，请确认后继续设计其他部分。

---

## 4. 简报相关表设计（4.1.2）

### 4.1 简报相关表设计说明

#### 4.1.1 简报模板管理
- 支持两种模板类型：常态化运行报告模板和非常态化突发预警简报模板
- 常态化模板支持按时间维度（日、周、月、年）配置
- 非常态化模板支持按预警类型、预警级别配置
- 模板内容支持变量占位符，通过 `variables` 字段说明可用变量
- 通过 `data_config` 字段定义需要统计的数据项

#### 4.1.2 简报策略管理
- 支持两种策略类型：常态化策略和非常态化策略
- 常态化策略：支持定时触发，可配置日报、周报、月报、年报
- 非常态化策略：支持事件触发，可配置预警类型、预警级别等触发条件
- 支持多种推送目标：指定用户、指定角色、指定组织
- 支持多种推送渠道：系统消息、短信、邮件

#### 4.1.3 简报数据生成
- 简报数据根据模板和策略自动生成
- 支持多维度数据统计：行业维度、区域维度、时间维度
- 简报内容包含数据摘要、报警次数、预警次数、风险隐患数量等
- 支持生成PDF附件

#### 4.1.4 简报推送管理
- 记录每次推送的详细信息
- 支持多种推送渠道，可同时通过多个渠道推送
- 跟踪推送状态和阅读状态
- 记录推送失败的错误信息，便于排查问题

---

### 4.2 简报模板表 (brief_templates)

**表名**: `brief_templates`  
**表说明**: 简报模板表，存储常态化运行报告模板和非常态化突发预警简报模板

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 模板ID，主键 |
| template_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 模板编码，唯一索引 |
| template_name | VARCHAR | 100 | NOT NULL | - | - | - | 模板名称 |
| template_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 模板类型：1-常态化运行报告，2-非常态化突发预警简报 |
| industry_type | TINYINT | - | NULL | - | - | INDEX | 行业类型：1-森林火灾，2-防汛，3-交通运输，4-危险化学品，NULL-全部 |
| time_dimension | VARCHAR | 20 | NULL | - | - | INDEX | 时间维度：day-日，week-周，month-月，year-年（常态化模板） |
| region_dimension | VARCHAR | 50 | NULL | - | - | - | 区域维度配置（JSON格式） |
| industry_dimension | VARCHAR | 50 | NULL | - | - | - | 行业维度配置（JSON格式） |
| template_content | TEXT | - | NOT NULL | - | - | - | 模板内容，支持变量占位符 |
| variables | TEXT | - | NULL | - | - | - | 变量说明（JSON格式） |
| data_config | TEXT | - | NULL | - | - | - | 数据配置（JSON格式），定义需要统计的数据项 |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| description | VARCHAR | 255 | NULL | - | - | - | 模板描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_template_code` (`template_code`)
- KEY `idx_template_type` (`template_type`)
- KEY `idx_industry_type` (`industry_type`)
- KEY `idx_time_dimension` (`time_dimension`)
- KEY `idx_status` (`status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 4.3 简报策略表 (brief_strategies)

**表名**: `brief_strategies`  
**表说明**: 简报策略表，定义简报自动生成策略

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 策略ID，主键 |
| strategy_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 策略编码，唯一索引 |
| strategy_name | VARCHAR | 100 | NOT NULL | - | - | - | 策略名称 |
| template_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 模板ID，外键关联brief_templates表 |
| strategy_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 策略类型：1-常态化策略，2-非常态化策略 |
| report_type | VARCHAR | 20 | NULL | - | - | INDEX | 报告类型：daily-日报，weekly-周报，monthly-月报，yearly-年报（常态化策略） |
| trigger_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 触发类型：1-定时触发，2-事件触发（非常态化策略） |
| trigger_config | TEXT | - | NULL | - | - | - | 触发配置（JSON格式），包含触发时间、触发条件等 |
| warning_type_filter | VARCHAR | 100 | NULL | - | - | - | 预警类型过滤（非常态化策略，JSON数组） |
| warning_level_filter | VARCHAR | 50 | NULL | - | - | - | 预警级别过滤（非常态化策略，JSON数组） |
| industry_filter | VARCHAR | 50 | NULL | - | - | - | 行业过滤（JSON数组） |
| region_filter | VARCHAR | 255 | NULL | - | - | - | 区域过滤（JSON数组） |
| push_target_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 推送目标类型：1-指定用户，2-指定角色，3-指定组织 |
| push_target_ids | TEXT | - | NULL | - | - | - | 推送目标ID列表（JSON数组） |
| push_channel | VARCHAR | 50 | NULL | - | - | - | 推送渠道（JSON数组）：system-系统消息，sms-短信，email-邮件 |
| message_template_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 消息模板ID，外键关联message_templates表 |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| last_execute_at | DATETIME | - | NULL | - | - | INDEX | 最后执行时间 |
| next_execute_at | DATETIME | - | NULL | - | - | INDEX | 下次执行时间 |
| description | VARCHAR | 255 | NULL | - | - | - | 策略描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_strategy_code` (`strategy_code`)
- KEY `idx_template_id` (`template_id`)
- KEY `idx_strategy_type` (`strategy_type`)
- KEY `idx_report_type` (`report_type`)
- KEY `idx_trigger_type` (`trigger_type`)
- KEY `idx_push_target_type` (`push_target_type`)
- KEY `idx_message_template_id` (`message_template_id`)
- KEY `idx_status` (`status`)
- KEY `idx_last_execute_at` (`last_execute_at`)
- KEY `idx_next_execute_at` (`next_execute_at`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 4.4 简报数据表 (brief_data)

**表名**: `brief_data`  
**表说明**: 简报数据表，存储生成的简报数据

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 简报ID，主键 |
| brief_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 简报编码，唯一索引 |
| template_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 模板ID，外键关联brief_templates表 |
| strategy_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 策略ID，外键关联brief_strategies表 |
| brief_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 简报类型：1-常态化运行报告，2-非常态化突发预警简报 |
| report_type | VARCHAR | 20 | NULL | - | - | INDEX | 报告类型：daily-日报，weekly-周报，monthly-月报，yearly-年报 |
| report_date | DATE | - | NOT NULL | - | - | INDEX | 报告日期 |
| report_period_start | DATETIME | - | NULL | - | - | INDEX | 报告周期开始时间 |
| report_period_end | DATETIME | - | NULL | - | - | INDEX | 报告周期结束时间 |
| brief_title | VARCHAR | 200 | NOT NULL | - | - | - | 简报标题 |
| brief_content | TEXT | - | NOT NULL | - | - | - | 简报内容 |
| data_summary | TEXT | - | NULL | - | - | - | 数据摘要（JSON格式） |
| alarm_count | INT | - | NULL | 0 | - | - | 报警次数 |
| warning_count | INT | - | NULL | 0 | - | - | 预警次数 |
| risk_count | INT | - | NULL | 0 | - | - | 风险隐患数量 |
| industry_data | TEXT | - | NULL | - | - | - | 行业维度数据（JSON格式） |
| region_data | TEXT | - | NULL | - | - | - | 区域维度数据（JSON格式） |
| time_data | TEXT | - | NULL | - | - | - | 时间维度数据（JSON格式） |
| attachment_url | VARCHAR | 500 | NULL | - | - | - | 附件URL（如PDF文件） |
| status | TINYINT | - | NOT NULL | 0 | - | INDEX | 状态：0-未推送，1-已推送，2-已查看 |
| generate_user_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 生成人ID，外键关联users表 |
| generate_time | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 生成时间 |
| description | VARCHAR | 255 | NULL | - | - | - | 简报描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_brief_code` (`brief_code`)
- KEY `idx_template_id` (`template_id`)
- KEY `idx_strategy_id` (`strategy_id`)
- KEY `idx_brief_type` (`brief_type`)
- KEY `idx_report_type` (`report_type`)
- KEY `idx_report_date` (`report_date`)
- KEY `idx_report_period_start` (`report_period_start`)
- KEY `idx_report_period_end` (`report_period_end`)
- KEY `idx_status` (`status`)
- KEY `idx_generate_user_id` (`generate_user_id`)
- KEY `idx_generate_time` (`generate_time`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 4.5 简报推送记录表 (brief_pushes)

**表名**: `brief_pushes`  
**表说明**: 简报推送记录表，记录简报的推送情况

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 推送记录ID，主键 |
| brief_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 简报ID，外键关联brief_data表 |
| push_target_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 推送目标类型：1-用户，2-角色，3-组织 |
| target_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 目标ID（用户ID、角色ID或组织ID） |
| push_channel | VARCHAR | 20 | NOT NULL | - | - | INDEX | 推送渠道：system-系统消息，sms-短信，email-邮件 |
| push_status | TINYINT | - | NOT NULL | 0 | - | INDEX | 推送状态：0-待推送，1-推送中，2-推送成功，3-推送失败 |
| push_time | DATETIME | - | NULL | - | - | INDEX | 推送时间 |
| read_status | TINYINT | - | NOT NULL | 0 | - | INDEX | 阅读状态：0-未读，1-已读 |
| read_time | DATETIME | - | NULL | - | - | - | 阅读时间 |
| error_message | VARCHAR | 500 | NULL | - | - | - | 错误信息（推送失败时） |
| message_id | VARCHAR | 100 | NULL | - | - | INDEX | 消息ID（系统消息或短信平台返回的ID） |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |

**索引设计**:
- PRIMARY KEY (`id`)
- KEY `idx_brief_id` (`brief_id`)
- KEY `idx_push_target_type` (`push_target_type`)
- KEY `idx_target_id` (`target_id`)
- KEY `idx_push_channel` (`push_channel`)
- KEY `idx_push_status` (`push_status`)
- KEY `idx_push_time` (`push_time`)
- KEY `idx_read_status` (`read_status`)
- KEY `idx_message_id` (`message_id`)
- KEY `idx_created_at` (`created_at`)

---

**说明**: 以上为简报相关表（4.1.2）的详细设计，请确认后继续设计其他部分。

---

## 5. 叫应相关表设计（4.1.3）

### 5.1 叫应相关表设计说明

#### 5.1.1 常态化叫应
- **叫应对象管理**：管理政府部门、企业事业单位等叫应对象
- **政策文件管理**：支持政策文件上传、发布
- **政策文件下发**：记录政策文件的下发情况，支持反馈跟踪和督办
- **叫应记录**：记录通过系统消息、短信等方式的叫应情况

#### 5.1.2 非常态化叫应
- **叫应人员管理**：管理应急叫应人员，支持按职级、事件级别分组
- **叫应分组管理**：对叫应人员进行分组，便于批量叫应
- **一键叫应**：支持一键叫应相关责任人，通过智能外呼系统实现
- **叫应结果反馈**：记录叫应的发送、接收、响应情况

#### 5.1.3 叫应流程
- **常态化叫应流程**：政策文件上传 → 政策文件下发 → 叫应通知 → 反馈跟踪 → 督办提醒
- **非常态化叫应流程**：预警触发/一键叫应 → 选择叫应人员/分组 → 发送叫应 → 接收确认 → 响应反馈
- **容错机制**：支持多次重试，记录发送失败的错误信息

#### 5.1.4 叫应统计
- 通过叫应记录表可以统计：被叫应总数、已叫应总数、未叫应总数
- 支持按时间、渠道、状态等维度统计
- 支持叫应明细查看

---

### 5.2 叫应分组表 (call_groups)

**表名**: `call_groups`  
**表说明**: 叫应分组表，用于对叫应人员进行分组管理

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 分组ID，主键 |
| group_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 分组编码，唯一索引 |
| group_name | VARCHAR | 100 | NOT NULL | - | - | - | 分组名称 |
| group_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 分组类型：1-常态化分组，2-非常态化分组 |
| event_level | TINYINT | - | NULL | - | - | INDEX | 负责应急事件级别：1-红色I级，2-橙色Ⅱ级，3-黄色Ⅲ级，4-蓝色Ⅳ级（非常态化分组） |
| description | VARCHAR | 255 | NULL | - | - | - | 分组描述 |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| sort_order | INT | - | NULL | 0 | - | - | 排序顺序 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_group_code` (`group_code`)
- KEY `idx_group_type` (`group_type`)
- KEY `idx_event_level` (`event_level`)
- KEY `idx_status` (`status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 5.3 叫应对象表 (call_targets)

**表名**: `call_targets`  
**表说明**: 叫应对象表，存储常态化叫应的对象信息（政府部门、企业事业单位）

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 叫应对象ID，主键 |
| target_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 对象编码，唯一索引 |
| target_name | VARCHAR | 100 | NOT NULL | - | - | - | 对象名称 |
| target_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 对象类型：1-政府部门，2-企业单位，3-事业单位 |
| organization_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 所属组织ID，外键关联organizations表 |
| enterprise_name | VARCHAR | 200 | NULL | - | - | - | 企业名称（企业单位） |
| enterprise_info | TEXT | - | NULL | - | - | - | 企业信息（企业单位） |
| safety_person | VARCHAR | 50 | NOT NULL | - | - | - | 安全责任人 |
| contact_phone | VARCHAR | 20 | NOT NULL | - | - | INDEX | 联系电话 |
| contact_address | VARCHAR | 255 | NULL | - | - | - | 联系地址 |
| description | VARCHAR | 255 | NULL | - | - | - | 对象描述 |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_target_code` (`target_code`)
- KEY `idx_target_type` (`target_type`)
- KEY `idx_organization_id` (`organization_id`)
- KEY `idx_contact_phone` (`contact_phone`)
- KEY `idx_status` (`status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 5.4 叫应人员表 (call_persons)

**表名**: `call_persons`  
**表说明**: 叫应人员表，存储非常态化叫应的人员信息

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 叫应人员ID，主键 |
| person_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 人员编码，唯一索引 |
| person_name | VARCHAR | 50 | NOT NULL | - | - | - | 人员姓名 |
| group_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 所属分组ID，外键关联call_groups表 |
| rank | VARCHAR | 50 | NULL | - | - | INDEX | 职级 |
| mobile_phone | VARCHAR | 20 | NOT NULL | - | - | INDEX | 手机号码 |
| office_phone | VARCHAR | 20 | NULL | - | - | - | 办公电话 |
| contact_address | VARCHAR | 255 | NULL | - | - | - | 通讯地址 |
| event_level | TINYINT | - | NULL | - | - | INDEX | 负责应急事件级别：1-红色I级，2-橙色Ⅱ级，3-黄色Ⅲ级，4-蓝色Ⅳ级 |
| organization_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 所属组织ID，外键关联organizations表 |
| description | VARCHAR | 255 | NULL | - | - | - | 人员描述 |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_person_code` (`person_code`)
- KEY `idx_group_id` (`group_id`)
- KEY `idx_rank` (`rank`)
- KEY `idx_mobile_phone` (`mobile_phone`)
- KEY `idx_event_level` (`event_level`)
- KEY `idx_organization_id` (`organization_id`)
- KEY `idx_status` (`status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 5.5 政策文件表 (policy_files)

**表名**: `policy_files`  
**表说明**: 政策文件表，存储上传的政策文件信息

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 文件ID，主键 |
| file_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 文件编码，唯一索引 |
| file_name | VARCHAR | 200 | NOT NULL | - | - | - | 文件名称 |
| file_path | VARCHAR | 500 | NOT NULL | - | - | - | 文件存储路径 |
| file_size | BIGINT | - | NULL | - | - | - | 文件大小（字节） |
| file_type | VARCHAR | 50 | NULL | - | - | INDEX | 文件类型 |
| file_ext | VARCHAR | 10 | NULL | - | - | - | 文件扩展名 |
| policy_title | VARCHAR | 200 | NOT NULL | - | - | - | 政策标题 |
| policy_content | TEXT | - | NULL | - | - | - | 政策内容（文本提取） |
| policy_requirement | TEXT | - | NULL | - | - | - | 政策要求 |
| upload_user_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 上传人ID，外键关联users表 |
| upload_time | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 上传时间 |
| publish_status | TINYINT | - | NOT NULL | 0 | - | INDEX | 发布状态：0-未发布，1-已发布 |
| publish_time | DATETIME | - | NULL | - | - | INDEX | 发布时间 |
| description | VARCHAR | 255 | NULL | - | - | - | 文件描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_file_code` (`file_code`)
- KEY `idx_file_type` (`file_type`)
- KEY `idx_upload_user_id` (`upload_user_id`)
- KEY `idx_upload_time` (`upload_time`)
- KEY `idx_publish_status` (`publish_status`)
- KEY `idx_publish_time` (`publish_time`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 5.6 政策文件下发表 (policy_distributions)

**表名**: `policy_distributions`  
**表说明**: 政策文件下发表，记录政策文件的下发情况

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 下发记录ID，主键 |
| distribution_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 下发编码，唯一索引 |
| policy_file_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 政策文件ID，外键关联policy_files表 |
| target_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 叫应对象ID，外键关联call_targets表 |
| feedback_content | TEXT | - | NULL | - | - | - | 反馈内容要求 |
| feedback_deadline | DATETIME | - | NOT NULL | - | - | INDEX | 反馈截止时间 |
| distribution_time | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 下发时间 |
| distribution_user_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 下发人ID，外键关联users表 |
| feedback_status | TINYINT | - | NOT NULL | 0 | - | INDEX | 反馈状态：0-未反馈，1-已反馈，2-超时未反馈 |
| feedback_time | DATETIME | - | NULL | - | - | - | 反馈时间 |
| feedback_content_actual | TEXT | - | NULL | - | - | - | 实际反馈内容 |
| supervise_status | TINYINT | - | NOT NULL | 0 | - | INDEX | 督办状态：0-无需督办，1-待督办，2-已督办 |
| supervise_time | DATETIME | - | NULL | - | - | - | 督办时间 |
| supervise_user_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 督办人ID，外键关联users表 |
| description | VARCHAR | 255 | NULL | - | - | - | 下发描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_distribution_code` (`distribution_code`)
- KEY `idx_policy_file_id` (`policy_file_id`)
- KEY `idx_target_id` (`target_id`)
- KEY `idx_feedback_deadline` (`feedback_deadline`)
- KEY `idx_distribution_time` (`distribution_time`)
- KEY `idx_distribution_user_id` (`distribution_user_id`)
- KEY `idx_feedback_status` (`feedback_status`)
- KEY `idx_supervise_status` (`supervise_status`)
- KEY `idx_supervise_user_id` (`supervise_user_id`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 5.7 叫应记录表 (call_records)

**表名**: `call_records`  
**表说明**: 叫应记录表，记录常态化叫应和非常态化叫应的详细信息

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 叫应记录ID，主键 |
| call_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 叫应编码，唯一索引 |
| call_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 叫应类型：1-常态化叫应，2-非常态化叫应 |
| call_source | TINYINT | - | NOT NULL | 1 | - | INDEX | 叫应来源：1-政策文件下发，2-一键叫应，3-预警触发 |
| policy_distribution_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 政策文件下发ID，外键关联policy_distributions表（常态化叫应） |
| warning_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 预警ID，外键关联risk_warnings表（预警触发） |
| target_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 叫应对象ID，外键关联call_targets表（常态化叫应） |
| person_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 叫应人员ID，外键关联call_persons表（非常态化叫应） |
| group_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 叫应分组ID，外键关联call_groups表（非常态化叫应） |
| call_channel | VARCHAR | 20 | NOT NULL | - | - | INDEX | 叫应渠道：system-系统消息，sms-短信，phone-电话 |
| call_content | TEXT | - | NOT NULL | - | - | - | 叫应内容 |
| call_time | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 叫应时间 |
| call_status | TINYINT | - | NOT NULL | 0 | - | INDEX | 叫应状态：0-待发送，1-发送中，2-发送成功，3-发送失败 |
| receive_status | TINYINT | - | NOT NULL | 0 | - | INDEX | 接收状态：0-未接收，1-已接收，2-未响应 |
| receive_time | DATETIME | - | NULL | - | - | INDEX | 接收时间 |
| response_status | TINYINT | - | NOT NULL | 0 | - | INDEX | 响应状态：0-未响应，1-已响应 |
| response_time | DATETIME | - | NULL | - | - | - | 响应时间 |
| response_content | TEXT | - | NULL | - | - | - | 响应内容 |
| retry_count | INT | - | NOT NULL | 0 | - | - | 重试次数 |
| last_retry_time | DATETIME | - | NULL | - | - | - | 最后重试时间 |
| error_message | VARCHAR | 500 | NULL | - | - | - | 错误信息（发送失败时） |
| external_call_id | VARCHAR | 100 | NULL | - | - | INDEX | 外部叫应ID（智能外呼系统返回的ID） |
| description | VARCHAR | 255 | NULL | - | - | - | 叫应描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_call_code` (`call_code`)
- KEY `idx_call_type` (`call_type`)
- KEY `idx_call_source` (`call_source`)
- KEY `idx_policy_distribution_id` (`policy_distribution_id`)
- KEY `idx_warning_id` (`warning_id`)
- KEY `idx_target_id` (`target_id`)
- KEY `idx_person_id` (`person_id`)
- KEY `idx_group_id` (`group_id`)
- KEY `idx_call_channel` (`call_channel`)
- KEY `idx_call_time` (`call_time`)
- KEY `idx_call_status` (`call_status`)
- KEY `idx_receive_status` (`receive_status`)
- KEY `idx_receive_time` (`receive_time`)
- KEY `idx_response_status` (`response_status`)
- KEY `idx_external_call_id` (`external_call_id`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

**说明**: 以上为叫应相关表（4.1.3）的详细设计，请确认后继续设计其他部分。

---

## 6. 预案相关表设计（4.1.4）

### 6.1 预案相关表设计说明

#### 6.1.1 预案结构化
- 支持三种预案类型：综合应急预案、专项应急预案、现场处置方案
- 预案支持文本识别，自动识别预案节点索引
- 预案结构支持树形结构，形成各个章节和条款
- 支持预案重点信息的快速检索

#### 6.1.2 预案数字化
- 预案流程数字化，按照树状流程图的形式呈现
- 支持预案流程的分解和编辑
- 实现跨部门、跨区域的协同工作

#### 6.1.3 任务流程化
- 建立预案与应急组织、角色、流程的关联关系
- 预案任务可自动下发至应急人员
- 支持任务接受和执行反馈跟踪
- 实现预案任务具体到人，落实到位

#### 6.1.4 预案统计分析
- 支持查看全区预案统计情况
- 支持查看各部门相关预案统计情况
- 按年度展现每月各类型预案的增长情况

---

### 6.2 应急预案表 (emergency_plans)

**表名**: `emergency_plans`  
**表说明**: 应急预案表，存储应急预案基本信息

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 预案ID，主键 |
| plan_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 预案编码，唯一索引 |
| plan_name | VARCHAR | 200 | NOT NULL | - | - | - | 预案名称 |
| plan_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 预案类型：1-综合应急预案，2-专项应急预案，3-现场处置方案 |
| industry_type | TINYINT | - | NULL | - | - | INDEX | 行业类型：1-森林火灾，2-防汛，3-交通运输，4-危险化学品 |
| organization_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 所属部门ID，外键关联organizations表 |
| version | VARCHAR | 20 | NOT NULL | 1.0 | - | - | 预案版本号 |
| plan_file_path | VARCHAR | 500 | NULL | - | - | - | 预案文件路径（原始文档） |
| plan_file_name | VARCHAR | 200 | NULL | - | - | - | 预案文件名称 |
| plan_summary | TEXT | - | NULL | - | - | - | 预案摘要 |
| plan_status | TINYINT | - | NOT NULL | 0 | - | INDEX | 预案状态：0-草稿，1-已发布，2-已修订，3-已废止 |
| publish_time | DATETIME | - | NULL | - | - | INDEX | 发布时间 |
| effective_time | DATETIME | - | NULL | - | - | - | 生效时间 |
| expire_time | DATETIME | - | NULL | - | - | - | 失效时间 |
| revision_reason | TEXT | - | NULL | - | - | - | 修订原因 |
| create_user_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 创建人ID，外键关联users表 |
| approve_user_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 审批人ID，外键关联users表 |
| approve_time | DATETIME | - | NULL | - | - | - | 审批时间 |
| description | VARCHAR | 255 | NULL | - | - | - | 预案描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_plan_code` (`plan_code`)
- KEY `idx_plan_type` (`plan_type`)
- KEY `idx_industry_type` (`industry_type`)
- KEY `idx_organization_id` (`organization_id`)
- KEY `idx_plan_status` (`plan_status`)
- KEY `idx_publish_time` (`publish_time`)
- KEY `idx_create_user_id` (`create_user_id`)
- KEY `idx_approve_user_id` (`approve_user_id`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 6.3 预案结构表 (plan_structures)

**表名**: `plan_structures`  
**表说明**: 预案结构表，存储预案的结构化信息（章节和条款）

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 结构节点ID，主键 |
| plan_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 预案ID，外键关联emergency_plans表 |
| node_code | VARCHAR | 50 | NOT NULL | - | - | - | 节点编码 |
| node_name | VARCHAR | 200 | NOT NULL | - | - | - | 节点名称 |
| parent_id | BIGINT UNSIGNED | - | NULL | 0 | - | INDEX | 父节点ID，0表示顶级节点 |
| node_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 节点类型：1-章节，2-条款，3-子条款 |
| node_level | INT | - | NOT NULL | 1 | - | - | 节点层级 |
| node_content | TEXT | - | NULL | - | - | - | 节点内容（文本） |
| node_index | INT | - | NULL | 0 | - | - | 节点索引（用于排序） |
| is_key_info | TINYINT | - | NOT NULL | 0 | - | INDEX | 是否重点信息：0-否，1-是 |
| description | VARCHAR | 255 | NULL | - | - | - | 节点描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_plan_node` (`plan_id`, `node_code`)
- KEY `idx_plan_id` (`plan_id`)
- KEY `idx_parent_id` (`parent_id`)
- KEY `idx_node_type` (`node_type`)
- KEY `idx_is_key_info` (`is_key_info`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 6.4 预案流程表 (plan_flows)

**表名**: `plan_flows`  
**表说明**: 预案流程表，存储预案的数字化流程信息

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 流程ID，主键 |
| plan_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 预案ID，外键关联emergency_plans表 |
| flow_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 流程编码，唯一索引 |
| flow_name | VARCHAR | 200 | NOT NULL | - | - | - | 流程名称 |
| parent_id | BIGINT UNSIGNED | - | NULL | 0 | - | INDEX | 父流程ID，0表示顶级流程 |
| flow_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 流程类型：1-主流程，2-子流程，3-任务节点 |
| flow_level | INT | - | NOT NULL | 1 | - | - | 流程层级 |
| flow_config | TEXT | - | NULL | - | - | - | 流程配置（JSON格式），包含流程节点、连线等信息 |
| next_flow_ids | TEXT | - | NULL | - | - | - | 下一流程ID列表（JSON数组） |
| condition_config | TEXT | - | NULL | - | - | - | 条件配置（JSON格式），定义流程执行条件 |
| sort_order | INT | - | NULL | 0 | - | - | 排序顺序 |
| description | VARCHAR | 255 | NULL | - | - | - | 流程描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_flow_code` (`flow_code`)
- KEY `idx_plan_id` (`plan_id`)
- KEY `idx_parent_id` (`parent_id`)
- KEY `idx_flow_type` (`flow_type`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 6.5 预案任务表 (plan_tasks)

**表名**: `plan_tasks`  
**表说明**: 预案任务表，存储预案的任务配置信息

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 任务ID，主键 |
| plan_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 预案ID，外键关联emergency_plans表 |
| flow_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 关联流程ID，外键关联plan_flows表 |
| task_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 任务编码，唯一索引 |
| task_name | VARCHAR | 200 | NOT NULL | - | - | - | 任务名称 |
| task_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 任务类型：1-信息收集，2-决策指挥，3-资源调配，4-现场处置，5-其他 |
| organization_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 负责组织ID，外键关联organizations表 |
| assign_user_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 指定执行人ID，外键关联users表 |
| assign_role_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 指定角色ID，外键关联roles表 |
| task_description | TEXT | - | NULL | - | - | - | 任务描述 |
| task_requirement | TEXT | - | NULL | - | - | - | 任务要求 |
| estimated_time | INT | - | NULL | - | - | - | 预计完成时间（分钟） |
| priority | TINYINT | - | NOT NULL | 3 | - | INDEX | 优先级：1-高，2-中，3-低 |
| sort_order | INT | - | NULL | 0 | - | - | 排序顺序 |
| description | VARCHAR | 255 | NULL | - | - | - | 任务描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_task_code` (`task_code`)
- KEY `idx_plan_id` (`plan_id`)
- KEY `idx_flow_id` (`flow_id`)
- KEY `idx_task_type` (`task_type`)
- KEY `idx_organization_id` (`organization_id`)
- KEY `idx_assign_user_id` (`assign_user_id`)
- KEY `idx_assign_role_id` (`assign_role_id`)
- KEY `idx_priority` (`priority`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 6.6 预案执行记录表 (plan_executions)

**表名**: `plan_executions`  
**表说明**: 预案执行记录表，记录预案的执行情况

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 执行记录ID，主键 |
| execution_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 执行编码，唯一索引 |
| plan_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 预案ID，外键关联emergency_plans表 |
| warning_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 关联预警ID，外键关联risk_warnings表 |
| execution_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 执行类型：1-演练执行，2-实战执行 |
| execution_status | TINYINT | - | NOT NULL | 0 | - | INDEX | 执行状态：0-未开始，1-执行中，2-已完成，3-已终止 |
| start_time | DATETIME | - | NULL | - | - | INDEX | 开始时间 |
| end_time | DATETIME | - | NULL | - | - | INDEX | 结束时间 |
| duration | INT | - | NULL | - | - | - | 执行时长（分钟） |
| command_user_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 指挥人ID，外键关联users表 |
| current_flow_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 当前流程ID，外键关联plan_flows表 |
| execution_result | TEXT | - | NULL | - | - | - | 执行结果 |
| execution_summary | TEXT | - | NULL | - | - | - | 执行总结 |
| description | VARCHAR | 255 | NULL | - | - | - | 执行描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_execution_code` (`execution_code`)
- KEY `idx_plan_id` (`plan_id`)
- KEY `idx_warning_id` (`warning_id`)
- KEY `idx_execution_type` (`execution_type`)
- KEY `idx_execution_status` (`execution_status`)
- KEY `idx_start_time` (`start_time`)
- KEY `idx_end_time` (`end_time`)
- KEY `idx_command_user_id` (`command_user_id`)
- KEY `idx_current_flow_id` (`current_flow_id`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 6.7 预案任务执行记录表 (plan_task_executions)

**表名**: `plan_task_executions`  
**表说明**: 预案任务执行记录表，记录预案任务的执行情况

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 任务执行记录ID，主键 |
| execution_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 预案执行记录ID，外键关联plan_executions表 |
| task_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 任务ID，外键关联plan_tasks表 |
| assign_user_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 执行人ID，外键关联users表 |
| task_status | TINYINT | - | NOT NULL | 0 | - | INDEX | 任务状态：0-待执行，1-执行中，2-已完成，3-已取消 |
| assign_time | DATETIME | - | NULL | - | - | INDEX | 分配时间 |
| accept_time | DATETIME | - | NULL | - | - | - | 接受时间 |
| start_time | DATETIME | - | NULL | - | - | INDEX | 开始时间 |
| end_time | DATETIME | - | NULL | - | - | INDEX | 结束时间 |
| duration | INT | - | NULL | - | - | - | 执行时长（分钟） |
| task_result | TEXT | - | NULL | - | - | - | 任务结果 |
| feedback_content | TEXT | - | NULL | - | - | - | 反馈内容 |
| feedback_time | DATETIME | - | NULL | - | - | - | 反馈时间 |
| description | VARCHAR | 255 | NULL | - | - | - | 执行描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- KEY `idx_execution_id` (`execution_id`)
- KEY `idx_task_id` (`task_id`)
- KEY `idx_assign_user_id` (`assign_user_id`)
- KEY `idx_task_status` (`task_status`)
- KEY `idx_assign_time` (`assign_time`)
- KEY `idx_start_time` (`start_time`)
- KEY `idx_end_time` (`end_time`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

**说明**: 以上为预案相关表（4.1.4）的详细设计，请确认后继续设计其他部分。

---

## 7. 安全资源相关表设计（4.1.5）

### 7.1 安全资源相关表设计说明

#### 7.1.1 安全运行一张图
- **安全基础数据信息展示**：在电子地图上展示危险源（重大危险源、一般危险源）、防护目标、物资装备、救援队伍等基础数据，直观地展现资源分布情况，并可根据风险位置进行资源分析
- **辖区基础情况展示**：展示辖区内行政区划及危险化学品、森林火灾、交通运输、防汛领域监测对象等基础信息
- **救援队伍**：对危化品、消防、应急抢险、医疗及社会救援等队伍类型进行分类统计
- **应急专家**：对行业专家、救援专家、技术专家进行分类统计
- **物资装备**：对个人防护、抢险救援等救援装备及食品、药品、饮用水、人员庇护等救灾物资进行分类统计
- **防护目标**：对学校、居民区等人员密集场所进行分类统计
- **避难场所**：对公园、广场、体育场等进行分类统计，汇总容纳能力

#### 7.1.2 安全态势一张图
- **行业态势展示**：对危险化学品、防汛、交通运输、森林防火行业安全态势数据进行分析和综合展示
- **区域态势展示**：基于辖区内的街道，对安全态势数据进行分析和综合展示
- **四色图渲染**：根据风险评估结果对区域进行四色图渲染

#### 7.1.3 监测预警一张图
- **监测数据信息展示**：展示实时监测数据，进行分类统计、在线情况统计
- **预警数据信息展示**：分级展示安全预警信息
- **预警事件信息展示**：基于GIS地图实时展示风险预警信息，展示预警附近监测点数量、危险源数量、应急资源等信息分布
- **视频监控设施展示**：根据事发地定位或指定位置，自动标示出一定范围内的所有视频监控设施的位置，方便最佳位置选择

---

### 7.2 安全资源表 (safety_resources)

**表名**: `safety_resources`  
**表说明**: 安全资源表，存储救援队伍、应急专家、物资装备等信息

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 资源ID，主键 |
| resource_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 资源编码，唯一索引 |
| resource_name | VARCHAR | 200 | NOT NULL | - | - | - | 资源名称 |
| resource_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 资源类型：1-救援队伍，2-应急专家，3-物资装备 |
| sub_type | VARCHAR | 50 | NULL | - | - | INDEX | 子类型（救援队伍：危化品、消防、应急抢险、医疗、社会救援；专家：行业专家、救援专家、技术专家；物资：个人防护、抢险救援、食品、药品、饮用水、人员庇护） |
| location | POINT | - | NULL | - | - | SPATIAL | 地理位置（空间数据类型） |
| longitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 经度 |
| latitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 纬度 |
| street | VARCHAR | 100 | NULL | - | - | INDEX | 所属街道 |
| address | VARCHAR | 255 | NULL | - | - | - | 详细地址 |
| organization_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 所属组织ID，外键关联organizations表 |
| contact_person | VARCHAR | 50 | NULL | - | - | - | 联系人 |
| contact_phone | VARCHAR | 20 | NULL | - | - | INDEX | 联系电话 |
| capacity | INT | - | NULL | - | - | - | 容量/人数（救援队伍、避难场所等） |
| equipment_info | TEXT | - | NULL | - | - | - | 装备信息（JSON格式，物资装备类型） |
| expert_field | VARCHAR | 200 | NULL | - | - | - | 专家领域（应急专家类型） |
| expert_level | VARCHAR | 50 | NULL | - | - | INDEX | 专家级别（应急专家类型） |
| quantity | INT | - | NULL | 0 | - | - | 数量（物资装备类型） |
| unit | VARCHAR | 20 | NULL | - | - | - | 单位（物资装备类型） |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| description | VARCHAR | 255 | NULL | - | - | - | 资源描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_resource_code` (`resource_code`)
- KEY `idx_resource_type` (`resource_type`)
- KEY `idx_sub_type` (`sub_type`)
- KEY `idx_longitude` (`longitude`)
- KEY `idx_latitude` (`latitude`)
- KEY `idx_street` (`street`)
- KEY `idx_organization_id` (`organization_id`)
- KEY `idx_contact_phone` (`contact_phone`)
- KEY `idx_expert_level` (`expert_level`)
- KEY `idx_status` (`status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)
- SPATIAL KEY `idx_location` (`location`)

---

### 7.3 防护目标表 (safety_targets)

**表名**: `safety_targets`  
**表说明**: 防护目标表，存储学校、居民区等人员密集场所信息

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 防护目标ID，主键 |
| target_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 目标编码，唯一索引 |
| target_name | VARCHAR | 200 | NOT NULL | - | - | - | 目标名称 |
| target_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 目标类型：1-学校，2-居民区，3-医院，4-商场，5-其他人员密集场所 |
| location | POINT | - | NULL | - | - | SPATIAL | 地理位置（空间数据类型） |
| longitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 经度 |
| latitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 纬度 |
| street | VARCHAR | 100 | NULL | - | - | INDEX | 所属街道 |
| address | VARCHAR | 255 | NULL | - | - | - | 详细地址 |
| population | INT | - | NULL | - | - | - | 人口数量 |
| area | DECIMAL(10,2) | - | NULL | - | - | - | 占地面积（平方米） |
| risk_level | TINYINT | - | NULL | - | - | INDEX | 风险等级：1-高，2-中，3-低 |
| contact_person | VARCHAR | 50 | NULL | - | - | - | 联系人 |
| contact_phone | VARCHAR | 20 | NULL | - | - | INDEX | 联系电话 |
| description | VARCHAR | 255 | NULL | - | - | - | 目标描述 |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_target_code` (`target_code`)
- KEY `idx_target_type` (`target_type`)
- KEY `idx_longitude` (`longitude`)
- KEY `idx_latitude` (`latitude`)
- KEY `idx_street` (`street`)
- KEY `idx_risk_level` (`risk_level`)
- KEY `idx_contact_phone` (`contact_phone`)
- KEY `idx_status` (`status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)
- SPATIAL KEY `idx_location` (`location`)

---

### 7.4 避难场所表 (shelters)

**表名**: `shelters`  
**表说明**: 避难场所表，存储公园、广场、体育场等避难场所信息

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 避难场所ID，主键 |
| shelter_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 场所编码，唯一索引 |
| shelter_name | VARCHAR | 200 | NOT NULL | - | - | - | 场所名称 |
| shelter_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 场所类型：1-公园，2-广场，3-体育场，4-学校，5-其他 |
| location | POINT | - | NULL | - | - | SPATIAL | 地理位置（空间数据类型） |
| longitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 经度 |
| latitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 纬度 |
| street | VARCHAR | 100 | NULL | - | - | INDEX | 所属街道 |
| address | VARCHAR | 255 | NULL | - | - | - | 详细地址 |
| capacity | INT | - | NOT NULL | 0 | - | - | 容纳能力（人数） |
| area | DECIMAL(10,2) | - | NULL | - | - | - | 占地面积（平方米） |
| facilities | TEXT | - | NULL | - | - | - | 设施信息（JSON格式） |
| contact_person | VARCHAR | 50 | NULL | - | - | - | 联系人 |
| contact_phone | VARCHAR | 20 | NULL | - | - | INDEX | 联系电话 |
| description | VARCHAR | 255 | NULL | - | - | - | 场所描述 |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_shelter_code` (`shelter_code`)
- KEY `idx_shelter_type` (`shelter_type`)
- KEY `idx_longitude` (`longitude`)
- KEY `idx_latitude` (`latitude`)
- KEY `idx_street` (`street`)
- KEY `idx_contact_phone` (`contact_phone`)
- KEY `idx_status` (`status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)
- SPATIAL KEY `idx_location` (`location`)

---

### 7.5 行业态势表 (industry_status)

**表名**: `industry_status`  
**表说明**: 行业态势表，存储各行业的安全态势数据

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 态势ID，主键 |
| stat_date | DATE | - | NOT NULL | - | - | INDEX | 统计日期 |
| industry_type | TINYINT | - | NOT NULL | - | - | INDEX | 行业类型：1-森林火灾，2-防汛，3-交通运输，4-危险化学品 |
| alarm_count | INT | - | NOT NULL | 0 | - | - | 报警数量 |
| warning_count | INT | - | NOT NULL | 0 | - | - | 预警数量 |
| risk_count | INT | - | NOT NULL | 0 | - | - | 风险隐患数量 |
| risk_level_1_count | INT | - | NOT NULL | 0 | - | - | 红色I级风险数量 |
| risk_level_2_count | INT | - | NOT NULL | 0 | - | - | 橙色Ⅱ级风险数量 |
| risk_level_3_count | INT | - | NOT NULL | 0 | - | - | 黄色Ⅲ级风险数量 |
| risk_level_4_count | INT | - | NOT NULL | 0 | - | - | 蓝色Ⅳ级风险数量 |
| status_data | TEXT | - | NULL | - | - | - | 详细态势数据（JSON格式） |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_industry_stat` (`stat_date`, `industry_type`)
- KEY `idx_stat_date` (`stat_date`)
- KEY `idx_industry_type` (`industry_type`)
- KEY `idx_created_at` (`created_at`)

---

### 7.6 区域态势表 (region_status)

**表名**: `region_status`  
**表说明**: 区域态势表，存储各街道的安全态势数据

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 态势ID，主键 |
| stat_date | DATE | - | NOT NULL | - | - | INDEX | 统计日期 |
| street | VARCHAR | 100 | NOT NULL | - | - | INDEX | 所属街道 |
| alarm_count | INT | - | NOT NULL | 0 | - | - | 报警数量 |
| warning_count | INT | - | NOT NULL | 0 | - | - | 预警数量 |
| risk_count | INT | - | NOT NULL | 0 | - | - | 风险隐患数量 |
| risk_level_1_count | INT | - | NOT NULL | 0 | - | - | 红色I级风险数量 |
| risk_level_2_count | INT | - | NOT NULL | 0 | - | - | 橙色Ⅱ级风险数量 |
| risk_level_3_count | INT | - | NOT NULL | 0 | - | - | 黄色Ⅲ级风险数量 |
| risk_level_4_count | INT | - | NOT NULL | 0 | - | - | 蓝色Ⅳ级风险数量 |
| risk_color | VARCHAR | 20 | NULL | - | - | INDEX | 风险颜色：red-红色，orange-橙色，yellow-黄色，blue-蓝色（用于四色图渲染） |
| status_data | TEXT | - | NULL | - | - | - | 详细态势数据（JSON格式） |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_region_stat` (`stat_date`, `street`)
- KEY `idx_stat_date` (`stat_date`)
- KEY `idx_street` (`street`)
- KEY `idx_risk_color` (`risk_color`)
- KEY `idx_created_at` (`created_at`)

---

### 7.7 监测数据表 (monitor_data)

**表名**: `monitor_data`  
**表说明**: 监测数据表，存储实时监测数据（用于大屏展示）

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 监测数据ID，主键 |
| monitor_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 监测点ID，外键关联risk_monitors表 |
| industry_type | TINYINT | - | NOT NULL | - | - | INDEX | 行业类型：1-森林火灾，2-防汛，3-交通运输，4-危险化学品 |
| data_time | DATETIME | - | NOT NULL | - | - | INDEX | 数据时间 |
| monitor_value | DECIMAL(10,2) | - | NULL | - | - | - | 监测数值 |
| monitor_unit | VARCHAR | 20 | NULL | - | - | - | 监测单位 |
| online_status | TINYINT | - | NOT NULL | 1 | - | INDEX | 在线状态：0-离线，1-在线 |
| data_source | VARCHAR | 50 | NULL | - | - | - | 数据来源 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |

**索引设计**:
- PRIMARY KEY (`id`)
- KEY `idx_monitor_id` (`monitor_id`)
- KEY `idx_industry_type` (`industry_type`)
- KEY `idx_data_time` (`data_time`)
- KEY `idx_online_status` (`online_status`)
- KEY `idx_created_at` (`created_at`)

---

### 7.8 预警事件表 (warning_events)

**表名**: `warning_events`  
**表说明**: 预警事件表，存储预警事件信息（用于大屏展示）

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 预警事件ID，主键 |
| warning_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 预警ID，外键关联risk_warnings表 |
| warning_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 预警事件编码，唯一索引 |
| warning_level_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 预警级别ID，外键关联warning_levels表 |
| industry_type | TINYINT | - | NOT NULL | - | - | INDEX | 行业类型：1-森林火灾，2-防汛，3-交通运输，4-危险化学品 |
| warning_type | VARCHAR | 50 | NOT NULL | - | - | INDEX | 预警类型 |
| warning_title | VARCHAR | 200 | NOT NULL | - | - | - | 预警标题 |
| location | POINT | - | NULL | - | - | SPATIAL | 预警位置（空间数据类型） |
| longitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 经度 |
| latitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 纬度 |
| street | VARCHAR | 100 | NULL | - | - | INDEX | 所属街道 |
| address | VARCHAR | 255 | NULL | - | - | - | 详细地址 |
| warning_time | DATETIME | - | NOT NULL | - | - | INDEX | 预警时间 |
| warning_status | TINYINT | - | NOT NULL | 0 | - | INDEX | 预警状态：0-未发布，1-已发布，2-处理中，3-已处置，4-已关闭 |
| nearby_monitor_count | INT | - | NULL | 0 | - | - | 附近监测点数量 |
| nearby_risk_count | INT | - | NULL | 0 | - | - | 附近危险源数量 |
| nearby_resource_count | INT | - | NULL | 0 | - | - | 附近应急资源数量 |
| description | VARCHAR | 255 | NULL | - | - | - | 预警描述 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_warning_code` (`warning_code`)
- KEY `idx_warning_id` (`warning_id`)
- KEY `idx_warning_level_id` (`warning_level_id`)
- KEY `idx_industry_type` (`industry_type`)
- KEY `idx_warning_type` (`warning_type`)
- KEY `idx_longitude` (`longitude`)
- KEY `idx_latitude` (`latitude`)
- KEY `idx_street` (`street`)
- KEY `idx_warning_time` (`warning_time`)
- KEY `idx_warning_status` (`warning_status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)
- SPATIAL KEY `idx_location` (`location`)

---

### 7.9 危险源表 (hazard_sources)

**表名**: `hazard_sources`  
**表说明**: 危险源表，存储危险源和重大危险源信息

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 危险源ID，主键 |
| source_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 危险源编码，唯一索引 |
| source_name | VARCHAR | 200 | NOT NULL | - | - | - | 危险源名称 |
| source_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 危险源类型：1-重大危险源，2-一般危险源 |
| industry_type | TINYINT | - | NOT NULL | - | - | INDEX | 行业类型：1-森林火灾，2-防汛，3-交通运输，4-危险化学品 |
| organization_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 所属企业ID，外键关联organizations表 |
| location | POINT | - | NULL | - | - | SPATIAL | 危险源位置（空间数据类型） |
| longitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 经度 |
| latitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 纬度 |
| street | VARCHAR | 100 | NULL | - | - | INDEX | 所属街道 |
| address | VARCHAR | 255 | NULL | - | - | - | 详细地址 |
| risk_level | TINYINT | - | NOT NULL | 1 | - | INDEX | 风险等级：1-高，2-中，3-低 |
| material_type | VARCHAR | 100 | NULL | - | - | - | 危险物质类型 |
| material_quantity | DECIMAL(10,2) | - | NULL | - | - | - | 危险物质数量 |
| material_unit | VARCHAR | 20 | NULL | - | - | - | 数量单位 |
| safety_measures | TEXT | - | NULL | - | - | - | 安全措施 |
| emergency_plan_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 关联应急预案ID，外键关联emergency_plans表 |
| contact_person | VARCHAR | 50 | NULL | - | - | - | 联系人 |
| contact_phone | VARCHAR | 20 | NULL | - | - | INDEX | 联系电话 |
| description | VARCHAR | 255 | NULL | - | - | - | 危险源描述 |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_source_code` (`source_code`)
- KEY `idx_source_type` (`source_type`)
- KEY `idx_industry_type` (`industry_type`)
- KEY `idx_organization_id` (`organization_id`)
- KEY `idx_longitude` (`longitude`)
- KEY `idx_latitude` (`latitude`)
- KEY `idx_street` (`street`)
- KEY `idx_risk_level` (`risk_level`)
- KEY `idx_emergency_plan_id` (`emergency_plan_id`)
- KEY `idx_contact_phone` (`contact_phone`)
- KEY `idx_status` (`status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)
- SPATIAL KEY `idx_location` (`location`)

---

### 7.10 视频监控设施表 (video_monitors)

**表名**: `video_monitors`  
**表说明**: 视频监控设施表，存储视频监控设施信息

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 监控设施ID，主键 |
| monitor_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 监控设施编码，唯一索引 |
| monitor_name | VARCHAR | 200 | NOT NULL | - | - | - | 监控设施名称 |
| monitor_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 监控类型：1-固定监控，2-移动监控，3-无人机监控 |
| industry_type | TINYINT | - | NOT NULL | - | - | INDEX | 行业类型：1-森林火灾，2-防汛，3-交通运输，4-危险化学品 |
| location | POINT | - | NULL | - | - | SPATIAL | 监控位置（空间数据类型） |
| longitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 经度 |
| latitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 纬度 |
| street | VARCHAR | 100 | NULL | - | - | INDEX | 所属街道 |
| address | VARCHAR | 255 | NULL | - | - | - | 详细地址 |
| video_url | VARCHAR | 500 | NULL | - | - | - | 视频流地址 |
| rtsp_url | VARCHAR | 500 | NULL | - | - | - | RTSP流地址 |
| coverage_radius | DECIMAL(10,2) | - | NULL | - | - | - | 覆盖半径（米） |
| camera_angle | DECIMAL(5,2) | - | NULL | - | - | - | 摄像头角度（度） |
| online_status | TINYINT | - | NOT NULL | 1 | - | INDEX | 在线状态：0-离线，1-在线 |
| organization_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 所属组织ID，外键关联organizations表 |
| description | VARCHAR | 255 | NULL | - | - | - | 监控设施描述 |
| status | TINYINT | - | NOT NULL | 1 | - | INDEX | 状态：0-禁用，1-启用 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_monitor_code` (`monitor_code`)
- KEY `idx_monitor_type` (`monitor_type`)
- KEY `idx_industry_type` (`industry_type`)
- KEY `idx_longitude` (`longitude`)
- KEY `idx_latitude` (`latitude`)
- KEY `idx_street` (`street`)
- KEY `idx_online_status` (`online_status`)
- KEY `idx_organization_id` (`organization_id`)
- KEY `idx_status` (`status`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)
- SPATIAL KEY `idx_location` (`location`)

---

**说明**: 以上为安全资源相关表（4.1.5）的详细设计，请确认后继续设计其他部分。

---

## 8. 演练相关表设计（4.1.6）

### 8.1 演练相关表设计说明

#### 8.1.1 演练事件管理
- 打通企业安全在线服务和化工园区安全智能化管控平台应急演练数据
- 对企业的演练事件进行监管，形成企业突发事件演练的基本信息
- 包含演练事件名称、事发单位、关联演练计划、事件类型、受伤人数、死亡人数、事件位置、事发时间、事故简介、需要启动的预案等

#### 8.1.2 演练过程评价
- 对企业的应急演练情况进行评估评价
- 对演练节点情况进行逐条详细评估
- 记录演练过程中的各项评价指标

#### 8.1.3 演练总结
- 基于演练过程评价和企业演练总结报告相关情况
- 结合监管单位意见，形成演练总体评价报告
- 包含企业内部沟通和传递是否顺畅、各级人员对预案的熟悉程度以及预案的可操作性、各级部门的职责定位是否明确、应急指挥是否科学、应急处置是否得当等信息分析存在的问题等

#### 8.1.4 演练分析
- 根据企业演练事件类型等信息，进行演练数据的统计分析
- 以不同的演练单位为维度，按照不同的演练类型、演练事故类型进行应急演练情况统计
- 根据不同的事故类型，进行各种事故类型演练的数量统计比对

---

### 8.2 演练事件表 (drill_events)

**表名**: `drill_events`  
**表说明**: 演练事件表，存储企业应急演练事件的基本信息

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 演练事件ID，主键 |
| event_code | VARCHAR | 50 | NOT NULL | - | - | UNIQUE | 事件编码，唯一索引 |
| event_name | VARCHAR | 200 | NOT NULL | - | - | - | 演练事件名称 |
| organization_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 事发单位ID，外键关联organizations表 |
| drill_plan_name | VARCHAR | 200 | NULL | - | - | - | 关联演练计划名称 |
| drill_plan_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 关联演练计划ID（如果有） |
| event_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 事件类型：1-火灾，2-爆炸，3-泄漏，4-坍塌，5-其他 |
| accident_type | VARCHAR | 50 | NULL | - | - | INDEX | 事故类型（详细分类） |
| location | POINT | - | NULL | - | - | SPATIAL | 事件位置（空间数据类型） |
| longitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 经度 |
| latitude | DECIMAL(10,7) | - | NULL | - | - | INDEX | 纬度 |
| street | VARCHAR | 100 | NULL | - | - | INDEX | 所属街道 |
| address | VARCHAR | 255 | NULL | - | - | - | 详细地址 |
| event_time | DATETIME | - | NOT NULL | - | - | INDEX | 事发时间 |
| injured_count | INT | - | NOT NULL | 0 | - | - | 受伤人数 |
| death_count | INT | - | NOT NULL | 0 | - | - | 死亡人数 |
| accident_summary | TEXT | - | NULL | - | - | - | 事故简介 |
| related_plan_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 需要启动的预案ID，外键关联emergency_plans表 |
| drill_status | TINYINT | - | NOT NULL | 0 | - | INDEX | 演练状态：0-未开始，1-进行中，2-已完成，3-已取消 |
| data_source | VARCHAR | 50 | NULL | - | - | INDEX | 数据来源：1-企业安全在线服务，2-化工园区安全智能化管控平台，3-手动录入 |
| external_id | VARCHAR | 100 | NULL | - | - | INDEX | 外部系统ID |
| description | VARCHAR | 255 | NULL | - | - | - | 事件描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_event_code` (`event_code`)
- KEY `idx_organization_id` (`organization_id`)
- KEY `idx_drill_plan_id` (`drill_plan_id`)
- KEY `idx_event_type` (`event_type`)
- KEY `idx_accident_type` (`accident_type`)
- KEY `idx_longitude` (`longitude`)
- KEY `idx_latitude` (`latitude`)
- KEY `idx_street` (`street`)
- KEY `idx_event_time` (`event_time`)
- KEY `idx_related_plan_id` (`related_plan_id`)
- KEY `idx_drill_status` (`drill_status`)
- KEY `idx_data_source` (`data_source`)
- KEY `idx_external_id` (`external_id`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)
- SPATIAL KEY `idx_location` (`location`)

---

### 8.3 演练评价表 (drill_evaluations)

**表名**: `drill_evaluations`  
**表说明**: 演练评价表，存储演练过程的详细评价信息

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 评价ID，主键 |
| event_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 演练事件ID，外键关联drill_events表 |
| node_name | VARCHAR | 200 | NOT NULL | - | - | - | 演练节点名称 |
| node_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 节点类型：1-信息收集，2-决策指挥，3-资源调配，4-现场处置，5-其他 |
| evaluation_item | VARCHAR | 200 | NOT NULL | - | - | - | 评价项 |
| evaluation_content | TEXT | - | NOT NULL | - | - | - | 评价内容 |
| evaluation_score | DECIMAL(5,2) | - | NULL | - | - | - | 评价得分（0-100） |
| evaluation_level | TINYINT | - | NULL | - | - | INDEX | 评价等级：1-优秀，2-良好，3-合格，4-不合格 |
| evaluator_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 评价人ID，外键关联users表 |
| evaluation_time | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 评价时间 |
| description | VARCHAR | 255 | NULL | - | - | - | 评价描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- KEY `idx_event_id` (`event_id`)
- KEY `idx_node_type` (`node_type`)
- KEY `idx_evaluation_level` (`evaluation_level`)
- KEY `idx_evaluator_id` (`evaluator_id`)
- KEY `idx_evaluation_time` (`evaluation_time`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 8.4 演练总结表 (drill_summaries)

**表名**: `drill_summaries`  
**表说明**: 演练总结表，存储演练总体评价报告

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 总结ID，主键 |
| event_id | BIGINT UNSIGNED | - | NOT NULL | - | - | UNIQUE | 演练事件ID，外键关联drill_events表，唯一索引 |
| summary_title | VARCHAR | 200 | NOT NULL | - | - | - | 总结标题 |
| communication_status | TINYINT | - | NULL | - | - | INDEX | 内部沟通和传递是否顺畅：1-顺畅，2-一般，3-不顺畅 |
| communication_comment | TEXT | - | NULL | - | - | - | 内部沟通评价说明 |
| plan_familiarity | TINYINT | - | NULL | - | - | INDEX | 各级人员对预案的熟悉程度：1-熟悉，2-一般，3-不熟悉 |
| plan_familiarity_comment | TEXT | - | NULL | - | - | - | 预案熟悉程度评价说明 |
| plan_operability | TINYINT | - | NULL | - | - | INDEX | 预案的可操作性：1-可操作，2-一般，3-不可操作 |
| plan_operability_comment | TEXT | - | NULL | - | - | - | 预案可操作性评价说明 |
| duty_clarity | TINYINT | - | NULL | - | - | INDEX | 各级部门的职责定位是否明确：1-明确，2-一般，3-不明确 |
| duty_clarity_comment | TEXT | - | NULL | - | - | - | 职责定位评价说明 |
| command_science | TINYINT | - | NULL | - | - | INDEX | 应急指挥是否科学：1-科学，2-一般，3-不科学 |
| command_science_comment | TEXT | - | NULL | - | - | - | 应急指挥评价说明 |
| disposal_appropriateness | TINYINT | - | NULL | - | - | INDEX | 应急处置是否得当：1-得当，2-一般，3-不得当 |
| disposal_appropriateness_comment | TEXT | - | NULL | - | - | - | 应急处置评价说明 |
| problems_analysis | TEXT | - | NULL | - | - | - | 存在的问题分析 |
| improvement_suggestions | TEXT | - | NULL | - | - | - | 改进建议 |
| overall_score | DECIMAL(5,2) | - | NULL | - | - | - | 总体得分（0-100） |
| overall_level | TINYINT | - | NULL | - | - | INDEX | 总体等级：1-优秀，2-良好，3-合格，4-不合格 |
| enterprise_summary | TEXT | - | NULL | - | - | - | 企业演练总结报告内容 |
| supervisor_opinion | TEXT | - | NULL | - | - | - | 监管单位意见 |
| summary_user_id | BIGINT UNSIGNED | - | NOT NULL | - | - | INDEX | 总结人ID，外键关联users表 |
| summary_time | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 总结时间 |
| description | VARCHAR | 255 | NULL | - | - | - | 总结描述 |
| remark | TEXT | - | NULL | - | - | - | 备注信息 |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |
| deleted_at | DATETIME | - | NULL | - | - | INDEX | 删除时间（软删除） |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_event_id` (`event_id`)
- KEY `idx_communication_status` (`communication_status`)
- KEY `idx_plan_familiarity` (`plan_familiarity`)
- KEY `idx_plan_operability` (`plan_operability`)
- KEY `idx_duty_clarity` (`duty_clarity`)
- KEY `idx_command_science` (`command_science`)
- KEY `idx_disposal_appropriateness` (`disposal_appropriateness`)
- KEY `idx_overall_level` (`overall_level`)
- KEY `idx_summary_user_id` (`summary_user_id`)
- KEY `idx_summary_time` (`summary_time`)
- KEY `idx_created_at` (`created_at`)
- KEY `idx_deleted_at` (`deleted_at`)

---

### 8.5 演练分析表 (drill_analyses)

**表名**: `drill_analyses`  
**表说明**: 演练分析表，存储演练数据的统计分析结果

| 字段名 | 类型 | 长度 | 是否为空 | 默认值 | 主键 | 索引 | 备注 |
|--------|------|------|----------|--------|------|------|------|
| id | BIGINT UNSIGNED | - | NOT NULL | AUTO_INCREMENT | ✓ | PRIMARY | 分析ID，主键 |
| stat_date | DATE | - | NOT NULL | - | - | INDEX | 统计日期 |
| stat_type | TINYINT | - | NOT NULL | 1 | - | INDEX | 统计类型：1-日报，2-周报，3-月报，4-年报 |
| organization_id | BIGINT UNSIGNED | - | NULL | - | - | INDEX | 演练单位ID，外键关联organizations表，NULL表示全部 |
| drill_type | TINYINT | - | NULL | - | - | INDEX | 演练类型：1-桌面演练，2-功能演练，3-全面演练，NULL表示全部 |
| accident_type | VARCHAR | 50 | NULL | - | - | INDEX | 事故类型，NULL表示全部 |
| drill_count | INT | - | NOT NULL | 0 | - | - | 演练次数 |
| completed_count | INT | - | NOT NULL | 0 | - | - | 已完成次数 |
| excellent_count | INT | - | NOT NULL | 0 | - | - | 优秀次数 |
| good_count | INT | - | NOT NULL | 0 | - | - | 良好次数 |
| qualified_count | INT | - | NOT NULL | 0 | - | - | 合格次数 |
| unqualified_count | INT | - | NOT NULL | 0 | - | - | 不合格次数 |
| avg_score | DECIMAL(5,2) | - | NULL | - | - | - | 平均得分 |
| analysis_data | TEXT | - | NULL | - | - | - | 详细分析数据（JSON格式） |
| created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP | - | INDEX | 创建时间 |
| updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | 更新时间 |

**索引设计**:
- PRIMARY KEY (`id`)
- UNIQUE KEY `uk_drill_stat` (`stat_date`, `stat_type`, `organization_id`, `drill_type`, `accident_type`)
- KEY `idx_stat_date` (`stat_date`)
- KEY `idx_stat_type` (`stat_type`)
- KEY `idx_organization_id` (`organization_id`)
- KEY `idx_drill_type` (`drill_type`)
- KEY `idx_accident_type` (`accident_type`)
- KEY `idx_created_at` (`created_at`)

---

**说明**: 以上为演练相关表（4.1.6）的详细设计，请确认后继续设计其他部分。

