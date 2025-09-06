import request from '@/utils/request'
import type { LoginForm, RegisterForm, AuthResponse, User } from '@/types/user'

export const authApi = {
  login: (data: LoginForm): Promise<AuthResponse> => {
    return request.post('/v1/auth/login', data)
  },

  register: (data: RegisterForm): Promise<AuthResponse> => {
    // 转换字段名以匹配后端API，移除前端特有字段，处理undefined值
    const { userType, confirmPassword, ...restData } = data
    const backendData = {
      ...restData,
      user_type: userType,
      // 将undefined值转换为null，避免后端验证错误
      age: restData.age || null,
      gender: restData.gender || null,
      phone: restData.phone || null,
      institution: restData.institution || null,
      department: restData.department || null
    }
    return request.post('/v1/auth/register', backendData)
  },

  getCurrentUser: (): Promise<User> => {
    return request.get('/v1/users/me')
  },

  refreshToken: (): Promise<{ token: string }> => {
    return request.post('/v1/auth/refresh')
  },

  logout: (): Promise<void> => {
    return request.post('/v1/auth/logout')
  }
} 