<template>
  <div class="add-patient-form">
    <el-form 
      ref="formRef" 
      :model="form" 
      :rules="rules" 
      label-width="120px"
      @submit.prevent="handleSubmit"
    >
      <!-- 基本信息 -->
      <el-divider content-position="left">基本信息</el-divider>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="患者姓名" prop="name">
            <el-input v-model="form.name" placeholder="请输入患者姓名" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="年龄" prop="age">
            <el-input-number v-model="form.age" :min="1" :max="120" placeholder="请输入年龄" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="性别" prop="gender">
            <el-radio-group v-model="form.gender">
              <el-radio label="male">男</el-radio>
              <el-radio label="female">女</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="联系电话" prop="phone">
            <el-input v-model="form.phone" placeholder="请输入联系电话" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="身份证号" prop="idCard">
            <el-input v-model="form.idCard" placeholder="请输入身份证号" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="随访等级" prop="followUpLevel">
            <el-select v-model="form.followUpLevel" placeholder="请选择随访等级">
              <el-option label="高危" value="high" />
              <el-option label="中危" value="medium" />
              <el-option label="低危" value="low" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item label="家庭住址" prop="address">
        <el-input v-model="form.address" placeholder="请输入家庭住址" />
      </el-form-item>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="紧急联系人" prop="emergencyContact">
            <el-input v-model="form.emergencyContact" placeholder="请输入紧急联系人" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="紧急联系电话" prop="emergencyPhone">
            <el-input v-model="form.emergencyPhone" placeholder="请输入紧急联系电话" />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 体格检查 -->
      <el-divider content-position="left">体格检查</el-divider>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="身高(cm)" prop="height">
            <el-input-number v-model="form.height" :min="100" :max="250" placeholder="身高" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="体重(kg)" prop="weight">
            <el-input-number v-model="form.weight" :min="20" :max="200" placeholder="体重" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="BMI">
            <el-input :value="bmi" disabled placeholder="自动计算" />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 骨密度检查 -->
      <el-divider content-position="left">骨密度检查</el-divider>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="腰椎T值" prop="lumbarTScore">
            <el-input-number v-model="form.lumbarTScore" :min="-5" :max="5" :precision="1" placeholder="腰椎T值" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="股骨颈T值" prop="femoralNeckTScore">
            <el-input-number v-model="form.femoralNeckTScore" :min="-5" :max="5" :precision="1" placeholder="股骨颈T值" />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 实验室检查 -->
      <el-divider content-position="left">实验室检查</el-divider>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-form-item label="血钙" prop="bloodCalcium">
            <el-input-number v-model="form.bloodCalcium" :min="1" :max="4" :precision="1" placeholder="mmol/L" />
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="血磷" prop="bloodPhosphorus">
            <el-input-number v-model="form.bloodPhosphorus" :min="0.5" :max="2" :precision="1" placeholder="mmol/L" />
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="25-羟维生素D" prop="vitaminD">
            <el-input-number v-model="form.vitaminD" :min="5" :max="100" placeholder="ng/ml" />
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="甲状旁腺激素" prop="parathyroidHormone">
            <el-input-number v-model="form.parathyroidHormone" :min="10" :max="100" placeholder="pg/ml" />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 病史信息 -->
      <el-divider content-position="left">病史信息</el-divider>
      <el-form-item label="主诉" prop="chiefComplaint">
        <el-input v-model="form.chiefComplaint" type="textarea" :rows="2" placeholder="请输入主诉" />
      </el-form-item>
      
      <el-form-item label="现病史" prop="presentIllness">
        <el-input v-model="form.presentIllness" type="textarea" :rows="3" placeholder="请输入现病史" />
      </el-form-item>
      
      <el-form-item label="既往史" prop="pastHistory">
        <el-input v-model="form.pastHistory" type="textarea" :rows="2" placeholder="请输入既往史" />
      </el-form-item>
      
      <el-form-item label="个人史" prop="personalHistory">
        <el-input v-model="form.personalHistory" type="textarea" :rows="2" placeholder="请输入个人史" />
      </el-form-item>
      
      <el-form-item label="家族史" prop="familyHistory">
        <el-input v-model="form.familyHistory" type="textarea" :rows="2" placeholder="请输入家族史" />
      </el-form-item>

      <!-- 诊断和治疗 -->
      <el-divider content-position="left">诊断和治疗</el-divider>
      <el-form-item label="诊断" prop="diagnosis">
        <el-input v-model="form.diagnosis" type="textarea" :rows="2" placeholder="请输入诊断" />
      </el-form-item>
      
      <el-form-item label="治疗方案" prop="treatmentPlan">
        <el-input v-model="form.treatmentPlan" type="textarea" :rows="3" placeholder="请输入治疗方案" />
      </el-form-item>

      <!-- 按钮 -->
      <el-form-item>
        <el-button type="primary" @click="handleSubmit" :loading="loading">保存患者</el-button>
        <el-button @click="$emit('cancel')">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import type { PatientDetailInfo } from '@/types/patient'

const emit = defineEmits<{
  submit: [patient: Omit<PatientDetailInfo, 'id'>]
  cancel: []
}>()

const formRef = ref<FormInstance>()
const loading = ref(false)

// 表单数据
const form = ref({
  name: '',
  age: undefined as number | undefined,
  gender: '' as 'male' | 'female' | '',
  phone: '',
  idCard: '',
  address: '',
  emergencyContact: '',
  emergencyPhone: '',
  followUpLevel: '' as 'high' | 'medium' | 'low' | '',
  height: undefined as number | undefined,
  weight: undefined as number | undefined,
  lumbarTScore: undefined as number | undefined,
  femoralNeckTScore: undefined as number | undefined,
  bloodCalcium: undefined as number | undefined,
  bloodPhosphorus: undefined as number | undefined,
  vitaminD: undefined as number | undefined,
  parathyroidHormone: undefined as number | undefined,
  chiefComplaint: '',
  presentIllness: '',
  pastHistory: '',
  personalHistory: '',
  familyHistory: '',
  diagnosis: '',
  treatmentPlan: ''
})

// 计算BMI
const bmi = computed(() => {
  if (form.value.height && form.value.weight) {
    const heightInMeters = form.value.height / 100
    return (form.value.weight / (heightInMeters * heightInMeters)).toFixed(1)
  }
  return ''
})

// 表单验证规则
const rules: FormRules = {
  name: [
    { required: true, message: '请输入患者姓名', trigger: 'blur' }
  ],
  age: [
    { required: true, message: '请输入年龄', trigger: 'blur' }
  ],
  gender: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ],
  phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  idCard: [
    { required: true, message: '请输入身份证号', trigger: 'blur' },
    { pattern: /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/, message: '请输入正确的身份证号', trigger: 'blur' }
  ],
  address: [
    { required: true, message: '请输入家庭住址', trigger: 'blur' }
  ],
  emergencyContact: [
    { required: true, message: '请输入紧急联系人', trigger: 'blur' }
  ],
  emergencyPhone: [
    { required: true, message: '请输入紧急联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  followUpLevel: [
    { required: true, message: '请选择随访等级', trigger: 'change' }
  ],
  height: [
    { required: true, message: '请输入身高', trigger: 'blur' }
  ],
  weight: [
    { required: true, message: '请输入体重', trigger: 'blur' }
  ],
  chiefComplaint: [
    { required: true, message: '请输入主诉', trigger: 'blur' }
  ],
  diagnosis: [
    { required: true, message: '请输入诊断', trigger: 'blur' }
  ]
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    // 构建患者数据
    const patientData: Omit<PatientDetailInfo, 'id'> = {
      name: form.value.name,
      age: form.value.age!,
      gender: form.value.gender as 'male' | 'female',
      phone: form.value.phone,
      idCard: form.value.idCard,
      address: form.value.address,
      emergencyContact: form.value.emergencyContact,
      emergencyPhone: form.value.emergencyPhone,
      followUpLevel: form.value.followUpLevel as 'high' | 'medium' | 'low',
      registrationDate: new Date().toISOString().split('T')[0],
      lastVisitDate: new Date().toISOString().split('T')[0],
      nextVisitDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      height: form.value.height!,
      weight: form.value.weight!,
      bmi: parseFloat(bmi.value),
      lumbarTScore: form.value.lumbarTScore || 0,
      femoralNeckTScore: form.value.femoralNeckTScore || 0,
      bloodCalcium: form.value.bloodCalcium || 0,
      bloodPhosphorus: form.value.bloodPhosphorus || 0,
      vitaminD: form.value.vitaminD || 0,
      parathyroidHormone: form.value.parathyroidHormone || 0,
      chiefComplaint: form.value.chiefComplaint,
      presentIllness: form.value.presentIllness,
      pastHistory: form.value.pastHistory,
      personalHistory: form.value.personalHistory,
      familyHistory: form.value.familyHistory,
      diagnosis: form.value.diagnosis,
      treatmentPlan: form.value.treatmentPlan,
      followUpRecords: []
    }
    
    emit('submit', patientData)
    ElMessage.success('患者信息保存成功')
  } catch (error) {
    console.error('表单验证失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.add-patient-form {
  padding: 20px;
}

.el-divider {
  margin: 20px 0;
}

.el-divider__text {
  font-weight: 600;
  color: #333;
}

.el-form-item {
  margin-bottom: 18px;
}

.el-row {
  margin-bottom: 0;
}

.el-col {
  margin-bottom: 0;
}
</style> 