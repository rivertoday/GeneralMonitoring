<template>
  <div class="emergency-call">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>一键叫应</h2>
    </div>

    <!-- 叫应表单 -->
    <el-card class="form-card">
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="120px"
      >
        <el-form-item label="叫应类型" prop="call_type">
          <el-radio-group v-model="formData.call_type" @change="handleCallTypeChange">
            <el-radio :label="1">常态化叫应</el-radio>
            <el-radio :label="2">非常态化叫应</el-radio>
          </el-radio-group>
        </el-form-item>

        <!-- 常态化叫应：选择叫应对象 -->
        <template v-if="formData.call_type === 1">
          <el-form-item label="叫应对象" prop="target_ids">
            <el-select
              v-model="formData.target_ids"
              placeholder="请选择叫应对象（可多选）"
              multiple
              filterable
              style="width: 100%"
            >
              <el-option
                v-for="target in targetOptions"
                :key="target.id"
                :label="`${target.target_name} (${target.target_type_display})`"
                :value="target.id"
              />
            </el-select>
            <div class="form-tip">请选择需要叫应的对象，支持多选</div>
          </el-form-item>
        </template>

        <!-- 非常态化叫应：选择叫应人员或分组 -->
        <template v-if="formData.call_type === 2">
          <el-form-item label="叫应人员" prop="person_ids">
            <el-select
              v-model="formData.person_ids"
              placeholder="请选择叫应人员（可多选）"
              multiple
              filterable
              style="width: 100%"
            >
              <el-option
                v-for="person in personOptions"
                :key="person.id"
                :label="`${person.person_name} (${person.mobile_phone})`"
                :value="person.id"
              />
            </el-select>
            <div class="form-tip">请选择需要叫应的人员，支持多选</div>
          </el-form-item>
          <el-form-item label="叫应分组" prop="group_ids">
            <el-select
              v-model="formData.group_ids"
              placeholder="请选择叫应分组（可多选）"
              multiple
              filterable
              style="width: 100%"
            >
              <el-option
                v-for="group in groupOptions"
                :key="group.id"
                :label="group.group_name"
                :value="group.id"
              />
            </el-select>
            <div class="form-tip">选择分组后，该分组下的所有人员将被叫应</div>
          </el-form-item>
        </template>

        <el-form-item label="叫应渠道" prop="call_channel">
          <el-radio-group v-model="formData.call_channel">
            <el-radio value="system">系统消息</el-radio>
            <el-radio value="sms">短信</el-radio>
            <el-radio value="phone">电话</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="叫应内容" prop="call_content">
          <el-input
            v-model="formData.call_content"
            type="textarea"
            :rows="6"
            placeholder="请输入叫应内容"
            maxlength="1000"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="关联预警ID">
          <el-input-number
            v-model="formData.warning_id"
            :min="1"
            placeholder="请输入预警ID（可选）"
            style="width: 100%"
            :precision="0"
          />
          <div class="form-tip">如果是预警触发的叫应，可填写关联的预警ID</div>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="submitLoading" @click="handleSubmit" size="large">
            <el-icon><Phone /></el-icon>
            一键叫应
          </el-button>
          <el-button @click="handleReset" size="large">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 叫应结果提示 -->
    <el-card v-if="callResult" class="result-card">
      <template #header>
        <div class="result-header">
          <span>叫应结果</span>
          <el-button type="primary" link @click="goToRecords">查看叫应记录</el-button>
        </div>
      </template>
      <el-alert
        :title="`一键叫应成功，已创建 ${callResult.created_count} 条叫应记录`"
        type="success"
        :closable="false"
        show-icon
      >
        <template #default>
          <div class="result-content">
            <p>成功创建了 {{ callResult.created_count }} 条叫应记录</p>
            <p v-if="callResult.record_ids.length > 0">
              记录ID: {{ callResult.record_ids.join(', ') }}
            </p>
          </div>
        </template>
      </el-alert>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { Phone } from '@element-plus/icons-vue'
import { emergencyCallApi, callTargetApi, callPersonApi, callGroupApi } from '@/api/modules/call'
import type {
  EmergencyCallData,
  EmergencyCallResponse,
  CallType,
  CallChannel,
} from '@/types/modules/call'
import type { CallTarget } from '@/types/modules/call'
import type { CallPerson } from '@/types/modules/call'
import type { CallGroup } from '@/types/modules/call'

const router = useRouter()

// 加载状态
const submitLoading = ref(false)
const loading = ref(false)

// 选项数据
const targetOptions = ref<CallTarget[]>([])
const personOptions = ref<CallPerson[]>([])
const groupOptions = ref<CallGroup[]>([])

// 叫应结果
const callResult = ref<EmergencyCallResponse | null>(null)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<EmergencyCallData>({
  call_type: 1,
  call_source: 2, // 默认一键叫应
  target_ids: [],
  person_ids: [],
  group_ids: [],
  call_channel: 'system',
  call_content: '',
  warning_id: null,
})

// 表单验证规则
const formRules: FormRules = {
  call_type: [
    { required: true, message: '请选择叫应类型', trigger: 'change' },
  ],
  target_ids: [
    {
      validator: (rule, value, callback) => {
        if (formData.call_type === 1 && (!value || value.length === 0)) {
          callback(new Error('常态化叫应必须选择至少一个叫应对象'))
        } else {
          callback()
        }
      },
      trigger: 'change',
    },
  ],
  person_ids: [
    {
      validator: (rule, value, callback) => {
        if (formData.call_type === 2 && (!value || value.length === 0) && (!formData.group_ids || formData.group_ids.length === 0)) {
          callback(new Error('非常态化叫应必须选择至少一个叫应人员或分组'))
        } else {
          callback()
        }
      },
      trigger: 'change',
    },
  ],
  group_ids: [
    {
      validator: (rule, value, callback) => {
        if (formData.call_type === 2 && (!formData.person_ids || formData.person_ids.length === 0) && (!value || value.length === 0)) {
          callback(new Error('非常态化叫应必须选择至少一个叫应人员或分组'))
        } else {
          callback()
        }
      },
      trigger: 'change',
    },
  ],
  call_channel: [
    { required: true, message: '请选择叫应渠道', trigger: 'change' },
  ],
  call_content: [
    { required: true, message: '请输入叫应内容', trigger: 'blur' },
    { min: 5, message: '叫应内容至少5个字符', trigger: 'blur' },
  ],
}

// 获取叫应对象列表
const fetchTargets = async () => {
  try {
    const response = await callTargetApi.getList({ page_size: 1000, status: 1 })
    targetOptions.value = response.results
  } catch (error: any) {
    console.error('获取叫应对象列表失败:', error)
  }
}

// 获取叫应人员列表
const fetchPersons = async () => {
  try {
    const response = await callPersonApi.getList({ page_size: 1000, status: 1 })
    personOptions.value = response.results
  } catch (error: any) {
    console.error('获取叫应人员列表失败:', error)
  }
}

// 获取叫应分组列表
const fetchGroups = async () => {
  try {
    const response = await callGroupApi.getList({ page_size: 1000, status: 1 })
    groupOptions.value = response.results
  } catch (error: any) {
    console.error('获取叫应分组列表失败:', error)
  }
}

// 叫应类型变化
const handleCallTypeChange = () => {
  // 清空选择
  formData.target_ids = []
  formData.person_ids = []
  formData.group_ids = []
  formRef.value?.clearValidate()
  callResult.value = null
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    submitLoading.value = true
    callResult.value = null

    const data: EmergencyCallData = {
      call_type: formData.call_type,
      call_source: 2, // 一键叫应
      call_channel: formData.call_channel,
      call_content: formData.call_content,
    }

    if (formData.call_type === 1) {
      // 常态化叫应
      data.target_ids = formData.target_ids
    } else {
      // 非常态化叫应
      if (formData.person_ids && formData.person_ids.length > 0) {
        data.person_ids = formData.person_ids
      }
      if (formData.group_ids && formData.group_ids.length > 0) {
        data.group_ids = formData.group_ids
      }
    }

    if (formData.warning_id) {
      data.warning_id = formData.warning_id
    }

    const result = await emergencyCallApi.call(data)
    callResult.value = result
    ElMessage.success(`一键叫应成功，已创建 ${result.created_count} 条叫应记录`)
    
    // 滚动到结果区域
    setTimeout(() => {
      const resultCard = document.querySelector('.result-card')
      if (resultCard) {
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    }, 100)
  } catch (error: any) {
    if (error !== false) {
      ElMessage.error(error.message || '一键叫应失败')
    }
  } finally {
    submitLoading.value = false
  }
}

// 重置表单
const handleReset = () => {
  Object.assign(formData, {
    call_type: 1,
    call_source: 2,
    target_ids: [],
    person_ids: [],
    group_ids: [],
    call_channel: 'system',
    call_content: '',
    warning_id: null,
  })
  callResult.value = null
  formRef.value?.clearValidate()
}

// 跳转到叫应记录页面
const goToRecords = () => {
  router.push('/call/record')
}

// 初始化
onMounted(() => {
  fetchTargets()
  fetchPersons()
  fetchGroups()
})
</script>

<style scoped lang="scss">
.emergency-call {
  padding: 20px;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h2 {
      margin: 0;
      font-size: 20px;
      font-weight: 500;
    }
  }

  .form-card {
    margin-bottom: 20px;

    .form-tip {
      font-size: 12px;
      color: #909399;
      margin-top: 5px;
    }
  }

  .result-card {
    .result-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .result-content {
      margin-top: 10px;
      p {
        margin: 5px 0;
      }
    }
  }
}
</style>
