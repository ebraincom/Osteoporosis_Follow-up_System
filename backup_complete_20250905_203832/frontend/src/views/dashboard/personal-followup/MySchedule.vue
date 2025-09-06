<template>
  <div class="personal-followup-schedule">
    <div class="page-header">
      <h2>随访计划</h2>
      <p>查看和管理您的随访安排</p>
    </div>

    <div class="content-area">
      <!-- 随访事件横向时间线展示 -->
      <el-card class="timeline-card">
        <template #header>
          <div class="card-header">
            <span>随访事件时间线</span>
            <el-button type="primary" size="small" @click="refreshSchedule">
              刷新数据
            </el-button>
          </div>
        </template>
        
        <div class="horizontal-timeline">
          <!-- 加载状态 -->
          <div v-if="loading" class="loading-overlay">
            <el-icon class="loading-icon" :size="24"><Loading /></el-icon>
            <span>正在加载随访数据...</span>
          </div>
          
          <!-- 时间轴 -->
          <div class="timeline-axis">
            <div class="axis-line"></div>
            <div 
              v-for="event in scheduleList" 
              :key="event.id"
              class="axis-marker"
              :style="{ left: getTimelinePosition(event.time) + '%' }"
            >
              <div class="marker-dot" :class="getEventClass(getEventType(event))"></div>
              <div class="marker-date">{{ formatDate(event.time) }}</div>
              <div class="marker-time">{{ formatTime(event.time) }}</div>
            </div>
          </div>
          
          <!-- 事件卡片 -->
          <div class="events-container">
            <div 
              v-for="event in scheduleList" 
              :key="event.id"
              class="event-card"
              :class="getEventClass(getEventType(event))"
              :style="{ left: getTimelinePosition(event.time) + '%', transform: 'translateX(-50%)' }"
            >
              <div class="card-arrow"></div>
              <div class="card-content">
                <div class="card-header">
                  <el-icon class="event-icon" :size="16">
                    <component :is="getEventIcon(getEventType(event))" />
                  </el-icon>
                  <el-tag :type="getStatusType(getSmartStatus(event))" size="small">
                    {{ getSmartStatus(event) }}
                  </el-tag>
                </div>
                
                <h4 class="event-title">{{ event.method || '随访' }}</h4>
                <p class="event-details">{{ event.details || '随访安排' }}</p>
                
                <div class="event-meta">
                  <div class="meta-item">
                    <el-icon><Location /></el-icon>
                    <span>{{ event.location || '待定' }}</span>
                  </div>
                  <div class="meta-item">
                    <el-icon><User /></el-icon>
                    <span>{{ event.doctor_name || '医生' }}</span>
                  </div>
                  <div class="meta-item" v-if="event.notes">
                    <el-icon><Document /></el-icon>
                    <span>{{ event.notes }}</span>
                  </div>
                </div>
                
                <div class="card-actions">
                  <el-button 
                    type="primary" 
                    size="small" 
                    @click="viewEventDetail(event)"
                  >
                    查看详情
                  </el-button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 如果没有事件 -->
          <div v-if="!loading && scheduleList.length === 0" class="no-events-placeholder">
            <el-empty description="暂无随访安排" />
          </div>
        </div>
      </el-card>

      <!-- 随访记录列表 -->
      <el-card class="list-card">
        <template #header>
          <div class="card-header">
            <span>随访记录列表</span>
            <el-button type="primary" size="small" @click="refreshSchedule">
              刷新数据
            </el-button>
          </div>
        </template>
        
        <div class="table-container">
          <el-table 
            :data="scheduleList" 
            v-loading="loading"
            stripe
            style="width: 100%"
          >
            <el-table-column prop="time" label="随访时间" width="180">
              <template #default="{ row }">
                <div class="time-cell">
                  <div class="date">{{ formatDate(row.time) }}</div>
                  <div class="time">{{ formatTime(row.time) }}</div>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column prop="method" label="随访方式" width="120">
              <template #default="{ row }">
                <el-tag :type="getMethodTagType(row.method)" size="small">
                  {{ row.method }}
                </el-tag>
              </template>
            </el-table-column>
            
            <el-table-column prop="details" label="随访内容" min-width="200">
              <template #default="{ row }">
                <div class="details-cell">
                  <span class="details-text">{{ row.details || '随访安排' }}</span>
                  <div class="notes" v-if="row.notes">
                    <el-icon><Document /></el-icon>
                    <span>{{ row.notes }}</span>
                  </div>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column prop="location" label="随访地点" width="120">
              <template #default="{ row }">
                <div class="location-cell">
                  <el-icon><Location /></el-icon>
                  <span>{{ row.location || '待定' }}</span>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column prop="doctor_name" label="负责医生" width="100">
              <template #default="{ row }">
                <div class="doctor-cell">
                  <el-icon><User /></el-icon>
                  <span>{{ row.doctor_name || '医生' }}</span>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column prop="patient_status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(getSmartStatus(row))" size="small">
                  {{ getSmartStatus(row) }}
                </el-tag>
              </template>
            </el-table-column>
            
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="viewEventDetail(row)"
                >
                  查看详情
                </el-button>
                <el-button 
                  type="info" 
                  size="small" 
                  @click="editEvent(row)"
                >
                  编辑
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <!-- 分页 -->
          <div class="pagination-container" v-if="total > 0">
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
        </div>
      </el-card>
    </div>

    <!-- 随访详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="随访详情"
      width="60%"
      :before-close="handleCloseDetail"
      destroy-on-close
    >
      <div v-if="selectedEvent" class="event-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="随访ID">
            {{ selectedEvent.id }}
          </el-descriptions-item>
          <el-descriptions-item label="计划日期">
            {{ formatDate(selectedEvent.time) }} {{ formatTime(selectedEvent.time) }}
          </el-descriptions-item>
          <el-descriptions-item label="随访方式">
            <el-tag :type="getMethodTagType(selectedEvent.method)" size="small">
              {{ selectedEvent.method }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(getSmartStatus(selectedEvent))" size="small">
              {{ getSmartStatus(selectedEvent) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="随访地点">
            {{ selectedEvent.location || '待定' }}
          </el-descriptions-item>
          <el-descriptions-item label="负责医生">
            {{ selectedEvent.doctor_name || '医生' }}
          </el-descriptions-item>
        </el-descriptions>

        <div class="detail-section">
          <h4>随访内容</h4>
          <p>{{ selectedEvent.details || '随访安排' }}</p>
        </div>

        <div class="detail-section" v-if="selectedEvent.notes">
          <h4>医生备注</h4>
          <p>{{ selectedEvent.notes }}</p>
        </div>

        <div class="detail-section">
          <h4>患者信息</h4>
          <p>患者ID: {{ selectedEvent.patient_id }}</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { WarningFilled, DocumentCopy, Bell, Calendar, Location, User, Loading } from '@element-plus/icons-vue'
import request from '@/utils/request'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 移除未使用的变量
const loading = ref(false)
const scheduleList = ref<any[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 详情对话框相关
const detailDialogVisible = ref(false)
const selectedEvent = ref<any>(null)

// 获取随访计划
const fetchSchedule = async () => {
  try {
    loading.value = true
    console.log('开始获取随访计划...')
    
    // 调用原有随访记录接口
    const response = await request.get('/v1/followups/my-records', {
      params: { 
        skip: (currentPage.value - 1) * pageSize.value, 
        limit: pageSize.value 
      }
    })
    
    console.log('=== 完整的response对象 ===')
    console.log('response:', response)
    console.log('response类型:', typeof response)
    console.log('response.keys:', Object.keys(response))
    console.log('response.data类型:', typeof response.data)
    console.log('response.data内容:', response.data)
    console.log('response.status:', response.status)
    console.log('response.statusText:', response.statusText)
    
    // 尝试不同的数据访问方式
    let data = null
    if (response.data && Array.isArray(response.data)) {
      data = response.data
      console.log('✅ 方式1成功: response.data')
    } else if (response && Array.isArray(response)) {
      data = response
      console.log('✅ 方式2成功: response本身')
    } else if (response.data && response.data.data && Array.isArray(response.data.data)) {
      data = response.data.data
      console.log('✅ 方式3成功: response.data.data')
    } else {
      console.log('❌ 所有方式都失败，无法获取数据')
      console.log('response.data:', response.data)
      console.log('response.data.data:', response.data?.data)
    }
    
    if (data && Array.isArray(data)) {
      scheduleList.value = data
      total.value = data.length
      console.log('🎉 成功获取随访数据:', { 
        scheduleList: data, 
        total: total.value, 
        length: data.length,
        firstItem: data[0]
      })
    } else {
      console.log('❌ 数据格式不正确或为空')
      scheduleList.value = []
      total.value = 0
    }
  } catch (error: any) {
    console.error('获取随访计划失败:', error)
    ElMessage.error('获取随访数据失败，请稍后重试')
    scheduleList.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

// 获取事件类型
const getEventType = (event: any) => {
  if (event.method === '家访') return 'urgent'
  if (event.method === '门诊随访') return 'regular'
  if (event.method === '电话随访' || event.method === '电话') return 'initial'
  return 'default'
}

// 查看事件详情
const viewEventDetail = (event: any) => {
  selectedEvent.value = event
  detailDialogVisible.value = true
  console.log('查看事件详情:', event)
}

// 关闭详情对话框
const handleCloseDetail = () => {
  detailDialogVisible.value = false
  selectedEvent.value = null
}

// 刷新数据
const refreshSchedule = () => {
  fetchSchedule()
}

// 获取随访方式标签类型
const getMethodTagType = (method: string) => {
  switch (method) {
    case '家访':
      return 'danger'
    case '门诊随访':
      return 'success'
    case '电话随访':
    case '电话':
      return 'warning'
    default:
      return 'info'
  }
}

// 编辑事件
const editEvent = (event: any) => {
  ElMessage.info('编辑功能开发中...')
  console.log('编辑事件:', event)
}

// 分页处理
const handleSizeChange = (newSize: number) => {
  pageSize.value = newSize
  currentPage.value = 1
  fetchSchedule()
}

const handleCurrentChange = (newPage: number) => {
  currentPage.value = newPage
  fetchSchedule()
}

// 格式化日期
const formatDate = (dateString: string) => {
  if (!dateString) return '未知'
  return new Date(dateString).toLocaleDateString('zh-CN')
}

// 格式化时间
const formatTime = (dateString: string) => {
  if (!dateString) return '未知'
  return new Date(dateString).toLocaleTimeString('zh-CN', { hour: 'numeric', minute: 'numeric' })
}

// 获取事件类型对应的CSS类
const getEventClass = (type: string) => {
  return `event-${type}`
}

// 获取事件图标
const getEventIcon = (type: string) => {
  switch (type) {
    case 'urgent': return WarningFilled
    case 'regular': return DocumentCopy
    case 'initial': return Bell
    default: return Calendar
  }
}

// 获取智能状态
const getSmartStatus = (event: any) => {
  const eventTime = new Date(event.time)
  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const eventDate = new Date(eventTime.getFullYear(), eventTime.getMonth(), eventTime.getDate())
  
  // 优先进行时间判断，而不是直接相信后端的patient_status
  const currentTime = now.getTime()
  const eventTimeMs = eventTime.getTime()
  
  // 如果随访时间还没到，强制显示为"已安排"
  if (eventTimeMs > currentTime) {
    return '已安排'
  }
  
  // 如果随访时间在今天，显示"今天"
  if (eventDate.getTime() === today.getTime()) {
    return '今天'
  }
  
  // 如果随访时间已过，但后端标记为"已完成"，则显示"已完成"
  if (eventTimeMs < currentTime && event.patient_status === '已完成') {
    return '已完成'
  }
  
  // 如果随访时间已过，但后端没有标记为"已完成"，则显示"已逾期"
  if (eventTimeMs < currentTime) {
    return '已逾期'
  }
  
  // 如果随访时间在未来7天内，显示"即将到来"
  if (eventTimeMs - currentTime <= 7 * 24 * 60 * 60 * 1000) {
    return '即将到来'
  }
  
  // 默认显示"已安排"
  return '已安排'
}

// 获取状态类型
const getStatusType = (status: string) => {
  switch (status) {
    case '已完成': return 'success'
    case '今天': return 'warning'
    case '即将到来': return 'primary'
    case '已逾期': return 'danger'
    case '已安排': return 'info'
    default: return 'info'
  }
}

// 计算时间线位置
const getTimelinePosition = (timeString: string) => {
  if (scheduleList.value.length === 0) return 0
  
  const eventTime = new Date(timeString).getTime()
  const sortedEvents = [...scheduleList.value].sort((a, b) => new Date(a.time).getTime() - new Date(b.time).getTime())
  const startTime = new Date(sortedEvents[0].time).getTime()
  const endTime = new Date(sortedEvents[sortedEvents.length - 1].time).getTime()
  
  if (startTime === endTime) {
    return 50 // 只有一个事件，位置在中间
  }
  
  const totalDuration = endTime - startTime
  const eventDuration = eventTime - startTime
  const percentage = (eventDuration / totalDuration) * 80 + 10 // 留出10%的边距
  
  return Math.max(10, Math.min(90, percentage))
}

// 页面加载时获取数据
onMounted(() => {
  fetchSchedule()
})
</script>

<style scoped>
.personal-followup-schedule {
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

.calendar-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.schedule-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.pagination-wrapper {
  margin-top: 20px;
  text-align: center;
}

.event-detail {
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

.detail-section p {
  margin: 0;
  color: #666;
  line-height: 1.6;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 4px;
}

/* 时间线样式 */
.timeline-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 24px;
}

.horizontal-timeline {
  position: relative;
  height: 200px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  padding: 20px 0;
  margin: 20px 0;
  overflow: visible;
}

.timeline-axis {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 1;
}

.axis-line {
  position: absolute;
  left: 0;
  top: 50%;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, #409eff, #67c23a, #e6a23c, #f56c6c);
  transform: translateY(-50%);
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.axis-marker {
  position: absolute;
  top: 0;
  left: 0;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
}

.marker-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: #dcdfe6;
  border: 3px solid white;
  box-shadow: 0 2px 12px rgba(0,0,0,0.3);
  transition: all 0.3s ease;
}

.marker-dot:hover {
  transform: scale(1.2);
  box-shadow: 0 4px 16px rgba(0,0,0,0.4);
}

/* 标记点颜色与卡片保持一致 */
.axis-marker:nth-child(1) .marker-dot {
  background-color: #e6a23c; /* 电话随访 - 橙色 */
}

.axis-marker:nth-child(2) .marker-dot {
  background-color: #f56c6c; /* 家访 - 红色 */
}

.axis-marker:nth-child(3) .marker-dot {
  background-color: #e6a23c; /* 电话随访 - 橙色 */
}

.marker-date {
  margin-top: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  white-space: nowrap;
  background: white;
  padding: 4px 8px;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.marker-time {
  margin-top: 4px;
  font-size: 11px;
  color: #606266;
  white-space: nowrap;
  background: rgba(255,255,255,0.8);
  padding: 2px 6px;
  border-radius: 4px;
}

.events-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 0 20px;
}

.event-card {
  position: absolute;
  width: 320px;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.12);
  border: 2px solid transparent;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  gap: 16px;
  z-index: 3;
  backdrop-filter: blur(10px);
}

.event-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 16px 48px rgba(0,0,0,0.2);
}

/* 不同类型卡片的悬停边框颜色 */
.event-card.event-urgent:hover {
  border-color: #f56c6c;
  box-shadow: 0 16px 48px rgba(245, 108, 108, 0.3);
}

.event-card.event-regular:hover {
  border-color: #67c23a;
  box-shadow: 0 16px 48px rgba(103, 194, 58, 0.3);
}

.event-card.event-initial:hover {
  border-color: #e6a23c;
  box-shadow: 0 16px 48px rgba(230, 162, 60, 0.3);
}

.event-card.event-default:hover {
  border-color: #909399;
  box-shadow: 0 16px 48px rgba(144, 147, 153, 0.3);
}

.card-arrow {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 12px solid transparent;
  border-right: 12px solid transparent;
  border-bottom: 12px solid #ffffff;
  filter: drop-shadow(0 -4px 8px rgba(0,0,0,0.1));
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.event-icon {
  color: #409eff;
  font-size: 24px;
  filter: drop-shadow(0 2px 4px rgba(64, 158, 255, 0.3));
}

.event-title {
  margin: 0 0 12px 0;
  font-size: 20px;
  font-weight: 700;
  color: #303133;
  text-align: center;
  text-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

.event-details {
  font-size: 15px;
  color: #606266;
  line-height: 1.6;
  text-align: center;
  margin: 0;
  padding: 12px;
  background: rgba(64, 158, 255, 0.05);
  border-radius: 8px;
  border-left: 4px solid #409eff;
}

.event-meta {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 12px;
  font-size: 14px;
  color: #606266;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  border: 1px solid rgba(64, 158, 255, 0.1);
  transition: all 0.3s ease;
}

.meta-item:hover {
  background: rgba(64, 158, 255, 0.05);
  border-color: rgba(64, 158, 255, 0.3);
  transform: translateX(4px);
}

.meta-item .el-icon {
  color: #409eff;
  font-size: 16px;
}

.card-actions {
  display: flex;
  justify-content: center;
  margin-top: 16px;
  gap: 12px;
}

.card-actions .el-button {
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.card-actions .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

/* 详情对话框样式 */
.event-detail {
  padding: 20px 0;
}

.detail-section {
  margin-top: 24px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #409eff;
}

.detail-section h4 {
  margin: 0 0 12px 0;
  color: #303133;
  font-size: 16px;
  font-weight: 600;
}

.detail-section p {
  margin: 0;
  color: #606266;
  line-height: 1.6;
}

/* 美化表格样式 */
.list-card {
  margin-top: 20px;
}

.table-container {
  padding: 0;
}

.el-table {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.el-table th {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  color: #303133;
  font-weight: 600;
}

.el-table td {
  padding: 16px 0;
}

.el-table--striped .el-table__body tr.el-table__row--striped td {
  background: rgba(64, 158, 255, 0.02);
}

.no-events-placeholder {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 5;
}

/* 事件类型样式 */
.event-card.event-urgent {
  border-left: 4px solid #f56c6c;
  background: linear-gradient(135deg, #fff5f5 0%, #fef0f0 100%);
  border-color: #f56c6c;
}

.event-card.event-urgent .event-title {
  color: #c03131;
}

.event-card.event-urgent .event-details {
  background: rgba(245, 108, 108, 0.1);
  border-left-color: #f56c6c;
  color: #a94442;
}

.event-card.event-urgent .meta-item {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(245, 108, 108, 0.2);
}

.event-card.event-urgent .meta-item:hover {
  background: rgba(245, 108, 108, 0.05);
  border-color: rgba(245, 108, 108, 0.4);
}

.event-card.event-urgent .meta-item .el-icon {
  color: #f56c6c;
}

.event-card.event-urgent .card-arrow {
  border-bottom-color: #fff5f5;
}

.event-card.event-regular {
  border-left: 4px solid #67c23a;
  background: linear-gradient(135deg, #f0f9ff 0%, #e8f5e8 100%);
  border-color: #67c23a;
}

.event-card.event-regular .event-title {
  color: #2d5a2d;
}

.event-card.event-regular .event-details {
  background: rgba(103, 194, 58, 0.1);
  border-left-color: #67c23a;
  color: #3c763d;
}

.event-card.event-regular .meta-item {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(103, 194, 58, 0.2);
}

.event-card.event-regular .meta-item:hover {
  background: rgba(103, 194, 58, 0.05);
  border-color: rgba(103, 194, 58, 0.4);
}

.event-card.event-regular .meta-item .el-icon {
  color: #67c23a;
}

.event-card.event-regular .card-arrow {
  border-bottom-color: #f0f9ff;
}

.event-card.event-initial {
  border-left: 4px solid #e6a23c;
  background: linear-gradient(135deg, #fffbf0 0%, #fef9e7 100%);
  border-color: #e6a23c;
}

.event-card.event-initial .event-title {
  color: #a0522d;
}

.event-card.event-initial .event-details {
  background: rgba(230, 162, 60, 0.1);
  border-left-color: #e6a23c;
  color: #8a6d3b;
}

.event-card.event-initial .meta-item {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(230, 162, 60, 0.2);
}

.event-card.event-initial .meta-item:hover {
  background: rgba(230, 162, 60, 0.05);
  border-color: rgba(230, 162, 60, 0.4);
}

.event-card.event-initial .meta-item .el-icon {
  color: #e6a23c;
}

.event-card.event-initial .card-arrow {
  border-bottom-color: #fffbf0;
}

.event-card.event-default {
  border-left: 4px solid #909399;
  background: linear-gradient(135deg, #f8f9fa 0%, #f1f2f3 100%);
  border-color: #909399;
}

.event-card.event-default .event-title {
  color: #4a4a4a;
}

.event-card.event-default .event-details {
  background: rgba(144, 147, 153, 0.1);
  border-left-color: #909399;
  color: #6c757d;
}

.event-card.event-default .meta-item {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(144, 147, 153, 0.2);
}

.event-card.event-default .meta-item:hover {
  background: rgba(144, 147, 153, 0.05);
  border-color: rgba(144, 147, 153, 0.4);
}

.event-card.event-default .meta-item .el-icon {
  color: #909399;
}

.event-card.event-default .card-arrow {
  border-bottom-color: #f8f9fa;
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

/* 日历样式 */
:deep(.el-calendar) {
  border-radius: 8px;
}

:deep(.el-calendar__header) {
  padding: 20px;
  background-color: #fafafa;
  border-radius: 8px 8px 0 0;
}

:deep(.el-calendar__body) {
  padding: 0;
}

:deep(.el-calendar-table) {
  border: none;
}

:deep(.el-calendar-table td) {
  border: 1px solid #ebeef5;
  padding: 0;
}

:deep(.el-calendar-table th) {
  background-color: #fafafa;
  border: 1px solid #ebeef5;
  padding: 12px 0;
  font-weight: 600;
  color: #333;
}

/* 随访事件卡片样式 */
.events-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-top: 24px;
}

.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
  padding: 16px;
}

.event-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  gap: 10px;
  border: 1px solid #ebeef5;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.event-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.event-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  padding-bottom: 8px;
  border-bottom: 1px dashed #eee;
}

.event-type-icon {
  color: white;
}

.event-date {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.event-content {
  flex: 1;
}

.event-title {
  margin: 0 0 5px 0;
  font-size: 16px;
  font-weight: 700;
  color: #333;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.event-details {
  font-size: 13px;
  color: #666;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.event-meta {
  display: flex;
  gap: 15px;
  margin-top: 10px;
  font-size: 12px;
  color: #909399;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.event-status {
  margin-top: 10px;
}

.no-events-placeholder {
  padding: 40px 0;
  text-align: center;
}

/* 加载状态样式 */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.loading-icon {
  color: #409eff;
  margin-bottom: 10px;
}

.loading-overlay span {
  font-size: 16px;
  color: #333;
}

/* 表格样式 */
.list-card {
  margin-top: 20px;
}

.table-container {
  padding: 0;
}

/* 时间单元格样式 */
.time-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.time-cell .date {
  font-weight: 600;
  color: #303133;
  font-size: 14px;
}

.time-cell .time {
  color: #909399;
  font-size: 12px;
}

/* 详情单元格样式 */
.details-cell {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.details-text {
  font-weight: 500;
  color: #303133;
}

.notes {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #909399;
  font-size: 12px;
}

.notes .el-icon {
  font-size: 12px;
}

/* 位置和医生单元格样式 */
.location-cell,
.doctor-cell {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #606266;
}

.location-cell .el-icon,
.doctor-cell .el-icon {
  color: #409eff;
  font-size: 14px;
}

/* 分页容器样式 */
.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  padding: 20px 0;
}
</style> 