import request from '@/utils/request'

// 用户信息接口
export interface UserInfo {
  id: number
  username: string
  email?: string
  name: string
  phone?: string
  user_type: 'institutional' | 'personal'
  institution?: string
  department?: string
  age?: number
  gender?: 'male' | 'female'
  avatar?: string
  is_active: boolean
  is_verified: boolean
  created_at: string
  updated_at?: string
}

// 用户更新接口
export interface UserUpdate {
  name?: string
  phone?: string
  institution?: string
  department?: string
  age?: number
  gender?: 'male' | 'female'
  avatar?: string
}

// 获取当前用户信息
export const getCurrentUser = (): Promise<UserInfo> => {
  return request({
    url: '/v1/users/me',
    method: 'get'
  })
}

// 更新当前用户信息
export const updateCurrentUser = (userData: UserUpdate): Promise<UserInfo> => {
  return request({
    url: '/v1/users/me',
    method: 'put',
    data: userData
  })
}

// 更新用户头像
export const updateUserAvatar = (avatar: string): Promise<UserInfo> => {
  return updateCurrentUser({ avatar })
}