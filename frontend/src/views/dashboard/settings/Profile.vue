<template>
  <div class="profile-page">
    <div class="profile-content">
      <h2 class="page-title">个人信息</h2>
      
      <!-- 头像区域 -->
      <div class="avatar-section">
        <div class="avatar-container">
          <div class="avatar-placeholder">
            <el-icon size="60" color="#ccc"><User /></el-icon>
          </div>
          <div class="avatar-actions">
            <el-button type="primary" size="small">更换头像</el-button>
            <el-button size="small">删除头像</el-button>
          </div>
        </div>
      </div>

      <!-- 个人信息表单 -->
      <div class="profile-form">
        <el-form 
          ref="formRef" 
          :model="profileForm" 
          :rules="formRules" 
          label-width="120px"
          class="profile-form-content"
        >
          <el-form-item label="姓名" prop="name">
            <div class="form-item-content">
              <span class="form-value">{{ profileForm.name }}</span>
              <el-button type="primary" size="small" @click="editField('name')">修改</el-button>
            </div>
          </el-form-item>

          <el-form-item label="性别" prop="gender">
            <div class="form-item-content">
              <span class="form-value">{{ profileForm.gender === 'male' ? '男' : '女' }}</span>
              <el-button type="primary" size="small" @click="editField('gender')">修改</el-button>
            </div>
          </el-form-item>

          <el-form-item label="生日" prop="birthday">
            <div class="form-item-content">
              <span class="form-value">{{ profileForm.birthday }} ({{ profileForm.age }}岁)</span>
              <el-button type="primary" size="small" @click="editField('birthday')">修改</el-button>
            </div>
          </el-form-item>

          <el-form-item label="绑定手机" prop="phone">
            <div class="form-item-content">
              <span class="form-value">{{ maskPhone(profileForm.phone) }}</span>
              <el-button type="primary" size="small" @click="editField('phone')">修改</el-button>
            </div>
          </el-form-item>

          <el-form-item label="登录邮箱" prop="email">
            <div class="form-item-content">
              <span class="form-value">{{ profileForm.email }}</span>
              <el-button type="primary" size="small" @click="editField('email')">修改</el-button>
            </div>
          </el-form-item>

          <el-form-item label="登录密码" prop="password">
            <div class="form-item-content">
              <span class="form-value">***************</span>
              <el-button type="primary" size="small" @click="editField('password')">修改</el-button>
            </div>
          </el-form-item>

          <el-form-item label="用户类型" prop="userType">
            <div class="form-item-content">
              <span class="form-value">{{ profileForm.userType === 'institutional' ? '机构用户' : '个人用户' }}</span>
            </div>
          </el-form-item>

          <el-form-item v-if="profileForm.userType === 'institutional'" label="机构名称" prop="institution">
            <div class="form-item-content">
              <span class="form-value">{{ profileForm.institution }}</span>
              <el-button type="primary" size="small" @click="editField('institution')">修改</el-button>
            </div>
          </el-form-item>

          <el-form-item v-if="profileForm.userType === 'institutional'" label="科室" prop="department">
            <div class="form-item-content">
              <span class="form-value">{{ profileForm.department }}</span>
              <el-button type="primary" size="small" @click="editField('department')">修改</el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
    </div>

    <!-- 编辑对话框 -->
    <el-dialog 
      v-model="editDialogVisible" 
      :title="`修改${editFieldLabel}`" 
      width="500px"
      @close="cancelEdit"
    >
      <el-form :model="editForm" :rules="editRules" ref="editFormRef" label-width="100px">
        <el-form-item :label="editFieldLabel" :prop="editFieldName">
          <el-input 
            v-if="editFieldName === 'name' || editFieldName === 'email' || editFieldName === 'institution' || editFieldName === 'department'"
            v-model="editForm[editFieldName]" 
            :placeholder="`请输入${editFieldLabel}`"
          />
          <el-select 
            v-else-if="editFieldName === 'gender'" 
            v-model="editForm[editFieldName]" 
            placeholder="请选择性别"
          >
            <el-option label="男" value="male" />
            <el-option label="女" value="female" />
          </el-select>
          <el-date-picker
            v-else-if="editFieldName === 'birthday'"
            v-model="editForm[editFieldName]"
            type="date"
            placeholder="请选择生日"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
          <el-input 
            v-else-if="editFieldName === 'phone'"
            v-model="editForm[editFieldName]" 
            placeholder="请输入手机号"
            maxlength="11"
          />
          <el-input 
            v-else-if="editFieldName === 'password'"
            v-model="editForm[editFieldName]" 
            type="password"
            placeholder="请输入新密码"
            show-password
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="cancelEdit">取消</el-button>
          <el-button type="primary" @click="saveEdit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { User } from '@element-plus/icons-vue'

const userStore = useUserStore()

// 表单引用
const formRef = ref()
const editFormRef = ref()

// 个人信息表单数据
const profileForm = reactive({
  name: userStore.user?.name || '李文',
  gender: userStore.user?.gender || 'male',
  birthday: '1995-08-23',
  age: 28,
  phone: userStore.user?.phone || '13800138000',
  email: userStore.user?.email || 'li.wen@email.com',
  password: '',
  userType: userStore.user?.user_type || 'personal',
  institution: userStore.user?.institution || '',
  department: userStore.user?.department || ''
})

// 编辑对话框
const editDialogVisible = ref(false)
const editFieldName = ref('')
const editFieldLabel = ref('')
const editForm = reactive({
  name: '',
  gender: '',
  birthday: '',
  phone: '',
  email: '',
  password: '',
  institution: '',
  department: ''
})

// 表单验证规则
const formRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号格式', trigger: 'blur' }
  ]
}

// 编辑表单验证规则
const editRules = computed(() => {
  const rules: any = {}
  rules[editFieldName.value] = formRules[editFieldName.value as keyof typeof formRules] || []
  return rules
})

// 手机号脱敏
const maskPhone = (phone: string) => {
  if (!phone) return ''
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

// 编辑字段
const editField = (fieldName: string) => {
  editFieldName.value = fieldName
  editFieldLabel.value = getFieldLabel(fieldName)
  editForm[fieldName as keyof typeof editForm] = profileForm[fieldName as keyof typeof profileForm]
  editDialogVisible.value = true
}

// 获取字段标签
const getFieldLabel = (fieldName: string) => {
  const labels: Record<string, string> = {
    name: '姓名',
    gender: '性别',
    birthday: '生日',
    phone: '手机号',
    email: '邮箱',
    password: '密码',
    institution: '机构名称',
    department: '科室'
  }
  return labels[fieldName] || fieldName
}

// 取消编辑
const cancelEdit = () => {
  editDialogVisible.value = false
  editFormRef.value?.resetFields()
}

// 保存编辑
const saveEdit = async () => {
  try {
    await editFormRef.value?.validate()
    
    // 更新表单数据
    profileForm[editFieldName.value as keyof typeof profileForm] = editForm[editFieldName.value as keyof typeof editForm]
    
    // 如果是生日，计算年龄
    if (editFieldName.value === 'birthday') {
      const birthDate = new Date(editForm.birthday)
      const today = new Date()
      profileForm.age = today.getFullYear() - birthDate.getFullYear()
    }
    
    ElMessage.success('修改成功')
    editDialogVisible.value = false
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}
</script>

<style scoped>
.profile-page {
  height: 100%;
  padding: 20px;
  background: #f5f5f5;
}

.profile-content {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  max-width: 800px;
  margin: 0 auto;
}

.page-title {
  text-align: center;
  color: #333;
  font-size: 1.5rem;
  margin-bottom: 30px;
  font-weight: 600;
}

.avatar-section {
  text-align: center;
  margin-bottom: 40px;
}

.avatar-container {
  display: inline-block;
}

.avatar-placeholder {
  width: 120px;
  height: 120px;
  border: 2px dashed #ddd;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  margin: 0 auto 15px;
}

.avatar-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.profile-form {
  max-width: 600px;
  margin: 0 auto;
}

.profile-form-content {
  width: 100%;
}

.form-item-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.form-value {
  color: #333;
  font-size: 1rem;
  flex: 1;
}

:deep(.el-form-item__label) {
  font-weight: 600;
  color: #333;
}

:deep(.el-form-item) {
  margin-bottom: 25px;
}

:deep(.el-form-item__content) {
  width: 100%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 