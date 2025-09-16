export interface User {
  id: number
  username: string
  name: string
  email?: string  // 改为可选，因为个人用户没有email字段
  phone?: string
  user_type: 'institutional' | 'personal'
  institution?: string
  department?: string
  age?: number
  gender?: 'male' | 'female'
  avatar?: string
  created_at: string
  updated_at?: string
  is_active: boolean
  is_verified: boolean
  // 添加更多字段
  height?: number
  weight?: number
  t_score?: number
  z_score?: number
  risk_level?: string
  address?: string
  medical_history?: string
  family_history?: string
  medications?: string
}

export interface LoginForm {
  username: string
  password: string
}

export interface RegisterForm {
  username: string
  password: string
  confirmPassword: string
  name: string
  phone?: string
  userType: 'institutional' | 'personal'
  institution?: string
  department?: string
  age?: number
  gender?: 'male' | 'female'
}

export interface AuthResponse {
  access_token: string
  token: string
  user: User
  refresh_token?: string
  token_type?: string
  expires_in?: number
} 