<template>
  <el-dialog
    v-model="visible"
    :title="record?.title || '历史记录详情'"
    width="80%"
    :before-close="handleClose"
    class="history-detail-dialog"
  >
    <div v-if="record" class="history-detail-content">
      <!-- 基本信息 -->
      <div class="basic-info">
        <div class="info-row">
          <span class="label">记录类型:</span>
          <span class="value">{{ getTypeLabel(record.type) }}</span>
        </div>
        <div class="info-row">
          <span class="label">创建时间:</span>
          <span class="value">{{ record.date }}</span>
        </div>
        <div class="info-row">
          <span class="label">摘要:</span>
          <span class="value">{{ record.summary }}</span>
        </div>
      </div>

      <!-- 语音自述详情 -->
      <div v-if="record.type === 'voice'" class="voice-detail">
        <h4>对话记录</h4>
        <div class="conversation-list">
          <div
            v-for="(conversation, index) in record.conversations"
            :key="index"
            class="conversation-item"
            :class="conversation.role"
          >
            <div class="conversation-header">
              <span class="role-label">{{ conversation.role === 'user' ? '用户' : 'AI助手' }}</span>
              <span class="timestamp">{{ conversation.timestamp }}</span>
            </div>
            <div class="conversation-content" v-html="formatContent(conversation.content)"></div>
          </div>
        </div>
        <div v-if="record.duration" class="duration-info">
          <span>录音时长: {{ formatDuration(record.duration) }}</span>
        </div>
      </div>

      <!-- 饮食识别详情 -->
      <div v-if="record.type === 'diet'" class="diet-detail">
        <div class="food-image-section">
          <h4>食物图片</h4>
          <div class="food-image">
            <el-image
              :src="record.foodImage"
              fit="cover"
              :preview-src-list="[record.foodImage]"
              class="food-preview"
            >
              <template #error>
                <div class="image-placeholder">
                  <el-icon size="40"><Picture /></el-icon>
                  <p>图片加载失败</p>
                </div>
              </template>
            </el-image>
          </div>
        </div>

        <div class="nutrition-section">
          <h4>营养分析</h4>
          <div class="nutrition-grid">
            <div class="nutrition-item">
              <span class="label">热量:</span>
              <span class="value">{{ record.nutritionData.calories }} kcal</span>
            </div>
            <div class="nutrition-item">
              <span class="label">蛋白质:</span>
              <span class="value">{{ record.nutritionData.protein }}g</span>
            </div>
            <div class="nutrition-item">
              <span class="label">脂肪:</span>
              <span class="value">{{ record.nutritionData.fat }}g</span>
            </div>
            <div class="nutrition-item">
              <span class="label">碳水化合物:</span>
              <span class="value">{{ record.nutritionData.carbohydrates }}g</span>
            </div>
            <div class="nutrition-item">
              <span class="label">钙:</span>
              <span class="value">{{ record.nutritionData.calcium }}mg</span>
            </div>
            <div class="nutrition-item">
              <span class="label">维生素D:</span>
              <span class="value">{{ record.nutritionData.vitaminD }}μg</span>
            </div>
          </div>
        </div>

        <div class="benefits-section">
          <h4>健康益处</h4>
          <ul class="benefits-list">
            <li v-for="benefit in record.benefits" :key="benefit">{{ benefit }}</li>
          </ul>
        </div>

        <div class="recommendations-section">
          <h4>营养建议</h4>
          <ul class="recommendations-list">
            <li v-for="recommendation in record.recommendations" :key="recommendation">{{ recommendation }}</li>
          </ul>
        </div>
      </div>

      <!-- HIS接口详情 -->
      <div v-if="record.type === 'his'" class="his-detail">
        <div class="patient-info-section">
          <h4>患者信息</h4>
          <div class="patient-info-grid">
            <div class="info-item">
              <span class="label">姓名:</span>
              <span class="value">{{ record.patientInfo.name }}</span>
            </div>
            <div class="info-item">
              <span class="label">性别:</span>
              <span class="value">{{ record.patientInfo.gender }}</span>
            </div>
            <div class="info-item">
              <span class="label">年龄:</span>
              <span class="value">{{ record.patientInfo.age }}岁</span>
            </div>
            <div class="info-item">
              <span class="label">检查日期:</span>
              <span class="value">{{ record.patientInfo.examDate }}</span>
            </div>
            <div class="info-item">
              <span class="label">检查类型:</span>
              <span class="value">{{ record.patientInfo.examType }}</span>
            </div>
          </div>
        </div>

        <div class="report-section">
          <h4>检查报告</h4>
          <div class="report-content" v-html="formatContent(record.reportContent)"></div>
        </div>

        <div v-if="record.images.length > 0" class="images-section">
          <h4>影像图片</h4>
          <div class="images-grid">
            <el-image
              v-for="(image, index) in record.images"
              :key="index"
              :src="image"
              fit="cover"
              :preview-src-list="record.images"
              class="report-image"
            >
              <template #error>
                <div class="image-placeholder">
                  <el-icon size="30"><Picture /></el-icon>
                  <p>影像{{ index + 1 }}</p>
                </div>
              </template>
            </el-image>
          </div>
        </div>
      </div>

      <!-- 校验规则详情 -->
      <div v-if="record.type === 'validation'" class="validation-detail">
        <div class="validation-status">
          <h4>校验状态</h4>
          <el-tag :type="getStatusType(record.status)" size="large">
            {{ getStatusLabel(record.status) }}
          </el-tag>
        </div>

        <div class="rules-section">
          <h4>校验规则详情</h4>
          <div class="rules-list">
            <div
              v-for="rule in record.rules"
              :key="rule.name"
              class="rule-item"
              :class="rule.status"
            >
              <div class="rule-header">
                <h5>{{ rule.name }}</h5>
                <el-tag :type="getStatusType(rule.status)" size="small">
                  {{ getStatusLabel(rule.status) }}
                </el-tag>
              </div>
              <p class="rule-description">{{ rule.description }}</p>
              <p class="rule-details">{{ rule.details }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">关闭</el-button>
        <el-button type="danger" @click="handleDelete" v-if="record">删除记录</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { Picture } from '@element-plus/icons-vue'
import type { HistoryRecord } from '@/types/history'

interface Props {
  modelValue: boolean
  record: HistoryRecord | null
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
  (e: 'delete', id: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const handleClose = () => {
  visible.value = false
}

const handleDelete = async () => {
  if (!props.record) return
  
  try {
    await ElMessageBox.confirm(
      '确定要删除这条历史记录吗？删除后无法恢复。',
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    emit('delete', props.record.id)
    ElMessage.success('删除成功')
    handleClose()
  } catch {
    // 用户取消删除
  }
}

const getTypeLabel = (type: string) => {
  const typeMap: Record<string, string> = {
    voice: '语音自述',
    diet: '饮食识别',
    his: 'HIS接口',
    validation: '校验规则'
  }
  return typeMap[type] || type
}

const getStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    passed: 'success',
    failed: 'danger',
    warning: 'warning'
  }
  return statusMap[status] || 'info'
}

const getStatusLabel = (status: string) => {
  const statusMap: Record<string, string> = {
    passed: '通过',
    failed: '失败',
    warning: '警告'
  }
  return statusMap[status] || status
}

const formatContent = (content: string) => {
  return content.replace(/\n/g, '<br>')
}

const formatDuration = (seconds: number) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}分${remainingSeconds}秒`
}
</script>

<style scoped>
.history-detail-dialog {
  max-height: 80vh;
}

.history-detail-content {
  max-height: 60vh;
  overflow-y: auto;
}

.basic-info {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.info-row {
  display: flex;
  margin-bottom: 10px;
}

.info-row:last-child {
  margin-bottom: 0;
}

.label {
  font-weight: 600;
  color: #333;
  min-width: 100px;
  margin-right: 10px;
}

.value {
  color: #666;
  flex: 1;
}

/* 语音自述样式 */
.voice-detail h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-weight: 600;
}

.conversation-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.conversation-item {
  border-radius: 8px;
  padding: 15px;
  border-left: 4px solid;
}

.conversation-item.user {
  background: #e3f2fd;
  border-left-color: #2196f3;
  margin-left: 20px;
}

.conversation-item.ai {
  background: #f3e5f5;
  border-left-color: #9c27b0;
  margin-right: 20px;
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.role-label {
  font-weight: 600;
  color: #333;
}

.timestamp {
  font-size: 0.8rem;
  color: #666;
}

.conversation-content {
  line-height: 1.6;
  color: #333;
}

.duration-info {
  margin-top: 15px;
  text-align: center;
  color: #666;
  font-style: italic;
}

/* 饮食识别样式 */
.diet-detail h4 {
  margin: 20px 0 15px 0;
  color: #333;
  font-weight: 600;
}

.diet-detail h4:first-child {
  margin-top: 0;
}

.food-image-section {
  text-align: center;
  margin-bottom: 20px;
}

.food-preview {
  width: 200px;
  height: 200px;
  border-radius: 8px;
  border: 2px solid #e9ecef;
}

.image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
}

.nutrition-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.nutrition-item {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 6px;
}

.benefits-list,
.recommendations-list {
  margin: 0;
  padding-left: 20px;
}

.benefits-list li,
.recommendations-list li {
  margin-bottom: 8px;
  line-height: 1.6;
}

/* HIS接口样式 */
.patient-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 6px;
}

.report-content {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  line-height: 1.6;
  white-space: pre-line;
}

.images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.report-image {
  width: 100%;
  height: 120px;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

/* 校验规则样式 */
.validation-status {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.validation-status h4 {
  margin: 0;
  color: #333;
  font-weight: 600;
}

.rules-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.rule-item {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 15px;
  border-left: 4px solid;
}

.rule-item.passed {
  border-left-color: #67c23a;
  background: #f0f9ff;
}

.rule-item.failed {
  border-left-color: #f56c6c;
  background: #fef0f0;
}

.rule-item.warning {
  border-left-color: #e6a23c;
  background: #fdf6ec;
}

.rule-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.rule-header h5 {
  margin: 0;
  color: #333;
  font-weight: 600;
}

.rule-description {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 0.9rem;
}

.rule-details {
  margin: 0;
  color: #333;
  font-weight: 500;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 