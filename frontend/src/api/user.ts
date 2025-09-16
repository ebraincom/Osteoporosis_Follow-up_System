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
  // 从localStorage获取用户类型
  const userStr = localStorage.getItem('user')
  if (userStr) {
    const user = JSON.parse(userStr)
    if (user.user_type === 'personal') {
      return request.get('/v1/personal-auth/me')
    }
  }
  
  // 默认使用机构用户API
  return request.get('/v1/users/me')
}

// 更新当前用户信息
export const updateCurrentUser = (userData: UserUpdate): Promise<UserInfo> => {
  // 从localStorage获取用户类型
  const userStr = localStorage.getItem('user')
  if (userStr) {
    const user = JSON.parse(userStr)
    if (user.user_type === 'personal') {
      return request.put('/v1/personal-auth/me', userData)
    }
  }
  
  // 默认使用机构用户API
  return request.put('/v1/users/me', userData)
}

// 更新用户头像
export const updateUserAvatar = (avatar: string): Promise<UserInfo> => {
  return updateCurrentUser({ avatar })
}