<template>
  <div class="home-container">
    <!-- 个人用户首页：个人信息展示 -->
    <div class="personal-home">
      <!-- 主内容区 -->
      <div class="main-content">
        <!-- 左侧：个人信息展示 -->
        <div class="left-panel">
          <!-- 个人信息展示 -->
          <div class="form-section">
            <div class="form-header">
              <h3>我的个人信息</h3>
              <p>以下是您的基本信息，如需修改请前往个人设置页面</p>
            </div>
            
            <!-- 个人信息展示卡片 -->
            <div class="personal-info-card">
              <el-card class="info-card">
                <template #header>
                  <div class="card-header">
                    <span>基本信息</span>
                    <el-button type="primary" size="small" @click="showEditDialog">
                      <el-icon><Edit /></el-icon>
                      编辑信息
                    </el-button>
                  </div>
                </template>
                
                <div class="info-content">
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <div class="info-item">
                        <label>姓名：</label>
                        <span>{{ userStore.user?.name || '未设置' }}</span>
                      </div>
                    </el-col>
                    <el-col :span="12">
                      <div class="info-item">
                        <label>年龄：</label>
                        <span>{{ userStore.user?.age || '未设置' }}</span>
                      </div>
                    </el-col>
                  </el-row>
                  
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <div class="info-item">
                        <label>性别：</label>
                        <span>{{ userStore.user?.gender === 'male' ? '男' : userStore.user?.gender === 'female' ? '女' : '未设置' }}</span>
                      </div>
                    </el-col>
                    <el-col :span="12">
                      <div class="info-item">
                        <label>联系电话：</label>
                        <span>{{ userStore.user?.phone || '未设置' }}</span>
                      </div>
                    </el-col>
                  </el-row>
                  
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <div class="info-item">
                        <label>邮箱：</label>
                        <span>{{ userStore.user?.email || '未设置' }}</span>
                      </div>
                    </el-col>
                    <el-col :span="12">
                      <div class="info-item">
                        <label>机构：</label>
                        <span>{{ userStore.user?.institution || '未设置' }}</span>
                      </div>
                    </el-col>
                  </el-row>
                  
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <div class="info-item">
                        <label>身高：</label>
                        <span>{{ userStore.user?.height ? userStore.user.height + 'cm' : '未设置' }}</span>
                      </div>
                    </el-col>
                    <el-col :span="12">
                      <div class="info-item">
                        <label>体重：</label>
                        <span>{{ userStore.user?.weight ? userStore.user.weight + 'kg' : '未设置' }}</span>
                      </div>
                    </el-col>
                  </el-row>
                  
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <div class="info-item">
                        <label>T值：</label>
                        <span>{{ userStore.user?.t_score || '未设置' }}</span>
                      </div>
                    </el-col>
                    <el-col :span="12">
                      <div class="info-item">
                        <label>Z值：</label>
                        <span>{{ userStore.user?.z_score || '未设置' }}</span>
                      </div>
                    </el-col>
                  </el-row>
                  
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <div class="info-item">
                        <label>风险等级：</label>
                        <span>{{ getRiskLevelText(userStore.user?.risk_level) }}</span>
                      </div>
                    </el-col>
                    <el-col :span="12">
                      <div class="info-item">
                        <label>地址：</label>
                        <span>{{ userStore.user?.address || '未设置' }}</span>
                      </div>
                    </el-col>
                  </el-row>
                  
                  <el-row :gutter="20">
                    <el-col :span="24">
                      <div class="info-item">
                        <label>注册时间：</label>
                        <span>{{ formatDate(userStore.user?.created_at || '') }}</span>
                      </div>
                    </el-col>
                  </el-row>
                </div>
              </el-card>
            </div>
          </div>
        </div>

        <!-- 右侧：功能导航 -->
        <div class="right-panel">
          <div class="function-nav">
            <h3>功能导航</h3>
            <div class="nav-cards">
              <el-card class="nav-card" @click="goToFollowup">
                <div class="nav-content">
                  <el-icon size="24" color="#409EFF"><Calendar /></el-icon>
                  <span>随访跟踪</span>
                </div>
              </el-card>
              
              <el-card class="nav-card" @click="goToDataCollection">
                <div class="nav-content">
                  <el-icon size="24" color="#67C23A"><Document /></el-icon>
                  <span>数据采集</span>
                </div>
              </el-card>
              
              <el-card class="nav-card" @click="goToAI">
                <div class="nav-content">
                  <el-icon size="24" color="#E6A23C"><ChatDotRound /></el-icon>
                  <span>AI辅助</span>
                </div>
              </el-card>
              
              <el-card class="nav-card" @click="goToSettings">
                <div class="nav-content">
                  <el-icon size="24" color="#F56C6C"><Setting /></el-icon>
                  <span>个人设置</span>
                </div>
              </el-card>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 个人信息编辑对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑个人信息"
      width="800px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="editFormRules"
        label-width="120px"
        class="edit-form"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="editForm.name" placeholder="请输入姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="年龄" prop="age">
              <el-input v-model="editForm.age" type="number" placeholder="请输入年龄" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="editForm.gender" placeholder="请选择性别" style="width: 100%">
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="editForm.phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="editForm.email" placeholder="请输入邮箱（可选）" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="机构" prop="institution">
              <el-input v-model="editForm.institution" placeholder="请输入机构（可选）" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="身高(cm)" prop="height">
              <el-input v-model="editForm.height" type="number" placeholder="请输入身高" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="体重(kg)" prop="weight">
              <el-input v-model="editForm.weight" type="number" placeholder="请输入体重" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="T值" prop="t_score">
              <el-input v-model="editForm.t_score" type="number" step="0.1" placeholder="请输入T值" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Z值" prop="z_score">
              <el-input v-model="editForm.z_score" type="number" step="0.1" placeholder="请输入Z值" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="风险等级" prop="risk_level">
              <el-select v-model="editForm.risk_level" placeholder="请选择风险等级" style="width: 100%">
                <el-option label="低危" value="low" />
                <el-option label="中危" value="medium" />
                <el-option label="高危" value="high" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="地址" prop="address">
              <el-input v-model="editForm.address" placeholder="请输入详细地址" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="现病史" prop="medical_history">
              <el-input 
                v-model="editForm.medical_history" 
                type="textarea" 
                :rows="3"
                placeholder="请描述您的现病史（可选）" 
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="家族史" prop="family_history">
              <el-input 
                v-model="editForm.family_history" 
                type="textarea" 
                :rows="3"
                placeholder="请描述您的家族史（可选）" 
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="用药史" prop="medications">
              <el-input 
                v-model="editForm.medications" 
                type="textarea" 
                :rows="3"
                placeholder="请描述您的用药史（可选）" 
              />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitEditForm" :loading="submitting">
            保存
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Edit, Calendar, Document, ChatDotRound, Setting } from '@element-plus/icons-vue'
import { updateCurrentUser } from '@/api/user'

const userStore = useUserStore()
const router = useRouter()

// 编辑对话框相关
const editDialogVisible = ref(false)
const editFormRef = ref()
const submitting = ref(false)

// 编辑表单数据
const editForm = reactive({
  name: '',
  age: undefined as number | undefined,
  gender: '',
  phone: '',
  email: '',
  institution: '',
  height: undefined as number | undefined,
  weight: undefined as number | undefined,
  t_score: undefined as number | undefined,
  z_score: undefined as number | undefined,
  risk_level: 'low',
  address: '',
  medical_history: '',
  family_history: '',
  medications: ''
})

// 编辑表单验证规则
const editFormRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  age: [{ required: true, message: '请输入年龄', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
  email: [
    { type: 'email' as const, message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

// 格式化日期
const formatDate = (dateString: string) => {
  if (!dateString) return '未知'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取风险等级文本
const getRiskLevelText = (riskLevel: string | undefined) => {
  if (!riskLevel) return '未设置'
  switch (riskLevel) {
    case 'low': return '低危'
    case 'medium': return '中危'
    case 'high': return '高危'
    default: return riskLevel
  }
}

// 显示编辑对话框
const showEditDialog = () => {
  // 用当前用户信息填充表单
  if (userStore.user) {
    editForm.name = userStore.user.name || ''
    editForm.age = userStore.user.age || undefined
    editForm.gender = userStore.user.gender || ''
    editForm.phone = userStore.user.phone || ''
    editForm.email = userStore.user.email || ''
    editForm.institution = userStore.user.institution || ''
    editForm.height = userStore.user.height || undefined
    editForm.weight = userStore.user.weight || undefined
    editForm.t_score = userStore.user.t_score || undefined
    editForm.z_score = userStore.user.z_score || undefined
    editForm.risk_level = userStore.user.risk_level || 'low'
    editForm.address = userStore.user.address || ''
    editForm.medical_history = userStore.user.medical_history || ''
    editForm.family_history = userStore.user.family_history || ''
    editForm.medications = userStore.user.medications || ''
  }
  editDialogVisible.value = true
}

// 提交编辑表单
const submitEditForm = async () => {
  if (!editFormRef.value) return

  try {
    await editFormRef.value.validate()
    submitting.value = true

    // 准备更新数据
    const updateData: any = {
      name: editForm.name,
      age: editForm.age,
      gender: editForm.gender,
      phone: editForm.phone,
      email: editForm.email,
      institution: editForm.institution,
      height: editForm.height,
      weight: editForm.weight,
      t_score: editForm.t_score,
      z_score: editForm.z_score,
      risk_level: editForm.risk_level,
      address: editForm.address,
      medical_history: editForm.medical_history,
      family_history: editForm.family_history,
      medications: editForm.medications
    }

    // 调用后端API更新用户信息
    const updatedUser = await updateCurrentUser(updateData)
    console.log('用户信息更新成功:', updatedUser)

    // 更新用户store
    userStore.setUser(updatedUser)

    ElMessage.success('个人信息更新成功！')
    editDialogVisible.value = false

    // 不需要刷新页面，数据已经更新到store中

  } catch (error: any) {
    console.error('更新用户信息失败:', error)
    ElMessage.error('更新失败，请重试')
  } finally {
    submitting.value = false
  }
}

// 导航函数
const goToFollowup = () => {
  router.push('/dashboard/followup')
}

const goToDataCollection = () => {
  router.push('/dashboard/data-collection')
}

const goToAI = () => {
  router.push('/dashboard/ai')
}

const goToSettings = () => {
  router.push('/dashboard/settings')
}
</script>

<style scoped>
.home-container {
  display: flex;
  height: 100vh;
  background-color: #f5f5f5;
}

.personal-home {
  width: 100%;
  display: flex;
  flex-direction: column;
}

.main-content {
  display: flex;
  flex: 1;
  gap: 20px;
  padding: 20px;
}

.left-panel {
  flex: 2;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.right-panel {
  flex: 1;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-section {
  width: 100%;
}

.form-header {
  margin-bottom: 20px;
}

.form-header h3 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 1.5rem;
}

.form-header p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.personal-info-card {
  width: 100%;
}

.info-card {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #333;
}

.info-content {
  padding: 10px 0;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.info-item label {
  font-weight: 600;
  color: #333;
  min-width: 80px;
  margin-right: 10px;
}

.info-item span {
  color: #666;
  flex: 1;
}

.function-nav h3 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 1.2rem;
}

.nav-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.nav-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e4e7ed;
}

.nav-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-color: #409EFF;
}

.nav-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 10px;
}

.nav-content span {
  font-size: 0.9rem;
  color: #333;
  font-weight: 500;
}

/* 编辑对话框样式 */
.edit-form {
  max-width: 100%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

:deep(.el-form-item__label) {
  font-weight: 600;
  color: #333;
}

:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-dialog__body) {
  padding: 20px 20px 0 20px;
}

:deep(.el-dialog__footer) {
  padding: 10px 20px 20px 20px;
}
</style>