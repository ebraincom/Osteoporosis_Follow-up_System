import request from '@/utils/request'

export interface FollowupResponseCreate {
  followup_id: number
  overall_feeling?: string
  improvement_level?: string
  medication_adherence?: string
  exercise_volume?: string
  diet_adjustment?: string
  pain_level?: number
  sleep_quality?: string
  daily_activity?: string
  mood_status?: string
  side_effects?: string
  concerns?: string
  additional_info?: string
}

export interface FollowupResponseUpdate {
  overall_feeling?: string
  improvement_level?: string
  medication_adherence?: string
  exercise_volume?: string
  diet_adjustment?: string
  pain_level?: number
  sleep_quality?: string
  daily_activity?: string
  mood_status?: string
  side_effects?: string
  concerns?: string
  additional_info?: string
  is_completed?: boolean
}

export interface FollowupResponseQuery {
  skip?: number
  limit?: number
  patient_id?: number
  followup_id?: number
  is_completed?: boolean
}

export const followupResponseApi = {
  // 创建随访应答
  createResponse: (data: FollowupResponseCreate) => {
    return request.post('/v1/followup-responses/', data)
  },

  // 获取随访应答列表
  getResponses: (params?: FollowupResponseQuery) => {
    return request.get('/v1/followup-responses/', { params })
  },

  // 获取包含患者信息的随访应答列表（机构用户）
  getResponsesWithPatientInfo: (params?: FollowupResponseQuery) => {
    return request.get('/v1/followup-responses/with-patient-info', { params })
  },

  // 获取待回复的随访记录（个人用户）
  getPendingResponses: (params?: { skip?: number; limit?: number }) => {
    return request.get('/v1/followup-responses/pending', { params })
  },

  // 获取单个随访应答
  getResponse: (responseId: number) => {
    return request.get(`/v1/followup-responses/${responseId}`)
  },

  // 更新随访应答
  updateResponse: (responseId: number, data: FollowupResponseUpdate) => {
    return request.put(`/v1/followup-responses/${responseId}`, data)
  },

  // 删除随访应答
  deleteResponse: (responseId: number) => {
    return request.delete(`/v1/followup-responses/${responseId}`)
  },

  // 获取指定患者的随访应答列表
  getPatientResponses: (patientId: number, params?: { skip?: number; limit?: number }) => {
    return request.get(`/v1/followup-responses/patient/${patientId}`, { params })
  }
}