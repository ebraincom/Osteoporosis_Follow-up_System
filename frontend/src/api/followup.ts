import request from '@/utils/request'

// 获取个人用户的随访记录列表
export function getMyFollowupRecords(params?: {
  skip?: number
  limit?: number
}) {
  return request({
    url: '/v1/followups/my-records',
    method: 'get',
    params
  })
}

// 获取指定患者的随访记录列表
export function getPatientFollowupRecords(patientId: number, params?: {
  skip?: number
  limit?: number
}) {
  return request({
    url: `/v1/followups/patient/${patientId}`,
    method: 'get',
    params
  })
}

// 获取随访记录详情
export function getFollowupRecord(followupId: number) {
  return request({
    url: `/v1/followups/${followupId}`,
    method: 'get'
  })
}

// 创建随访记录
export function createFollowupRecord(data: any) {
  return request({
    url: '/v1/followups/',
    method: 'post',
    data
  })
}

// 更新随访记录
export function updateFollowupRecord(followupId: number, data: any) {
  return request({
    url: `/v1/followups/${followupId}`,
    method: 'put',
    data
  })
}

// 删除随访记录
export function deleteFollowupRecord(followupId: number) {
  return request({
    url: `/v1/followups/${followupId}`,
    method: 'delete'
  })
} 