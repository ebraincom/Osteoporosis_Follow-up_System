import request from '@/utils/request'
import type { Patient, PatientCreate, PatientUpdate, PatientList } from '@/types/patient'

export const patientApi = {
  // 获取患者列表
  getPatients: (params: {
    skip?: number
    limit?: number
    search?: string
    risk_level?: string
  } = {}): Promise<PatientList> => {
    return request.get('/v1/patients', { params })
  },

  // 获取单个患者信息
  getPatient: (patientId: number): Promise<Patient> => {
    return request.get(`/v1/patients/${patientId}`)
  },

  // 创建新患者
  createPatient: (data: PatientCreate): Promise<Patient> => {
    return request.post('/v1/patients', data)
  },

  // 更新患者信息
  updatePatient: (patientId: number, data: PatientUpdate): Promise<Patient> => {
    return request.put(`/v1/patients/${patientId}`, data)
  },

  // 删除患者
  deletePatient: (patientId: number): Promise<void> => {
    return request.delete(`/v1/patients/${patientId}`)
  },

  // 获取患者统计信息
  getPatientStatistics: (): Promise<any> => {
    return request.get('/v1/patients/statistics')
  }
} 