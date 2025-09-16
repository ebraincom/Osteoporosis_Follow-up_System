<template>
  <div class="followup-records">
    <div class="main-content">
      <!-- 左侧患者列表 -->
      <div class="left-panel">
        <!-- 搜索和筛选区域 -->
        <div class="search-section">
          <div class="filter-group">
            <span class="filter-label">分类查找:</span>
            <el-button-group>
              <el-button 
                :type="currentFilter === 'all' ? 'primary' : 'default'"
                @click="setFilter('all')"
              >
                展示全部
              </el-button>
              <el-button 
                :type="currentFilter === 'high' ? 'primary' : 'default'"
                @click="setFilter('high')"
              >
                高危
              </el-button>
              <el-button 
                :type="currentFilter === 'medium' ? 'primary' : 'default'"
                @click="setFilter('medium')"
              >
                中危
              </el-button>
              <el-button 
                :type="currentFilter === 'low' ? 'primary' : 'default'"
                @click="setFilter('low')"
              >
                低危
              </el-button>
            </el-button-group>
          </div>
          
          <div class="search-group">
            <el-input
              v-model="searchKeyword"
              placeholder="请输入查找姓名或档案编号"
              class="search-input"
              clearable
              @keyup.enter="handleSearch"
            >
              <template #append>
                <el-button type="primary" @click="handleSearch">
                  搜索
                </el-button>
              </template>
            </el-input>
          </div>
        </div>

        <!-- 患者列表表格 -->
        <div class="table-section">
          <div class="table-header">
            <span>患者列表</span>
            <div class="table-actions">
              <el-button type="primary" @click="refreshPatients" :loading="loading">
                <el-icon><Refresh /></el-icon>
                刷新列表
              </el-button>
            </div>
          </div>
          
          <el-table
            :data="filteredPatients"
            style="width: 100%"
            @row-click="handlePatientClick"
            :row-class-name="getRowClassName"
            highlight-current-row
            v-loading="loading"
          >
            <el-table-column prop="patient_id" label="档案编号" width="150" />
            <el-table-column prop="name" label="用户名称" width="120" />
            <el-table-column label="病人等级" width="120">
              <template #default="{ row }">
                <el-tag 
                  :type="getLevelType(row.risk_level)"
                  size="small"
                >
                  {{ getLevelText(row.risk_level) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="lastFollowupTime" label="最近随访时间" width="180" />
            <el-table-column label="新增随访" width="120">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click.stop="addFollowup(row)">
                  +添加
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <!-- 数据统计 -->
          <div class="table-footer">
            <p>共找到 {{ filteredPatients.length }} 条患者记录</p>
          </div>
        </div>
      </div>

      <!-- 右侧随访设置和历史记录 -->
      <div class="right-panel">
        <div v-if="selectedPatient" class="followup-settings">
          <div class="settings-header">
            <h3>随访设置-{{ selectedPatient.name }}</h3>
            <div class="patient-info">
              <p>档案编号: {{ selectedPatient.patient_id }}</p>
              <p>年龄: {{ selectedPatient.age }}岁 | 性别: {{ selectedPatient.gender === 'male' ? '男' : '女' }}</p>
              <p>联系电话: {{ selectedPatient.phone }}</p>
              <p>风险等级: <el-tag :type="getLevelType(selectedPatient.risk_level)" size="small">{{ getLevelText(selectedPatient.risk_level) }}</el-tag></p>
            </div>
          </div>

          <!-- 设置最新随访日期 -->
          <div class="settings-section">
            <h4>设置最新随访日期</h4>
            <div class="date-time-inputs">
              <div class="input-group">
                <label>年:</label>
                <el-input v-model="followupYear" placeholder="2025" />
              </div>
              <div class="input-group">
                <label>月:</label>
                <el-input v-model="followupMonth" placeholder="8" />
              </div>
              <div class="input-group">
                <label>日:</label>
                <el-input v-model="followupDay" placeholder="20" />
              </div>
              <div class="input-group">
                <label>时间:</label>
                <el-input v-model="followupTime" placeholder="13:00" />
              </div>
            </div>
          </div>

          <!-- 随访方式和地点 -->
          <div class="settings-section">
            <div class="input-row">
              <label>随访方式:</label>
              <el-input v-model="followupMethod" placeholder="请输入随访方式" />
            </div>
            <div class="input-row">
              <label>随访地点:</label>
              <el-input v-model="followupLocation" placeholder="请输入随访地点" />
            </div>
          </div>

          <!-- 提交按钮 -->
          <div class="submit-section">
            <el-button type="primary" @click="submitFollowup" :loading="submitting">
              点击提交
            </el-button>
          </div>

          <!-- 历史随访记录 -->
          <div class="history-section">
            <h4>历史随访记录</h4>
            <div v-if="selectedPatient.historyRecords && selectedPatient.historyRecords.length > 0" class="history-list">
              <div 
                v-for="record in selectedPatient.historyRecords" 
                :key="record.id" 
                class="history-item"
                @click="viewHistoryDetail(record)"
              >
                <div class="history-time">
                  {{ record.time }}
                  <el-tag :type="getStatusType(getSmartStatus(record))" size="small" style="margin-left: 10px;">
                    {{ getSmartStatus(record) }}
                  </el-tag>
                </div>
                <div class="history-details">{{ record.details }}</div>
                <div class="history-actions">
                  <el-button size="small" type="primary" @click.stop="viewHistoryDetail(record)">
                    查看详情
                  </el-button>
                  <el-button size="small" type="danger" @click.stop="deleteFollowupRecord(record)" class="delete-btn">
                    删除
                  </el-button>
                </div>
              </div>
            </div>
            <div v-else class="no-records">
              <el-empty description="暂无随访记录" />
            </div>
          </div>
        </div>

        <div v-else class="no-patient-selected">
          <el-empty description="请选择患者查看随访设置" />
        </div>
      </div>
    </div>

    <!-- 历史记录详情弹窗 -->
    <el-dialog
      v-model="historyDetailVisible"
      title="随访记录详情"
      width="60%"
      :close-on-click-modal="true"
    >
      <div v-if="selectedHistoryRecord" class="history-detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="随访时间" :span="2">
            {{ selectedHistoryRecord.time }}
          </el-descriptions-item>
          <el-descriptions-item label="随访方式">
            {{ selectedHistoryRecord.method || '未记录' }}
          </el-descriptions-item>
          <el-descriptions-item label="随访地点">
            {{ selectedHistoryRecord.location || '未记录' }}
          </el-descriptions-item>
          <el-descriptions-item label="随访内容" :span="2">
            {{ selectedHistoryRecord.details }}
          </el-descriptions-item>
          <el-descriptions-item label="医生备注" :span="2">
            {{ selectedHistoryRecord.notes || '无备注' }}
          </el-descriptions-item>
        </el-descriptions>
        
        <!-- 随访结果 -->
        <div class="followup-result" v-if="selectedHistoryRecord.result">
          <h4>随访结果</h4>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="患者状态">
              <el-tag :type="getStatusType(getSmartStatus(selectedHistoryRecord))">
                {{ getSmartStatus(selectedHistoryRecord) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="下次随访时间">
              {{ selectedHistoryRecord.result.nextFollowup || '待定' }}
            </el-descriptions-item>
            <el-descriptions-item label="治疗建议" :span="2">
              {{ selectedHistoryRecord.result.recommendations || '无' }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="historyDetailVisible = false">关闭</el-button>
          <el-button type="primary" @click="editHistoryRecord" v-if="selectedHistoryRecord">
            编辑记录
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑随访记录弹窗 -->
    <el-dialog
      v-model="editHistoryVisible"
      title="编辑随访记录"
      width="70%"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <div v-if="editingHistoryRecord" class="edit-history-content">
        <el-form
          ref="editHistoryFormRef"
          :model="editHistoryForm"
          :rules="editHistoryRules"
          label-width="120px"
        >
          <!-- 随访时间 -->
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="随访时间" prop="time">
                <el-date-picker
                  v-model="editHistoryForm.time"
                  type="datetime"
                  placeholder="选择随访时间"
                  format="YYYY/MM/DD HH:mm"
                  value-format="YYYY/MM/DD HH:mm"
                  style="width: 100%"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="随访方式" prop="method">
                <el-select v-model="editHistoryForm.method" placeholder="请选择随访方式" style="width: 100%">
                  <el-option label="门诊随访" value="门诊随访" />
                  <el-option label="电话随访" value="电话随访" />
                  <el-option label="居家随访" value="居家随访" />
                  <el-option label="视频随访" value="视频随访" />
                  <el-option label="其他" value="其他" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>

          <!-- 随访地点和内容 -->
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="随访地点" prop="location">
                <el-input v-model="editHistoryForm.location" placeholder="请输入随访地点" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="随访内容" prop="details">
                <el-input v-model="editHistoryForm.details" placeholder="请输入随访内容" />
              </el-form-item>
            </el-col>
          </el-row>

          <!-- 医生备注 -->
          <el-row :gutter="20">
            <el-col :span="24">
              <el-form-item label="医生备注" prop="notes">
                <el-input
                  v-model="editHistoryForm.notes"
                  type="textarea"
                  :rows="3"
                  placeholder="请输入医生备注"
                />
              </el-form-item>
            </el-col>
          </el-row>

          <!-- 随访结果 -->
          <el-divider content-position="left">随访结果</el-divider>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="患者状态" prop="result.status">
                <el-select v-model="editHistoryForm.result.status" placeholder="请选择患者状态" style="width: 100%">
                  <el-option label="已完成" value="已完成" />
                  <el-option label="已安排" value="已安排" />
                  <el-option label="进行中" value="进行中" />
                  <el-option label="已取消" value="已取消" />
                  <el-option label="恢复良好" value="恢复良好" />
                  <el-option label="稳定" value="稳定" />
                  <el-option label="改善" value="改善" />
                  <el-option label="恶化" value="恶化" />
                  <el-option label="需要调整治疗" value="需要调整治疗" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="下次随访时间" prop="result.nextFollowup">
                <el-date-picker
                  v-model="editHistoryForm.result.nextFollowup"
                  type="date"
                  placeholder="选择下次随访时间"
                  format="YYYY/MM/DD"
                  value-format="YYYY/MM/DD"
                  style="width: 100%"
                />
              </el-form-item>
            </el-col>
          </el-row>

          <el-row :gutter="20">
            <el-col :span="24">
              <el-form-item label="治疗建议" prop="result.recommendations">
                <el-input
                  v-model="editHistoryForm.result.recommendations"
                  type="textarea"
                  :rows="3"
                  placeholder="请输入治疗建议"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editHistoryVisible = false">取消</el-button>
          <el-button type="primary" @click="submitEditHistory" :loading="submittingEdit">
            {{ submittingEdit ? '保存中...' : '保存修改' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'
import type { Patient } from '@/types/patient'
import { Refresh } from '@element-plus/icons-vue'

// 扩展Patient类型，添加随访相关属性
interface PatientWithFollowup extends Patient {
  historyRecords: Array<{
    id: number
    time: string
    details: string
    method: string
    location: string
    notes: string
    result: {
      status: string
      nextFollowup: string
      recommendations: string
    }
  }>
  lastFollowupTime: string
}

// 响应式数据
const selectedPatient = ref<PatientWithFollowup | null>(null)
const currentFilter = ref('all')
const searchKeyword = ref('')
const submitting = ref(false)
const loading = ref(false)
const patients = ref<PatientWithFollowup[]>([])

// 随访设置表单数据
const followupYear = ref('2025')
const followupMonth = ref('8')
const followupDay = ref('20')
const followupTime = ref('13:00')
const followupMethod = ref('')
const followupLocation = ref('')

// 历史记录详情弹窗
const historyDetailVisible = ref(false)
const selectedHistoryRecord = ref<any>(null)

// 编辑随访记录弹窗
const editHistoryVisible = ref(false)
const editingHistoryRecord = ref<any>(null)
const editHistoryFormRef = ref<any>(null)
const editHistoryForm = ref({
  time: '',
  method: '',
  location: '',
  details: '',
  notes: '',
  result: {
    status: '',
    nextFollowup: '',
    recommendations: ''
  }
})

const editHistoryRules = {
  time: [{ required: true, message: '请选择随访时间', trigger: 'change' }],
  method: [{ required: true, message: '请选择随访方式', trigger: 'change' }],
  location: [{ required: true, message: '请输入随访地点', trigger: 'blur' }],
  details: [{ required: true, message: '请输入随访内容', trigger: 'blur' }],
  'result.status': [{ required: true, message: '请选择患者状态', trigger: 'change' }],
  'result.nextFollowup': [{ required: true, message: '请选择下次随访时间', trigger: 'change' }],
  'result.recommendations': [{ required: true, message: '请输入治疗建议', trigger: 'blur' }]
}

const submittingEdit = ref(false)

// 计算属性
const filteredPatients = computed(() => {
  let result = patients.value

  // 等级筛选
  if (currentFilter.value !== 'all') {
    result = result.filter(patient => patient.risk_level === currentFilter.value)
  }

  // 关键词搜索
  if (searchKeyword.value.trim()) {
    const keyword = searchKeyword.value.toLowerCase().trim()
    result = result.filter(patient => 
      patient.name.toLowerCase().includes(keyword) ||
      patient.patient_id.toLowerCase().includes(keyword)
    )
  }

  return result
})

// 方法
const setFilter = (filter: string) => {
  currentFilter.value = filter
}

const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    ElMessage.success(`搜索"${searchKeyword.value}"完成，找到${filteredPatients.value.length}条记录`)
  } else {
    ElMessage.info('请输入搜索关键词')
  }
}

const handlePatientClick = (row: PatientWithFollowup) => {
  selectedPatient.value = row
  if (!row.historyRecords) {
    row.historyRecords = []
  }
  ElMessage.info(`已选择患者: ${row.name}`)
}

const addFollowup = (patient: PatientWithFollowup) => {
  selectedPatient.value = patient
  if (!patient.historyRecords) {
    patient.historyRecords = []
  }
  ElMessage.info(`已选择患者: ${patient.name}，可以设置随访`)
}

const submitFollowup = async () => {
  if (!selectedPatient.value) {
    ElMessage.warning('请先选择患者')
    return
  }

  if (!followupMethod.value || !followupLocation.value) {
    ElMessage.warning('请填写完整的随访信息')
    return
  }

  submitting.value = true
  
  try {
    // 构建随访时间
    const followupDateTime = `${followupYear.value}-${followupMonth.value.padStart(2, '0')}-${followupDay.value.padStart(2, '0')}T${followupTime.value}:00`
    const followupDate = new Date(followupDateTime)
    const now = new Date()
    
    // 智能判断状态：未来日期设置为"已安排"，过去日期设置为"已完成"
    let patientStatus = '已完成'
    if (followupDate > now) {
      patientStatus = '已安排'
    }
    
    // 构建随访记录数据
    const followupData = {
      patient_id: selectedPatient.value.id,
      time: followupDateTime,
      method: followupMethod.value,
      location: followupLocation.value,
      details: `${followupLocation.value} ${followupMethod.value}`,
      notes: '',
      patient_status: patientStatus,
      next_followup_date: null,
      recommendations: ''
    }
    
    console.log('提交的随访数据:', followupData)
    console.log('随访时间:', followupDateTime)
    console.log('当前时间:', now.toISOString())
    console.log('判断的状态:', patientStatus)
    
    // 调用API创建随访记录
    const response = await request.post('/v1/followups/', followupData)
    
    if (response && response.data) {
      const newRecord = response.data
      
      // 转换API返回的数据格式为前端使用的格式
      const frontendRecord = {
        id: newRecord.id,
        time: newRecord.time,
        details: newRecord.details,
        method: newRecord.method,
        location: newRecord.location,
        notes: newRecord.notes,
        result: {
          status: newRecord.patient_status,
          nextFollowup: newRecord.next_followup_date || '',
          recommendations: newRecord.recommendations || ''
        }
      }
      
      if (!selectedPatient.value.historyRecords) {
        selectedPatient.value.historyRecords = []
      }
      selectedPatient.value.historyRecords.unshift(frontendRecord)
      
      // 更新最后随访时间
      selectedPatient.value.lastFollowupTime = newRecord.time
      
      followupMethod.value = ''
      followupLocation.value = ''
      
      ElMessage.success(`随访记录创建成功！状态：${patientStatus}`)
      
      // 自动刷新患者列表
      await fetchPatients()
    }
  } catch (error) {
    console.error('创建随访记录失败:', error)
    ElMessage.error('提交失败，请重试')
  } finally {
    submitting.value = false
  }
}

const fetchPatients = async () => {
  try {
    loading.value = true
    console.log('开始获取患者列表...')
    
    const response = await request.get('/v1/patients/')
    console.log('API响应:', response)
    
    // 检查响应数据结构
    if (response && response.data && Array.isArray(response.data)) {
      patients.value = response.data
    } else if (response && (response as any).patients && Array.isArray((response as any).patients)) {
      patients.value = (response as any).patients
    } else {
      console.warn('响应数据结构不符合预期:', response)
      patients.value = []
    }
    
    console.log('获取到的患者数据:', patients.value)
    
    // 为每个患者获取随访记录
    for (const patient of patients.value) {
      // 初始化随访记录数组
      patient.historyRecords = []
      patient.lastFollowupTime = '暂无随访记录'
      
      try {
        const followupResponse = await request.get(`/v1/followups/patient/${patient.id}`)
        if (followupResponse && Array.isArray(followupResponse)) {
          // 转换API返回的随访记录格式为前端使用的格式
          patient.historyRecords = followupResponse.map((record: any) => ({
            id: record.id,
            time: record.time,
            details: record.details,
            method: record.method,
            location: record.location,
            notes: record.notes,
            result: {
              status: record.patient_status,
              nextFollowup: record.next_followup_date || '',
              recommendations: record.recommendations || ''
            }
          }))
          
          // 设置最后随访时间
          if (patient.historyRecords.length > 0) {
            patient.lastFollowupTime = patient.historyRecords[0].time
          }
        }
      } catch (error) {
        console.warn(`获取患者 ${patient.name} 的随访记录失败:`, error)
        // 保持默认的空数组和提示信息
      }
    }
    
    if (patients.value.length > 0) {
      selectedPatient.value = patients.value[0]
      ElMessage.success(`成功加载 ${patients.value.length} 条患者记录`)
    } else {
      ElMessage.info('暂无患者数据')
    }
  } catch (error) {
    console.error('获取患者列表失败:', error)
    ElMessage.error('获取患者列表失败，请检查网络连接')
    patients.value = []
  } finally {
    loading.value = false
  }
}

const refreshPatients = async () => {
  await fetchPatients()
  ElMessage.success('患者列表已刷新')
}

const getLevelType = (level: string | undefined) => {
  if (!level) return 'info'
  switch (level) {
    case 'high': return 'danger'
    case 'medium': return 'warning'
    case 'low': return 'success'
    default: return 'info'
  }
}

const getLevelText = (level: string | undefined) => {
  if (!level) return '未知'
  switch (level) {
    case 'high': return '高危'
    case 'medium': return '中危'
    case 'low': return '低危'
    default: return '未知'
  }
}

// 智能状态判断函数
const getSmartStatus = (record: any): string => {
  // 检查随访时间
  if (record.time) {
    const followupDate = new Date(record.time)
    const now = new Date()
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const followupDay = new Date(followupDate.getFullYear(), followupDate.getMonth(), followupDate.getDate())
    
    // 如果随访日期在今天之前，且状态是已完成，则显示已完成
    if (followupDay < today && record.result && record.result.status === '已完成') {
      return '已完成'
    }
    
    // 如果随访日期在今天之前，且状态不是已完成，则标记为已逾期
    if (followupDay < today && record.result && record.result.status !== '已完成') {
      return '已逾期'
    }
    
    // 如果随访日期在今天，则标记为今天
    if (followupDay.getTime() === today.getTime()) {
      return '今天'
    }
    
    // 如果随访日期在未来7天内，则标记为即将到来
    const diffTime = followupDay.getTime() - today.getTime()
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    if (diffDays > 0 && diffDays <= 7) {
      return '即将到来'
    }
    
    // 如果随访日期在未来，则标记为已安排
    if (followupDay > today) {
      return '已安排'
    }
  }
  
  // 如果后端明确标记为已完成，且时间已过，则显示已完成
  if (record.result && record.result.status === '已完成') {
    if (record.time) {
      const followupDate = new Date(record.time)
      const now = new Date()
      if (followupDate < now) {
        return '已完成'
      }
    }
  }
  
  // 默认返回后端状态
  return record.result && record.result.status ? record.result.status : '未知'
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

const getRowClassName = ({ row }: { row: PatientWithFollowup }) => {
  return selectedPatient.value?.id === row.id ? 'selected-row' : ''
}

const viewHistoryDetail = (record: any) => {
  selectedHistoryRecord.value = record
  historyDetailVisible.value = true
}

const editHistoryRecord = () => {
  editingHistoryRecord.value = selectedHistoryRecord.value
  editHistoryVisible.value = true
  
  // 将时间字符串转换为日期对象，以便 el-date-picker 能正确显示
  if (editingHistoryRecord.value.time) {
    editHistoryForm.value.time = editingHistoryRecord.value.time
  }
  if (editingHistoryRecord.value.result?.nextFollowup) {
    editHistoryForm.value.result.nextFollowup = editingHistoryRecord.value.result.nextFollowup
  }
  
  // 复制其他字段
  editHistoryForm.value.method = editingHistoryRecord.value.method || ''
  editHistoryForm.value.location = editingHistoryRecord.value.location || ''
  editHistoryForm.value.details = editingHistoryRecord.value.details || ''
  editHistoryForm.value.notes = editingHistoryRecord.value.notes || ''
  editHistoryForm.value.result.status = editingHistoryRecord.value.result?.status || ''
  editHistoryForm.value.result.recommendations = editingHistoryRecord.value.result?.recommendations || ''
}

const submitEditHistory = async () => {
  if (!editHistoryFormRef.value) return

  await editHistoryFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      submittingEdit.value = true
      try {
        // 构建更新数据
        const updateData = {
          time: editHistoryForm.value.time,
          method: editHistoryForm.value.method,
          location: editHistoryForm.value.location,
          details: editHistoryForm.value.details,
          notes: editHistoryForm.value.notes,
          patient_status: editHistoryForm.value.result.status,
          next_followup_date: editHistoryForm.value.result.nextFollowup,
          recommendations: editHistoryForm.value.result.recommendations
        }
        
        // 调用API更新随访记录
        const response = await request.put(`/v1/followups/${editingHistoryRecord.value.id}`, updateData)
        
        if (response && response.data) {
          const updatedRecord = response.data
          
          // 转换API返回的数据格式为前端使用的格式
          const frontendRecord = {
            id: updatedRecord.id,
            time: updatedRecord.time,
            details: updatedRecord.details,
            method: updatedRecord.method,
            location: updatedRecord.location,
            notes: updatedRecord.notes,
            result: {
              status: updatedRecord.patient_status,
              nextFollowup: updatedRecord.next_followup_date || '',
              recommendations: updatedRecord.recommendations || ''
            }
          }

          // 找到并更新历史记录
          if (selectedPatient.value?.historyRecords) {
            const index = selectedPatient.value.historyRecords.findIndex(
              (record: any) => record.id === frontendRecord.id
            )
            if (index !== -1) {
              selectedPatient.value.historyRecords[index] = frontendRecord
              
              // 更新最后随访时间
              if (selectedPatient.value.historyRecords.length > 0) {
                selectedPatient.value.lastFollowupTime = selectedPatient.value.historyRecords[0].time
              }
            }
          }

          ElMessage.success('随访记录修改成功')
          editHistoryVisible.value = false
        }
      } catch (error) {
        console.error('更新随访记录失败:', error)
        ElMessage.error('修改失败，请重试')
      } finally {
        submittingEdit.value = false
      }
    }
  })
}

const deleteFollowupRecord = async (record: any) => {
  if (!selectedPatient.value) {
    ElMessage.warning('请先选择患者')
    return
  }

  ElMessageBox.confirm(`确定要删除此随访记录吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    try {
      await request.delete(`/v1/followups/${record.id}`)
      ElMessage.success('随访记录删除成功！')
      
      // 确保selectedPatient存在
      if (selectedPatient.value) {
        selectedPatient.value.historyRecords = selectedPatient.value.historyRecords.filter(
          (r: any) => r.id !== record.id
        )
        if (selectedPatient.value.historyRecords.length === 0) {
          selectedPatient.value.lastFollowupTime = '暂无随访记录'
        } else {
          selectedPatient.value.lastFollowupTime = selectedPatient.value.historyRecords[0].time
        }
      }
      
      await fetchPatients() // 重新获取患者列表以更新随访记录
    } catch (error) {
      console.error('删除随访记录失败:', error)
      ElMessage.error('删除失败，请重试')
    }
  }).catch(() => {
    // 用户取消删除
  })
}

onMounted(async () => {
  console.log('组件挂载，开始获取患者数据...')
  console.log('当前用户类型:', userStore.user?.user_type)
  
  // 只对机构用户获取患者列表，个人用户不需要
  if (userStore.user?.user_type === 'institutional') {
    await fetchPatients()
  } else {
    console.log('个人用户登录，跳过患者列表获取')
  }
})
</script>

<style scoped>
.followup-records {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  display: flex;
  gap: 20px;
  min-height: 0;
}

.left-panel {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.search-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.filter-label {
  font-weight: 500;
  color: #333;
  min-width: 80px;
}

.search-group {
  display: flex;
  align-items: center;
  gap: 15px;
}

.search-input {
  flex: 1;
}

.table-section {
  flex: 1;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.table-header span {
  font-size: 18px;
  font-weight: 500;
  color: #333;
}

.table-actions {
  display: flex;
  gap: 10px;
}

.table-footer {
  padding: 15px 20px;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
  text-align: center;
  color: #666;
}

.right-panel {
  flex: 1;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: auto;
}

.followup-settings {
  padding: 20px;
}

.settings-header {
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.settings-header h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 18px;
}

.patient-info {
  margin-top: 15px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #007bff;
}

.patient-info p {
  margin: 8px 0;
  color: #666;
  font-size: 14px;
  line-height: 1.4;
}

.patient-info p:first-child {
  color: #333;
  font-weight: 500;
}

.settings-section {
  border-top: 1px solid #e9ecef;
  padding-top: 20px;
  margin-top: 20px;
}

.settings-section h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 16px;
  font-weight: 500;
}

.date-time-inputs {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
}

.input-group label {
  margin-bottom: 8px;
  color: #666;
  font-size: 14px;
  font-weight: 500;
}

.input-row {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  gap: 15px;
}

.input-row label {
  min-width: 80px;
  color: #666;
  font-size: 14px;
  font-weight: 500;
}

.input-row .el-input {
  flex: 1;
}

.submit-section {
  margin: 25px 0;
  text-align: center;
}

.submit-section .el-button {
  padding: 12px 30px;
  font-size: 16px;
}

.history-section {
  border-top: 1px solid #e9ecef;
  padding-top: 20px;
  margin-top: 20px;
}

.history-section h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 16px;
  font-weight: 500;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.history-item {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #007bff;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.history-item:hover {
  background: #e3f2fd;
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.15);
}

.history-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, transparent, rgba(0, 123, 255, 0.05));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.history-item:hover::before {
  opacity: 1;
}

.history-time {
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
  font-size: 14px;
  display: flex;
  align-items: center;
}

.history-time::before {
  content: '📅';
  margin-right: 8px;
  font-size: 16px;
}

.history-details {
  color: #666;
  line-height: 1.5;
  margin-bottom: 10px;
  flex: 1;
}

.history-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
  opacity: 0.7;
  gap: 8px;
}

.delete-btn {
  margin-left: 8px;
}

.delete-btn:hover {
  opacity: 1;
}

.history-detail-content {
  padding: 20px;
}

.edit-history-content {
  padding: 20px;
}

.followup-result {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #e9ecef;
}

.followup-result h4 {
  margin-bottom: 15px;
  color: #333;
  font-size: 16px;
  font-weight: 500;
}

.no-patient-selected {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
}

.no-records {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 120px;
  color: #999;
  background: #f8f9fa;
  border-radius: 8px;
  border: 2px dashed #dee2e6;
}

:deep(.el-table) {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

:deep(.el-table th) {
  background-color: #f8f9fa;
  color: #333;
  font-weight: bold;
}

:deep(.selected-row) {
  background-color: #e3f2fd !important;
  border-left: 4px solid #1976d2 !important;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.2) !important;
}

:deep(.selected-row td) {
  background-color: #e3f2fd !important;
  color: #1565c0 !important;
  font-weight: 500 !important;
}

:deep(.el-table__row:hover) {
  background-color: #f5f5f5;
  cursor: pointer;
}

:deep(.el-table__row.selected-row:hover) {
  background-color: #bbdefb !important;
}

@media (max-width: 1200px) {
  .main-content {
    flex-direction: column;
  }
  
  .left-panel,
  .right-panel {
    flex: none;
  }
}

@media (max-width: 768px) {
  .date-time-inputs {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .filter-group {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .input-row {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .search-group {
    flex-direction: column;
    align-items: stretch;
  }
}
</style> 