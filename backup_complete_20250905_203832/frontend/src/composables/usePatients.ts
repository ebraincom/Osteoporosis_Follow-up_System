
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { patientApi } from '@/api/patient'
import type { Patient, PatientCreate, PatientUpdate, PatientList, PatientFormData } from '@/types/patient'
import { Gender, RiskLevel } from '@/types/patient'

// 模拟患者数据（已禁用，留空以避免类型冲突）
const mockPatients: Patient[] = []

export function usePatients() {
  // 响应式数据
  const patients = ref<Patient[]>([])
  const loading = ref(false)
  const total = ref(0)
  const currentPage = ref(1)
  const pageSize = ref(10)
  const searchKeyword = ref('')
  const riskLevelFilter = ref('')
  const useMockData = ref(false) // 使用真实API

  // 计算属性
  const filteredPatients = computed(() => {
    let result = patients.value

    // 风险等级筛选
    if (riskLevelFilter.value && riskLevelFilter.value !== 'all') {
      result = result.filter(patient => patient.risk_level === riskLevelFilter.value)
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

  // 获取患者列表
  const fetchPatients = async (params: {
    skip?: number
    limit?: number
    search?: string
    risk_level?: string
  } = {}) => {
    try {
      loading.value = true
      
      if (useMockData.value) {
        // 使用模拟数据
        await new Promise(resolve => setTimeout(resolve, 500)) // 模拟网络延迟
        
        let filteredData = [...mockPatients]
        
        // 搜索过滤
        if (params.search) {
          filteredData = filteredData.filter(p => 
            p.name.includes(params.search!) || 
            p.patient_id.includes(params.search!) ||
            p.phone.includes(params.search!)
          )
        }
        
        // 风险等级过滤
        if (params.risk_level && params.risk_level !== 'all') {
          filteredData = filteredData.filter(p => p.risk_level === params.risk_level)
        }
        
        patients.value = filteredData
        total.value = filteredData.length
        currentPage.value = 1
        pageSize.value = params.limit || 10
        
        return {
          patients: filteredData,
          total: filteredData.length,
          page: 1,
          size: params.limit || 10,
          pages: Math.ceil(filteredData.length / (params.limit || 10))
        }
      } else {
        // 使用真实API - 修复参数传递问题
        const apiParams: any = {
          skip: params.skip || (currentPage.value - 1) * pageSize.value,
          limit: params.limit || pageSize.value
        }
        
        // 只有当搜索关键词不为空时才传递
        if (params.search && params.search.trim()) {
          apiParams.search = params.search.trim()
        }
        
        // 只有当风险等级不为空且不是'all'时才传递
        if (params.risk_level && params.risk_level.trim() && params.risk_level !== 'all') {
          apiParams.risk_level = params.risk_level.trim()
        }
        
        console.log('usePatients: 调用API参数:', apiParams)
        
        const response = await patientApi.getPatients(apiParams)
        
        patients.value = response.patients
        total.value = response.total
        currentPage.value = response.page
        pageSize.value = response.size
        
        return response
      }
    } catch (error) {
      console.error('获取患者列表失败:', error)
      ElMessage.error('获取患者列表失败')
      
      // 如果API失败，回退到模拟数据
      if (!useMockData.value) {
        useMockData.value = true
        ElMessage.warning('API连接失败，使用模拟数据')
        return fetchPatients(params)
      }
      
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取单个患者
  const fetchPatient = async (patientId: number) => {
    try {
      loading.value = true
      const patient = await patientApi.getPatient(patientId)
      return patient
    } catch (error) {
      console.error('获取患者信息失败:', error)
      ElMessage.error('获取患者信息失败')
      throw error
    } finally {
      loading.value = false
    }
  }

  // 创建患者
  const createPatient = async (formData: PatientFormData) => {
    try {
      console.log('usePatients: createPatient 开始执行')
      console.log('usePatients: 表单数据:', formData)
      
      loading.value = true
      
      // 检查认证状态
      const token = localStorage.getItem('token')
      console.log('usePatients: 当前token:', token ? token.substring(0, 20) + '...' : null)
      
      if (!token) {
        console.error('usePatients: 没有找到token，无法创建患者')
        throw new Error('未认证，请重新登录')
      }
      
      // 转换数据格式
      const patientData: PatientCreate = {
        patient_id: generatePatientId(), // 生成患者编号
        name: formData.name,
        age: formData.age,
        gender: formData.gender as Gender, // 直接转换，因为表单中的值已经是 'male' 或 'female'
        phone: formData.phone,
        email: undefined, // 可选字段
        address: formData.address || undefined,
        height: undefined, // 可选字段
        weight: undefined, // 可选字段
        bmi: undefined, // 可选字段
        t_score: undefined, // 可选字段
        z_score: undefined, // 可选字段
        risk_level: formData.level as RiskLevel, // 直接转换，因为表单中的值已经是 'low', 'medium', 'high'
        medical_history: formData.currentHistory || undefined,
        family_history: formData.pastHistory || undefined,
        medications: formData.personalHistory || undefined
      }

      console.log('usePatients: 转换后的患者数据:', patientData)
      console.log('usePatients: 准备调用 patientApi.createPatient...')

      const newPatient = await patientApi.createPatient(patientData)

      console.log('usePatients: 患者创建成功:', newPatient)
      
      // 添加到本地列表
      patients.value.unshift(newPatient)
      total.value++
      
      ElMessage.success('患者创建成功')
      return newPatient
    } catch (error) {
      console.error('usePatients: 创建患者失败:', error)
      ElMessage.error(`创建患者失败: ${error}`)
      throw error
    } finally {
      loading.value = false
      console.log('usePatients: createPatient 执行完成')
    }
  }

  // 更新患者
  const updatePatient = async (patientId: number, data: PatientUpdate) => {
    try {
      loading.value = true
      const updatedPatient = await patientApi.updatePatient(patientId, data)
      
      // 更新本地数据
      const index = patients.value.findIndex(p => p.id === patientId)
      if (index !== -1) {
        patients.value[index] = updatedPatient
      }
      
      ElMessage.success('患者信息更新成功')
      return updatedPatient
    } catch (error) {
      console.error('更新患者失败:', error)
      ElMessage.error('更新患者失败')
      throw error
    } finally {
      loading.value = false
    }
  }

  // 删除患者
  const deletePatient = async (patientId: number) => {
    try {
      loading.value = true
      await patientApi.deletePatient(patientId)
      
      // 从本地列表中移除
      patients.value = patients.value.filter(p => p.id !== patientId)
      total.value--
      
      ElMessage.success('患者删除成功')
    } catch (error) {
      console.error('删除患者失败:', error)
      ElMessage.error('删除患者失败')
      throw error
    } finally {
      loading.value = false
    }
  }

  // 生成患者编号
  const generatePatientId = () => {
    const timestamp = Date.now()
    const random = Math.floor(Math.random() * 1000)
    return `BJ-OST-${timestamp}-${random.toString().padStart(3, '0')}`
  }

  // 设置筛选条件
  const setFilter = (filter: string) => {
    riskLevelFilter.value = filter
    currentPage.value = 1
    // 修复：传递正确的参数
    fetchPatients({
      risk_level: filter !== 'all' ? filter : undefined
    })
  }

  // 设置搜索关键词
  const setSearchKeyword = (keyword: string) => {
    searchKeyword.value = keyword
    currentPage.value = 1
    // 修复：传递正确的参数
    fetchPatients({
      search: keyword.trim() || undefined
    })
  }

  // 分页处理
  const handlePageChange = (page: number) => {
    currentPage.value = page
    fetchPatients()
  }

  const handleSizeChange = (size: number) => {
    pageSize.value = size
    currentPage.value = 1
    fetchPatients()
  }

  return {
    // 数据
    patients,
    loading,
    total,
    currentPage,
    pageSize,
    searchKeyword,
    riskLevelFilter,
    filteredPatients,

    // 方法
    fetchPatients,
    fetchPatient,
    createPatient,
    updatePatient,
    deletePatient,
    setFilter,
    setSearchKeyword,
    handlePageChange,
    handleSizeChange
  }
} 