// 风险等级枚举
export enum RiskLevel {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high'
}

// 性别枚举
export enum Gender {
  MALE = 'male',
  FEMALE = 'female'
}

// 患者基础信息
export interface PatientBase {
  patient_id: string
  name: string
  age: number
  gender: Gender
  phone: string
  email?: string
  address?: string
  height?: number
  weight?: number
  bmi?: number
  t_score?: number
  z_score?: number
  risk_level?: RiskLevel
  medical_history?: string
  family_history?: string
  medications?: string
}

// 患者完整信息（包含系统字段）
export interface Patient extends PatientBase {
  id: number
  user_id: number
  created_at: string
  updated_at: string
}

// 创建患者请求
export interface PatientCreate extends PatientBase {}

// 更新患者请求
export interface PatientUpdate {
  patient_id?: string
  name?: string
  age?: number
  gender?: Gender
  phone?: string
  email?: string
  address?: string
  height?: number
  weight?: number
  bmi?: number
  t_score?: number
  z_score?: number
  risk_level?: RiskLevel
  medical_history?: string
  family_history?: string
  medications?: string
}

// 患者列表响应
export interface PatientList {
  patients: Patient[]
  total: number
  page: number
  size: number
  pages: number
}

// 患者统计信息
export interface PatientStatistics {
  total: number
  low_risk: number
  medium_risk: number
  high_risk: number
}

// 前端表单数据（用于新增患者）
export interface PatientFormData {
  name: string
  gender: string
  age: number
  phone: string
  idCard: string
  level: string
  address: string
  emergencyContact: string
  diagnosis: string
  currentHistory: string
  pastHistory: string
  personalHistory: string
} 