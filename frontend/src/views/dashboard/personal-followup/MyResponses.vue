<template>
  <div class="my-responses">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>我的随访回复</h2>
      <p>查看和回复医生的随访询问</p>
    </div>

    <!-- 待回复列表 -->
    <div class="pending-section">
      <h3>待回复的随访</h3>
      <div v-if="pendingFollowups.length === 0" class="empty-state">
        <el-empty description="暂无待回复的随访" />
      </div>
      <div v-else class="pending-list">
        <div 
          v-for="followup in pendingFollowups" 
          :key="followup.followup_id"
          class="pending-item"
        >
          <div class="followup-info">
            <div class="followup-header">
              <h4>{{ followup.patient_name }}</h4>
              <span class="followup-time">{{ formatDate(followup.followup_time) }}</span>
            </div>
            <div class="followup-details">
              <p><strong>随访方式:</strong> {{ followup.method }}</p>
              <p><strong>随访地点:</strong> {{ followup.location }}</p>
              <p><strong>随访内容:</strong> {{ followup.details }}</p>
              <p v-if="followup.recommendations"><strong>治疗建议:</strong> {{ followup.recommendations }}</p>
            </div>
          </div>
          <div class="action-buttons">
            <el-button type="primary" @click="startResponse(followup)">
              开始回复
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 已回复列表 -->
    <div class="completed-section">
      <h3>已回复的随访</h3>
      <div v-if="completedResponses.length === 0" class="empty-state">
        <el-empty description="暂无已回复的随访" />
      </div>
      <div v-else class="completed-list">
        <div 
          v-for="response in completedResponses" 
          :key="response.id"
          class="completed-item"
        >
          <div class="response-info">
            <div class="response-header">
              <h4>{{ response.patient_name }}</h4>
              <span class="response-time">{{ formatDate(response.response_time) }}</span>
            </div>
            <div class="response-summary">
              <p><strong>总体感受:</strong> {{ response.overall_feeling || '未填写' }}</p>
              <p><strong>状况改善:</strong> {{ response.improvement_level || '未填写' }}</p>
              <p><strong>用药依从性:</strong> {{ response.medication_adherence || '未填写' }}</p>
            </div>
          </div>
          <div class="action-buttons">
            <el-button type="text" @click="viewResponse(response)">
              查看详情
            </el-button>
            <el-button type="text" @click="editResponse(response)">
              编辑回复
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 回复对话框 -->
    <el-dialog
      v-model="responseDialogVisible"
      :title="responseDialogTitle"
      width="800px"
      :close-on-click-modal="false"
    >
      <div v-if="currentFollowup" class="response-form">
        <!-- 随访信息展示 -->
        <div class="followup-display">
          <h4>随访信息</h4>
          <div class="followup-content">
            <p><strong>随访时间:</strong> {{ formatDate(currentFollowup.followup_time) }}</p>
            <p><strong>随访方式:</strong> {{ currentFollowup.method }}</p>
            <p><strong>随访地点:</strong> {{ currentFollowup.location }}</p>
            <p><strong>随访内容:</strong> {{ currentFollowup.details }}</p>
            <p v-if="currentFollowup.recommendations"><strong>治疗建议:</strong> {{ currentFollowup.recommendations }}</p>
          </div>
        </div>

        <!-- 回复表单 -->
        <el-form :model="responseForm" label-width="120px" class="response-form-content">
          <el-form-item label="总体感受">
            <el-select v-model="responseForm.overall_feeling" placeholder="请选择">
              <el-option label="良好" value="良好" />
              <el-option label="一般" value="一般" />
              <el-option label="较差" value="较差" />
            </el-select>
          </el-form-item>

          <el-form-item label="状况改善">
            <el-select v-model="responseForm.improvement_level" placeholder="请选择">
              <el-option label="明显改善" value="明显改善" />
              <el-option label="有所改善" value="有所改善" />
              <el-option label="改善不明显" value="改善不明显" />
              <el-option label="无改善" value="无改善" />
            </el-select>
          </el-form-item>

          <el-form-item label="用药依从性">
            <el-select v-model="responseForm.medication_adherence" placeholder="请选择">
              <el-option label="完全按照医嘱" value="完全按照医嘱" />
              <el-option label="基本按照医嘱" value="基本按照医嘱" />
              <el-option label="有时忘记服药" value="有时忘记服药" />
              <el-option label="经常忘记服药" value="经常忘记服药" />
            </el-select>
          </el-form-item>

          <el-form-item label="运动量">
            <el-input
              v-model="responseForm.exercise_volume"
              type="textarea"
              :rows="3"
              placeholder="请描述您的运动情况"
            />
          </el-form-item>

          <el-form-item label="饮食调整">
            <el-input
              v-model="responseForm.diet_adjustment"
              type="textarea"
              :rows="3"
              placeholder="请描述您的饮食调整情况"
            />
          </el-form-item>

          <el-form-item label="疼痛程度">
            <el-slider
              v-model="responseForm.pain_level"
              :min="1"
              :max="10"
              :marks="{ 1: '1分', 5: '5分', 10: '10分' }"
              show-stops
            />
          </el-form-item>

          <el-form-item label="睡眠质量">
            <el-select v-model="responseForm.sleep_quality" placeholder="请选择">
              <el-option label="很好" value="很好" />
              <el-option label="一般" value="一般" />
              <el-option label="较差" value="较差" />
            </el-select>
          </el-form-item>

          <el-form-item label="日常活动能力">
            <el-select v-model="responseForm.daily_activity" placeholder="请选择">
              <el-option label="正常" value="正常" />
              <el-option label="轻度受限" value="轻度受限" />
              <el-option label="中度受限" value="中度受限" />
              <el-option label="重度受限" value="重度受限" />
            </el-select>
          </el-form-item>

          <el-form-item label="情绪状态">
            <el-select v-model="responseForm.mood_status" placeholder="请选择">
              <el-option label="积极" value="积极" />
              <el-option label="一般" value="一般" />
              <el-option label="消极" value="消极" />
            </el-select>
          </el-form-item>

          <el-form-item label="副作用">
            <el-input
              v-model="responseForm.side_effects"
              type="textarea"
              :rows="2"
              placeholder="如有副作用，请详细描述"
            />
          </el-form-item>

          <el-form-item label="担忧或问题">
            <el-input
              v-model="responseForm.concerns"
              type="textarea"
              :rows="2"
              placeholder="如有担忧或问题，请详细描述"
            />
          </el-form-item>

          <el-form-item label="其他补充">
            <el-input
              v-model="responseForm.additional_info"
              type="textarea"
              :rows="2"
              placeholder="其他需要补充的信息"
            />
          </el-form-item>
        </el-form>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="responseDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveResponse" :loading="saving">
            {{ isEditing ? '更新回复' : '提交回复' }}
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 查看详情对话框 -->
    <el-dialog
      v-model="viewDialogVisible"
      title="随访回复详情"
      width="600px"
    >
      <div v-if="viewingResponse" class="response-detail">
        <div class="detail-section">
          <h4>基本信息</h4>
          <p><strong>回复时间:</strong> {{ formatDate(viewingResponse.response_time) }}</p>
          <p><strong>总体感受:</strong> {{ viewingResponse.overall_feeling || '未填写' }}</p>
          <p><strong>状况改善:</strong> {{ viewingResponse.improvement_level || '未填写' }}</p>
          <p><strong>用药依从性:</strong> {{ viewingResponse.medication_adherence || '未填写' }}</p>
        </div>

        <div class="detail-section">
          <h4>生活状况</h4>
          <p><strong>运动量:</strong> {{ viewingResponse.exercise_volume || '未填写' }}</p>
          <p><strong>饮食调整:</strong> {{ viewingResponse.diet_adjustment || '未填写' }}</p>
          <p><strong>疼痛程度:</strong> {{ viewingResponse.pain_level ? viewingResponse.pain_level + '分' : '未填写' }}</p>
          <p><strong>睡眠质量:</strong> {{ viewingResponse.sleep_quality || '未填写' }}</p>
          <p><strong>日常活动能力:</strong> {{ viewingResponse.daily_activity || '未填写' }}</p>
          <p><strong>情绪状态:</strong> {{ viewingResponse.mood_status || '未填写' }}</p>
        </div>

        <div v-if="viewingResponse.side_effects || viewingResponse.concerns || viewingResponse.additional_info" class="detail-section">
          <h4>其他信息</h4>
          <p v-if="viewingResponse.side_effects"><strong>副作用:</strong> {{ viewingResponse.side_effects }}</p>
          <p v-if="viewingResponse.concerns"><strong>担忧或问题:</strong> {{ viewingResponse.concerns }}</p>
          <p v-if="viewingResponse.additional_info"><strong>其他补充:</strong> {{ viewingResponse.additional_info }}</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { followupResponseApi } from '@/api/followupResponse'

// 响应式数据
const pendingFollowups = ref<any[]>([])
const completedResponses = ref<any[]>([])
const responseDialogVisible = ref(false)
const viewDialogVisible = ref(false)
const responseDialogTitle = ref('')
const currentFollowup = ref<any>(null)
const viewingResponse = ref<any>(null)
const isEditing = ref(false)
const saving = ref(false)

// 回复表单数据
const responseForm = ref({
  followup_id: 0,
  overall_feeling: '',
  improvement_level: '',
  medication_adherence: '',
  exercise_volume: '',
  diet_adjustment: '',
  pain_level: 1,
  sleep_quality: '',
  daily_activity: '',
  mood_status: '',
  side_effects: '',
  concerns: '',
  additional_info: ''
})

// 方法
const loadPendingFollowups = async () => {
  try {
    const response = await followupResponseApi.getPendingResponses()
    pendingFollowups.value = response || []
    console.log('加载的待回复随访:', response)
  } catch (error) {
    console.error('加载待回复随访失败:', error)
    ElMessage.error('加载待回复随访失败')
  }
}

const loadCompletedResponses = async () => {
  try {
    const response = await followupResponseApi.getResponses({ is_completed: true })
    completedResponses.value = response?.responses || []
    console.log('加载的已回复随访:', response)
  } catch (error) {
    console.error('加载已回复随访失败:', error)
    ElMessage.error('加载已回复随访失败')
  }
}

const startResponse = (followup: any) => {
  currentFollowup.value = followup
  responseForm.value = {
    followup_id: followup.followup_id,
    overall_feeling: '',
    improvement_level: '',
    medication_adherence: '',
    exercise_volume: '',
    diet_adjustment: '',
    pain_level: 1,
    sleep_quality: '',
    daily_activity: '',
    mood_status: '',
    side_effects: '',
    concerns: '',
    additional_info: ''
  }
  responseDialogTitle.value = '回复随访'
  isEditing.value = false
  responseDialogVisible.value = true
}

const editResponse = (response: any) => {
  viewingResponse.value = response
  responseForm.value = {
    followup_id: response.followup_id,
    overall_feeling: response.overall_feeling || '',
    improvement_level: response.improvement_level || '',
    medication_adherence: response.medication_adherence || '',
    exercise_volume: response.exercise_volume || '',
    diet_adjustment: response.diet_adjustment || '',
    pain_level: response.pain_level || 1,
    sleep_quality: response.sleep_quality || '',
    daily_activity: response.daily_activity || '',
    mood_status: response.mood_status || '',
    side_effects: response.side_effects || '',
    concerns: response.concerns || '',
    additional_info: response.additional_info || ''
  }
  responseDialogTitle.value = '编辑回复'
  isEditing.value = true
  responseDialogVisible.value = true
}

const viewResponse = (response: any) => {
  viewingResponse.value = response
  viewDialogVisible.value = true
}

const saveResponse = async () => {
  try {
    saving.value = true
    
    if (isEditing.value) {
      // 更新回复
      await followupResponseApi.updateResponse(responseForm.value.followup_id, {
        ...responseForm.value,
        is_completed: true
      })
      ElMessage.success('回复更新成功')
    } else {
      // 创建新回复
      await followupResponseApi.createResponse({
        ...responseForm.value,
        is_completed: true
      })
      ElMessage.success('回复提交成功')
    }
    
    responseDialogVisible.value = false
    await loadPendingFollowups()
    await loadCompletedResponses()
  } catch (error) {
    console.error('保存回复失败:', error)
    ElMessage.error('保存回复失败')
  } finally {
    saving.value = false
  }
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadPendingFollowups()
  loadCompletedResponses()
})
</script>

<style scoped>
.my-responses {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 30px;
  text-align: center;
}

.page-header h2 {
  margin: 0 0 10px 0;
  color: #333;
}

.page-header p {
  margin: 0;
  color: #666;
}

.pending-section,
.completed-section {
  margin-bottom: 40px;
}

.pending-section h3,
.completed-section h3 {
  margin: 0 0 20px 0;
  color: #333;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 10px;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
}

.pending-list,
.completed-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.pending-item,
.completed-item {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.pending-item:hover,
.completed-item:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.followup-info,
.response-info {
  flex: 1;
}

.followup-header,
.response-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.followup-header h4,
.response-header h4 {
  margin: 0;
  color: #333;
}

.followup-time,
.response-time {
  color: #666;
  font-size: 14px;
}

.followup-details p,
.response-summary p {
  margin: 8px 0;
  color: #666;
  line-height: 1.5;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-left: 20px;
}

.response-form {
  max-height: 600px;
  overflow-y: auto;
}

.followup-display {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 20px;
}

.followup-display h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.followup-content p {
  margin: 5px 0;
  color: #666;
}

.response-form-content {
  padding: 0 10px;
}

.detail-section {
  margin-bottom: 20px;
}

.detail-section h4 {
  margin: 0 0 10px 0;
  color: #333;
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 5px;
}

.detail-section p {
  margin: 8px 0;
  color: #666;
  line-height: 1.5;
}

.dialog-footer {
  text-align: right;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .pending-item,
  .completed-item {
    flex-direction: column;
  }
  
  .action-buttons {
    margin-left: 0;
    margin-top: 15px;
    flex-direction: row;
  }
  
  .followup-header,
  .response-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>