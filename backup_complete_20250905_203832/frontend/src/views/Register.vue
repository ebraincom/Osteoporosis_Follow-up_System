<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-card glass-card">
        <div class="register-header">
          <el-icon class="logo-icon"><Monitor /></el-icon>
          <h2>注册账号</h2>
          <p>创建您的骨质疏松症随访系统账号</p>
        </div>

        <el-form
          ref="registerFormRef"
          :model="registerForm"
          :rules="registerRules"
          class="register-form"
          @submit.prevent="handleRegister"
        >
          <!-- 用户类型选择 -->
          <el-form-item>
            <el-radio-group v-model="registerForm.userType" class="user-type-group">
              <el-radio label="institutional">机构用户</el-radio>
              <el-radio label="personal">个人用户</el-radio>
            </el-radio-group>
          </el-form-item>

          <!-- 机构用户表单 -->
          <div v-if="registerForm.userType === 'institutional'">
            <el-form-item prop="institution">
              <el-input
                v-model="registerForm.institution"
                placeholder="请输入机构名称"
                size="large"
                prefix-icon="OfficeBuilding"
              />
            </el-form-item>

            <el-form-item prop="department">
              <el-input
                v-model="registerForm.department"
                placeholder="请输入科室名称"
                size="large"
                prefix-icon="OfficeBuilding"
              />
            </el-form-item>
          </div>

          <!-- 个人用户表单 -->
          <div v-if="registerForm.userType === 'personal'">
            <el-form-item prop="institution">
              <el-input
                v-model="registerForm.institution"
                placeholder="请输入就诊机构（可选）"
                size="large"
                prefix-icon="OfficeBuilding"
              />
            </el-form-item>

            <el-form-item prop="age">
              <el-input
                v-model="registerForm.age"
                placeholder="请输入年龄"
                size="large"
                type="number"
                :min="1"
                :max="120"
              />
            </el-form-item>

            <el-form-item prop="gender">
              <el-select
                v-model="registerForm.gender"
                placeholder="请选择性别"
                size="large"
                style="width: 100%"
              >
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
              </el-select>
            </el-form-item>
          </div>

          <!-- 通用表单字段 -->
          <el-form-item prop="name">
            <el-input
              v-model="registerForm.name"
              placeholder="请输入姓名"
              size="large"
              prefix-icon="User"
            />
          </el-form-item>

          <el-form-item prop="phone">
            <el-input
              v-model="registerForm.phone"
              placeholder="请输入手机号"
              size="large"
              prefix-icon="Phone"
            />
          </el-form-item>

          <el-form-item prop="username">
            <el-input
              v-model="registerForm.username"
              placeholder="请输入用户名"
              size="large"
              prefix-icon="User"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              prefix-icon="Lock"
              show-password
            />
          </el-form-item>

          <el-form-item prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="请确认密码"
              size="large"
              prefix-icon="Lock"
              show-password
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              class="register-btn gradient-btn"
              :loading="loading"
              @click="handleRegister"
            >
              注册
            </el-button>
          </el-form-item>
        </el-form>

        <div class="register-footer">
          <p>已有账号？</p>
          <el-button type="text" @click="$router.push('/login')">
            立即登录
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { Monitor, User, Lock, Message, Phone, OfficeBuilding } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import type { RegisterForm } from '@/types/user'

const router = useRouter()
const userStore = useUserStore()

const registerFormRef = ref<FormInstance>()
const loading = ref(false)

const registerForm = reactive<RegisterForm>({
  username: '',
  password: '',
  confirmPassword: '',
  name: '',
  phone: '',
  userType: 'institutional',
  institution: '',
  department: '',
  age: undefined,
  gender: undefined
})

const registerRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号格式', trigger: 'blur' }
  ],
  institution: [
    {
      validator: (rule, value, callback) => {
        if (registerForm.userType === 'institutional' && !value) {
          callback(new Error('请输入机构名称'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  department: [
    {
      validator: (rule, value, callback) => {
        if (registerForm.userType === 'institutional' && !value) {
          callback(new Error('请输入科室名称'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  age: [
    {
      validator: (rule, value, callback) => {
        if (registerForm.userType === 'personal' && !value) {
          callback(new Error('请输入年龄'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  gender: [
    {
      validator: (rule, value, callback) => {
        if (registerForm.userType === 'personal' && !value) {
          callback(new Error('请选择性别'))
        } else {
          callback()
        }
      },
      trigger: 'change'
    }
  ]
}

const handleRegister = async () => {
  if (!registerFormRef.value) return

  try {
    await registerFormRef.value.validate()
    loading.value = true

    const result = await userStore.register(registerForm)
    
    if (result.success) {
      ElMessage.success('注册成功')
      router.push('/dashboard')
    } else {
      ElMessage.error(result.error || '注册失败')
    }
  } catch (error) {
    console.error('注册错误:', error)
    ElMessage.error('注册失败，请检查输入信息')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.register-container {
  width: 100%;
  max-width: 500px;
}

.register-card {
  padding: 40px;
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo-icon {
  font-size: 3rem;
  color: #667eea;
  margin-bottom: 15px;
}

.register-header h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 10px;
}

.register-header p {
  color: #666;
  font-size: 0.9rem;
}

.user-type-group {
  width: 100%;
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.register-form {
  margin-bottom: 20px;
}

.register-btn {
  width: 100%;
  height: 48px;
  font-size: 1.1rem;
}

.register-footer {
  border-top: 1px solid #f0f0f0;
  padding-top: 20px;
  text-align: center;
  color: #666;
}

.register-footer p {
  margin-bottom: 10px;
}

@media (max-width: 480px) {
  .register-card {
    padding: 30px 20px;
  }
  
  .register-header h2 {
    font-size: 1.5rem;
  }
}
</style> 