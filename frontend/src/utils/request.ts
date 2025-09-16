import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const request = axios.create({
  baseURL: '',  // 直接使用相对路径，因为后端已经在/v1路径下
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    console.log('=== 请求拦截器开始 ===')
    console.log('API请求:', config.method?.toUpperCase(), config.url)
    console.log('原始数据:', config.data)
    console.log('数据类型:', typeof config.data)
    
    // 检查数据序列化
    if (config.data && typeof config.data === 'object') {
      try {
        const jsonString = JSON.stringify(config.data)
        console.log('JSON序列化结果:', jsonString)
        console.log('JSON序列化长度:', jsonString.length)
        
        // 验证JSON格式
        const parsed = JSON.parse(jsonString)
        console.log('JSON解析验证:', parsed)
        console.log('数据完整性检查:', {
          hasUsername: !!parsed.username,
          hasPassword: !!parsed.password,
          hasName: !!parsed.name,
          hasUserType: !!parsed.user_type,
          username: parsed.username,
          name: parsed.name
        })
      } catch (error) {
        console.error('JSON序列化/解析错误:', error)
      }
    }
    
    // 直接从 localStorage 读取，避免store未初始化造成的丢失
    const token = localStorage.getItem('token')
    console.log('请求拦截器 - Token检查:', {
      hasToken: !!token,
      tokenValue: token ? token.substring(0, 20) + '...' : null,
      url: config.url
    })
    if (token) {
      ;(config.headers as any).Authorization = `Bearer ${token}`
      console.log('请求拦截器 - 已添加Authorization头')
    } else {
      console.log('请求拦截器 - 没有找到token')
    }
    
    console.log('=== 请求拦截器完成 ===')
    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const { response } = error
    
    console.log('请求响应拦截器捕获错误:', {
      status: response?.status,
      url: error.config?.url,
      method: error.config?.method,
      data: error.config?.data,
      responseData: response?.data
    })
    
    if (response?.status === 401) {
      console.log('检测到401未授权错误，开始处理...')
      
      // 检查是否是登录页面的请求，如果是则不自动跳转
      const isLoginRequest = error.config?.url?.includes('/login')
      
      if (isLoginRequest) {
        console.log('这是登录请求的401错误，不执行自动登出')
        // 对于登录请求的401错误，直接返回错误，让登录组件处理
        return Promise.reject(error)
      }
      
      // 检查是否是用户状态初始化过程中的错误
      const userStore = useUserStore()
      if (!userStore.isInitialized) {
        console.log('用户状态尚未初始化，跳过401处理')
        return Promise.reject(error)
      }
      
      console.log('用户状态已初始化，执行登出操作')
      userStore.logout()
      window.location.href = '/login'
      ElMessage.error('登录已过期，请重新登录')
    } else if (response?.status === 403) {
      ElMessage.error('权限不足')
    } else if (response?.status === 404) {
      ElMessage.error('请求的资源不存在')
    } else if (response?.status === 500) {
      ElMessage.error('服务器内部错误')
    } else {
      ElMessage.error(response?.data?.message || '网络错误')
    }
    
    return Promise.reject(error)
  }
)

export default request 