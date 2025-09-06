<template>
  <div class="digital-companion-page">
    <div class="content-layout">
      <!-- 左侧：数字人情感陪伴 -->
      <div class="left-panel">
        <div class="panel-section">
          <div class="section-header">
            <h3 class="section-title">数字人情感陪伴</h3>
            <el-button type="primary" class="create-btn">+创建新对话</el-button>
          </div>
          
          <div class="companion-content">
            <!-- 数字人形象 -->
            <div class="digital-human-section">
              <div class="digital-human-image">
                <div class="image-placeholder">
                  <el-icon size="80" color="#667eea"><UserFilled /></el-icon>
                  <p>数字人形象</p>
                </div>
              </div>
            </div>
            
            <!-- 对话输入区域 -->
            <div class="conversation-input">
              <el-input
                v-model="conversationText"
                type="textarea"
                :rows="4"
                placeholder="输入对话内容"
                class="conversation-textarea"
              />
              <div class="input-actions">
                <el-button type="primary" class="voice-btn">
                  <el-icon><Microphone /></el-icon>
                  语音输入
                </el-button>
                <el-button type="primary" class="submit-btn" @click="submitConversation">
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
          <div class="response-content">
            <div v-if="isResponding" class="responding-indicator">
              <el-icon class="is-loading"><Loading /></el-icon>
              <p>数字人正在思考中...</p>
            </div>
            <div v-else-if="currentResponse" class="response-text">
              {{ currentResponse }}
            </div>
            <div v-else class="empty-state">
              <el-icon size="60" color="#ccc"><ChatDotRound /></el-icon>
              <p>等待您的对话...</p>
            </div>
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
const conversationText = ref('')
const isResponding = ref(false)
const currentResponse = ref('')

// 提交对话
const submitConversation = () => {
  if (!conversationText.value.trim()) {
    return
  }
  
  isResponding.value = true
  currentResponse.value = ''
  
  // 模拟数字人回答
  setTimeout(() => {
    const responses = [
      '我理解您的感受，让我们一起面对这个挑战。记住，您并不孤单，我会一直陪伴着您。',
      '您的坚强让我很感动。生活中的困难只是暂时的，相信您一定能够克服。',
      '我感受到了您的情绪，这很正常。让我们一起来分析一下情况，找到最好的解决方案。',
      '您的想法很有道理。有时候我们需要换个角度思考问题，也许会有新的发现。',
      '我完全理解您的担忧。让我们一起制定一个计划，一步一步来解决这个问题。'
    ]
    
    const randomResponse = responses[Math.floor(Math.random() * responses.length)]
    currentResponse.value = randomResponse
    isResponding.value = false
  }, 1500)
}
</script>

<style scoped>
.digital-companion-page {
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

.companion-content {
  display: flex;
  flex-direction: column;
  height: calc(100% - 80px);
  gap: 30px;
}

.digital-human-section {
  text-align: center;
  margin-bottom: 20px;
}

.digital-human-image {
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

.conversation-input {
  margin-top: auto;
}

.conversation-textarea {
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

.response-content {
  flex: 1;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.responding-indicator {
  text-align: center;
  color: #667eea;
}

.responding-indicator .el-icon {
  font-size: 2rem;
  margin-bottom: 10px;
}

.response-text {
  width: 100%;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  line-height: 1.6;
  color: #333;
  font-style: italic;
}

.empty-state {
  text-align: center;
  color: #ccc;
}

.empty-state p {
  margin-top: 10px;
  font-size: 1.1rem;
}
</style> 