export interface User {
  id: number
  username: string
  name: string
  email: string
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
  email: string
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