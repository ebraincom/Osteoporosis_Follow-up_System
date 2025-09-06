<template>
  <div class="intelligent-qa-page">
    <div class="content-layout">
      <!-- 左侧：智能问答 -->
      <div class="left-panel">
        <div class="panel-section">
          <div class="section-header">
            <h3 class="section-title">智能问答助手</h3>
            <div class="header-actions">
              <el-button type="success" size="small" @click="clearHistory">
                <el-icon><Delete /></el-icon>
                清空历史
              </el-button>
              <el-button type="primary" size="small" @click="createNewChat">
                <el-icon><Plus /></el-icon>
                新建对话
              </el-button>
            </div>
          </div>
          
          <div class="qa-content">
            <!-- 医生形象 -->
            <div class="doctor-image-section">
              <div class="doctor-avatar">
                <div class="avatar-container">
                  <el-icon size="60" color="white"><UserFilled /></el-icon>
                  <div class="status-indicator" :class="{ 'online': isOnline }"></div>
                </div>
                <h4>AI医疗助手</h4>
                <p class="status-text">{{ isOnline ? '在线服务中' : '离线' }}</p>
              </div>
            </div>
            
            <!-- 智能建议 -->
            <div class="smart-suggestions" v-if="suggestions.length > 0">
              <h4>常见问题</h4>
              <div class="suggestion-tags">
                <el-tag 
                  v-for="suggestion in suggestions" 
                  :key="suggestion"
                  class="suggestion-tag"
                  @click="selectSuggestion(suggestion)"
                  effect="plain"
                >
                  {{ suggestion }}
                </el-tag>
              </div>
            </div>
            
            <!-- 交互风格选择 -->
            <div class="style-selection">
              <h4>回答风格</h4>
              <div class="style-buttons">
                <el-button 
                  :type="selectedStyle === 'concise' ? 'primary' : 'default'"
                  @click="selectedStyle = 'concise'"
                  class="style-btn"
                  size="small"
                >
                  <el-icon><ChatDotRound /></el-icon>
                  简洁
                </el-button>
                <el-button 
                  :type="selectedStyle === 'detailed' ? 'primary' : 'default'"
                  @click="selectedStyle = 'detailed'"
                  class="style-btn"
                  size="small"
                >
                  <el-icon><Document /></el-icon>
                  详细
                </el-button>
                <el-button 
                  :type="selectedStyle === 'professional' ? 'primary' : 'default'"
                  @click="selectedStyle = 'professional'"
                  class="style-btn"
                  size="small"
                >
                  <el-icon><Reading /></el-icon>
                  专业
                </el-button>
              </div>
            </div>
            
            <!-- AI模型选择 -->
            <div class="model-selection">
              <h4>AI模型</h4>
              <div class="model-buttons">
                <el-button 
                  :type="selectedModel === 'qwen' ? 'primary' : 'default'"
                  @click="selectedModel = 'qwen'"
                  class="model-btn"
                  size="small"
                >
                  <el-icon><ChatDotRound /></el-icon>
                  通义千问
                </el-button>
                <el-button 
                  :type="selectedModel === 'gemini' ? 'primary' : 'default'"
                  @click="selectedModel = 'gemini'"
                  class="model-btn"
                  size="small"
                >
                  <el-icon><Document /></el-icon>
                  Google Gemini
                </el-button>
                <el-button 
                  :type="selectedModel === 'doubao' ? 'primary' : 'default'"
                  @click="selectedModel = 'doubao'"
                  class="model-btn"
                  size="small"
                >
                  <el-icon><Document /></el-icon>
                  豆包AI
                </el-button>
              </div>
            </div>
            
            <!-- 输入区域 -->
            <div class="input-section">
              <el-input
                v-model="userQuestion"
                type="textarea"
                :rows="4"
                placeholder="请输入您的问题，例如：骨质疏松症的症状有哪些？"
                class="question-input"
                @keydown.ctrl.enter="submitQuestion"
                :disabled="isAnswering"
              />
              <div class="input-actions">
                <el-button 
                  type="info" 
                  class="voice-btn"
                  @click="toggleVoiceInput"
                  :disabled="isAnswering"
                >
                  <el-icon><Microphone /></el-icon>
                  {{ isVoiceInput ? '停止录音' : '语音输入' }}
                </el-button>
                <el-button 
                  type="primary" 
                  class="submit-btn" 
                  @click="submitQuestion"
                  :loading="isAnswering"
                  :disabled="!userQuestion.trim() || isAnswering"
                >
                  <el-icon><Right /></el-icon>
                  {{ isAnswering ? '思考中...' : '发送' }}
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：对话历史 -->
      <div class="right-panel">
        <div class="panel-section">
          <div class="section-header">
            <h3 class="section-title">对话历史</h3>
            <el-button type="text" size="small" @click="exportHistory">
              <el-icon><Download /></el-icon>
              导出
            </el-button>
          </div>
          
          <div class="chat-history">
            <div v-if="chatHistory.length === 0" class="empty-history">
              <el-icon size="60" color="#ccc"><ChatDotRound /></el-icon>
              <p>还没有对话记录</p>
              <p class="hint">开始提问吧！</p>
            </div>
            
            <div v-else class="history-list">
              <div 
                v-for="(chat, index) in filteredHistory" 
                :key="index"
                class="chat-item"
                @click="loadChat(chat)"
              >
                <div class="chat-preview">
                  <div class="question-preview">
                    <el-icon><QuestionFilled /></el-icon>
                    <span>{{ chat.question.substring(0, 30) }}{{ chat.question.length > 30 ? '...' : '' }}</span>
                  </div>
                  <div class="answer-preview">
                    <el-icon><ChatDotRound /></el-icon>
                    <span>{{ chat.answer.substring(0, 50) }}{{ chat.answer.length > 50 ? '...' : '' }}</span>
                  </div>
                </div>
                <div class="chat-meta">
                  <span class="chat-time">{{ formatTime(chat.timestamp) }}</span>
                  <span class="chat-style">{{ getStyleText(chat.style) }}</span>
                  <span class="chat-model">{{ getModelText(chat.model) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 当前对话显示区域 -->
    <div v-if="currentChat" class="current-chat-overlay">
      <div class="chat-dialog">
        <div class="dialog-header">
          <h3>当前对话</h3>
          <el-button type="text" @click="closeCurrentChat">
            <el-icon><Close /></el-icon>
          </el-button>
        </div>
        <div class="dialog-content">
          <div class="question-section">
            <div class="question-label">
              <el-icon><QuestionFilled /></el-icon>
              问题
            </div>
            <div class="question-text">{{ currentChat.question }}</div>
          </div>
          <div class="answer-section">
            <div class="answer-label">
              <el-icon><ChatDotRound /></el-icon>
              回答
            </div>
            <div class="answer-text">{{ currentChat.answer }}</div>
          </div>
        </div>
        <div class="dialog-actions">
          <el-button @click="closeCurrentChat">关闭</el-button>
          <el-button type="primary" @click="continueChat">继续对话</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { 
  Microphone, UserFilled, ChatDotRound, Loading, 
  Delete, Plus, Right, Download, QuestionFilled,
  Close, Document, Reading 
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// 接口定义
interface ChatHistory {
  id: string
  question: string
  answer: string
  style: 'concise' | 'detailed' | 'professional'
  model: 'qwen' | 'gemini' | 'doubao'
  timestamp: Date
  rating?: number
  tags?: string[]
}

// 响应式数据
const selectedStyle = ref<'concise' | 'detailed' | 'professional'>('concise')
const selectedModel = ref<'qwen' | 'gemini' | 'doubao'>('qwen')
const userQuestion = ref('')
const isAnswering = ref(false)
const currentAnswer = ref('')
const isOnline = ref(true)
const isVoiceInput = ref(false)
const chatHistory = ref<ChatHistory[]>([])
const currentChat = ref<ChatHistory | null>(null)

// 智能建议
const suggestions = ref([
  '骨质疏松症的症状有哪些？',
  '如何预防骨质疏松？',
  '骨质疏松症的治疗方法',
  '钙片应该怎么吃？',
  '运动对骨骼健康的影响',
  '骨质疏松症的饮食建议'
])

// 知识库答案模板
const knowledgeBase = {
  concise: {
    '骨质疏松症的症状有哪些？': '主要症状包括：腰背疼痛、身高变矮、驼背、易骨折等。',
    '如何预防骨质疏松？': '预防措施：补充钙质、维生素D、适量运动、避免吸烟饮酒。',
    '骨质疏松症的治疗方法': '治疗方法：药物治疗、物理治疗、生活方式调整、定期监测。'
  },
  detailed: {
    '骨质疏松症的症状有哪些？': `骨质疏松症的常见症状包括：

1. **疼痛症状**
   - 腰背疼痛，特别是夜间疼痛
   - 全身骨骼疼痛
   - 关节疼痛

2. **形态改变**
   - 身高逐渐变矮
   - 驼背（脊柱后凸）
   - 胸廓变形

3. **骨折风险**
   - 轻微外伤即可骨折
   - 常见骨折部位：腕部、髋部、脊柱

4. **其他症状**
   - 牙齿松动
   - 指甲变脆
   - 肌肉无力

建议：如有上述症状，应及时就医检查骨密度。`,
    '如何预防骨质疏松？': `骨质疏松症的预防策略：

**营养补充**
- 钙质：每日1000-1200mg
- 维生素D：每日800-1000IU
- 蛋白质：适量摄入

**运动锻炼**
- 负重运动：步行、慢跑、爬楼梯
- 抗阻训练：举重、弹力带训练
- 平衡训练：太极拳、瑜伽

**生活方式**
- 戒烟限酒
- 避免过度节食
- 保持健康体重

**定期检查**
- 40岁后定期骨密度检查
- 关注家族病史
- 及时治疗相关疾病`
  },
  professional: {
    '骨质疏松症的症状有哪些？': `# 骨质疏松症临床症状分析

## 病理生理机制
骨质疏松症是一种以骨量减少、骨微结构破坏为特征的全身性骨骼疾病，导致骨脆性增加和骨折风险增高。

## 临床表现分类

### 1. 疼痛综合征
- **机械性疼痛**：负重时加重，休息时缓解
- **病理性疼痛**：持续性疼痛，夜间加重
- **神经根性疼痛**：椎体压缩性骨折导致

### 2. 骨骼变形
- **脊柱后凸**：胸椎后凸角度>40°
- **身高缩短**：年缩短>2cm需警惕
- **胸廓变形**：影响心肺功能

### 3. 骨折并发症
- **椎体骨折**：最常见，多无症状
- **髋部骨折**：死亡率高，需手术治疗
- **腕部骨折**：Colles骨折多见

## 诊断标准
- **T值≤-2.5**：骨质疏松症
- **T值-1.0至-2.5**：骨量减少
- **FRAX评分**：评估10年骨折风险

## 治疗原则
1. 基础治疗：钙剂+维生素D
2. 抗骨质疏松药物：双膦酸盐类
3. 物理治疗：运动康复
4. 手术治疗：骨折内固定

**建议**：出现相关症状应及时进行DXA骨密度检查，早期诊断和治疗。`
  }
}

// 计算属性
const filteredHistory = computed(() => {
  return chatHistory.value.slice().reverse()
})

// 方法
const submitQuestion = async () => {
  if (!userQuestion.value.trim()) {
    ElMessage.warning('请输入问题')
    return
  }
  
  isAnswering.value = true
  currentAnswer.value = ''
  
  try {
    // 调用AI问答API
    const response = await fetch('/api/v1/ai-qa/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        question: userQuestion.value,
        style: selectedStyle.value,
        model: selectedModel.value
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    currentAnswer.value = data.answer
    
    // 保存到历史记录
    const newChat: ChatHistory = {
      id: Date.now().toString(),
      question: userQuestion.value,
      answer: data.answer,
      style: selectedStyle.value,
      model: selectedModel.value,
      timestamp: new Date()
    }
    
    chatHistory.value.push(newChat)
    saveHistoryToLocal()
    
    ElMessage.success('回答完成')
  } catch (error) {
    console.error('AI问答错误:', error)
    ElMessage.error('AI服务暂时不可用，请稍后重试')
    
    // 如果API调用失败，使用本地知识库作为备选
    const fallbackAnswer = getAnswer(userQuestion.value, selectedStyle.value)
    currentAnswer.value = fallbackAnswer
    
    // 保存到历史记录
    const newChat: ChatHistory = {
      id: Date.now().toString(),
      question: userQuestion.value,
      answer: fallbackAnswer,
      style: selectedStyle.value,
      model: selectedModel.value,
      timestamp: new Date()
    }
    
    chatHistory.value.push(newChat)
    saveHistoryToLocal()
  } finally {
    isAnswering.value = false
  }
}

const getAnswer = (question: string, style: string): string => {
  const styleAnswers = knowledgeBase[style as keyof typeof knowledgeBase]
  const answer = styleAnswers[question as keyof typeof styleAnswers]
  
  if (answer) {
    return answer
  }
  
  // 默认回答
  const defaultAnswers = {
    concise: '根据您的问题，建议咨询专业医生获取详细解答。',
    detailed: '您的问题需要更详细的医学评估，建议：\n1. 咨询专科医生\n2. 进行相关检查\n3. 制定个性化治疗方案',
    professional: '基于循证医学证据，您的问题涉及复杂的医学知识，建议：\n\n**专业建议**\n- 寻求专科医生咨询\n- 进行必要的医学检查\n- 制定循证治疗方案\n\n**注意事项**\n- 避免自我诊断\n- 及时就医治疗\n- 定期随访监测'
  }
  
  return defaultAnswers[style as keyof typeof defaultAnswers]
}

const selectSuggestion = (suggestion: string) => {
  userQuestion.value = suggestion
}

const toggleVoiceInput = () => {
  isVoiceInput.value = !isVoiceInput.value
  if (isVoiceInput.value) {
    ElMessage.info('语音输入功能开发中...')
  }
}

const loadChat = (chat: ChatHistory) => {
  currentChat.value = chat
  userQuestion.value = chat.question
  selectedStyle.value = chat.style
  selectedModel.value = chat.model
}

const closeCurrentChat = () => {
  currentChat.value = null
}

const continueChat = () => {
  if (currentChat.value) {
    userQuestion.value = currentChat.value.question
    selectedStyle.value = currentChat.value.style
    closeCurrentChat()
  }
}

const clearHistory = () => {
  chatHistory.value = []
  saveHistoryToLocal()
  ElMessage.success('历史记录已清空')
}

const createNewChat = () => {
  userQuestion.value = ''
  currentAnswer.value = ''
  currentChat.value = null
  ElMessage.success('已创建新对话')
}

const exportHistory = () => {
  if (chatHistory.value.length === 0) {
    ElMessage.warning('没有历史记录可导出')
    return
  }
  
  const data = chatHistory.value.map(chat => ({
    问题: chat.question,
    回答: chat.answer,
    风格: getStyleText(chat.style),
    时间: formatTime(chat.timestamp)
  }))
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `智能问答历史_${new Date().toISOString().split('T')[0]}.json`
  a.click()
  URL.revokeObjectURL(url)
  
  ElMessage.success('历史记录已导出')
}

const formatTime = (date: Date): string => {
  return new Intl.DateTimeFormat('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

const getStyleText = (style: string): string => {
  const styleMap = {
    concise: '简洁',
    detailed: '详细',
    professional: '专业'
  }
  return styleMap[style as keyof typeof styleMap] || style
}

const getModelText = (model: string): string => {
  const modelMap = {
    qwen: '通义千问',
    gemini: 'Google Gemini',
    doubao: '豆包AI'
  }
  return modelMap[model as keyof typeof modelMap] || model
}

const saveHistoryToLocal = () => {
  localStorage.setItem('chatHistory', JSON.stringify(chatHistory.value))
}

const loadHistoryFromLocal = () => {
  const saved = localStorage.getItem('chatHistory')
  if (saved) {
    try {
      const parsed = JSON.parse(saved)
      chatHistory.value = parsed.map((item: any) => ({
        ...item,
        timestamp: new Date(item.timestamp),
        model: item.model || 'qwen' // 为旧记录添加默认模型
      }))
    } catch (error) {
      console.error('加载历史记录失败:', error)
    }
  }
}

// 生命周期
onMounted(() => {
  loadHistoryFromLocal()
})
</script>

<style scoped>
.intelligent-qa-page {
  height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  overflow: hidden;
}

.content-layout {
  display: flex;
  gap: 20px;
  height: 100%;
  max-width: 1400px;
  margin: 0 auto;
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
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
  height: 100%;
  overflow-y: auto;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.2);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #409eff;
}

.section-title {
  margin: 0;
  font-size: 1.4rem;
  color: #303133;
  font-weight: 700;
  background: linear-gradient(135deg, #409eff, #67c23a);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.qa-content {
  display: flex;
  flex-direction: column;
  height: calc(100% - 100px);
  gap: 24px;
}

.doctor-image-section {
  text-align: center;
  margin-bottom: 20px;
}

.doctor-avatar {
  display: inline-block;
  text-align: center;
}

.avatar-container {
  position: relative;
  display: inline-block;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #409eff, #67c23a);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  box-shadow: 0 8px 24px rgba(64, 158, 255, 0.3);
}

.avatar-container .el-icon {
  color: white;
}

.status-indicator {
  position: absolute;
  bottom: 8px;
  right: 8px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #f56c6c;
  border: 3px solid white;
  transition: all 0.3s ease;
}

.status-indicator.online {
  background: #67c23a;
  box-shadow: 0 0 8px rgba(103, 194, 58, 0.5);
}

.doctor-avatar h4 {
  margin: 0 0 4px 0;
  color: #303133;
  font-weight: 600;
}

.status-text {
  margin: 0;
  color: #909399;
  font-size: 0.9rem;
}

.smart-suggestions {
  text-align: center;
}

.smart-suggestions h4 {
  margin: 0 0 16px 0;
  color: #303133;
  font-weight: 600;
}

.suggestion-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
}

.suggestion-tag {
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 20px;
  padding: 8px 16px;
}

.suggestion-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.style-selection {
  text-align: center;
}

.style-selection h4 {
  margin: 0 0 16px 0;
  color: #303133;
  font-weight: 600;
}

.style-buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.style-btn {
  min-width: 90px;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.model-selection {
  text-align: center;
  margin-top: 20px;
}

.model-selection h4 {
  margin: 0 0 16px 0;
  color: #303133;
  font-weight: 600;
}

.model-buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.model-btn {
  min-width: 120px;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.style-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.model-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.input-section {
  margin-top: auto;
}

.question-input {
  margin-bottom: 16px;
}

.question-input :deep(.el-textarea__inner) {
  border-radius: 12px;
  border: 2px solid #e4e7ed;
  transition: all 0.3s ease;
}

.question-input :deep(.el-textarea__inner):focus {
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.input-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.voice-btn, .submit-btn {
  border-radius: 20px;
  padding: 12px 24px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.voice-btn:hover, .submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.chat-history {
  flex: 1;
  overflow-y: auto;
}

.empty-history {
  text-align: center;
  padding: 40px 20px;
  color: #c0c4cc;
}

.empty-history p {
  margin: 12px 0 4px 0;
  font-size: 1.1rem;
}

.hint {
  font-size: 0.9rem !important;
  color: #909399 !important;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chat-item {
  padding: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #fafafa;
}

.chat-item:hover {
  border-color: #409eff;
  background: #f0f8ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.15);
}

.chat-preview {
  margin-bottom: 8px;
}

.question-preview, .answer-preview {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
  font-size: 0.9rem;
}

.question-preview {
  color: #409eff;
  font-weight: 600;
}

.answer-preview {
  color: #67c23a;
}

.chat-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  color: #909399;
}

.chat-style {
  background: #e4e7ed;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.75rem;
}

.chat-model {
  background: #f0f9ff;
  color: #0369a1;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.75rem;
  margin-left: 8px;
}

.current-chat-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.chat-dialog {
  background: white;
  border-radius: 16px;
  width: 80%;
  max-width: 800px;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: 0 16px 48px rgba(0,0,0,0.2);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e4e7ed;
  background: #f8f9fa;
}

.dialog-header h3 {
  margin: 0;
  color: #303133;
  font-weight: 600;
}

.dialog-content {
  padding: 24px;
  max-height: 60vh;
  overflow-y: auto;
}

.question-section, .answer-section {
  margin-bottom: 24px;
}

.question-label, .answer-label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-weight: 600;
  color: #303133;
}

.question-label {
  color: #409eff;
}

.answer-label {
  color: #67c23a;
}

.question-text, .answer-text {
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  line-height: 1.6;
  white-space: pre-line;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #e4e7ed;
  background: #f8f9fa;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-layout {
    flex-direction: column;
  }
  
  .left-panel, .right-panel {
    flex: none;
  }
  
  .right-panel {
    max-height: 300px;
  }
  
  .style-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .suggestion-tags {
    justify-content: flex-start;
  }
}

/* 滚动条样式 */
.panel-section::-webkit-scrollbar {
  width: 6px;
}

.panel-section::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.panel-section::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.panel-section::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>