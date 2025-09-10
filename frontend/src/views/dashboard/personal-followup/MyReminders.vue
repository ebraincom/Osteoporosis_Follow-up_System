<template>
  <div class="personal-followup-reminders">
    <div class="page-header">
      <h2>随访提醒</h2>
      <p>管理您的随访提醒设置和通知</p>
    </div>

    <div class="content-area">
      <!-- 提醒设置 -->
      <el-card class="settings-card">
        <template #header>
          <div class="card-header">
            <span>提醒设置</span>
            <el-button type="primary" size="small" @click="saveReminderSettings">
              保存设置
            </el-button>
          </div>
        </template>

        <el-form :model="reminderSettings" label-width="150px">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="启用提醒">
                <el-switch v-model="reminderSettings.enabled" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="提醒方式">
                <el-checkbox-group v-model="reminderSettings.methods">
                  <el-checkbox label="email">邮件提醒</el-checkbox>
                  <el-checkbox label="sms">短信提醒</el-checkbox>
                  <el-checkbox label="app">应用内提醒</el-checkbox>
                </el-checkbox-group>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="提前提醒天数">
                <el-select v-model="reminderSettings.advance_days" style="width: 100%">
                  <el-option label="1天前" :value="1" />
                  <el-option label="3天前" :value="3" />
                  <el-option label="7天前" :value="7" />
                  <el-option label="14天前" :value="14" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="提醒时间">
                <el-time-picker
                  v-model="reminderSettings.reminder_time"
                  format="HH:mm"
                  placeholder="选择提醒时间"
                  style="width: 100%"
                />
              </el-form-item>
            </el-col>
          </el-row>

          <el-row :gutter="20">
            <el-col :span="24">
              <el-form-item label="特殊提醒">
                <el-checkbox-group v-model="reminderSettings.special_reminders">
                  <el-checkbox label="urgent">紧急随访提醒</el-checkbox>
                  <el-checkbox label="medication">用药提醒</el-checkbox>
                  <el-checkbox label="test">检查结果提醒</el-checkbox>
                  <el-checkbox label="birthday">生日健康提醒</el-checkbox>
                </el-checkbox-group>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </el-card>

      <!-- 最近提醒 -->
      <el-card class="recent-reminders-card">
        <template #header>
          <div class="card-header">
            <span>最近提醒</span>
            <el-button type="primary" size="small" @click="refreshReminders">
              刷新提醒
            </el-button>
          </div>
        </template>

        <div class="reminders-list">
          <div v-if="recentReminders.length > 0">
            <div 
              v-for="reminder in recentReminders" 
              :key="reminder.id" 
              class="reminder-item"
              :class="getReminderClass(reminder.type)"
            >
              <div class="reminder-icon">
                <el-icon :size="24">
                  <Bell v-if="reminder.type === 'followup'" />
                  <Warning v-else-if="reminder.type === 'urgent'" />
                  <FirstAidKit v-else-if="reminder.type === 'medication'" />
                  <Document v-else />
                </el-icon>
              </div>
              <div class="reminder-content">
                <div class="reminder-title">{{ reminder.title }}</div>
                <div class="reminder-message">{{ reminder.message }}</div>
                <div class="reminder-time">{{ formatDateTime(reminder.created_at) }}</div>
                <div class="reminder-status">
                  <el-tag :type="getStatusColor(reminder.status)" size="small">
                    {{ getStatusText(reminder.status) }}
                  </el-tag>
                </div>
              </div>
              <div class="reminder-actions">
                <el-button 
                  v-if="reminder.status === 'unread'"
                  type="primary" 
                  size="small" 
                  @click="markAsRead(reminder)"
                >
                  标记已读
                </el-button>
                <el-button 
                  v-if="reminder.status === 'unread'"
                  type="success" 
                  size="small" 
                  @click="takeAction(reminder)"
                >
                  立即处理
                </el-button>
              </div>
            </div>
          </div>
          <div v-else class="no-reminders">
            <el-empty description="暂无提醒" :image-size="80" />
          </div>
        </div>
      </el-card>

      <!-- 提醒历史 -->
      <el-card class="history-card">
        <template #header>
          <div class="card-header">
            <span>提醒历史</span>
            <el-button type="primary" size="small" @click="exportReminderHistory">
              导出历史
            </el-button>
          </div>
        </template>

        <el-table
          :data="reminderHistory"
          style="width: 100%"
          v-loading="loading"
        >
          <el-table-column prop="type" label="提醒类型" width="120">
            <template #default="{ row }">
              <el-tag :type="getReminderTypeColor(row.type)" size="small">
                {{ getReminderTypeText(row.type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="title" label="提醒标题" min-width="200" />
          <el-table-column prop="created_at" label="创建时间" width="150">
            <template #default="{ row }">
              {{ formatDateTime(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusColor(row.status)" size="small">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="read_at" label="阅读时间" width="150">
            <template #default="{ row }">
              {{ row.read_at ? formatDateTime(row.read_at) : '未阅读' }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120" fixed="right">
            <template #default="{ row }">
              <el-button 
                type="primary" 
                size="small" 
                @click="viewReminderDetail(row)"
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
            :page-sizes="[10, 20, 50]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-card>
    </div>

    <!-- 提醒详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="提醒详情"
      width="50%"
      :before-close="handleCloseDetail"
    >
      <div v-if="selectedReminder" class="reminder-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="提醒类型">
            <el-tag :type="getReminderTypeColor(selectedReminder.type)">
              {{ getReminderTypeText(selectedReminder.type) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="提醒标题">
            {{ selectedReminder.title }}
          </el-descriptions-item>
          <el-descriptions-item label="提醒内容">
            {{ selectedReminder.message }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">
            {{ formatDateTime(selectedReminder.created_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusColor(selectedReminder.status)">
              {{ getStatusText(selectedReminder.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item v-if="selectedReminder.read_at" label="阅读时间">
            {{ formatDateTime(selectedReminder.read_at) }}
          </el-descriptions-item>
        </el-descriptions>

        <div v-if="selectedReminder.related_data" class="detail-section">
          <h4>相关数据</h4>
          <pre>{{ JSON.stringify(selectedReminder.related_data, null, 2) }}</pre>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Bell, Warning, FirstAidKit, Document } from '@element-plus/icons-vue'
import request from '@/utils/request'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 响应式数据
const loading = ref(false)
const reminderSettings = ref({
  enabled: true,
  methods: ['app'],
  advance_days: 3,
  reminder_time: new Date(2000, 0, 1, 9, 0),
  special_reminders: ['urgent', 'medication']
})

const recentReminders = ref<any[]>([])
const reminderHistory = ref<any[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const detailDialogVisible = ref(false)
const selectedReminder = ref<any>(null)

// 获取提醒设置
const fetchReminderSettings = async () => {
  try {
    const response = await request.get('/v1/reminders/settings')
    if (response.data) {
      reminderSettings.value = { ...reminderSettings.value, ...response.data }
    }
  } catch (error: any) {
    console.error('获取提醒设置失败:', error)
  }
}

// 保存提醒设置
const saveReminderSettings = async () => {
  try {
    const response = await request.post('/v1/reminders/settings', reminderSettings.value)
    if (response.data) {
      ElMessage.success('提醒设置已保存')
    }
  } catch (error: any) {
    console.error('保存提醒设置失败:', error)
    ElMessage.error('保存提醒设置失败，请稍后再试')
  }
}

// 获取最近提醒
const fetchRecentReminders = async () => {
  try {
    const response = await request.get('/v1/reminders/recent')
    if (response.data) {
      recentReminders.value = response.data.reminders || []
    }
  } catch (error: any) {
    console.error('获取最近提醒失败:', error)
  }
}

// 获取提醒历史
const fetchReminderHistory = async () => {
  try {
    loading.value = true
    const response = await request.get('/v1/reminders/history', {
      params: {
        skip: (currentPage.value - 1) * pageSize.value,
        limit: pageSize.value
      }
    })
    
    if (response.data) {
      reminderHistory.value = response.data.reminders || []
      total.value = response.data.total || 0
    }
  } catch (error: any) {
    console.error('获取提醒历史失败:', error)
    ElMessage.error('获取提醒历史失败，请稍后再试')
  } finally {
    loading.value = false
  }
}

// 标记提醒为已读
const markAsRead = async (reminder: any) => {
  try {
    const response = await request.post(`/v1/reminders/${reminder.id}/read`)
    if (response.data) {
      ElMessage.success('已标记为已读')
      fetchRecentReminders()
      fetchReminderHistory()
    }
  } catch (error: any) {
    console.error('标记已读失败:', error)
    ElMessage.error('标记已读失败，请稍后再试')
  }
}

// 立即处理提醒
const takeAction = (reminder: any) => {
  // 根据提醒类型执行相应操作
  switch (reminder.type) {
    case 'followup':
      // 跳转到随访页面
      ElMessage.info('跳转到随访页面')
      break
    case 'medication':
      // 跳转到用药管理页面
      ElMessage.info('跳转到用药管理页面')
      break
    default:
      ElMessage.info('处理提醒')
  }
  
  // 标记为已读
  markAsRead(reminder)
}

// 查看提醒详情
const viewReminderDetail = (reminder: any) => {
  selectedReminder.value = reminder
  detailDialogVisible.value = true
}

// 关闭详情对话框
const handleCloseDetail = () => {
  detailDialogVisible.value = false
  selectedReminder.value = null
}

// 刷新提醒
const refreshReminders = () => {
  fetchRecentReminders()
  fetchReminderHistory()
}

// 导出提醒历史
const exportReminderHistory = () => {
  ElMessage.info('导出功能开发中...')
}

// 分页处理
const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
  fetchReminderHistory()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchReminderHistory()
}

// 格式化日期时间
const formatDateTime = (dateString: string) => {
  if (!dateString) return '未知'
  return new Date(dateString).toLocaleString('zh-CN')
}

// 获取提醒类型颜色
const getReminderTypeColor = (type: string) => {
  switch (type) {
    case 'followup': return 'primary'
    case 'urgent': return 'danger'
    case 'medication': return 'warning'
    case 'test': return 'success'
    default: return 'info'
  }
}

// 获取提醒类型文本
const getReminderTypeText = (type: string) => {
  switch (type) {
    case 'followup': return '随访提醒'
    case 'urgent': return '紧急提醒'
    case 'medication': return '用药提醒'
    case 'test': return '检查提醒'
    default: return '其他提醒'
  }
}

// 获取状态颜色
const getStatusColor = (status: string) => {
  switch (status) {
    case 'read': return 'success'
    case 'unread': return 'warning'
    case 'archived': return 'info'
    default: return 'info'
  }
}

// 获取状态文本
const getStatusText = (status: string) => {
  switch (status) {
    case 'read': return '已读'
    case 'unread': return '未读'
    case 'archived': return '已归档'
    default: return '未知'
  }
}

// 获取提醒样式类
const getReminderClass = (type: string) => {
  switch (type) {
    case 'followup': return 'reminder-followup'
    case 'urgent': return 'reminder-urgent'
    case 'medication': return 'reminder-medication'
    default: return 'reminder-default'
  }
}

// 生命周期
onMounted(() => {
  fetchReminderSettings()
  fetchRecentReminders()
  fetchReminderHistory()
})
</script>

<style scoped>
.personal-followup-reminders {
  padding: 20px;
}

.page-header {
  margin-bottom: 24px;
  text-align: center;
}

.page-header h2 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 24px;
  font-weight: 600;
}

.page-header p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.content-area {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.settings-card,
.recent-reminders-card,
.history-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.reminders-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.reminder-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #ebeef5;
  transition: all 0.3s ease;
}

.reminder-item:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.reminder-followup {
  border-left: 4px solid #409eff;
  background-color: #f0f9ff;
}

.reminder-urgent {
  border-left: 4px solid #f56c6c;
  background-color: #fef0f0;
}

.reminder-medication {
  border-left: 4px solid #e6a23c;
  background-color: #fdf6ec;
}

.reminder-default {
  border-left: 4px solid #909399;
  background-color: #f4f4f5;
}

.reminder-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.reminder-content {
  flex: 1;
  min-width: 0;
}

.reminder-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.reminder-message {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  margin-bottom: 8px;
}

.reminder-time {
  font-size: 12px;
  color: #999;
  margin-bottom: 8px;
}

.reminder-actions {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.no-reminders {
  padding: 40px 20px;
  text-align: center;
}

.pagination-wrapper {
  margin-top: 20px;
  text-align: center;
}

.reminder-detail {
  padding: 20px 0;
}

.detail-section {
  margin-top: 20px;
}

.detail-section h4 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
  border-left: 3px solid #667eea;
  padding-left: 10px;
}

.detail-section pre {
  margin: 0;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
  overflow-x: auto;
}

/* 表格样式 */
:deep(.el-table) {
  border-radius: 8px;
}

:deep(.el-table th) {
  background-color: #fafafa;
  color: #333;
  font-weight: 600;
}

:deep(.el-table tr:hover) {
  background-color: #f5f7fa;
}

/* 卡片样式 */
:deep(.el-card) {
  border-radius: 8px;
  border: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

:deep(.el-card__header) {
  background-color: #fafafa;
  border-bottom: 1px solid #eee;
  padding: 15px 20px;
}

/* 按钮样式 */
:deep(.el-button) {
  border-radius: 6px;
  font-weight: 500;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

:deep(.el-button--primary:hover) {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
  transform: translateY(-1px);
}

/* 表单样式 */
:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-checkbox-group) {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

:deep(.el-switch) {
  margin-top: 4px;
}
</style> 