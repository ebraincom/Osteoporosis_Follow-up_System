import request from '@/utils/request'
import type { LoginForm, RegisterForm, AuthResponse, User } from '@/types/user'

export const authApi = {
  login: async (data: LoginForm): Promise<AuthResponse> => {
    // 智能登录：先尝试机构用户登录，失败则尝试个人用户登录
    try {
      console.log('尝试机构用户登录...')
      return await request.post('/v1/auth/login', data)
    } catch (error: any) {
      console.log('机构用户登录失败，尝试个人用户登录...')
      try {
        return await request.post('/v1/personal-auth/login', data)
      } catch (personalError: any) {
        // 如果两个都失败，抛出个人用户的错误（通常更具体）
        throw personalError
      }
    }
  },

  register: (data: RegisterForm): Promise<AuthResponse> => {
    console.log('=== 注册数据构造开始 ===')
    console.log('原始注册表单数据:', data)
    
    // 转换字段名以匹配后端API，移除前端特有字段，处理undefined值
    const { userType, confirmPassword, ...restData } = data
    console.log('解构后的数据:', restData)
    
    // 根据用户类型选择不同的接口和数据结构
    if (userType === 'personal') {
      // 个人用户注册 - 使用新的个人用户接口
      const personalData: any = {
        username: restData.username,
        password: restData.password,
        name: restData.name
      }
      
      // 条件添加可选字段
      if (restData.phone !== undefined && restData.phone !== '') {
        personalData.phone = restData.phone
      }
      
      if (restData.age !== undefined && restData.age !== null && String(restData.age).trim() !== '') {
        personalData.age = Number(restData.age)
      }
      
      if (restData.gender !== undefined && restData.gender !== null) {
        // 转换中文性别为英文
        personalData.gender = restData.gender === '男' ? 'male' : 'female'
      }
      
      if (restData.institution !== undefined && restData.institution !== '') {
        personalData.institution = restData.institution
      }
      
      console.log('=== 个人用户注册数据 ===')
      console.log('数据对象:', personalData)
      console.log('=== 注册数据构造完成 ===')
      
      return request.post('/v1/personal-auth/register', personalData)
    } else {
      // 机构用户注册 - 使用原有接口
      const institutionalData: any = {
        username: restData.username,
        password: restData.password,
        name: restData.name,
        user_type: userType
      }
      
      // 条件添加可选字段
      if (restData.phone !== undefined && restData.phone !== '') {
        institutionalData.phone = restData.phone
      }
      
      if (restData.institution !== undefined && restData.institution !== '') {
        institutionalData.institution = restData.institution
      }
      
      if (restData.department !== undefined && restData.department !== '') {
        institutionalData.department = restData.department
      }
      
      console.log('=== 机构用户注册数据 ===')
      console.log('数据对象:', institutionalData)
      console.log('=== 注册数据构造完成 ===')
      
      return request.post('/v1/auth/register', institutionalData)
    }
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