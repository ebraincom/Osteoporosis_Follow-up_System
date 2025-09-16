import request from '@/utils/request'

export interface FollowupCreate {
  patient_id: number
  time: string
  method: string
  location: string
  details: string
  notes?: string
  patient_status: string
  next_followup_date?: string
  recommendations?: string
}

export interface FollowupUpdate {
  time?: string
  method?: string
  location?: string
  details?: string
  notes?: string
  patient_status?: string
  next_followup_date?: string
  recommendations?: string
}

export interface FollowupQuery {
  skip?: number
  limit?: number
  patient_id?: number
}

export const followupApi = {
  // 创建随访记录
  createFollowup: (data: FollowupCreate) => {
    return request.post('/v1/followups/', data)
  },

  // 获取随访记录列表
  getFollowups: (params?: FollowupQuery) => {
    return request.get('/v1/followups/', { params })
  },

  // 获取指定患者的随访记录
  getPatientFollowups: (patientId: number, params?: { skip?: number; limit?: number }) => {
    return request.get(`/v1/followups/patient/${patientId}`, { params })
  },

  // 获取我的随访记录
  getMyFollowups: (params?: { skip?: number; limit?: number }) => {
    return request.get('/v1/followups/my-records', { params })
  },

  // 获取单个随访记录
  getFollowup: (followupId: number) => {
    return request.get(`/v1/followups/${followupId}`)
  },

  // 更新随访记录
  updateFollowup: (followupId: number, data: FollowupUpdate) => {
    return request.put(`/v1/followups/${followupId}`, data)
  },

  // 删除随访记录
  deleteFollowup: (followupId: number) => {
    return request.delete(`/v1/followups/${followupId}`)
  }
}