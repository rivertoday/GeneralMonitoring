<template>
  <div v-if="visible" class="dialog-overlay" @click="handleOverlayClick">
    <div class="dialog-container" @click.stop>
      <div class="dialog-header">
        <h3 class="dialog-title">区域态势详情</h3>
        <button class="close-btn" @click="handleClose">×</button>
      </div>
      <div class="dialog-content" v-if="regionData">
        <div class="info-section">
          <div class="info-item">
            <span class="info-label">街道名称：</span>
            <span class="info-value">{{ regionData.street }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">风险等级：</span>
            <span class="info-value" :class="getRiskColorClass(regionData.risk_color)">
              {{ regionData.risk_label }}
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">统计日期：</span>
            <span class="info-value">{{ formatDate(regionData.stat_date) }}</span>
          </div>
        </div>

        <div class="stats-section">
          <h4 class="section-title">风险统计</h4>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-label">报警数量</div>
              <div class="stat-value">{{ regionData.alarm_count || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">预警数量</div>
              <div class="stat-value">{{ regionData.warning_count || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">风险隐患</div>
              <div class="stat-value">{{ regionData.risk_count || 0 }}</div>
            </div>
          </div>
        </div>

        <div class="risk-level-section">
          <h4 class="section-title">风险等级分布</h4>
          <div class="risk-level-grid">
            <div class="risk-level-item red">
              <div class="risk-level-label">红色I级</div>
              <div class="risk-level-value">{{ regionData.risk_level_1_count || 0 }}</div>
            </div>
            <div class="risk-level-item orange">
              <div class="risk-level-label">橙色Ⅱ级</div>
              <div class="risk-level-value">{{ regionData.risk_level_2_count || 0 }}</div>
            </div>
            <div class="risk-level-item yellow">
              <div class="risk-level-label">黄色Ⅲ级</div>
              <div class="risk-level-value">{{ regionData.risk_level_3_count || 0 }}</div>
            </div>
            <div class="risk-level-item blue">
              <div class="risk-level-label">蓝色Ⅳ级</div>
              <div class="risk-level-value">{{ regionData.risk_level_4_count || 0 }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  visible: boolean
  regionData: any
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
}>()

const handleClose = () => {
  emit('update:visible', false)
}

const handleOverlayClick = () => {
  emit('update:visible', false)
}

const getRiskColorClass = (riskColor: string | null) => {
  if (!riskColor) return ''
  return `risk-${riskColor}`
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  })
}
</script>

<style scoped lang="scss">
@use '@/styles/variables.scss' as *;

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
  backdrop-filter: blur(4px);
}

.dialog-container {
  background: rgba(0, 20, 40, 0.95);
  border: 1px solid rgba(64, 158, 255, 0.3);
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}

.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(64, 158, 255, 0.2);
}

.dialog-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #409eff;
}

.close-btn {
  background: none;
  border: none;
  color: #e0e0e0;
  font-size: 28px;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.3s;

  &:hover {
    background: rgba(255, 255, 255, 0.1);
    color: #409eff;
  }
}

.dialog-content {
  padding: 24px;
}

.info-section {
  margin-bottom: 24px;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  font-size: 14px;

  &:last-child {
    margin-bottom: 0;
  }
}

.info-label {
  color: #999;
  min-width: 100px;
}

.info-value {
  color: #e0e0e0;
  font-weight: 500;

  &.risk-red {
    color: #ff4d4f;
  }

  &.risk-orange {
    color: #ffa940;
  }

  &.risk-yellow {
    color: #ffd666;
  }

  &.risk-blue {
    color: #1890ff;
  }
}

.stats-section,
.risk-level-section {
  margin-bottom: 24px;

  &:last-child {
    margin-bottom: 0;
  }
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #409eff;
  margin: 0 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(64, 158, 255, 0.2);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.stat-item {
  background: rgba(64, 158, 255, 0.1);
  border: 1px solid rgba(64, 158, 255, 0.3);
  border-radius: 8px;
  padding: 16px;
  text-align: center;
}

.stat-label {
  font-size: 13px;
  color: #999;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}

.risk-level-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.risk-level-item {
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  border: 2px solid;

  &.red {
    background: rgba(255, 0, 0, 0.1);
    border-color: rgba(255, 0, 0, 0.5);
  }

  &.orange {
    background: rgba(255, 165, 0, 0.1);
    border-color: rgba(255, 165, 0, 0.5);
  }

  &.yellow {
    background: rgba(255, 255, 0, 0.1);
    border-color: rgba(255, 255, 0, 0.5);
  }

  &.blue {
    background: rgba(0, 0, 255, 0.1);
    border-color: rgba(0, 0, 255, 0.5);
  }
}

.risk-level-label {
  font-size: 13px;
  color: #999;
  margin-bottom: 8px;
}

.risk-level-value {
  font-size: 20px;
  font-weight: bold;
  color: #e0e0e0;
}
</style>

