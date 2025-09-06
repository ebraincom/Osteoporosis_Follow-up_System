// 历史记录基础类型
export interface BaseHistoryRecord {
  id: string
  date: string
  title: string
  type: 'voice' | 'diet' | 'his' | 'validation'
  summary: string
}

// 语音自述历史记录
export interface VoiceHistoryRecord extends BaseHistoryRecord {
  type: 'voice'
  conversations: VoiceConversation[]
  duration?: number // 录音时长（秒）
}

// 饮食识别历史记录
export interface DietHistoryRecord extends BaseHistoryRecord {
  type: 'diet'
  foodImage: string
  nutritionData: NutritionData
  benefits: string[]
  recommendations: string[]
}

// HIS接口历史记录
export interface HISHistoryRecord extends BaseHistoryRecord {
  type: 'his'
  hospital: string
  patientInfo: PatientInfo
  reportContent: string
  images: string[]
}

// 校验规则历史记录
export interface ValidationHistoryRecord extends BaseHistoryRecord {
  type: 'validation'
  rules: ValidationRule[]
  status: 'passed' | 'failed' | 'warning'
}

// 语音对话
export interface VoiceConversation {
  role: 'user' | 'ai'
  content: string
  timestamp: string
}

// 营养数据
export interface NutritionData {
  calories: number
  protein: number
  fat: number
  carbohydrates: number
  calcium: number
  vitaminD: number
  otherNutrients: Record<string, number>
}

// 患者信息
export interface PatientInfo {
  name: string
  gender: string
  age: number
  examDate: string
  examType: string
}

// 校验规则
export interface ValidationRule {
  name: string
  description: string
  status: 'passed' | 'failed' | 'warning'
  details: string
}

// 历史记录类型联合
export type HistoryRecord = VoiceHistoryRecord | DietHistoryRecord | HISHistoryRecord | ValidationHistoryRecord 