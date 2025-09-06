import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const request = axios.create({
  baseURL: '/api',  // 明确指定API路径，让Vite代理处理
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    console.log('API请求:', config.method?.toUpperCase(), config.url, config.data)
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
      data: error.config?.data
    })
    
    if (response?.status === 401) {
      console.log('检测到401未授权错误，开始处理...')
      
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