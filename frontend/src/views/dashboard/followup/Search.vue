
<template>
  <div class="followup-search">
    <h2>随访跟踪 - 患者检索</h2>
    
    <!-- 主要操作按钮 -->
    <div class="action-section">
      <!-- 机构用户显示新增患者按钮 -->
      <el-button 
        v-if="userStore.user?.user_type === 'institutional'" 
        type="primary" 
        @click="showAddPatientDialog"
      >
        <el-icon><Plus /></el-icon>
        新增患者
      </el-button>
      
      <el-button type="success" @click="refreshPatients">
        <el-icon><Refresh /></el-icon>
        刷新列表
      </el-button>
      
      <el-button type="warning" @click="testPatientsAPI">
        <el-icon><List /></el-icon>
        自测试API
      </el-button>
    </div>

    <!-- 患者列表 -->
    <div class="patient-section">
      <el-card title="患者列表">
        <!-- 搜索和筛选 -->
        <div class="search-filters">
          <el-row :gutter="20">
            <el-col :span="6">
              <el-input
                v-model="searchKeyword"
                placeholder="搜索姓名、档案编号或电话"
                clearable
                @input="handleSearch"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </el-col>
            <el-col :span="4">
              <el-select v-model="riskLevelFilter" placeholder="风险等级" clearable @change="handleSearch">
                <el-option label="全部" value="" />
                <el-option label="低危" value="low" />
                <el-option label="中危" value="medium" />
                <el-option label="高危" value="high" />
              </el-select>
            </el-col>
            <el-col :span="4">
              <el-select v-model="genderFilter" placeholder="性别" clearable @change="handleSearch">
                <el-option label="全部" value="" />
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
              </el-select>
            </el-col>
          </el-row>
        </div>

        <!-- 患者表格 -->
        <el-table :data="filteredPatients" :loading="loading" style="width: 100%" v-loading="loading">
          <el-table-column prop="patient_id" label="档案编号" width="150" />
          <el-table-column prop="name" label="姓名" width="100" />
          <el-table-column prop="age" label="年龄" width="80" />
          <el-table-column prop="gender" label="性别" width="80">
            <template #default="{ row }">
              {{ row.gender === 'male' ? '男' : '女' }}
            </template>
          </el-table-column>
          <el-table-column prop="phone" label="联系电话" width="120" />
          <el-table-column prop="risk_level" label="风险等级" width="100">
            <template #default="{ row }">
              <el-tag :type="getLevelType(row.risk_level)" size="small">
                {{ getLevelText(row.risk_level) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="address" label="地址" min-width="150" show-overflow-tooltip />
          <el-table-column label="操作" width="280" fixed="right">
            <template #default="{ row }">
              <div class="action-buttons">
                <el-button size="small" type="primary" @click="viewPatientArchive(row)">查看档案</el-button>
                <!-- 机构用户显示编辑和删除按钮 -->
                <template v-if="userStore.user?.user_type === 'institutional'">
                  <el-button size="small" @click="editPatient(row)">编辑</el-button>
                  <!-- 只有管理员可以删除 -->
                  <el-button 
                    v-if="isAdmin()" 
                    size="small" 
                    type="danger" 
                    @click="deletePatient(row)"
                  >
                    删除
                  </el-button>
                </template>
              </div>
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
    </div>

    <!-- 医疗机构容器 -->
    <div class="medical-institutions-section">
      <el-card title="曾就医机构">
        <div class="institutions-container">
          <div v-if="medicalInstitutions.length === 0" class="no-institutions">
            <el-empty description="暂无就医机构记录" />
          </div>
          <div v-else class="institutions-list">
            <div
              v-for="institution in medicalInstitutions"
              :key="institution.id"
              class="institution-card"
            >
              <div class="institution-header">
                <h4>{{ institution.name }}</h4>
                <el-tag :type="institution.status === 'active' ? 'success' : 'info'" size="small">
                  {{ institution.status === 'active' ? '当前' : '历史' }}
                </el-tag>
              </div>
              <div class="institution-info">
                <p><strong>科室:</strong> {{ institution.department }}</p>
                <p><strong>主治医生:</strong> {{ institution.doctor }}</p>
                <p><strong>首次就诊:</strong> {{ institution.firstVisit }}</p>
                <p><strong>最近就诊:</strong> {{ institution.lastVisit }}</p>
                <p><strong>就诊次数:</strong> {{ institution.visitCount }}次</p>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 新增患者弹窗 -->
    <el-dialog
      v-model="addPatientDialogVisible"
      title="新增患者"
      width="70%"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <el-form
        ref="addPatientFormRef"
        :model="addPatientForm"
        :rules="addPatientRules"
        label-width="120px"
        @submit.prevent="submitAddPatient"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="addPatientForm.name" placeholder="请输入患者姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="addPatientForm.gender" placeholder="请选择性别" style="width: 100%">
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="年龄" prop="age">
              <el-input-number v-model="addPatientForm.age" :min="1" :max="120" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="addPatientForm.phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="风险等级" prop="risk_level">
              <el-select v-model="addPatientForm.risk_level" placeholder="请选择风险等级" style="width: 100%">
                <el-option label="低危" value="low" />
                <el-option label="中危" value="medium" />
                <el-option label="高危" value="high" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="addPatientForm.email" placeholder="请输入邮箱地址" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="地址" prop="address">
              <el-input v-model="addPatientForm.address" placeholder="请输入详细地址" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="身高(cm)" prop="height">
              <el-input-number v-model="addPatientForm.height" :min="100" :max="250" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="体重(kg)" prop="weight">
              <el-input-number v-model="addPatientForm.weight" :min="20" :max="200" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="T值" prop="t_score">
              <el-input-number v-model="addPatientForm.t_score" :min="-5" :max="5" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Z值" prop="z_score">
              <el-input-number v-model="addPatientForm.z_score" :min="-5" :max="5" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="现病史" prop="medical_history">
              <el-input
                v-model="addPatientForm.medical_history"
                type="textarea"
                :rows="3"
                placeholder="请输入现病史"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="既往史" prop="family_history">
              <el-input
                v-model="addPatientForm.family_history"
                type="textarea"
                :rows="3"
                placeholder="请输入既往史"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="用药史" prop="medications">
              <el-input
                v-model="addPatientForm.medications"
                type="textarea"
                :rows="3"
                placeholder="请输入用药史"
              />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addPatientDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAddPatient" :loading="submitting">
            {{ submitting ? '提交中...' : '确认添加' }}
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 患者详情弹窗 -->
    <el-dialog
      v-model="patientDetailDialogVisible"
      title="患者详情"
      width="60%"
      :close-on-click-modal="true"
    >
      <div v-if="selectedPatient" class="patient-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="档案编号">{{ selectedPatient.patient_id }}</el-descriptions-item>
          <el-descriptions-item label="姓名">{{ selectedPatient.name }}</el-descriptions-item>
          <el-descriptions-item label="年龄">{{ selectedPatient.age }}</el-descriptions-item>
          <el-descriptions-item label="性别">{{ selectedPatient.gender === 'male' ? '男' : '女' }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ selectedPatient.phone }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ selectedPatient.email || '无' }}</el-descriptions-item>
          <el-descriptions-item label="地址">{{ selectedPatient.address || '无' }}</el-descriptions-item>
          <el-descriptions-item label="风险等级">
            <el-tag :type="getLevelType(selectedPatient.risk_level)" size="small">
              {{ getLevelText(selectedPatient.risk_level) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="身高">{{ selectedPatient.height ? `${selectedPatient.height}cm` : '无' }}</el-descriptions-item>
          <el-descriptions-item label="体重">{{ selectedPatient.weight ? `${selectedPatient.weight}kg` : '无' }}</el-descriptions-item>
          <el-descriptions-item label="T值">{{ selectedPatient.t_score || '无' }}</el-descriptions-item>
          <el-descriptions-item label="Z值">{{ selectedPatient.z_score || '无' }}</el-descriptions-item>
          <el-descriptions-item label="现病史" :span="2">{{ selectedPatient.medical_history || '无' }}</el-descriptions-item>
          <el-descriptions-item label="既往史" :span="2">{{ selectedPatient.family_history || '无' }}</el-descriptions-item>
          <el-descriptions-item label="用药史" :span="2">{{ selectedPatient.medications || '无' }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>

    <!-- 编辑患者弹窗 -->
    <el-dialog
      v-model="editPatientDialogVisible"
      title="编辑患者"
      width="70%"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <el-form
        ref="editPatientFormRef"
        :model="editPatientForm"
        :rules="editPatientRules"
        label-width="120px"
        @submit.prevent="submitEditPatient"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="档案编号" prop="patient_id">
              <el-input v-model="editPatientForm.patient_id" placeholder="患者档案编号" disabled />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="editPatientForm.name" placeholder="请输入患者姓名" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="editPatientForm.gender" placeholder="请选择性别" style="width: 100%">
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="年龄" prop="age">
              <el-input-number v-model="editPatientForm.age" :min="1" :max="120" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="editPatientForm.phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="风险等级" prop="risk_level">
              <el-select v-model="editPatientForm.risk_level" placeholder="请选择风险等级" style="width: 100%">
                <el-option label="低危" value="low" />
                <el-option label="中危" value="medium" />
                <el-option label="高危" value="high" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="editPatientForm.email" placeholder="请输入邮箱地址" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="地址" prop="address">
              <el-input v-model="editPatientForm.address" placeholder="请输入详细地址" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="身高(cm)" prop="height">
              <el-input-number v-model="editPatientForm.height" :min="50" :max="250" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="体重(kg)" prop="weight">
              <el-input-number v-model="editPatientForm.weight" :min="20" :max="200" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="T值" prop="t_score">
              <el-input-number v-model="editPatientForm.t_score" :min="-5" :max="5" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Z值" prop="z_score">
              <el-input-number v-model="editPatientForm.z_score" :min="-5" :max="5" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="现病史" prop="medical_history">
              <el-input
                v-model="editPatientForm.medical_history"
                type="textarea"
                :rows="3"
                placeholder="请输入现病史"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="既往史" prop="family_history">
              <el-input
                v-model="editPatientForm.family_history"
                type="textarea"
                :rows="3"
                placeholder="请输入既往史"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="用药史" prop="medications">
              <el-input
                v-model="editPatientForm.medications"
                type="textarea"
                :rows="3"
                placeholder="请输入用药史"
              />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editPatientDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitEditPatient" :loading="editing">
            {{ editing ? '保存中...' : '保存修改' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh, List, Search } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import request from '@/utils/request'
import type { Patient, PatientCreate, PatientUpdate } from '@/types/patient'
import { Gender, RiskLevel } from '@/types/patient'

// 用户store
const userStore = useUserStore()

// 响应式数据
const loading = ref(false)
const submitting = ref(false)
const editing = ref(false)
const patients = ref<Patient[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const searchKeyword = ref('')
const riskLevelFilter = ref('')
const genderFilter = ref('')

// 医疗机构数据
const medicalInstitutions = ref([
  {
    id: 1,
    name: '北京潞河医院',
    department: '骨科',
    doctor: '王一鸣',
    firstVisit: '2025-01-15',
    lastVisit: '2025-09-17',
    visitCount: 5,
    status: 'active'
  },
  {
    id: 2,
    name: '北京协和医院',
    department: '内分泌科',
    doctor: '张医生',
    firstVisit: '2024-08-20',
    lastVisit: '2024-12-10',
    visitCount: 3,
    status: 'history'
  }
])

// 弹窗控制
const addPatientDialogVisible = ref(false)
const editPatientDialogVisible = ref(false)
const patientDetailDialogVisible = ref(false)
const selectedPatient = ref<Patient | null>(null)

// 表单相关
const addPatientFormRef = ref()
const editPatientFormRef = ref()
const addPatientForm = ref<PatientCreate>({
  patient_id: '',
  name: '',
  age: 0,
  gender: Gender.MALE,
  phone: '',
  email: undefined,
  address: undefined,
  height: undefined,
  weight: undefined,
  bmi: undefined,
  t_score: undefined,
  z_score: undefined,
  risk_level: RiskLevel.LOW,
  medical_history: undefined,
  family_history: undefined,
  medications: undefined
})

// 编辑表单
const editPatientForm = ref<PatientUpdate>({
  name: '',
  age: 0,
  gender: Gender.MALE,
  phone: '',
  email: undefined,
  address: undefined,
  height: undefined,
  weight: undefined,
  bmi: undefined,
  t_score: undefined,
  z_score: undefined,
  risk_level: RiskLevel.LOW,
  medical_history: undefined,
  family_history: undefined,
  medications: undefined
})

// 表单验证规则
const addPatientRules = {
  name: [{ required: true, message: '请输入患者姓名', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  age: [{ required: true, message: '请输入年龄', trigger: 'change' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
  risk_level: [{ required: true, message: '请选择风险等级', trigger: 'change' }]
}

const editPatientRules = {
  name: [{ required: true, message: '请输入患者姓名', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  age: [{ required: true, message: '请输入年龄', trigger: 'change' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
  risk_level: [{ required: true, message: '请选择风险等级', trigger: 'change' }]
}

// 计算属性

const filteredPatients = computed(() => {
  let result = patients.value

  // 关键词搜索
  if (searchKeyword.value.trim()) {
    const keyword = searchKeyword.value.toLowerCase().trim()
    result = result.filter(patient => 
      patient.name.toLowerCase().includes(keyword) ||
      patient.patient_id.toLowerCase().includes(keyword) ||
      patient.phone.includes(keyword)
    )
  }

  // 风险等级筛选
  if (riskLevelFilter.value) {
    result = result.filter(patient => patient.risk_level === riskLevelFilter.value)
  }

  // 性别筛选
  if (genderFilter.value) {
    result = result.filter(patient => patient.gender === genderFilter.value)
  }

  return result
})

// 方法
const generatePatientId = () => {
  const timestamp = Date.now()
  const random = Math.floor(Math.random() * 1000)
  return `P${timestamp}${random}`
}

const showAddPatientDialog = () => {
  // 重置表单
  addPatientForm.value = {
    patient_id: generatePatientId(),
    name: '',
    age: 0,
    gender: Gender.MALE,
    phone: '',
    email: undefined,
    address: undefined,
    height: undefined,
    weight: undefined,
    bmi: undefined,
    t_score: undefined,
    z_score: undefined,
    risk_level: RiskLevel.LOW,
    medical_history: undefined,
    family_history: undefined,
    medications: undefined
  }
  addPatientDialogVisible.value = true
}

const submitAddPatient = async () => {
  try {
    // 表单验证
    const valid = await addPatientFormRef.value.validate()
    if (!valid) return

    submitting.value = true

    // 计算BMI
    if (addPatientForm.value.height && addPatientForm.value.weight) {
      const heightInMeters = addPatientForm.value.height / 100
      addPatientForm.value.bmi = Number((addPatientForm.value.weight / (heightInMeters * heightInMeters)).toFixed(2))
    }

    // 调用API创建患者
    const response = await request.post('/v1/patients/', addPatientForm.value)
    
    ElMessage.success('患者创建成功')
    addPatientDialogVisible.value = false
    
    // 刷新患者列表
    await fetchPatients()
    
  } catch (error: any) {
    console.error('创建患者失败:', error)
    ElMessage.error(`创建患者失败: ${error.response?.data?.detail || error.message}`)
  } finally {
    submitting.value = false
  }
}


const fetchPatients = async () => {
  try {
    loading.value = true
    
    // 调用API获取患者列表，后端会根据用户类型自动过滤
    const response = await request.get('/v1/patients/', {
      params: {
        skip: (currentPage.value - 1) * pageSize.value,
        limit: pageSize.value,
        search: searchKeyword.value || undefined,
        risk_level: riskLevelFilter.value || undefined
      }
    })
    
    // 处理不同的响应格式
    if (response && (response as any).patients) {
      // 标准格式：{ patients: [...], total: 3, page: 1, size: 10 }
      patients.value = (response as any).patients
      total.value = (response as any).total || 0
    } else if (response && response.data && response.data.patients) {
      // 嵌套格式：{ data: { patients: [...] } }
      patients.value = response.data.patients
      total.value = response.data.total || 0
    } else if (Array.isArray(response)) {
      // 直接数组格式
      patients.value = response
      total.value = response.length
    } else {
      patients.value = []
      total.value = 0
    }
    
  } catch (error: any) {
    console.error('获取患者列表失败:', error)
    ElMessage.error('获取患者列表失败')
    patients.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

const refreshPatients = () => {
  currentPage.value = 1
  fetchPatients()
}

const handleSearch = () => {
  currentPage.value = 1
  fetchPatients()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  fetchPatients()
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
  fetchPatients()
}

const viewPatient = (patient: Patient) => {
  selectedPatient.value = patient
  patientDetailDialogVisible.value = true
}

const editPatient = (patient: Patient) => {
  // 复制患者数据到编辑表单
  editPatientForm.value = {
    name: patient.name,
    age: patient.age,
    gender: patient.gender,
    phone: patient.phone,
    email: patient.email,
    address: patient.address,
    height: patient.height,
    weight: patient.weight,
    bmi: patient.bmi,
    t_score: patient.t_score,
    z_score: patient.z_score,
    risk_level: patient.risk_level,
    medical_history: patient.medical_history,
    family_history: patient.family_history,
    medications: patient.medications
  }
  
  // 保存当前编辑的患者ID
  selectedPatient.value = patient
  editPatientDialogVisible.value = true
}

const submitEditPatient = async () => {
  if (!selectedPatient.value) {
    ElMessage.warning('请先选择要编辑的患者')
    return
  }

  try {
    // 表单验证
    const valid = await editPatientFormRef.value.validate()
    if (!valid) return

    editing.value = true

    // 计算BMI
    if (editPatientForm.value.height && editPatientForm.value.weight) {
      const heightInMeters = editPatientForm.value.height / 100
      editPatientForm.value.bmi = Number((editPatientForm.value.weight / (heightInMeters * heightInMeters)).toFixed(2))
    }

    // 调用API更新患者
            const response = await request.put(`/v1/patients/${selectedPatient.value.id}`, editPatientForm.value)
    
    ElMessage.success('患者信息更新成功')
    editPatientDialogVisible.value = false
    
    // 刷新患者列表
    await fetchPatients()
    
  } catch (error: any) {
    console.error('更新患者失败:', error)
    ElMessage.error(`更新患者失败: ${error.response?.data?.detail || error.message}`)
  } finally {
    editing.value = false
  }
}

const deletePatient = async (patient: Patient) => {
  try {
    await ElMessageBox.confirm(`确定要删除患者 "${patient.name}" 吗？`, '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })

            await request.delete(`/v1/patients/${patient.id}`)
    ElMessage.success('患者删除成功')
    await fetchPatients()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除患者失败:', error)
      ElMessage.error(`删除患者失败: ${error.response?.data?.detail || error.message}`)
    }
  }
}

const testPatientsAPI = async () => {
  try {
    const response = await request.get('/v1/patients/')
    ElMessage.success(`患者列表API正常，患者数量: ${response.data?.total || 0}`)
  } catch (error) {
    ElMessage.error('患者列表API测试失败')
  }
}

const viewPatientArchive = (patient: any) => {
  // 调用原来的查看患者详情方法
  viewPatient(patient)
}

// 判断是否为管理员（简单判断：用户名为"admin"或包含"管理员"）
const isAdmin = () => {
  const username = userStore.user?.username || ''
  return username === 'admin' || username.includes('管理员') || username.includes('admin')
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

// 生命周期
onMounted(async () => {
  // 所有用户类型都需要获取患者列表
  // 机构用户获取所有患者，个人用户获取自己的患者
  await fetchPatients()
})
</script>

<style scoped>
.followup-search {
  padding: 20px;
}

.status-section {
  margin-bottom: 20px;
}

.action-section {
  margin: 20px 0;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.patient-section {
  margin-top: 20px;
}

.search-filters {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.pagination-wrapper {
  margin-top: 20px;
  text-align: center;
}

.patient-detail {
  padding: 20px 0;
}

.dialog-footer {
  text-align: right;
}

/* 医疗机构容器样式 */
.medical-institutions-section {
  margin-top: 20px;
}

.institutions-container {
  padding: 10px 0;
}

.no-institutions {
  text-align: center;
  padding: 40px 0;
}

.institutions-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
}

.institution-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
}

.institution-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  border-color: #667eea;
}

.institution-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e9ecef;
}

.institution-header h4 {
  margin: 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.institution-info p {
  margin: 6px 0;
  font-size: 14px;
  color: #666;
  line-height: 1.4;
}

.institution-info strong {
  color: #333;
  font-weight: 600;
}

/* 操作按钮样式 */
.action-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
}

.action-buttons .el-button {
  margin: 0;
  flex-shrink: 0;
}
</style> 