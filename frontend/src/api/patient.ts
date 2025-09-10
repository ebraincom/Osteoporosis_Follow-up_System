import request from '@/utils/request'

export interface PatientQuery {
  skip?: number
  limit?: number
  search?: string
  risk_level?: string
}

export const patientApi = {
  // 获取患者列表
  getPatients: (params?: PatientQuery) => {
    return request.get('/v1/patients/', { params })
  },

  // 获取单个患者信息
  getPatient: (patientId: number) => {
    return request.get(`/v1/patients/${patientId}`)
  },

  // 创建患者
  createPatient: (data: any) => {
    return request.post('/v1/patients/', data)
  },

  // 更新患者信息
  updatePatient: (patientId: number, data: any) => {
    return request.put(`/v1/patients/${patientId}`, data)
  },

  // 删除患者
  deletePatient: (patientId: number) => {
    return request.delete(`/v1/patients/${patientId}`)
  },

  // 根据风险等级获取患者
  getPatientsByRiskLevel: (riskLevel: string) => {
    return request.get(`/v1/patients/risk-level/${riskLevel}`)
  },

  // 获取患者统计信息
  getPatientStatistics: () => {
    return request.get('/v1/patients/statistics/overview')
  }
}