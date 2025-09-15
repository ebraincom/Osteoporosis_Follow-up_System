<template>
  <div class="my-followup-records">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>我的随访记录</h2>
      <p class="page-description">
        查看医生为您安排的随访计划和历史随访记录
      </p>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <el-row :gutter="20">
        <el-col :span="4">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.total }}</div>
              <div class="stat-label">总随访记录</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.completed }}</div>
              <div class="stat-label">已完成</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.scheduled }}</div>
              <div class="stat-label">已安排</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.upcoming }}</div>
              <div class="stat-label">即将到来</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card class="stat-card overdue-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.overdue }}</div>
              <div class="stat-label">已逾期</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 随访记录表格 -->
    <el-card class="records-table">
      <template #header>
        <div class="table-header">
          <span>随访记录列表</span>
          <el-button type="primary" @click="refreshRecords" :loading="loading">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </div>
      </template>

      <el-table
        :data="followupRecords"
        v-loading="loading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="patient_patient_id" label="档案编号" width="180" />
        <el-table-column prop="time" label="随访时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.time) }}
          </template>
        </el-table-column>
        <el-table-column prop="method" label="随访方式" width="120" />
        <el-table-column prop="location" label="随访地点" width="150" />
        <el-table-column prop="details" label="随访内容" min-width="200" />
        <el-table-column prop="patient_status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(getSmartStatus(row))">
              {{ getStatusText(getSmartStatus(row)) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="doctor_name" label="医生" width="120" />
        <el-table-column prop="next_followup_date" label="下次随访" width="180">
          <template #default="{ row }">
            {{ row.next_followup_date ? formatDateTime(row.next_followup_date) : '暂无安排' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="viewDetail(row)"
            >
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 随访记录详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="随访记录详情"
      width="600px"
      :before-close="handleCloseDetail"
    >
      <div v-if="selectedRecord" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="档案编号">
            {{ selectedRecord.patient_patient_id }}
          </el-descriptions-item>
          <el-descriptions-item label="随访时间">
            {{ formatDateTime(selectedRecord.time) }}
          </el-descriptions-item>
          <el-descriptions-item label="随访方式">
            {{ selectedRecord.method }}
          </el-descriptions-item>
          <el-descriptions-item label="随访地点">
            {{ selectedRecord.location }}
          </el-descriptions-item>
          <el-descriptions-item label="患者状态">
            <el-tag :type="getStatusType(selectedRecord.patient_status)">
              {{ selectedRecord.patient_status }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="负责医生">
            {{ selectedRecord.doctor_name }}
          </el-descriptions-item>
          <el-descriptions-item label="下次随访时间" :span="2">
            {{ selectedRecord.next_followup_date ? formatDateTime(selectedRecord.next_followup_date) : '暂无安排' }}
          </el-descriptions-item>
          <el-descriptions-item label="随访内容" :span="2">
            {{ selectedRecord.details }}
          </el-descriptions-item>
          <el-descriptions-item label="医生备注" :span="2">
            {{ selectedRecord.notes || '无备注' }}
          </el-descriptions-item>
          <el-descriptions-item label="治疗建议" :span="2">
            {{ selectedRecord.recommendations || '无建议' }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailDialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { followupApi } from '@/api/followup'

// 类型定义
interface FollowupRecord {
  id: number
  patient_id: number
  user_id: number
  time: string
  method: string
  location: string
  details: string
  notes: string | null
  patient_status: string
  next_followup_date: string | null
  recommendations: string | null
  created_at: string
  updated_at: string
  patient_name: string
  patient_patient_id: string
  doctor_name: string
}

// 响应式数据
const loading = ref(false)
const followupRecords = ref<FollowupRecord[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const detailDialogVisible = ref(false)
const selectedRecord = ref<FollowupRecord | null>(null)

// 计算属性
const stats = computed(() => {
  const total = followupRecords.value.length
  const completed = followupRecords.value.filter((r: FollowupRecord) => getSmartStatus(r) === '已完成').length
  const scheduled = followupRecords.value.filter((r: FollowupRecord) => getSmartStatus(r) === '已安排').length
  const upcoming = followupRecords.value.filter((r: FollowupRecord) => getSmartStatus(r) === '即将到来').length
  const overdue = followupRecords.value.filter((r: FollowupRecord) => getSmartStatus(r) === '已逾期').length

  return { total, completed, scheduled, upcoming, overdue }
})

// 智能状态判断
const getSmartStatus = (record: FollowupRecord): string => {
  console.log('=== 状态判断调试 ===')
  console.log('记录ID:', record.id)
  console.log('随访时间:', record.time)
  console.log('后端状态:', record.patient_status)
  
  // 检查随访时间
  if (record.time) {
    const followupDate = new Date(record.time)
    const now = new Date()
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const followupDay = new Date(followupDate.getFullYear(), followupDate.getMonth(), followupDate.getDate())
    
    console.log('随访日期:', followupDate)
    console.log('今天日期:', today)
    console.log('随访日期（仅日期）:', followupDay)
    console.log('随访日期是否在今天之前:', followupDay < today)
    console.log('随访日期是否在今天:', followupDay.getTime() === today.getTime())
    
    // 如果随访日期在今天之前，且状态是已完成，则显示已完成
    if (followupDay < today && record.patient_status === '已完成') {
      console.log('结果: 已完成（过去日期且状态已完成）')
      return '已完成'
    }
    
    // 如果随访日期在今天之前，且状态不是已完成，则标记为已逾期
    if (followupDay < today && record.patient_status !== '已完成') {
      console.log('结果: 已逾期（过去日期但状态未完成）')
      return '已逾期'
    }
    
    // 如果随访日期在今天，则标记为今天
    if (followupDay.getTime() === today.getTime()) {
      console.log('结果: 今天')
      return '今天'
    }
    
    // 如果随访日期在未来7天内，则标记为即将到来
    const diffTime = followupDay.getTime() - today.getTime()
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    console.log('距离今天的天数:', diffDays)
    
    if (diffDays > 0 && diffDays <= 7) {
      console.log('结果: 即将到来（7天内）')
      return '即将到来'
    }
    
    // 如果随访日期在未来，则标记为已安排
    if (followupDay > today) {
      console.log('结果: 已安排（未来日期）')
      return '已安排'
    }
  }
  
  // 如果后端明确标记为已完成，且时间已过，则显示已完成
  if (record.patient_status === '已完成') {
    if (record.time) {
      const followupDate = new Date(record.time)
      const now = new Date()
      if (followupDate < now) {
        console.log('结果: 已完成（后端标记已完成且时间已过）')
        return '已完成'
      }
    }
  }
  
  // 默认返回后端状态
  console.log('结果: 使用后端状态 -', record.patient_status || '未知')
  return record.patient_status || '未知'
}

// 获取状态类型（用于标签颜色）
const getStatusType = (status: string) => {
  switch (status) {
    case '已完成':
      return 'success'
    case '已安排':
      return 'primary'
    case '即将到来':
      return 'warning'
    case '今天':
      return 'danger'
    case '已逾期':
      return 'danger'
    case '进行中':
      return 'warning'
    case '已取消':
      return 'info'
    default:
      return 'info'
  }
}

// 获取状态显示文本
const getStatusText = (status: string) => {
  switch (status) {
    case '已完成':
      return '已完成'
    case '已安排':
      return '已安排'
    case '即将到来':
      return '即将到来'
    case '今天':
      return '今天'
    case '已逾期':
      return '已逾期'
    case '进行中':
      return '进行中'
    case '已取消':
      return '已取消'
    default:
      return status || '未知'
  }
}

// 方法
const fetchRecords = async () => {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    }
    
    const response = await followupApi.getMyFollowups(params)
    console.log('API响应:', response)
    console.log('响应类型:', typeof response)
    console.log('响应长度:', Array.isArray(response) ? response.length : 0)
    
    // 由于响应拦截器已经返回了response.data，所以这里直接使用response
    if (Array.isArray(response)) {
      followupRecords.value = response
      total.value = response.length
    } else {
      followupRecords.value = []
      total.value = 0
      console.warn('API响应不是数组格式:', response)
    }
    
    console.log('处理后的随访记录:', followupRecords.value)
    console.log('总数:', total.value)
  } catch (error) {
    console.error('获取随访记录失败:', error)
    ElMessage.error('获取随访记录失败')
  } finally {
    loading.value = false
  }
}

const refreshRecords = () => {
  currentPage.value = 1
  fetchRecords()
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
  fetchRecords()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchRecords()
}

const viewDetail = (record: FollowupRecord) => {
  selectedRecord.value = record
  detailDialogVisible.value = true
}

const handleCloseDetail = () => {
  detailDialogVisible.value = false
  selectedRecord.value = null
}

const formatDateTime = (dateTime: string) => {
  if (!dateTime) return ''
  const date = new Date(dateTime)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 生命周期
onMounted(() => {
  fetchRecords()
})
</script>

<style scoped>
.my-followup-records {
  padding: 20px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.page-description {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.stats-cards {
  margin-bottom: 24px;
}

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 20px;
}

.stat-number {
  font-size: 32px;
  font-weight: 600;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.overdue-card .stat-number {
  color: #f56c6c;
}

.overdue-card .stat-label {
  color: #f56c6c;
}

.records-table {
  margin-bottom: 24px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination-wrapper {
  margin-top: 20px;
  text-align: right;
}

.detail-content {
  max-height: 400px;
  overflow-y: auto;
}

.dialog-footer {
  text-align: right;
}
</style> 