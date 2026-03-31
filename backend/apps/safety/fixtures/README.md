# 安全态势模块演示数据初始化说明

本目录包含安全态势模块的资源数据初始化文件（Django Fixtures）。

## 文件说明

### 加载顺序

按照依赖关系，请按以下顺序加载fixtures：

1. `initial_safety_resources.json` - 安全资源（救援队伍、应急专家、物资装备）
2. `initial_safety_targets.json` - 防护目标
3. `initial_shelters.json` - 避难场所
4. `initial_hazard_sources.json` - 危险源
5. `initial_video_monitors.json` - 视频监控设施
6. `initial_industry_status.json` - 行业态势数据（用于安全态势一张图）
7. `initial_region_status.json` - 区域态势数据（用于四色风险图）

### 数据说明

#### 安全资源（23个资源）

- **救援队伍（9支）**：
  - 危化品救援队：2支
  - 消防队：2支
  - 应急抢险队：2支
  - 医疗救援队：2支
  - 社会救援队：1支

- **应急专家（5名）**：
  - 行业专家：2名（危化品、气象）
  - 救援专家：2名（消防、地震救援）
  - 技术专家：1名（应急通信）

- **物资装备（9项）**：
  - 个人防护：2项（防毒面具、防护服）
  - 抢险救援：2项（生命探测仪、破拆工具）
  - 食品：2项（方便面、压缩饼干）
  - 药品：1项（急救药品包）
  - 饮用水：1项（瓶装饮用水）
  - 人员庇护：1项（帐篷）

#### 防护目标（10个）

- 学校：2个（中学、小学）
- 居民区：2个（大型小区）
- 医院：2个（综合医院、中医院）
- 商场：2个（大型购物中心）
- 其他人员密集场所：2个（火车站、高铁站）

#### 避难场所（6个）

- 公园：2个（雨山湖公园、翠螺山公园）
- 广场：2个（市政广场、文化广场）
- 体育场：1个（市体育场）
- 学校：1个（第一中学）

#### 危险源（7个）

- 重大危险源（4个）：
  - 马钢焦化厂
  - 中石化油库
  - 马钢高炉煤气柜
  - 某化工厂液氨储罐

- 一般危险源（3个）：
  - 加油站
  - 化工厂盐酸储罐
  - 长江堤防险工险段

#### 视频监控（8个）

- 固定监控：7个（覆盖公园、危险源、交通枢纽、学校等）
- 无人机监控：1个（移动监控设备）

#### 行业态势（4条记录）

- **森林火灾（industry_type: 1）**：
  - 报警数量：2
  - 预警数量：8
  - 风险隐患数量：5
  - 风险等级分布：红色I级1个、橙色Ⅱ级2个、黄色Ⅲ级1个、蓝色Ⅳ级1个

- **防汛（industry_type: 2）**：
  - 报警数量：3
  - 预警数量：10
  - 风险隐患数量：6
  - 风险等级分布：红色I级1个、橙色Ⅱ级2个、黄色Ⅲ级2个、蓝色Ⅳ级1个

- **交通运输（industry_type: 3）**：
  - 报警数量：4
  - 预警数量：15
  - 风险隐患数量：8
  - 风险等级分布：红色I级2个、橙色Ⅱ级3个、黄色Ⅲ级2个、蓝色Ⅳ级1个

- **危险化学品（industry_type: 4）**：
  - 报警数量：1
  - 预警数量：5
  - 风险隐患数量：3
  - 风险等级分布：红色I级0个、橙色Ⅱ级1个、黄色Ⅲ级1个、蓝色Ⅳ级1个

**数据特点**：
- 统计日期：2024-12-22（最新日期）
- 覆盖所有四个行业类型
- 每个行业一条最新记录
- 数据用于安全态势一张图的行业态势面板展示

#### 区域态势（7条记录，用于四色风险图）

**重要说明**：
- 区域态势数据按照**实际风险区域**来设定，不严格按照行政区域边界
- `street` 字段表示风险区域名称（如"马钢工业园区风险区域"），用于标识风险区域，不要求与行政区域完全对应
- 风险区域在地图上以圆形区域展示，中心点和半径根据实际风险分布设定
- 色块边界不要求完整对应行政区域边界，大概齐能对应上即可

- **马钢工业园区风险区域**（红色I级）：
  - 报警数量：5
  - 预警数量：12
  - 风险隐患数量：8
  - 风险等级分布：红色I级2个、橙色Ⅱ级3个、黄色Ⅲ级2个、蓝色Ⅳ级1个

- **雨山湖周边风险区域**（橙色Ⅱ级）：
  - 报警数量：3
  - 预警数量：8
  - 风险隐患数量：5
  - 风险等级分布：红色I级0个、橙色Ⅱ级2个、黄色Ⅲ级2个、蓝色Ⅳ级1个

- **市中心商业区风险区域**（黄色Ⅲ级）：
  - 报警数量：2
  - 预警数量：5
  - 风险隐患数量：3
  - 风险等级分布：红色I级0个、橙色Ⅱ级0个、黄色Ⅲ级2个、蓝色Ⅳ级1个

- **东部新区风险区域**（蓝色Ⅳ级）：
  - 报警数量：1
  - 预警数量：2
  - 风险隐患数量：1
  - 风险等级分布：红色I级0个、橙色Ⅱ级0个、黄色Ⅲ级0个、蓝色Ⅳ级1个

- **长江沿岸风险区域**（黄色Ⅲ级）：
  - 报警数量：2
  - 预警数量：4
  - 风险隐患数量：2
  - 风险等级分布：红色I级0个、橙色Ⅱ级1个、黄色Ⅲ级1个、蓝色Ⅳ级0个

- **南部山区风险区域**（蓝色Ⅳ级）：
  - 报警数量：1
  - 预警数量：3
  - 风险隐患数量：2
  - 风险等级分布：红色I级0个、橙色Ⅱ级0个、黄色Ⅲ级1个、蓝色Ⅳ级1个

- **西部工业区风险区域**（蓝色Ⅳ级）：
  - 报警数量：1
  - 预警数量：2
  - 风险隐患数量：1
  - 风险等级分布：红色I级0个、橙色Ⅱ级0个、黄色Ⅲ级0个、蓝色Ⅳ级1个

**数据特点**：
- 统计日期：2024-12-22（最新日期）
- 覆盖7个风险区域（不严格按照行政区域）
- 每个区域都有 `risk_color` 字段（red/orange/yellow/blue），用于四色风险图渲染
- 风险颜色根据各风险等级数量自动计算：优先显示最高风险等级
- 风险区域名称反映实际风险分布（如"马钢工业园区风险区域"、"雨山湖周边风险区域"等）
- 数据用于安全态势一张图的四色风险图展示
- 前端会根据区域名称匹配对应的中心坐标和半径，在地图上绘制风险区域

## 使用方法

### 加载数据

```bash
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

## 注意事项

1. 所有地理坐标均位于马鞍山市范围内（约118.3-118.7, 31.6-31.9）
2. 数据分布在主要街道：佳山街道、平湖街道、雨山街道、解放路街道
3. 危险源数据需要关联组织ID，部分数据organization_id可能为null
4. 视频监控的video_url和rtsp_url为示例地址，实际使用时需替换为真实地址

