<template>
  <div class="intelligent-qa-page">
    <div class="content-layout">
      <!-- 左侧：智能问答 -->
      <div class="left-panel">
        <div class="panel-section">
          <div class="section-header">
            <h3 class="section-title">智能问答</h3>
            <el-button type="primary" class="create-btn">+创建新对话</el-button>
          </div>
          
          <div class="qa-content">
            <!-- 医生形象 -->
            <div class="doctor-image-section">
              <div class="doctor-image">
                <div class="image-placeholder">
                  <el-icon size="80" color="#667eea"><UserFilled /></el-icon>
                  <p>专业医生形象</p>
                </div>
              </div>
            </div>
            
            <!-- 交互风格选择 -->
            <div class="style-selection">
              <h4>选择回答风格</h4>
              <div class="style-buttons">
                <el-button 
                  :type="selectedStyle === 'concise' ? 'primary' : 'default'"
                  @click="selectedStyle = 'concise'"
                  class="style-btn"
                >
                  简洁
                </el-button>
                <el-button 
                  :type="selectedStyle === 'detailed' ? 'primary' : 'default'"
                  @click="selectedStyle = 'detailed'"
                  class="style-btn"
                >
                  深入
                </el-button>
                <el-button 
                  :type="selectedStyle === 'research' ? 'primary' : 'default'"
                  @click="selectedStyle = 'research'"
                  class="style-btn"
                >
                  深度研究
                </el-button>
              </div>
            </div>
            
            <!-- 输入区域 -->
            <div class="input-section">
              <el-input
                v-model="userQuestion"
                type="textarea"
                :rows="4"
                placeholder="输入你想要了解的内容"
                class="question-input"
              />
              <div class="input-actions">
                <el-button type="primary" class="voice-btn">
                  <el-icon><Microphone /></el-icon>
                  语音输入
                </el-button>
                <el-button type="primary" class="submit-btn" @click="submitQuestion">
                  点击提交
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：回答显示 -->
      <div class="right-panel">
        <div class="panel-section">
          <h3 class="section-title">回答中</h3>
          <div class="answer-content">
            <div v-if="isAnswering" class="answering-indicator">
              <el-icon class="is-loading"><Loading /></el-icon>
              <p>AI正在思考中...</p>
            </div>
            <div v-else-if="currentAnswer" class="answer-text">
              {{ currentAnswer }}
            </div>
            <div v-else class="empty-state">
              <el-icon size="60" color="#ccc"><ChatDotRound /></el-icon>
              <p>等待您的问题...</p>
            </div>
          </div>
          <div class="answer-actions">
            <el-button 
              v-if="isAnswering" 
              type="danger" 
              class="stop-btn"
              @click="stopAnswer"
            >
              停止回答
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Microphone, UserFilled, ChatDotRound, Loading } from '@element-plus/icons-vue'

// 响应式数据
const selectedStyle = ref('concise')
const userQuestion = ref('')
const isAnswering = ref(false)
const currentAnswer = ref('')

// 提交问题
const submitQuestion = () => {
  if (!userQuestion.value.trim()) {
    return
  }
  
  isAnswering.value = true
  currentAnswer.value = ''
  
  // 模拟AI回答
  setTimeout(() => {
    const answers = {
      concise: '根据您的症状，建议立即就医检查。',
      detailed: '根据您描述的症状，可能存在以下情况：\n1. 急性腰扭伤\n2. 腰椎间盘突出\n3. 肌肉拉伤\n\n建议：\n- 立即停止剧烈运动\n- 采取舒适体位休息\n- 及时就医检查',
      research: '基于最新的医学研究，您描述的症状可能与以下疾病相关：\n\n**急性腰扭伤 (Acute Lumbar Sprain)**\n- 发病率：约15-20%的成年人\n- 主要病因：突然的扭转动作\n- 治疗周期：2-6周\n\n**腰椎间盘突出 (Lumbar Disc Herniation)**\n- 发病率：约2-3%的成年人\n- 危险因素：年龄、职业、遗传\n- 诊断方法：MRI、CT检查\n\n**建议治疗方案：**\n1. 立即就医进行专业检查\n2. 根据检查结果制定个性化治疗方案\n3. 配合物理治疗和康复训练'
    }
    
    currentAnswer.value = answers[selectedStyle.value as keyof typeof answers]
    isAnswering.value = false
  }, 2000)
}

// 停止回答
const stopAnswer = () => {
  isAnswering.value = false
  currentAnswer.value = '回答已停止'
}
</script>

<style scoped>
.intelligent-qa-page {
  height: 100%;
  padding: 20px;
  background: #f5f5f5;
}

.content-layout {
  display: flex;
  gap: 20px;
  height: 100%;
}

.left-panel {
  flex: 2;
  display: flex;
  flex-direction: column;
}

.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.panel-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  height: 100%;
  overflow-y: auto;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #667eea;
}

.section-title {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
  font-weight: 600;
}

.create-btn {
  font-size: 0.9rem;
}

.qa-content {
  display: flex;
  flex-direction: column;
  height: calc(100% - 80px);
  gap: 30px;
}

.doctor-image-section {
  text-align: center;
  margin-bottom: 20px;
}

.doctor-image {
  display: inline-block;
  width: 200px;
  height: 200px;
  border: 2px dashed #667eea;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f8ff;
  margin: 0 auto;
}

.image-placeholder {
  text-align: center;
  color: #667eea;
}

.image-placeholder p {
  margin-top: 10px;
  font-weight: 500;
}

.style-selection {
  text-align: center;
}

.style-selection h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-weight: 600;
}

.style-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.style-btn {
  min-width: 80px;
}

.input-section {
  margin-top: auto;
}

.question-input {
  margin-bottom: 15px;
}

.input-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.voice-btn {
  display: flex;
  align-items: center;
  gap: 5px;
}

.submit-btn {
  min-width: 100px;
}

.answer-content {
  flex: 1;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.answering-indicator {
  text-align: center;
  color: #667eea;
}

.answering-indicator .el-icon {
  font-size: 2rem;
  margin-bottom: 10px;
}

.answer-text {
  width: 100%;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  line-height: 1.6;
  white-space: pre-line;
  color: #333;
}

.empty-state {
  text-align: center;
  color: #ccc;
}

.empty-state p {
  margin-top: 10px;
  font-size: 1.1rem;
}

.answer-actions {
  margin-top: 20px;
  text-align: center;
}

.stop-btn {
  min-width: 120px;
}
</style> 