<template>
  <div class="dashboard">
    <div class="dashboard-header">
    <h1>仪表盘</h1>
      <div class="header-actions">
        <el-button :icon="Refresh" @click="handleRefresh" :loading="loading">刷新</el-button>
        <span class="last-update-time" v-if="lastUpdateTime">
          最后更新：{{ lastUpdateTime }}
        </span>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading && !lastUpdateTime" class="loading-container">
      <el-skeleton :rows="8" animated />
    </div>

    <!-- 最近活动/通知 - 移到顶部 -->
    <div v-if="!loading || lastUpdateTime" class="activities-section">
      <el-row :gutter="20">
        <!-- 左侧：最近活动 -->
        <el-col :xs="24" :sm="24" :md="16" :lg="16">
          <el-card class="activities-card">
            <template #header>
              <div class="card-header">
                <span class="card-title">最近活动</span>
              </div>
            </template>

            <el-tabs v-model="activeActivityTab" class="activity-tabs">
              <!-- 最近预警事件 -->
              <el-tab-pane label="预警事件" name="warning">
                <div class="activity-list">
                  <div
                    v-for="item in recentWarnings"
                    :key="item.id"
                    class="activity-item"
                    @click="handleViewWarning(item.id)"
                  >
                    <div class="activity-icon warning-icon">
                      <el-icon><Warning /></el-icon>
                    </div>
                    <div class="activity-content">
                      <div class="activity-title">{{ item.warning_title || item.title }}</div>
                      <div class="activity-meta">
                        <el-tag
                          :type="getWarningLevelType(item.warning_level)"
                          size="small"
                        >
                          {{ getWarningLevelName(item.warning_level) }}
                        </el-tag>
                        <span class="activity-time">{{ formatActivityTime(item.warning_time || item.created_at) }}</span>
                        <el-tag
                          :type="getWarningStatusType(item.warning_status)"
                          size="small"
                        >
                          {{ getWarningStatusName(item.warning_status) }}
                        </el-tag>
                      </div>
                    </div>
                  </div>
                  <div v-if="recentWarnings.length === 0" class="empty-state">
                    暂无预警事件
                  </div>
                </div>
              </el-tab-pane>

              <!-- 最近报警记录 -->
              <el-tab-pane label="报警记录" name="alarm">
                <div class="activity-list">
                  <div
                    v-for="item in recentAlarms"
                    :key="item.id"
                    class="activity-item"
                    @click="handleViewAlarm(item.id)"
                  >
                    <div class="activity-icon alarm-icon">
                      <el-icon><Bell /></el-icon>
                    </div>
                    <div class="activity-content">
                      <div class="activity-title">{{ item.alarm_content || item.content || `报警记录 #${item.id}` }}</div>
                      <div class="activity-meta">
                        <el-tag
                          :type="getAlarmStatusType(item.alarm_status)"
                          size="small"
                        >
                          {{ getAlarmStatusName(item.alarm_status) }}
                        </el-tag>
                        <span class="activity-time">{{ formatActivityTime(item.alarm_time || item.created_at) }}</span>
                        <span v-if="item.handle_user" class="activity-handler">
                          处理人：{{ item.handle_user?.username || item.handle_user }}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div v-if="recentAlarms.length === 0" class="empty-state">
                    暂无报警记录
                  </div>
                </div>
              </el-tab-pane>

              <!-- 最近预案执行记录 -->
              <el-tab-pane label="预案执行" name="plan">
                <div class="activity-list">
                  <div
                    v-for="item in recentPlanExecutions"
                    :key="item.id"
                    class="activity-item"
                    @click="handleViewPlanExecution(item.id)"
                  >
                    <div class="activity-icon plan-icon">
                      <el-icon><Document /></el-icon>
                    </div>
                    <div class="activity-content">
                      <div class="activity-title">{{ item.plan?.plan_name || item.plan_name || `预案执行 #${item.id}` }}</div>
                      <div class="activity-meta">
                        <el-tag
                          :type="getExecutionStatusType(item.execution_status)"
                          size="small"
                        >
                          {{ getExecutionStatusName(item.execution_status) }}
                        </el-tag>
                        <span class="activity-time">{{ formatActivityTime(item.start_time || item.created_at) }}</span>
                      </div>
                    </div>
                  </div>
                  <div v-if="recentPlanExecutions.length === 0" class="empty-state">
                    暂无预案执行记录
                  </div>
                </div>
              </el-tab-pane>

              <!-- 最近演练事件 -->
              <el-tab-pane label="演练事件" name="drill">
                <div class="activity-list">
                  <div
                    v-for="item in recentDrillEvents"
                    :key="item.id"
                    class="activity-item"
                    @click="handleViewDrillEvent(item.id)"
                  >
                    <div class="activity-icon drill-icon">
                      <el-icon><Trophy /></el-icon>
                    </div>
                    <div class="activity-content">
                      <div class="activity-title">{{ item.event_name || item.name || `演练事件 #${item.id}` }}</div>
                      <div class="activity-meta">
                        <el-tag size="small">{{ getDrillTypeName(item.event_type) }}</el-tag>
                        <el-tag
                          :type="getDrillStatusType(item.drill_status)"
                          size="small"
                        >
                          {{ getDrillStatusName(item.drill_status) }}
                        </el-tag>
                        <span class="activity-time">{{ formatActivityTime(item.event_time || item.created_at) }}</span>
                      </div>
                    </div>
                  </div>
                  <div v-if="recentDrillEvents.length === 0" class="empty-state">
                    暂无演练事件
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>
          </el-card>
        </el-col>

        <!-- 右侧：系统通知 -->
        <el-col :xs="24" :sm="24" :md="8" :lg="8">
          <el-card class="notifications-card">
            <template #header>
              <div class="card-header">
                <span class="card-title">系统通知</span>
                <el-badge :value="unreadNotifications.length" :hidden="unreadNotifications.length === 0" class="notification-badge">
                  <el-button text :icon="Bell" @click="handleMarkAllRead">全部已读</el-button>
                </el-badge>
              </div>
            </template>

            <div class="notification-list">
              <div
                v-for="notification in notifications"
                :key="notification.id"
                class="notification-item"
                :class="{ unread: !notification.read }"
                @click="handleViewNotification(notification)"
              >
                <div class="notification-icon" :class="`notification-${notification.type}`">
                  <el-icon>
                    <Warning v-if="notification.type === 'warning'" />
                    <Bell v-else-if="notification.type === 'alarm'" />
                    <Connection v-else-if="notification.type === 'datasource'" />
                    <InfoFilled v-else />
                  </el-icon>
                </div>
                <div class="notification-content">
                  <div class="notification-title">{{ notification.title }}</div>
                  <div class="notification-desc">{{ notification.content }}</div>
                  <div class="notification-time">{{ formatActivityTime(notification.created_at) }}</div>
                </div>
                <div v-if="!notification.read" class="notification-dot"></div>
              </div>
              <div v-if="notifications.length === 0" class="empty-state">
                暂无系统通知
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 其他版块 - 使用 Tab 切换 -->
    <div v-if="!loading || lastUpdateTime" class="main-content-section">
      <el-tabs v-model="activeMainTab" class="main-tabs">
        <!-- Tab 1: 关键指标卡片 -->
        <el-tab-pane label="关键指标" name="statistics">
          <div class="statistics-cards">
      <el-row :gutter="20">
        <!-- 预警事件统计 -->
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <div class="stat-icon warning-icon">
                <el-icon><Warning /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-title">预警事件</div>
                <div class="stat-value">{{ warningStats.total || 0 }}</div>
                <div class="stat-detail" v-if="warningStats.levels">
                  <span class="level-item level-red">I级: {{ warningStats.levels[1] || 0 }}</span>
                  <span class="level-item level-orange">II级: {{ warningStats.levels[2] || 0 }}</span>
                  <span class="level-item level-yellow">III级: {{ warningStats.levels[3] || 0 }}</span>
                  <span class="level-item level-blue">IV级: {{ warningStats.levels[4] || 0 }}</span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 报警记录统计 -->
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <div class="stat-icon alarm-icon">
                <el-icon><Bell /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-title">报警记录</div>
                <div class="stat-value">{{ alarmStats.total || 0 }}</div>
                <div class="stat-detail" v-if="alarmStats.statuses">
                  <span class="status-item">待处理: {{ alarmStats.statuses[0] || 0 }}</span>
                  <span class="status-item">处理中: {{ alarmStats.statuses[1] || 0 }}</span>
                  <span class="status-item">已处理: {{ alarmStats.statuses[2] || 0 }}</span>
                  <span class="status-item">已忽略: {{ alarmStats.statuses[3] || 0 }}</span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 预案统计 -->
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <div class="stat-icon plan-icon">
                <el-icon><Document /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-title">应急预案</div>
                <div class="stat-value">{{ planStats.total_count || 0 }}</div>
                <div class="stat-detail" v-if="planStats.status_stats">
                  <span class="status-item">已发布: {{ getStatusCount(planStats.status_stats, 'published') || 0 }}</span>
                  <span class="status-item">已修订: {{ getStatusCount(planStats.status_stats, 'revised') || 0 }}</span>
                  <span class="status-item">已废止: {{ getStatusCount(planStats.status_stats, 'abolished') || 0 }}</span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 演练统计 -->
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <div class="stat-icon drill-icon">
                <el-icon><Trophy /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-title">演练事件</div>
                <div class="stat-value">{{ drillStats.total_count || 0 }}</div>
                <div class="stat-detail" v-if="drillStats.status_stats">
                  <span class="status-item">已完成: {{ getStatusCount(drillStats.status_stats, 'completed') || 0 }}</span>
                  <span class="status-item">进行中: {{ getStatusCount(drillStats.status_stats, 'in_progress') || 0 }}</span>
                  <span class="status-item">未开始: {{ getStatusCount(drillStats.status_stats, 'not_started') || 0 }}</span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 安全资源统计 -->
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <div class="stat-icon resource-icon">
                <el-icon><Box /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-title">安全资源</div>
                <div class="stat-value">{{ resourceStats.total_count || 0 }}</div>
                <div class="stat-detail" v-if="resourceStats.type_stats">
                  <span class="type-item">救援队伍: {{ getTypeCount(resourceStats.type_stats, 1) || 0 }}</span>
                  <span class="type-item">应急专家: {{ getTypeCount(resourceStats.type_stats, 2) || 0 }}</span>
                  <span class="type-item">物资装备: {{ getTypeCount(resourceStats.type_stats, 3) || 0 }}</span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 视频监控统计 -->
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <div class="stat-icon video-icon">
                <el-icon><VideoCamera /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-title">视频监控</div>
                <div class="stat-value">{{ videoStats.total_count || 0 }}</div>
                <div class="stat-detail" v-if="videoStats.online_count !== undefined">
                  <span class="status-item status-online">在线: {{ videoStats.online_count || 0 }}</span>
                  <span class="status-item status-offline">离线: {{ videoStats.offline_count || 0 }}</span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 数据源统计 -->
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <div class="stat-icon datasource-icon">
                <el-icon><Connection /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-title">数据源</div>
                <div class="stat-value">{{ datasourceStats.total_count || 0 }}</div>
                <div class="stat-detail" v-if="datasourceStats.status_stats">
                  <span class="status-item status-normal">正常: {{ getStatusCount(datasourceStats.status_stats, 'normal') || 0 }}</span>
                  <span class="status-item status-error">异常: {{ getStatusCount(datasourceStats.status_stats, 'error') || 0 }}</span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 叫应记录统计 -->
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <div class="stat-icon call-icon">
                <el-icon><Phone /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-title">叫应记录</div>
                <div class="stat-value">{{ callStats.total_count || 0 }}</div>
                <div class="stat-detail" v-if="callStats.response_status_stats">
                  <span class="status-item status-success">已响应: {{ getResponseStatusCount(callStats.response_status_stats, 'responded') || 0 }}</span>
                  <span class="status-item status-warning">未响应: {{ getResponseStatusCount(callStats.response_status_stats, 'not_responded') || 0 }}</span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
          </div>
        </el-tab-pane>

        <!-- Tab 2: 数据图表展示 -->
        <el-tab-pane label="数据图表" name="charts">
          <div class="charts-section">
      <el-card class="chart-card">
        <template #header>
          <div class="chart-header">
            <span class="chart-title">数据图表展示</span>
            <div class="chart-actions">
              <el-radio-group v-model="timeRange" size="small" @change="handleTimeRangeChange">
                <el-radio-button label="7">近7天</el-radio-button>
                <el-radio-button label="30">近30天</el-radio-button>
              </el-radio-group>
            </div>
          </div>
        </template>

        <el-row :gutter="20">
          <!-- 预警事件趋势图 -->
          <el-col :xs="24" :sm="24" :md="12" :lg="12">
            <div class="chart-item">
              <h3 class="chart-item-title">预警事件趋势</h3>
              <div ref="warningTrendChart" class="chart-container"></div>
            </div>
          </el-col>

          <!-- 报警记录趋势图 -->
          <el-col :xs="24" :sm="24" :md="12" :lg="12">
            <div class="chart-item">
              <h3 class="chart-item-title">报警记录趋势</h3>
              <div ref="alarmTrendChart" class="chart-container"></div>
            </div>
          </el-col>

          <!-- 预警级别分布图 -->
          <el-col :xs="24" :sm="24" :md="12" :lg="12">
            <div class="chart-item">
              <h3 class="chart-item-title">预警级别分布</h3>
              <div ref="warningLevelChart" class="chart-container"></div>
            </div>
          </el-col>

          <!-- 报警状态分布图 -->
          <el-col :xs="24" :sm="24" :md="12" :lg="12">
            <div class="chart-item">
              <h3 class="chart-item-title">报警状态分布</h3>
              <div ref="alarmStatusChart" class="chart-container"></div>
            </div>
          </el-col>

          <!-- 预案类型分布图 -->
          <el-col :xs="24" :sm="24" :md="12" :lg="12">
            <div class="chart-item">
              <h3 class="chart-item-title">预案类型分布</h3>
              <div ref="planTypeChart" class="chart-container"></div>
            </div>
          </el-col>

          <!-- 演练完成情况图 -->
          <el-col :xs="24" :sm="24" :md="12" :lg="12">
            <div class="chart-item">
              <h3 class="chart-item-title">演练完成情况</h3>
              <div ref="drillStatusChart" class="chart-container"></div>
            </div>
          </el-col>

          <!-- 行业态势对比图 -->
          <el-col :xs="24" :sm="24" :md="24" :lg="24">
            <div class="chart-item">
              <h3 class="chart-item-title">行业态势对比</h3>
              <div ref="industryCompareChart" class="chart-container"></div>
            </div>
          </el-col>
        </el-row>
          </el-card>
          </div>
        </el-tab-pane>

        <!-- Tab 3: 快捷操作入口 -->
        <el-tab-pane label="快捷操作" name="actions">
          <div class="quick-actions-section">
      <el-card class="quick-actions-card">
        <template #header>
          <div class="card-header">
            <span class="card-title">快捷操作</span>
          </div>
        </template>

        <div class="quick-actions-grid">
          <el-button
            type="danger"
            :icon="Warning"
            size="large"
            class="quick-action-btn"
            @click="handleQuickCreateWarning"
          >
            <div class="action-content">
              <div class="action-title">创建预警事件</div>
              <div class="action-desc">快速创建新的风险预警</div>
            </div>
          </el-button>

          <el-button
            type="warning"
            :icon="Bell"
            size="large"
            class="quick-action-btn"
            @click="handleQuickCreateAlarm"
          >
            <div class="action-content">
              <div class="action-title">创建报警记录</div>
              <div class="action-desc">快速创建新的报警记录</div>
            </div>
          </el-button>

          <el-button
            type="primary"
            :icon="Document"
            size="large"
            class="quick-action-btn"
            @click="handleQuickStartPlanExecution"
          >
            <div class="action-content">
              <div class="action-title">启动预案执行</div>
              <div class="action-desc">快速启动应急预案执行</div>
            </div>
          </el-button>

          <el-button
            type="success"
            :icon="Trophy"
            size="large"
            class="quick-action-btn"
            @click="handleQuickCreateDrillEvent"
          >
            <div class="action-content">
              <div class="action-title">创建演练事件</div>
              <div class="action-desc">快速创建新的演练事件</div>
            </div>
          </el-button>

          <el-button
            type="info"
            :icon="VideoCamera"
            size="large"
            class="quick-action-btn"
            @click="handleGoToScreen('safety-run')"
          >
            <div class="action-content">
              <div class="action-title">安全运行一张图</div>
              <div class="action-desc">查看安全运行大屏</div>
            </div>
          </el-button>

          <el-button
            type="info"
            :icon="VideoCamera"
            size="large"
            class="quick-action-btn"
            @click="handleGoToScreen('safety-status')"
          >
            <div class="action-content">
              <div class="action-title">安全态势一张图</div>
              <div class="action-desc">查看安全态势大屏</div>
            </div>
          </el-button>

          <el-button
            type="info"
            :icon="VideoCamera"
            size="large"
            class="quick-action-btn"
            @click="handleGoToScreen('monitor-warn')"
          >
            <div class="action-content">
              <div class="action-title">监测预警一张图</div>
              <div class="action-desc">查看监测预警大屏</div>
            </div>
          </el-button>
        </div>
          </el-card>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, watch, computed } from 'vue'
import { Refresh, Warning, Bell, Document, Trophy, Box, VideoCamera, Connection, Phone, InfoFilled } from '@element-plus/icons-vue'
import { riskWarningApi, alarmRecordApi } from '@/api/modules/risk'
import { emergencyPlanApi, planExecutionApi } from '@/api/modules/plan'
import { drillEventApi } from '@/api/modules/drill'
import { safetyResourceApi, videoMonitorApi } from '@/api/modules/safety'
import { datasourceApi } from '@/api/modules/system'
import { callRecordApi } from '@/api/modules/call'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import dayjs from 'dayjs'
import { useRouter } from 'vue-router'

// 强制刷新模块缓存

// 统计数据
const warningStats = ref<{
  total: number
  levels: Record<number, number>
}>({
  total: 0,
  levels: {},
})

const alarmStats = ref<{
  total: number
  statuses: Record<number, number>
}>({
  total: 0,
  statuses: {},
})

const planStats = ref<any>({})
const drillStats = ref<any>({})
const resourceStats = ref<any>({})
const videoStats = ref<any>({})
const datasourceStats = ref<any>({})
const callStats = ref<any>({})

// 最近活动数据
const router = useRouter()
const activeActivityTab = ref<string>('warning')
const activeMainTab = ref<string>('statistics')
const recentWarnings = ref<any[]>([])
const recentAlarms = ref<any[]>([])
const recentPlanExecutions = ref<any[]>([])
const recentDrillEvents = ref<any[]>([])

// 系统通知
interface Notification {
  id: number
  type: 'warning' | 'alarm' | 'datasource' | 'system'
  title: string
  content: string
  created_at: string
  read: boolean
}

const notifications = ref<Notification[]>([])
const unreadNotifications = computed(() => notifications.value.filter(n => !n.read))

const loading = ref(false)
const lastUpdateTime = ref<string>('')
let refreshTimer: ReturnType<typeof setInterval> | null = null

// 图表实例
const warningTrendChart = ref<HTMLDivElement | null>(null)
const alarmTrendChart = ref<HTMLDivElement | null>(null)
const warningLevelChart = ref<HTMLDivElement | null>(null)
const alarmStatusChart = ref<HTMLDivElement | null>(null)
const planTypeChart = ref<HTMLDivElement | null>(null)
const drillStatusChart = ref<HTMLDivElement | null>(null)
const industryCompareChart = ref<HTMLDivElement | null>(null)

let warningTrendChartInstance: echarts.ECharts | null = null
let alarmTrendChartInstance: echarts.ECharts | null = null
let warningLevelChartInstance: echarts.ECharts | null = null
let alarmStatusChartInstance: echarts.ECharts | null = null
let planTypeChartInstance: echarts.ECharts | null = null
let drillStatusChartInstance: echarts.ECharts | null = null
let industryCompareChartInstance: echarts.ECharts | null = null

// 时间范围
const timeRange = ref<string>('7')

// 格式化时间
const formatTime = (date: Date): string => {
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  return `${hours}:${minutes}:${seconds}`
}

// 获取预警事件统计
const fetchWarningStats = async () => {
  try {
    const response = await riskWarningApi.getList({ page_size: 1 })
    const total = response.count || 0

    // 获取所有预警数据以统计级别分布
    const allWarnings = await riskWarningApi.getList({ page_size: 1000 })
    const levels: Record<number, number> = {}
    
    if (allWarnings.results) {
      allWarnings.results.forEach((warning: any) => {
        const levelId = warning.warning_level?.id || warning.warning_level
        if (levelId) {
          levels[levelId] = (levels[levelId] || 0) + 1
        }
      })
    }

    warningStats.value = { total, levels }
  } catch (error: any) {
    console.error('获取预警事件统计失败:', error)
    ElMessage.error('获取预警事件统计失败: ' + (error.message || '未知错误'))
  }
}

// 获取报警记录统计
const fetchAlarmStats = async () => {
  try {
    const response = await alarmRecordApi.getList({ page_size: 1 })
    const total = response.count || 0

    // 获取所有报警数据以统计状态分布
    const allAlarms = await alarmRecordApi.getList({ page_size: 1000 })
    const statuses: Record<number, number> = {}
    
    if (allAlarms.results) {
      allAlarms.results.forEach((alarm: any) => {
        const status = alarm.alarm_status
        if (status !== undefined && status !== null) {
          statuses[status] = (statuses[status] || 0) + 1
        }
      })
    }

    alarmStats.value = { total, statuses }
  } catch (error: any) {
    console.error('获取报警记录统计失败:', error)
    ElMessage.error('获取报警记录统计失败: ' + (error.message || '未知错误'))
  }
}

// 获取预案统计
const fetchPlanStats = async () => {
  try {
    const stats = await emergencyPlanApi.getStatistics()
    planStats.value = stats || {}
  } catch (error: any) {
    console.error('获取预案统计失败:', error)
    ElMessage.error('获取预案统计失败: ' + (error.message || '未知错误'))
  }
}

// 获取演练统计
const fetchDrillStats = async () => {
  try {
    const stats = await drillEventApi.getStatistics()
    drillStats.value = stats || {}
  } catch (error: any) {
    console.error('获取演练统计失败:', error)
    ElMessage.error('获取演练统计失败: ' + (error.message || '未知错误'))
  }
}

// 获取安全资源统计
const fetchResourceStats = async () => {
  try {
    const stats = await safetyResourceApi.getStatistics()
    resourceStats.value = stats || {}
  } catch (error: any) {
    console.error('获取安全资源统计失败:', error)
    ElMessage.error('获取安全资源统计失败: ' + (error.message || '未知错误'))
  }
}

// 获取视频监控统计
const fetchVideoStats = async () => {
  try {
    const stats = await videoMonitorApi.getStatistics()
    videoStats.value = stats || {}
  } catch (error: any) {
    console.error('获取视频监控统计失败:', error)
    ElMessage.error('获取视频监控统计失败: ' + (error.message || '未知错误'))
  }
}

// 获取数据源统计
const fetchDatasourceStats = async () => {
  try {
    const stats = await datasourceApi.getStatistics()
    datasourceStats.value = stats || {}
  } catch (error: any) {
    console.error('获取数据源统计失败:', error)
    ElMessage.error('获取数据源统计失败: ' + (error.message || '未知错误'))
  }
}

// 获取叫应记录统计
const fetchCallStats = async () => {
  try {
    const stats = await callRecordApi.getStatistics()
    callStats.value = stats || {}
  } catch (error: any) {
    console.error('获取叫应记录统计失败:', error)
    ElMessage.error('获取叫应记录统计失败: ' + (error.message || '未知错误'))
  }
}

// 获取所有统计数据
const fetchAllStats = async () => {
  loading.value = true
  try {
    await Promise.all([
      fetchWarningStats(),
      fetchAlarmStats(),
      fetchPlanStats(),
      fetchDrillStats(),
      fetchResourceStats(),
      fetchVideoStats(),
      fetchDatasourceStats(),
      fetchCallStats(),
    ])
    lastUpdateTime.value = formatTime(new Date())
  } catch (error) {
    console.error('获取统计数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 获取最近预警事件
const fetchRecentWarnings = async () => {
  try {
    const response = await riskWarningApi.getList({
      page_size: 10,
      ordering: '-warning_time,-created_at',
    })
    recentWarnings.value = response.results || []
  } catch (error: any) {
    console.error('获取最近预警事件失败:', error)
  }
}

// 获取最近报警记录
const fetchRecentAlarms = async () => {
  try {
    const response = await alarmRecordApi.getList({
      page_size: 10,
      ordering: '-alarm_time,-created_at',
    })
    recentAlarms.value = response.results || []
  } catch (error: any) {
    console.error('获取最近报警记录失败:', error)
  }
}

// 获取最近预案执行记录
const fetchRecentPlanExecutions = async () => {
  try {
    const response = await planExecutionApi.getList({
      page_size: 10,
      ordering: '-start_time,-created_at',
    })
    recentPlanExecutions.value = response.results || []
  } catch (error: any) {
    console.error('获取最近预案执行记录失败:', error)
  }
}

// 获取最近演练事件
const fetchRecentDrillEvents = async () => {
  try {
    const response = await drillEventApi.getList({
      page_size: 10,
      ordering: '-event_time,-created_at',
    })
    recentDrillEvents.value = response.results || []
  } catch (error: any) {
    console.error('获取最近演练事件失败:', error)
  }
}

// 生成系统通知（基于数据源状态、预警发布等）
const generateNotifications = async () => {
  try {
    const newNotifications: Notification[] = []
    
    // 检查数据源状态
    try {
      const datasourceStatsData = await datasourceApi.getStatistics()
      if (datasourceStatsData && datasourceStatsData.status_stats) {
        const errorCount = datasourceStatsData.status_stats.find((s: any) => s.status === 'error' || s.status === 0)?.count || 0
        if (errorCount > 0) {
          newNotifications.push({
            id: Date.now() + 1,
            type: 'datasource',
            title: '数据源异常',
            content: `有 ${errorCount} 个数据源状态异常，请及时处理`,
            created_at: new Date().toISOString(),
            read: false,
          })
        }
      }
    } catch (error) {
      // 数据源统计失败，忽略
      console.warn('获取数据源统计失败:', error)
    }
    
    // 检查最新预警（红色I级和橙色Ⅱ级）
    try {
      const warnings = await riskWarningApi.getList({
        page_size: 5,
        ordering: '-warning_time',
      })
      if (warnings.results && warnings.results.length > 0) {
        warnings.results.forEach((warning: any) => {
          const warningTime = dayjs(warning.warning_time || warning.created_at)
          const levelId = warning.warning_level?.id || warning.warning_level
          // 只显示最近24小时内的红色I级和橙色Ⅱ级预警
          if (warningTime.isAfter(dayjs().subtract(24, 'hour')) && (levelId === 1 || levelId === 2)) {
            const levelName = levelId === 1 ? '红色I级' : '橙色Ⅱ级'
            newNotifications.push({
              id: warning.id || Date.now() + Math.random(),
              type: 'warning',
              title: `${levelName}预警发布`,
              content: warning.warning_title || warning.title || '重要预警',
              created_at: warning.warning_time || warning.created_at,
              read: false,
            })
          }
        })
      }
    } catch (error) {
      // 预警获取失败，忽略
      console.warn('获取预警数据失败:', error)
    }
    
    // 合并新通知和已有通知，去重
    const existingIds = new Set(notifications.value.map(n => n.id))
    const uniqueNewNotifications = newNotifications.filter(n => !existingIds.has(n.id))
    notifications.value = [...uniqueNewNotifications, ...notifications.value].slice(0, 20) // 最多保留20条
  } catch (error: any) {
    console.error('生成系统通知失败:', error)
  }
}

// 获取所有最近活动
const fetchAllRecentActivities = async () => {
  await Promise.all([
    fetchRecentWarnings(),
    fetchRecentAlarms(),
    fetchRecentPlanExecutions(),
    fetchRecentDrillEvents(),
    generateNotifications(),
  ])
}

// 手动刷新
const handleRefresh = async () => {
  loading.value = true
  try {
    await Promise.all([
      fetchAllStats(),
      fetchAllCharts(),
      fetchAllRecentActivities(),
    ])
    lastUpdateTime.value = formatTime(new Date())
    ElMessage.success('数据刷新成功')
  } catch (error) {
    console.error('刷新数据失败:', error)
    ElMessage.error('刷新数据失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 辅助函数：获取状态统计数量
const getStatusCount = (statusStats: any[], statusValue: string): number => {
  if (!statusStats || !Array.isArray(statusStats)) return 0
  const item = statusStats.find((s: any) => s.status === statusValue || s.plan_status === statusValue || s.drill_status === statusValue)
  return item?.count || 0
}

// 辅助函数：获取类型统计数量
const getTypeCount = (typeStats: any[], typeValue: number): number => {
  if (!typeStats || !Array.isArray(typeStats)) return 0
  const item = typeStats.find((t: any) => t.resource_type === typeValue)
  return item?.count || 0
}

// 辅助函数：获取响应状态统计数量
const getResponseStatusCount = (responseStats: any[], statusValue: string): number => {
  if (!responseStats || !Array.isArray(responseStats)) return 0
  const item = responseStats.find((s: any) => {
    if (statusValue === 'responded') {
      return s.response_status === 'responded' || s.response_status === 1
    } else if (statusValue === 'not_responded') {
      return s.response_status === 'not_responded' || s.response_status === 0
    }
    return false
  })
  return item?.count || 0
}

// 启动自动刷新
const startAutoRefresh = () => {
  stopAutoRefresh()
  refreshTimer = setInterval(async () => {
    if (!document.hidden) {
      try {
        // 静默刷新，不显示加载状态
        await Promise.all([
          fetchAllStats(),
          fetchAllCharts(),
          fetchAllRecentActivities(),
        ])
        lastUpdateTime.value = formatTime(new Date())
      } catch (error) {
        console.error('自动刷新数据失败:', error)
        // 自动刷新失败时不显示错误提示，避免打扰用户
      }
    }
  }, 5 * 60 * 1000) // 每5分钟刷新一次
}

// 停止自动刷新
const stopAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}

// 页面可见性变化处理
const handleVisibilityChange = async () => {
  if (!document.hidden) {
    // 页面重新可见时，立即刷新所有数据
    try {
      await Promise.all([
        fetchAllStats(),
        fetchAllCharts(),
        fetchAllRecentActivities(),
      ])
      lastUpdateTime.value = formatTime(new Date())
    } catch (error) {
      console.error('页面可见性变化时刷新数据失败:', error)
    }
    startAutoRefresh()
  } else {
    stopAutoRefresh()
  }
}

// 时间范围变化处理
const handleTimeRangeChange = () => {
  fetchAllCharts()
}

// 获取时间范围
const getTimeRange = () => {
  const days = parseInt(timeRange.value)
  const endTime = dayjs().format('YYYY-MM-DD HH:mm:ss')
  const startTime = dayjs().subtract(days, 'day').format('YYYY-MM-DD HH:mm:ss')
  return { startTime, endTime, days }
}

// 初始化图表
const initCharts = async () => {
  await nextTick()
  
  if (warningTrendChart.value && !warningTrendChartInstance) {
    warningTrendChartInstance = echarts.init(warningTrendChart.value)
  }
  if (alarmTrendChart.value && !alarmTrendChartInstance) {
    alarmTrendChartInstance = echarts.init(alarmTrendChart.value)
  }
  if (warningLevelChart.value && !warningLevelChartInstance) {
    warningLevelChartInstance = echarts.init(warningLevelChart.value)
  }
  if (alarmStatusChart.value && !alarmStatusChartInstance) {
    alarmStatusChartInstance = echarts.init(alarmStatusChart.value)
  }
  if (planTypeChart.value && !planTypeChartInstance) {
    planTypeChartInstance = echarts.init(planTypeChart.value)
  }
  if (drillStatusChart.value && !drillStatusChartInstance) {
    drillStatusChartInstance = echarts.init(drillStatusChart.value)
  }
  if (industryCompareChart.value && !industryCompareChartInstance) {
    industryCompareChartInstance = echarts.init(industryCompareChart.value)
  }
}

// 销毁图表
const disposeCharts = () => {
  warningTrendChartInstance?.dispose()
  alarmTrendChartInstance?.dispose()
  warningLevelChartInstance?.dispose()
  alarmStatusChartInstance?.dispose()
  planTypeChartInstance?.dispose()
  drillStatusChartInstance?.dispose()
  industryCompareChartInstance?.dispose()
  
  warningTrendChartInstance = null
  alarmTrendChartInstance = null
  warningLevelChartInstance = null
  alarmStatusChartInstance = null
  planTypeChartInstance = null
  drillStatusChartInstance = null
  industryCompareChartInstance = null
}

// 渲染预警事件趋势图
const renderWarningTrendChart = async () => {
  if (!warningTrendChartInstance) return
  
  try {
    const { startTime, endTime, days } = getTimeRange()
    const response = await riskWarningApi.getList({ 
      page_size: 1000,
      start_time: startTime,
      end_time: endTime,
    })
    
    // 按日期分组统计
    const dateMap: Record<string, number> = {}
    const dates: string[] = []
    
    for (let i = days - 1; i >= 0; i--) {
      const date = dayjs().subtract(i, 'day').format('MM-DD')
      dates.push(date)
      dateMap[date] = 0
    }
    
    if (response.results) {
      response.results.forEach((warning: any) => {
        const date = dayjs(warning.warning_time || warning.created_at).format('MM-DD')
        if (dateMap.hasOwnProperty(date) && dateMap[date] !== undefined) {
          dateMap[date] = (dateMap[date] || 0) + 1
        }
      })
    }
    
    const option = {
      tooltip: {
        trigger: 'axis',
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true,
      },
      xAxis: {
        type: 'category',
        data: dates,
        boundaryGap: false,
      },
      yAxis: {
        type: 'value',
      },
      series: [
        {
          name: '预警数量',
          type: 'line',
          smooth: true,
          data: dates.map(date => dateMap[date]),
          itemStyle: {
            color: '#f56c6c',
          },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(245, 108, 108, 0.3)' },
                { offset: 1, color: 'rgba(245, 108, 108, 0.1)' },
              ],
            },
          },
        },
      ],
    }
    
    warningTrendChartInstance.setOption(option)
  } catch (error: any) {
    console.error('渲染预警事件趋势图失败:', error)
  }
}

// 渲染报警记录趋势图
const renderAlarmTrendChart = async () => {
  if (!alarmTrendChartInstance) return
  
  try {
    const { startTime, endTime, days } = getTimeRange()
    const response = await alarmRecordApi.getList({ 
      page_size: 1000,
      start_time: startTime,
      end_time: endTime,
    })
    
    // 按日期分组统计
    const dateMap: Record<string, number> = {}
    const dates: string[] = []
    
    for (let i = days - 1; i >= 0; i--) {
      const date = dayjs().subtract(i, 'day').format('MM-DD')
      dates.push(date)
      dateMap[date] = 0
    }
    
    if (response.results) {
      response.results.forEach((alarm: any) => {
        const date = dayjs(alarm.alarm_time || alarm.created_at).format('MM-DD')
        if (dateMap.hasOwnProperty(date) && dateMap[date] !== undefined) {
          dateMap[date] = (dateMap[date] || 0) + 1
        }
      })
    }
    
    const option = {
      tooltip: {
        trigger: 'axis',
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true,
      },
      xAxis: {
        type: 'category',
        data: dates,
        boundaryGap: false,
      },
      yAxis: {
        type: 'value',
      },
      series: [
        {
          name: '报警数量',
          type: 'line',
          smooth: true,
          data: dates.map(date => dateMap[date]),
          itemStyle: {
            color: '#e6a23c',
          },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(230, 162, 60, 0.3)' },
                { offset: 1, color: 'rgba(230, 162, 60, 0.1)' },
              ],
            },
          },
        },
      ],
    }
    
    alarmTrendChartInstance.setOption(option)
  } catch (error: any) {
    console.error('渲染报警记录趋势图失败:', error)
  }
}

// 渲染预警级别分布图
const renderWarningLevelChart = () => {
  if (!warningLevelChartInstance) return
  
  const levelNames: Record<number, string> = {
    1: '红色I级',
    2: '橙色Ⅱ级',
    3: '黄色Ⅲ级',
    4: '蓝色Ⅳ级',
  }
  
  const levelColors: Record<number, string> = {
    1: '#f56c6c',
    2: '#e6a23c',
    3: '#e6a23c',
    4: '#409eff',
  }
  
  const data = Object.keys(warningStats.value.levels || {}).map(levelId => ({
    value: warningStats.value.levels[parseInt(levelId)],
    name: levelNames[parseInt(levelId)] || `级别${levelId}`,
    itemStyle: {
      color: levelColors[parseInt(levelId)] || '#909399',
    },
  })).filter(item => (item.value ?? 0) > 0)
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)',
    },
    legend: {
      orient: 'vertical',
      left: 'left',
    },
    series: [
      {
        name: '预警级别',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2,
        },
        label: {
          show: true,
          formatter: '{b}\n{c} ({d}%)',
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: 'bold',
          },
        },
        data,
      },
    ],
  }
  
  warningLevelChartInstance.setOption(option)
}

// 渲染报警状态分布图
const renderAlarmStatusChart = () => {
  if (!alarmStatusChartInstance) return
  
  const statusNames: Record<number, string> = {
    0: '待处理',
    1: '处理中',
    2: '已处理',
    3: '已忽略',
  }
  
  const statusColors: Record<number, string> = {
    0: '#e6a23c',
    1: '#409eff',
    2: '#67c23a',
    3: '#909399',
  }
  
  const data = Object.keys(alarmStats.value.statuses || {}).map(status => ({
    value: alarmStats.value.statuses[parseInt(status)],
    name: statusNames[parseInt(status)] || `状态${status}`,
    itemStyle: {
      color: statusColors[parseInt(status)] || '#909399',
    },
  })).filter(item => (item.value ?? 0) > 0)
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)',
    },
    legend: {
      orient: 'vertical',
      left: 'left',
    },
    series: [
      {
        name: '报警状态',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2,
        },
        label: {
          show: true,
          formatter: '{b}\n{c} ({d}%)',
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: 'bold',
          },
        },
        data,
      },
    ],
  }
  
  alarmStatusChartInstance.setOption(option)
}

// 渲染预案类型分布图
const renderPlanTypeChart = () => {
  if (!planTypeChartInstance) return
  
  const typeStats = planStats.value.type_stats || []
  const data = typeStats.map((item: any) => ({
    value: item.count,
    name: item.plan_type || '未知类型',
  }))
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: data.map((item: any) => item.name),
      axisLabel: {
        rotate: 45,
      },
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        name: '预案数量',
        type: 'bar',
        data: data.map((item: any) => item.value),
        itemStyle: {
          color: '#409eff',
        },
      },
    ],
  }
  
  planTypeChartInstance.setOption(option)
}

// 渲染演练完成情况图
const renderDrillStatusChart = () => {
  if (!drillStatusChartInstance) return
  
  const statusStats = drillStats.value.status_stats || []
  const statusNames: Record<string, string> = {
    completed: '已完成',
    in_progress: '进行中',
    not_started: '未开始',
  }
  
  const data = statusStats.map((item: any) => ({
    value: item.count,
    name: statusNames[item.drill_status] || item.drill_status,
  }))
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: data.map((item: any) => item.name),
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        name: '演练数量',
        type: 'bar',
        data: data.map((item: any) => item.value),
        itemStyle: {
          color: (params: any) => {
            const colors: Record<string, string> = {
              '已完成': '#67c23a',
              '进行中': '#409eff',
              '未开始': '#909399',
            }
            return colors[params.name] || '#909399'
          },
        },
      },
    ],
  }
  
  drillStatusChartInstance.setOption(option)
}

// 渲染行业态势对比图
const renderIndustryCompareChart = async () => {
  if (!industryCompareChartInstance) return
  
  try {
    // 获取预警和报警的行业统计
    const warnings = await riskWarningApi.getList({ page_size: 1000 })
    const alarms = await alarmRecordApi.getList({ page_size: 1000 })
    
    const industryNames: Record<number, string> = {
      1: '危险化学品',
      2: '防汛',
      3: '交通运输',
      4: '森林火灾',
    }
    
    const warningIndustryMap: Record<number, number> = {}
    const alarmIndustryMap: Record<number, number> = {}
    
    if (warnings.results) {
      warnings.results.forEach((warning: any) => {
        const industry = warning.industry_type
        if (industry) {
          warningIndustryMap[industry] = (warningIndustryMap[industry] || 0) + 1
        }
      })
    }
    
    if (alarms.results) {
      alarms.results.forEach((alarm: any) => {
        const industry = alarm.industry_type
        if (industry) {
          alarmIndustryMap[industry] = (alarmIndustryMap[industry] || 0) + 1
        }
      })
    }
    
    const industries = [1, 2, 3, 4]
    const industryLabels = industries.map(id => industryNames[id] || `行业${id}`)
    const warningData = industries.map(id => warningIndustryMap[id] || 0)
    const alarmData = industries.map(id => alarmIndustryMap[id] || 0)
    
    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow',
        },
      },
      legend: {
        data: ['预警数量', '报警数量'],
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true,
      },
      xAxis: {
        type: 'category',
        data: industryLabels,
        axisLabel: {
          rotate: 45,
        },
      },
      yAxis: {
        type: 'value',
      },
      series: [
        {
          name: '预警数量',
          type: 'bar',
          data: warningData,
          itemStyle: {
            color: '#f56c6c',
          },
        },
        {
          name: '报警数量',
          type: 'bar',
          data: alarmData,
          itemStyle: {
            color: '#e6a23c',
          },
        },
      ],
    }
    
    industryCompareChartInstance.setOption(option)
  } catch (error: any) {
    console.error('渲染行业态势对比图失败:', error)
  }
}

// 获取所有图表数据
const fetchAllCharts = async () => {
  await initCharts()
  await Promise.all([
    renderWarningTrendChart(),
    renderAlarmTrendChart(),
    renderWarningLevelChart(),
    renderAlarmStatusChart(),
    renderPlanTypeChart(),
    renderDrillStatusChart(),
    renderIndustryCompareChart(),
  ])
}

// 监听统计数据变化，更新图表
watch([warningStats, alarmStats, planStats, drillStats], () => {
  nextTick(() => {
    renderWarningLevelChart()
    renderAlarmStatusChart()
    renderPlanTypeChart()
    renderDrillStatusChart()
  })
})

// 格式化活动时间
const formatActivityTime = (time: string | undefined): string => {
  if (!time) return ''
  const date = dayjs(time)
  const now = dayjs()
  const diffMinutes = now.diff(date, 'minute')
  const diffHours = now.diff(date, 'hour')
  const diffDays = now.diff(date, 'day')
  
  if (diffMinutes < 1) return '刚刚'
  if (diffMinutes < 60) return `${diffMinutes}分钟前`
  if (diffHours < 24) return `${diffHours}小时前`
  if (diffDays < 7) return `${diffDays}天前`
  return date.format('MM-DD HH:mm')
}

// 预警级别相关函数
const getWarningLevelName = (level: any): string => {
  if (!level) return '未知级别'
  const levelId = level.id || level
  const levelNames: Record<number, string> = {
    1: '红色I级',
    2: '橙色Ⅱ级',
    3: '黄色Ⅲ级',
    4: '蓝色Ⅳ级',
  }
  return levelNames[levelId] || `级别${levelId}`
}

const getWarningLevelType = (level: any): string => {
  if (!level) return ''
  const levelId = level.id || level
  const types: Record<number, string> = {
    1: 'danger',
    2: 'warning',
    3: 'warning',
    4: 'info',
  }
  return types[levelId] || ''
}

// 预警状态相关函数
const getWarningStatusName = (status: number | undefined): string => {
  if (status === undefined || status === null) return '未知状态'
  const statusNames: Record<number, string> = {
    0: '待发布',
    1: '已发布',
    2: '处置中',
    3: '已处置',
    4: '已关闭',
  }
  return statusNames[status] || `状态${status}`
}

const getWarningStatusType = (status: number | undefined): string => {
  if (status === undefined || status === null) return ''
  const types: Record<number, string> = {
    0: 'info',
    1: 'success',
    2: 'warning',
    3: 'success',
    4: 'info',
  }
  return types[status] || ''
}

// 报警状态相关函数
const getAlarmStatusName = (status: number | undefined): string => {
  if (status === undefined || status === null) return '未知状态'
  const statusNames: Record<number, string> = {
    0: '待处理',
    1: '处理中',
    2: '已处理',
    3: '已忽略',
  }
  return statusNames[status] || `状态${status}`
}

const getAlarmStatusType = (status: number | undefined): string => {
  if (status === undefined || status === null) return ''
  const types: Record<number, string> = {
    0: 'warning',
    1: 'primary',
    2: 'success',
    3: 'info',
  }
  return types[status] || ''
}

// 预案执行状态相关函数
const getExecutionStatusName = (status: number | undefined): string => {
  if (status === undefined || status === null) return '未知状态'
  const statusNames: Record<number, string> = {
    0: '待启动',
    1: '执行中',
    2: '已完成',
    3: '已终止',
  }
  return statusNames[status] || `状态${status}`
}

const getExecutionStatusType = (status: number | undefined): string => {
  if (status === undefined || status === null) return ''
  const types: Record<number, string> = {
    0: 'info',
    1: 'primary',
    2: 'success',
    3: 'danger',
  }
  return types[status] || ''
}

// 演练类型相关函数
const getDrillTypeName = (type: number | string | undefined): string => {
  if (!type) return '未知类型'
  const typeNames: Record<number | string, string> = {
    1: '桌面演练',
    2: '功能演练',
    3: '全面演练',
    'desktop': '桌面演练',
    'functional': '功能演练',
    'full': '全面演练',
  }
  return typeNames[type] || `类型${type}`
}

// 演练状态相关函数
const getDrillStatusName = (status: number | string | undefined): string => {
  if (!status) return '未知状态'
  const statusNames: Record<number | string, string> = {
    0: '未开始',
    1: '进行中',
    2: '已完成',
    'not_started': '未开始',
    'in_progress': '进行中',
    'completed': '已完成',
  }
  return statusNames[status] || `状态${status}`
}

const getDrillStatusType = (status: number | string | undefined): string => {
  if (!status) return ''
  const types: Record<number | string, string> = {
    0: 'info',
    1: 'primary',
    2: 'success',
    'not_started': 'info',
    'in_progress': 'primary',
    'completed': 'success',
  }
  return types[status] || ''
}

// 点击处理函数
const handleViewWarning = (id: number) => {
  router.push({ path: '/risk/warning', query: { id } })
}

const handleViewAlarm = (id: number) => {
  router.push({ path: '/risk/alarm', query: { id } })
}

const handleViewPlanExecution = (id: number) => {
  router.push({ path: '/plan/execution', query: { id } })
}

const handleViewDrillEvent = (id: number) => {
  router.push({ path: '/drill/event', query: { id } })
}

const handleViewNotification = (notification: Notification) => {
  notification.read = true
  // 根据通知类型跳转到相应页面
  if (notification.type === 'warning') {
    // 从通知内容中提取ID或跳转到预警列表
    router.push('/risk/warning')
  } else if (notification.type === 'alarm') {
    router.push('/risk/alarm')
  } else if (notification.type === 'datasource') {
    router.push('/system/datasource')
  }
}

const handleMarkAllRead = () => {
  notifications.value.forEach(n => {
    n.read = true
  })
}

// 快捷操作处理函数
const handleQuickCreateWarning = () => {
  router.push('/risk/warning?action=create')
}

const handleQuickCreateAlarm = () => {
  router.push('/risk/alarm?action=create')
}

const handleQuickStartPlanExecution = () => {
  router.push('/plan/execution?action=create')
}

const handleQuickCreateDrillEvent = () => {
  router.push('/drill/event?action=create')
}

const handleGoToScreen = (_type: string) => {
  // 跳转到大屏展示系统
  // 大屏系统在 screen 项目中，这里跳转到大屏总览页面
  router.push('/screen/overview')
  // 如果需要直接跳转到具体大屏，可以使用外部链接或路由参数
  // 注意：大屏系统是独立项目，可能需要在新窗口打开或使用不同的路由
}

onMounted(async () => {
  // 首次加载数据
  loading.value = true
  try {
    await Promise.all([
      fetchAllStats(),
      fetchAllCharts(),
      fetchAllRecentActivities(),
    ])
    lastUpdateTime.value = formatTime(new Date())
  } catch (error) {
    console.error('初始化数据失败:', error)
    ElMessage.error('加载数据失败，请稍后刷新')
  } finally {
    loading.value = false
  }
  
  // 启动自动刷新
  startAutoRefresh()
  document.addEventListener('visibilitychange', handleVisibilityChange)
  
  // 监听窗口大小变化，自动调整图表大小
  window.addEventListener('resize', () => {
    warningTrendChartInstance?.resize()
    alarmTrendChartInstance?.resize()
    warningLevelChartInstance?.resize()
    alarmStatusChartInstance?.resize()
    planTypeChartInstance?.resize()
    drillStatusChartInstance?.resize()
    industryCompareChartInstance?.resize()
  })
})

onUnmounted(() => {
  stopAutoRefresh()
  document.removeEventListener('visibilitychange', handleVisibilityChange)
  disposeCharts()
  window.removeEventListener('resize', () => {})
})
</script>

<style scoped lang="scss">
.dashboard {
  padding: 20px;
  background-color: #f5f5f5;
  min-height: calc(100vh - 60px);
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;

  h1 {
    margin: 0;
    font-size: 24px;
    font-weight: 500;
    color: #303133;
  }

  .header-actions {
    display: flex;
    align-items: center;
    gap: 16px;

    .last-update-time {
      font-size: 12px;
      color: #909399;
    }
  }
}

.statistics-cards {
  margin-bottom: 20px;
}

.stat-card {
  margin-bottom: 20px;
  transition: all 0.3s;

  &:hover {
    transform: translateY(-4px);
  }
}

.stat-content {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: #fff;
  flex-shrink: 0;

  &.warning-icon {
    background: linear-gradient(135deg, #f56c6c 0%, #e74c3c 100%);
  }

  &.alarm-icon {
    background: linear-gradient(135deg, #e6a23c 0%, #f39c12 100%);
  }

  &.plan-icon {
    background: linear-gradient(135deg, #409eff 0%, #3498db 100%);
  }

  &.drill-icon {
    background: linear-gradient(135deg, #67c23a 0%, #27ae60 100%);
  }

  &.resource-icon {
    background: linear-gradient(135deg, #909399 0%, #7f8c8d 100%);
  }

  &.video-icon {
    background: linear-gradient(135deg, #9c27b0 0%, #8e44ad 100%);
  }

  &.datasource-icon {
    background: linear-gradient(135deg, #00bcd4 0%, #16a085 100%);
  }

  &.call-icon {
    background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
  }
}

.stat-info {
  flex: 1;
  min-width: 0;
}

.stat-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 12px;
  line-height: 1;
}

.stat-detail {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 12px;
  color: #606266;

  .level-item,
  .status-item,
  .type-item {
    padding: 2px 8px;
    border-radius: 4px;
    background-color: #f5f7fa;
  }

  .level-red {
    color: #f56c6c;
    background-color: #fef0f0;
  }

  .level-orange {
    color: #e6a23c;
    background-color: #fdf6ec;
  }

  .level-yellow {
    color: #e6a23c;
    background-color: #fdf6ec;
  }

  .level-blue {
    color: #409eff;
    background-color: #ecf5ff;
  }

  .status-online {
    color: #67c23a;
    background-color: #f0f9ff;
  }

  .status-offline {
    color: #909399;
    background-color: #f5f7fa;
  }

  .status-normal {
    color: #67c23a;
    background-color: #f0f9ff;
  }

  .status-error {
    color: #f56c6c;
    background-color: #fef0f0;
  }

  .status-success {
    color: #67c23a;
    background-color: #f0f9ff;
  }

  .status-warning {
    color: #e6a23c;
    background-color: #fdf6ec;
  }
}

// 图表区域样式
.charts-section {
  margin-top: 20px;
}

.chart-card {
  .chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .chart-title {
      font-size: 16px;
      font-weight: 500;
      color: #303133;
    }

    .chart-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
  }
}

.chart-item {
  margin-bottom: 20px;

  .chart-item-title {
    font-size: 14px;
    font-weight: 500;
    color: #606266;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #ebeef5;
  }

  .chart-container {
    width: 100%;
    height: 300px;
    min-height: 300px;
  }
}

// 最近活动/通知区域样式
.activities-section {
  margin-top: 20px;
  margin-bottom: 20px;
}

// 主内容区域样式
.main-content-section {
  margin-top: 20px;

  .main-tabs {
    :deep(.el-tabs__header) {
      margin-bottom: 20px;
    }

    :deep(.el-tabs__content) {
      padding: 0;
    }
  }
}

.activities-card,
.notifications-card {
  height: 100%;
  min-height: 500px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .card-title {
    font-size: 16px;
    font-weight: 500;
    color: #303133;
  }

  .notification-badge {
    cursor: pointer;
  }
}

.activity-tabs {
  :deep(.el-tabs__content) {
    padding-top: 12px;
  }
}

.activity-list {
  max-height: 600px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid transparent;

  &:hover {
    background-color: #f5f7fa;
    border-color: #e4e7ed;
  }

  .activity-icon {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    color: #fff;
    flex-shrink: 0;

    &.warning-icon {
      background: linear-gradient(135deg, #f56c6c 0%, #e74c3c 100%);
    }

    &.alarm-icon {
      background: linear-gradient(135deg, #e6a23c 0%, #f39c12 100%);
    }

    &.plan-icon {
      background: linear-gradient(135deg, #409eff 0%, #3498db 100%);
    }

    &.drill-icon {
      background: linear-gradient(135deg, #67c23a 0%, #27ae60 100%);
    }
  }

  .activity-content {
    flex: 1;
    min-width: 0;

    .activity-title {
      font-size: 14px;
      font-weight: 500;
      color: #303133;
      margin-bottom: 8px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .activity-meta {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      font-size: 12px;
      color: #909399;

      .activity-time {
        margin: 0 4px;
      }

      .activity-handler {
        color: #606266;
      }
    }
  }
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #909399;
  font-size: 14px;
}

.notification-list {
  max-height: 600px;
  overflow-y: auto;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid transparent;
  position: relative;

  &:hover {
    background-color: #f5f7fa;
    border-color: #e4e7ed;
  }

  &.unread {
    background-color: #f0f9ff;
    border-color: #b3d8ff;
  }

  .notification-icon {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    color: #fff;
    flex-shrink: 0;

    &.notification-warning {
      background: linear-gradient(135deg, #f56c6c 0%, #e74c3c 100%);
    }

    &.notification-alarm {
      background: linear-gradient(135deg, #e6a23c 0%, #f39c12 100%);
    }

    &.notification-datasource {
      background: linear-gradient(135deg, #00bcd4 0%, #16a085 100%);
    }

    &.notification-system {
      background: linear-gradient(135deg, #909399 0%, #7f8c8d 100%);
    }
  }

  .notification-content {
    flex: 1;
    min-width: 0;

    .notification-title {
      font-size: 14px;
      font-weight: 500;
      color: #303133;
      margin-bottom: 4px;
    }

    .notification-desc {
      font-size: 12px;
      color: #606266;
      margin-bottom: 4px;
      line-height: 1.5;
    }

    .notification-time {
      font-size: 12px;
      color: #909399;
    }
  }

  .notification-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #f56c6c;
    flex-shrink: 0;
    margin-top: 4px;
  }
}

// 快捷操作区域样式
.quick-actions-section {
  margin-top: 20px;
}

.quick-actions-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .card-title {
      font-size: 16px;
      font-weight: 500;
      color: #303133;
    }
  }
}

.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;

  .quick-action-btn {
    height: auto;
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    text-align: left;
    border-radius: 8px;
    transition: all 0.3s;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    :deep(.el-icon) {
      font-size: 24px;
      margin-bottom: 8px;
    }

    .action-content {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 4px;

      .action-title {
        font-size: 14px;
        font-weight: 500;
        line-height: 1.2;
      }

      .action-desc {
        font-size: 12px;
        opacity: 0.8;
        line-height: 1.2;
      }
    }
  }
}

// 响应式布局
@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .stat-content {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .quick-actions-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 12px;
  }
}
</style>
