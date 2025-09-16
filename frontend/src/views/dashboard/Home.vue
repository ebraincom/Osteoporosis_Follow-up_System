<template>
  <div class="home-container">
    <!-- 机构用户首页：患者信息列表 -->
    <div v-if="userStore.user?.user_type === 'institutional'" class="institutional-home">
      <!-- 主内容区 -->
      <div class="main-content">
        <!-- 左侧：患者列表 -->
        <div class="left-panel">
          <div class="search-section">
            <div class="search-header">
              <span class="search-title">分类查找:</span>
              <div class="filter-buttons">
                <el-button 
                  :type="currentFilter === 'all' ? 'primary' : 'default'"
                  size="small"
                  @click="setFilter('all')"
                >
                  展示全部
                </el-button>
                <el-button 
                  :type="currentFilter === 'high' ? 'primary' : 'default'"
                  size="small"
                  @click="setFilter('high')"
                >
                  高危
                </el-button>
                <el-button 
                  :type="currentFilter === 'medium' ? 'primary' : 'default'"
                  size="small"
                  @click="setFilter('medium')"
                >
                  中危
                </el-button>
                <el-button 
                  :type="currentFilter === 'low' ? 'primary' : 'default'"
                  size="small"
                  @click="setFilter('low')"
                >
                  低危
                </el-button>
              </div>
            </div>
            <div class="search-input-section">
              <el-input
                v-model="searchKeyword"
                placeholder="输入想要查找的名称"
                class="search-input"
                clearable
              />
              <el-button type="primary" @click="handleSearch" class="search-button">
                点击搜索
              </el-button>
            </div>
          </div>

          <!-- 患者表格 -->
          <div class="patient-table-section">
            <el-table
              :data="filteredPatients"
              style="width: 100%"
              @row-click="handlePatientClick"
              :row-class-name="getRowClassName"
              highlight-current-row
            >
              <el-table-column prop="name" label="用户名称" width="120" />
              <el-table-column prop="level" label="病人等级" width="100">
                <template #default="{ row }">
                  <el-tag
                    :type="getLevelType(row.level)"
                    size="small"
                  >
                    {{ getLevelText(row.level) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="age" label="年龄" width="80" />
              <el-table-column prop="gender" label="性别" width="80" />
              <el-table-column prop="keyIndicator" label="关键指标" width="100" />
              <el-table-column prop="hospital" label="就医机构" min-width="150" />
              <el-table-column label="操作" width="120" fixed="right">
                <template #default="{ row }">
                  <el-button 
                    type="primary" 
                    size="small" 
                    @click.stop="viewPatient(row)"
                    :class="{ 'is-selected': selectedPatient?.id === row.id }"
                  >
                    {{ selectedPatient?.id === row.id ? '已选中' : '查看' }}
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>

        <!-- 右侧：患者详情 -->
        <div class="right-panel">
          <div v-if="selectedPatient" class="patient-detail">
            <div class="detail-header">
              <h2>患者综合信息档案-{{ selectedPatient.name }}</h2>
              <div class="file-info">
                <span>档案编号: {{ selectedPatient.fileNo }}</span>
                <span>生成日期: {{ selectedPatient.generateDate }}</span>
              </div>
            </div>

            <div class="detail-content">
              <!-- 基本信息 -->
              <div class="info-section">
                <h3>一、基本信息</h3>
                <div class="info-grid">
                  <div class="info-item">
                    <span class="label">姓名:</span>
                    <span class="value">{{ selectedPatient.name }}</span>
                  </div>
                  <div class="info-item">
                    <span class="label">性别:</span>
                    <span class="value">{{ selectedPatient.gender }}</span>
                  </div>
                  <div class="info-item">
                    <span class="label">年龄:</span>
                    <span class="value">{{ selectedPatient.age }}岁</span>
                  </div>
                  <div class="info-item">
                    <span class="label">联系电话:</span>
                    <span class="value">{{ selectedPatient.phone }}</span>
                  </div>
                  <div class="info-item">
                    <span class="label">身份证号:</span>
                    <span class="value">{{ selectedPatient.idCard }}</span>
                  </div>
                  <div class="info-item">
                    <span class="label">地址:</span>
                    <span class="value">{{ selectedPatient.address }}</span>
                  </div>
                  <div class="info-item">
                    <span class="label">紧急联系人:</span>
                    <span class="value">{{ selectedPatient.emergencyContact }}</span>
                  </div>
                </div>
              </div>

              <!-- 临床诊断信息 -->
              <div class="info-section">
                <h3>二、临床诊断信息</h3>
                <div class="info-grid">
                  <div class="info-item">
                    <span class="label">主要诊断:</span>
                    <span class="value">{{ selectedPatient.diagnosis }}</span>
                  </div>
                  <div class="info-item">
                    <span class="label">患者等级:</span>
                    <el-tag :type="getLevelType(selectedPatient.level)" size="small">
                      {{ getLevelText(selectedPatient.level) }}
                    </el-tag>
                  </div>
                  <div class="info-item">
                    <span class="label">关键指标:</span>
                    <span class="value">{{ selectedPatient.keyIndicator }}</span>
                  </div>
                </div>
                <div class="bone-density-info">
                  <h4>骨密度详情</h4>
                  <div class="info-grid">
                    <div class="info-item">
                      <span class="label">检测方法:</span>
                      <span class="value">{{ selectedPatient.boneDensity.method }}</span>
                    </div>
                    <div class="info-item">
                      <span class="label">检测部位:</span>
                      <span class="value">{{ selectedPatient.boneDensity.site }}</span>
                    </div>
                    <div class="info-item">
                      <span class="label">T值:</span>
                      <span class="value">{{ selectedPatient.boneDensity.tScore }}</span>
                    </div>
                    <div class="info-item">
                      <span class="label">Z值:</span>
                      <span class="value">{{ selectedPatient.boneDensity.zScore }}</span>
                    </div>
                    <div class="info-item full-width">
                      <span class="label">结论:</span>
                      <span class="value">{{ selectedPatient.boneDensity.conclusion }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 病史与风险因素 -->
              <div class="info-section">
                <h3>三、病史与风险因素</h3>
                <div class="history-item">
                  <h4>现病史</h4>
                  <p>{{ selectedPatient.currentHistory }}</p>
                </div>
                <div class="history-item">
                  <h4>既往史</h4>
                  <p>{{ selectedPatient.pastHistory }}</p>
                </div>
                <div class="history-item">
                  <h4>个人史</h4>
                  <p>{{ selectedPatient.personalHistory }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <div v-else class="no-patient-selected">
            <el-empty description="请选择患者查看详细信息" />
          </div>
        </div>
      </div>
    </div>

    <!-- 个人用户首页：个人信息展示和患者档案 -->
    <div v-else class="personal-home">
      <!-- 主内容区 -->
      <div class="main-content">
        <!-- 左侧：个人信息展示 -->
        <div class="left-panel">
          <!-- 个人信息展示 -->
          <div class="personal-info-section">
            <div class="info-header">
              <h3>个人信息</h3>
            </div>
            
            <!-- 个人信息卡片 -->
            <div class="personal-info-card">
              <!-- 基本信息区域 -->
              <div class="basic-info-section">
                <h4 class="section-title">基本信息</h4>
                <div class="info-grid">
                  <div class="info-item">
                    <label>姓名</label>
                    <span>{{ personalUserInfo.name || '未设置' }}</span>
                  </div>
                  <div class="info-item">
                    <label>年龄</label>
                    <span>{{ personalUserInfo.age || '未设置' }}</span>
                  </div>
                  <div class="info-item">
                    <label>性别</label>
                    <span>{{ personalUserInfo.gender === 'FEMALE' ? '女' : personalUserInfo.gender === 'MALE' ? '男' : '未设置' }}</span>
                  </div>
                  <div class="info-item">
                    <label>联系电话</label>
                    <span>{{ personalUserInfo.phone || '未设置' }}</span>
                  </div>
                  <div class="info-item">
                    <label>邮箱</label>
                    <span>{{ personalUserInfo.email || '未设置' }}</span>
                  </div>
                  <div class="info-item">
                    <label>地址</label>
                    <span>{{ personalUserInfo.address || '未设置' }}</span>
                  </div>
                </div>
              </div>

              <!-- 身体指标区域 -->
              <div class="health-metrics-section">
                <h4 class="section-title">身体指标</h4>
                <div class="metrics-grid">
                  <div class="metric-item">
                    <div class="metric-label">身高</div>
                    <div class="metric-value">{{ personalUserInfo.height ? personalUserInfo.height + 'cm' : '未设置' }}</div>
                  </div>
                  <div class="metric-item">
                    <div class="metric-label">体重</div>
                    <div class="metric-value">{{ personalUserInfo.weight ? personalUserInfo.weight + 'kg' : '未设置' }}</div>
                  </div>
                  <div class="metric-item">
                    <div class="metric-label">T值</div>
                    <div class="metric-value">{{ personalUserInfo.t_score || '未设置' }}</div>
                  </div>
                  <div class="metric-item">
                    <div class="metric-label">Z值</div>
                    <div class="metric-value">{{ personalUserInfo.z_score || '未设置' }}</div>
                  </div>
                </div>
              </div>

              <!-- 病史信息区域 -->
              <div class="medical-history-section">
                <h4 class="section-title">病史信息</h4>
                <div class="history-cards">
                  <div class="history-card">
                    <div class="history-label">现病史</div>
                    <div class="history-content">
                      {{ personalUserInfo.medical_history || '暂无现病史记录' }}
                    </div>
                  </div>
                  <div class="history-card">
                    <div class="history-label">家族史</div>
                    <div class="history-content">
                      {{ personalUserInfo.family_history || '暂无家族史记录' }}
                    </div>
                  </div>
                  <div class="history-card">
                    <div class="history-label">用药史</div>
                    <div class="history-content">
                      {{ personalUserInfo.medications || '暂无用药史记录' }}
                    </div>
                  </div>
                </div>
              </div>

              <!-- 操作按钮区域 -->
              <div class="action-buttons">
                <el-button type="primary" @click="showAddDetailsDialog" size="large">
                  <el-icon><Plus /></el-icon>
                  添加详情
                </el-button>
                <el-button type="success" @click="showEditInfoDialog" size="large">
                  <el-icon><Edit /></el-icon>
                  编辑信息
                </el-button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 右侧：患者档案信息 -->
        <div class="right-panel">
          <div class="patient-files-section">
            <div class="files-header">
              <h3>我的患者档案</h3>
              <p>以下是您的患者档案信息</p>
            </div>
            
            <!-- 患者档案列表 -->
            <div class="patient-files-list">
              <div v-if="patientFiles.length === 0" class="no-files">
                <el-empty description="暂无患者档案" />
              </div>
              <div v-else>
                <div 
                  v-for="file in patientFiles" 
                  :key="file.id"
                  class="patient-file-item"
                  @click="selectPatientFile(file)"
                >
                  <div class="file-header">
                    <span class="file-id">{{ file.patient_id }}</span>
                    <el-tag :type="getRiskLevelType(file.risk_level)" size="small">
                      {{ getRiskLevelText(file.risk_level) }}
                    </el-tag>
                  </div>
                  <div class="file-info">
                    <p><strong>姓名:</strong> {{ file.name }}</p>
                    <p><strong>年龄:</strong> {{ file.age }}岁</p>
                    <p><strong>性别:</strong> {{ file.gender === 'female' ? '女' : '男' }}</p>
                    <p><strong>电话:</strong> {{ file.phone }}</p>
                    <p v-if="file.address"><strong>地址:</strong> {{ file.address }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加详情弹窗 -->
    <el-dialog
      v-model="addDetailsDialogVisible"
      title="添加详情信息"
      width="60%"
      :close-on-click-modal="false"
    >
      <el-form
        ref="addDetailsFormRef"
        :model="addDetailsForm"
        :rules="addDetailsRules"
        label-width="120px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="地址" prop="address">
              <el-input v-model="addDetailsForm.address" placeholder="请输入详细地址" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="身高(cm)" prop="height">
              <el-input-number v-model="addDetailsForm.height" :min="100" :max="250" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="体重(kg)" prop="weight">
              <el-input-number v-model="addDetailsForm.weight" :min="20" :max="200" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="T值" prop="t_score">
              <el-input-number v-model="addDetailsForm.t_score" :min="-5" :max="5" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Z值" prop="z_score">
              <el-input-number v-model="addDetailsForm.z_score" :min="-5" :max="5" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="风险等级" prop="risk_level">
              <el-select v-model="addDetailsForm.risk_level" placeholder="请选择风险等级" style="width: 100%">
                <el-option label="低危" value="low" />
                <el-option label="中危" value="medium" />
                <el-option label="高危" value="high" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="现病史" prop="medical_history">
              <el-input v-model="addDetailsForm.medical_history" type="textarea" :rows="3" placeholder="请描述您的现病史" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="家族史" prop="family_history">
              <el-input v-model="addDetailsForm.family_history" type="textarea" :rows="3" placeholder="请描述您的家族史" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="用药史" prop="medications">
              <el-input v-model="addDetailsForm.medications" type="textarea" :rows="3" placeholder="请输入用药史" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addDetailsDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAddDetails" :loading="submittingDetails">
            {{ submittingDetails ? '提交中...' : '确认添加' }}
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑信息弹窗 -->
    <el-dialog
      v-model="editInfoDialogVisible"
      title="编辑个人信息"
      width="60%"
      :close-on-click-modal="false"
    >
      <el-form
        ref="editInfoFormRef"
        :model="editInfoForm"
        :rules="editInfoRules"
        label-width="120px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="editInfoForm.name" placeholder="请输入姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="年龄" prop="age">
              <el-input-number v-model="editInfoForm.age" :min="1" :max="120" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="editInfoForm.gender" placeholder="请选择性别" style="width: 100%">
                <el-option label="男" value="MALE" />
                <el-option label="女" value="FEMALE" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="editInfoForm.phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="editInfoForm.email" placeholder="请输入邮箱" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editInfoDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitEditInfo" :loading="submittingEdit">
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
import { Plus, Refresh, Edit } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import request from '@/utils/request'
import type { Patient } from '@/types/patient'

// 用户store
const userStore = useUserStore()

// 机构用户相关数据
const loading = ref(false)
const patients = ref<any[]>([])
const selectedPatient = ref<any>(null)
const currentFilter = ref('all')
const searchKeyword = ref('')

// 历史记录数组
const historyRecords = ref<any[]>([])

// 个人用户相关数据
const personalUserInfo = ref<any>({})
const patientFiles = ref<any[]>([])
const selectedPatientFile = ref<any>(null)

// 弹窗控制
const addDetailsDialogVisible = ref(false)
const editInfoDialogVisible = ref(false)
const submittingDetails = ref(false)
const submittingEdit = ref(false)

// 添加详情表单
const addDetailsForm = ref({
  address: '',
  height: null,
  weight: null,
  t_score: null,
  z_score: null,
  risk_level: '',
  medical_history: '',
  family_history: '',
  medications: ''
})

// 编辑信息表单
const editInfoForm = ref({
  name: '',
  age: null,
  gender: '',
  phone: '',
  email: ''
})

// 表单验证规则
const addDetailsRules = {
  address: [{ required: true, message: '请输入地址', trigger: 'blur' }]
}

const editInfoRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  age: [{ required: true, message: '请输入年龄', trigger: 'change' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }]
}

// 计算属性
const filteredPatients = computed(() => {
  let result = patients.value

  // 风险等级筛选
  if (currentFilter.value !== 'all') {
    result = result.filter(patient => patient.risk_level === currentFilter.value)
  }

  // 关键词搜索
  if (searchKeyword.value.trim()) {
    const keyword = searchKeyword.value.toLowerCase().trim()
    result = result.filter(patient => 
      patient.name.toLowerCase().includes(keyword) ||
      patient.patient_id.toLowerCase().includes(keyword) ||
      patient.phone.includes(keyword)
    )
  }

  return result
})

// 方法
const setFilter = (filter: string) => {
  currentFilter.value = filter
}

const handleSearch = () => {
  // 搜索逻辑已在计算属性中处理
}

const handlePatientClick = (row: any) => {
  selectedPatient.value = row
  // 添加历史记录
  addHistoryRecord(row)
}

const viewPatient = (patient: any) => {
  selectedPatient.value = patient
  ElMessage.info(`已选择患者: ${patient.name}`)
  addHistoryRecord(patient)
}

const getRowClassName = ({ row }: { row: any }) => {
  return selectedPatient.value?.id === row.id ? 'selected-row' : ''
}

const addHistoryRecord = (patient: any) => {
  const record = {
    id: Date.now(),
    patientName: patient.name,
    patientId: patient.id,
    action: '查看患者信息',
    timestamp: new Date(),
    description: `查看了患者${patient.name}的基本信息`
  }
  
  // 检查是否已存在相同记录，避免重复
  const existingRecord = historyRecords.value.find(r => 
    r.patientId === patient.id && r.action === '查看患者信息'
  )
  
  if (!existingRecord) {
    historyRecords.value.unshift(record)
    // 限制历史记录数量，保留最近20条
    if (historyRecords.value.length > 20) {
      historyRecords.value = historyRecords.value.slice(0, 20)
    }
  }
}

// 个人用户方法
const showAddDetailsDialog = () => {
  addDetailsDialogVisible.value = true
}

const showEditInfoDialog = () => {
  // 填充编辑表单
  editInfoForm.value = {
    name: personalUserInfo.value.name || '',
    age: personalUserInfo.value.age || null,
    gender: personalUserInfo.value.gender || '',
    phone: personalUserInfo.value.phone || '',
    email: personalUserInfo.value.email || ''
  }
  editInfoDialogVisible.value = true
}

const selectPatientFile = (file: any) => {
  selectedPatientFile.value = file
}

const submitAddDetails = async () => {
  try {
    submittingDetails.value = true
    
    // 调用API更新个人用户详情
    const response = await request.put('/v1/personal-auth/me', addDetailsForm.value)
    
    ElMessage.success('详情信息添加成功')
    addDetailsDialogVisible.value = false
    
    // 重新获取个人用户信息
    await fetchPersonalUserInfo()
    
  } catch (error: any) {
    console.error('添加详情失败:', error)
    ElMessage.error(`添加详情失败: ${error.response?.data?.detail || error.message}`)
  } finally {
    submittingDetails.value = false
  }
}

const submitEditInfo = async () => {
  try {
    submittingEdit.value = true
    
    // 调用API更新个人用户信息
    const response = await request.put('/v1/personal-auth/me', editInfoForm.value)
    
    ElMessage.success('个人信息更新成功')
    editInfoDialogVisible.value = false
    
    // 重新获取个人用户信息
    await fetchPersonalUserInfo()
    
  } catch (error: any) {
    console.error('更新信息失败:', error)
    ElMessage.error(`更新信息失败: ${error.response?.data?.detail || error.message}`)
  } finally {
    submittingEdit.value = false
  }
}

// 获取机构用户患者列表
const fetchPatients = async () => {
  try {
    const response = await request.get('/v1/patients/')
    
    let patientData: any[] = []
    
    // 兼容不同的API响应格式
    if (response && ((response as any).patients || response.data?.patients || Array.isArray(response) || Array.isArray(response.data))) {
      // 优先检查response.patients，然后检查response.data.patients
      const patientsData = (response as any).patients || response.data?.patients
      
      if (patientsData && Array.isArray(patientsData)) {
        // 标准格式：{ patients: [...], total: 3, page: 1, size: 10 }
        patientData = patientsData
      } else if (Array.isArray(response) || Array.isArray(response.data)) {
        // 直接返回数组格式：[...]
        patientData = Array.isArray(response) ? response : response.data
      } else {
        patientData = []
      }
    } else {
      patientData = []
    }
    
    if (patientData.length > 0) {
      // 将后端数据格式转换为前端使用的格式
      patients.value = patientData.map((patient: any) => ({
        id: patient.id,
        name: patient.name,
        level: patient.risk_level || 'medium', // 映射风险等级
        age: patient.age,
        gender: patient.gender === 'male' ? '男' : '女',
        keyIndicator: patient.t_score || 0,
        hospital: '北京潞河医院', // 默认医院，可以从用户信息获取
        // 详细信息
        fileNo: patient.patient_id,
        generateDate: new Date(patient.created_at).toLocaleDateString('zh-CN'),
        phone: patient.phone || '未填写',
        idCard: '未填写', // 后端没有身份证字段
        address: patient.address || '未填写',
        emergencyContact: '未填写', // 后端没有紧急联系人字段
        diagnosis: '骨质疏松症', // 根据风险等级判断
        boneDensity: {
          method: 'DXA',
          site: '腰椎L1-L4及左股骨颈',
          tScore: patient.t_score || 0,
          zScore: patient.z_score || 0,
          conclusion: getBoneDensityConclusion(patient.t_score)
        },
        currentHistory: patient.medical_history || '无特殊症状',
        pastHistory: patient.family_history || '无重大疾病史',
        personalHistory: patient.medications || '无特殊个人史'
      }))
      
      // 默认选中第一个患者
      if (patients.value.length > 0) {
        const firstPatient = patients.value[0]
        selectedPatient.value = firstPatient
        addHistoryRecord(firstPatient)
        ElMessage.info(`已自动选择患者: ${firstPatient.name}`)
      }
    } else {
      patients.value = []
    }
    
  } catch (error: any) {
    console.error('获取患者数据失败:', error)
    ElMessage.error('获取患者数据失败，请检查网络连接')
    patients.value = []
  }
}

// 根据T值获取骨密度结论
const getBoneDensityConclusion = (tScore: number) => {
  if (tScore >= -1.0) return '骨密度正常'
  if (tScore >= -2.5) return '骨密度偏低，符合轻度骨质疏松症标准'
  if (tScore >= -3.0) return '骨密度明显偏低，符合中度骨质疏松症标准'
  return '骨密度显著偏低，符合重度骨质疏松症标准'
}

// 获取个人用户信息
const fetchPersonalUserInfo = async () => {
  try {
    const response = await request.get('/v1/personal-auth/me')
    personalUserInfo.value = response
  } catch (error: any) {
    console.error('获取个人用户信息失败:', error)
    ElMessage.error('获取个人用户信息失败')
  }
}

// 获取个人用户患者档案
const fetchPatientFiles = async () => {
  try {
    // 个人用户直接使用现有的API获取患者档案
    const response = await request.get('/v1/patients/')
    
    if (response && (response as any).patients) {
      patientFiles.value = (response as any).patients
    } else {
      patientFiles.value = []
    }
  } catch (error: any) {
    console.error('获取患者档案失败:', error)
    ElMessage.error('获取患者档案失败')
    patientFiles.value = []
  }
}

// 工具方法
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

const getRiskLevelType = (level: string | undefined) => {
  if (!level) return 'info'
  switch (level) {
    case 'high': return 'danger'
    case 'medium': return 'warning'
    case 'low': return 'success'
    default: return 'info'
  }
}

const getRiskLevelText = (level: string | undefined) => {
  if (!level) return '未知'
  switch (level) {
    case 'high': return '高危'
    case 'medium': return '中危'
    case 'low': return '低危'
    default: return '未知'
  }
}

// 生命周期
onMounted(async () => {
  if (userStore.user?.user_type === 'institutional') {
    // 机构用户获取患者列表
    await fetchPatients()
  } else {
    // 个人用户获取个人信息和患者档案
    await fetchPersonalUserInfo()
    await fetchPatientFiles()
  }
})
</script>

<style scoped>
.home-container {
  display: flex;
  height: 100vh;
  background-color: #f5f5f5;
}

.institutional-home {
  width: 100%;
}

.personal-home {
  width: 100%;
}

.main-content {
  display: flex;
  height: 100%;
}

.left-panel {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.right-panel {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  border-left: 1px solid #e0e0e0;
}

/* 机构用户样式 */
.search-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.search-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.search-title {
  font-weight: 600;
  margin-right: 15px;
}

.filter-buttons {
  display: flex;
  gap: 10px;
}

.search-input-section {
  display: flex;
  gap: 10px;
}

.search-input {
  flex: 1;
}

.patient-table-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.table-actions {
  display: flex;
  gap: 10px;
}

.patient-table {
  width: 100%;
}

.patient-detail {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.detail-header {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #667eea;
}

.detail-header h2 {
  color: #333;
  margin: 0 0 10px 0;
}

.file-info {
  display: flex;
  gap: 20px;
  color: #666;
  font-size: 14px;
}

.info-section {
  margin-bottom: 25px;
}

.info-section h3 {
  color: #667eea;
  margin-bottom: 15px;
  font-size: 16px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.info-item {
  display: flex;
  align-items: center;
}

.info-item.full-width {
  grid-column: 1 / -1;
  flex-direction: column;
  align-items: flex-start;
}

.info-item .label {
  font-weight: 600;
  color: #333;
  margin-right: 10px;
  min-width: 80px;
}

.info-item .value {
  color: #666;
  flex: 1;
}

.no-selection {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* 个人用户样式 */
.personal-info-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.info-header {
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid #667eea;
}

.info-header h3 {
  color: #333;
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.personal-info-card {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  max-height: calc(100vh - 200px);
  overflow-y: auto;
}

/* 区域标题样式 */
.section-title {
  color: #667eea;
  font-size: 15px;
  font-weight: 600;
  margin: 0 0 12px 0;
  padding-bottom: 6px;
  border-bottom: 2px solid #e9ecef;
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 30px;
  height: 2px;
  background: #667eea;
}

/* 基本信息区域 */
.basic-info-section {
  margin-bottom: 18px;
}

.basic-info-section .info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
}

.basic-info-section .info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 10px;
  background: white;
  border-radius: 6px;
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
}

.basic-info-section .info-item:hover {
  border-color: #667eea;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
}

.basic-info-section .info-item label {
  font-weight: 600;
  color: #333;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.basic-info-section .info-item span {
  color: #666;
  font-size: 13px;
  font-weight: 500;
}

/* 身体指标区域 */
.health-metrics-section {
  margin-bottom: 18px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.metric-item {
  background: white;
  border-radius: 8px;
  padding: 12px;
  text-align: center;
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.metric-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.metric-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
  border-color: #667eea;
}

.metric-label {
  font-size: 11px;
  color: #666;
  font-weight: 500;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.metric-value {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

/* 病史信息区域 */
.medical-history-section {
  margin-bottom: 18px;
}

.history-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-card {
  background: white;
  border-radius: 8px;
  padding: 15px;
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.history-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 3px;
  height: 100%;
  background: linear-gradient(180deg, #667eea, #764ba2);
}

.history-card:hover {
  transform: translateX(2px);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
  border-color: #667eea;
}

.history-label {
  font-size: 13px;
  font-weight: 600;
  color: #667eea;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.history-content {
  font-size: 13px;
  color: #666;
  line-height: 1.5;
  min-height: 32px;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 2px solid #667eea;
}

/* 操作按钮区域 */
.action-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 18px;
  padding-top: 15px;
  border-top: 1px solid #e9ecef;
}

.action-buttons .el-button {
  padding: 10px 20px;
  font-size: 13px;
  font-weight: 600;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.action-buttons .el-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.patient-files-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.files-header {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #667eea;
}

.files-header h3 {
  color: #333;
  margin: 0 0 10px 0;
}

.files-header p {
  color: #666;
  margin: 0;
}

.patient-files-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.patient-file-item {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.patient-file-item:hover {
  background: #e9ecef;
  border-color: #667eea;
}

.file-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.file-id {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.file-info p {
  margin: 5px 0;
  font-size: 13px;
  color: #666;
}

.no-files {
  text-align: center;
  padding: 40px 20px;
}

/* 弹窗样式 */
.dialog-footer {
  text-align: right;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
  
  .right-panel {
    border-left: none;
    border-top: 1px solid #e0e0e0;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>