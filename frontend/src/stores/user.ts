import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import type { User, LoginForm, RegisterForm } from '@/types/user'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const loading = ref(false)
  const isInitialized = ref(false)

  const isAuthenticated = computed(() => {
    const result = !!token.value
    console.log('useUserStore: isAuthenticated 计算:', {
      hasToken: !!token.value,
      tokenValue: token.value ? token.value.substring(0, 20) + '...' : null,
      result
    })
    return result
  })

  // 初始化用户状态（同步）
  const initializeAuth = () => {
    const storedToken = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')
    
    if (storedToken) {
      token.value = storedToken
      if (storedUser) {
        try {
          user.value = JSON.parse(storedUser)
        } catch (error) {
          console.error('解析用户信息失败:', error)
          localStorage.removeItem('user')
        }
      }
    }
    isInitialized.value = true
  }

  const login = async (loginForm: LoginForm) => {
    try {
      loading.value = true
      const response = await authApi.login(loginForm)
      console.log('登录响应:', response)
      
      // 确保token字段存在
      const tokenValue = response.token || response.access_token
      if (!tokenValue) {
        console.error('登录响应中没有token字段:', response)
        return { success: false, error: '登录响应格式错误' }
      }
      
      token.value = tokenValue
      user.value = response.user
      localStorage.setItem('token', tokenValue)
      localStorage.setItem('user', JSON.stringify(response.user))
      
      console.log('登录成功，token已存储:', {
        hasToken: !!tokenValue,
        tokenValue: tokenValue.substring(0, 20) + '...'
      })
      
      return { success: true }
    } catch (error: any) {
      console.error('登录失败:', error)
      
      // 提取具体的错误信息
      let errorMessage = '登录失败，请检查输入信息'
      
      if (error?.response?.data?.detail) {
        // 后端返回的具体错误信息
        errorMessage = error.response.data.detail
      } else if (error?.response?.data?.message) {
        // 其他格式的错误信息
        errorMessage = error.response.data.message
      } else if (error?.message) {
        // 网络错误或其他错误
        errorMessage = error.message
      }
      
      return { success: false, error: errorMessage }
    } finally {
      loading.value = false
    }
  }

  const register = async (registerForm: RegisterForm) => {
    try {
      loading.value = true
      
      console.log('注册表单数据:', registerForm)
      console.log('注册表单数据类型:', {
        username: typeof registerForm.username,
        password: typeof registerForm.password,
        name: typeof registerForm.name,
        phone: typeof registerForm.phone,
        userType: typeof registerForm.userType,
        institution: typeof registerForm.institution,
        department: typeof registerForm.department,
        age: typeof registerForm.age,
        gender: typeof registerForm.gender
      })
      
      const response = await authApi.register(registerForm)
      console.log('注册响应:', response)
      
      // 确保token字段存在
      const tokenValue = response.token || response.access_token
      if (!tokenValue) {
        console.error('注册响应中没有token字段:', response)
        return { success: false, error: '注册响应格式错误' }
      }
      
      token.value = tokenValue
      user.value = response.user
      localStorage.setItem('token', tokenValue)
      localStorage.setItem('user', JSON.stringify(response.user))
      
      console.log('注册成功，token已存储:', {
        hasToken: !!tokenValue,
        tokenValue: tokenValue.substring(0, 20) + '...'
      })
      
      return { success: true }
    } catch (error) {
      console.error('注册失败:', error)
      return { success: false, error: error as string }
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const checkAuthStatus = async () => {
    if (token.value && !user.value) {
      try {
        const response = await authApi.getCurrentUser()
        user.value = response
        localStorage.setItem('user', JSON.stringify(response))
      } catch (error) {
        console.error('验证用户状态失败:', error)
        logout()
      }
    }
  }

  const updateUser = (updatedUser: Partial<User>) => {
    if (user.value) {
      user.value = { ...user.value, ...updatedUser }
      localStorage.setItem('user', JSON.stringify(user.value))
    }
  }

  const setUser = (newUser: User) => {
    user.value = newUser
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  return {
    user,
    token,
    loading,
    isInitialized,
    isAuthenticated,
    initializeAuth,
    login,
    register,
    logout,
    checkAuthStatus,
    updateUser,
    setUser
  }
}) 