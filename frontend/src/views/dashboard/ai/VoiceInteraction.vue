<template>
  <div class="voice-interaction-page">
    <div class="content-layout">
      <!-- 左侧：语音交互控制 -->
      <div class="left-panel">
        <div class="panel-section">
          <div class="section-header">
            <h3 class="section-title">语音交互助手</h3>
            <div class="header-actions">
              <el-button type="success" size="small" @click="clearHistory">
                <el-icon><Delete /></el-icon>
                清空历史
              </el-button>
              <el-button type="primary" size="small" @click="startNewSession">
                <el-icon><Plus /></el-icon>
                新建会话
              </el-button>
            </div>
          </div>
          
          <div class="voice-content">
            <!-- 语音助手形象 -->
            <div class="voice-assistant-section">
              <div class="assistant-avatar">
                <div class="avatar-container" :class="{ 'speaking': isSpeaking, 'listening': isListening }">
                  <el-icon size="60" color="white"><ChatLineRound /></el-icon>
                  <div class="status-indicator" :class="{ 'online': isConnected }"></div>
                </div>
                <h4>AI语音助手</h4>
                <p class="status-text">{{ getStatusText() }}</p>
              </div>
            </div>
            
            <!-- 语音控制 -->
            <div class="voice-controls">
              <div class="control-section">
                <h4>语音设置</h4>
                <div class="voice-options">
                  <el-select v-model="selectedVoice" placeholder="选择语音" size="small">
                    <el-option
                      v-for="voice in voiceOptions"
                      :key="voice.id"
                      :label="voice.name"
                      :value="voice.id"
                    >
                      <span>{{ voice.name }}</span>
                      <span style="float: right; color: #8492a6; font-size: 13px">{{ voice.description }}</span>
                    </el-option>
                  </el-select>
                </div>
              </div>
              
              <div class="control-section">
                <h4>语音交互</h4>
                <div class="voice-interaction-controls">
                  <div 
                    class="voice-button"
                    :class="{ 
                      'recording': isRecording, 
                      'disabled': !isConnected,
                      'speaking': isSpeaking
                    }"
                    @mousedown="startVoiceInput"
                    @mouseup="stopVoiceInput"
                    @mouseleave="stopVoiceInput"
                    @touchstart="startVoiceInput"
                    @touchend="stopVoiceInput"
                  >
                    <div class="voice-button-inner">
                      <el-icon size="40" color="white">
                        <Microphone v-if="!isRecording && !isSpeaking" />
                        <VideoPause v-else-if="isRecording" />
                        <VideoPlay v-else-if="isSpeaking" />
                      </el-icon>
                    </div>
                    <div class="voice-button-text">
                      {{ getVoiceButtonText() }}
                    </div>
                  </div>
                  <div class="voice-hint">
                    {{ getVoiceHint() }}
                  </div>
                </div>
              </div>
              
              <div class="control-section">
                <h4>音量控制</h4>
                <div class="volume-controls">
                  <el-slider
                    v-model="volume"
                    :min="0"
                    :max="100"
                    :show-tooltip="false"
                    @change="updateVolume"
                  />
                  <span class="volume-text">{{ volume }}%</span>
                </div>
              </div>
            </div>
            
            <!-- 连接状态 -->
            <div class="connection-status">
              <el-alert
                :title="connectionStatus.title"
                :type="connectionStatus.type"
                :description="connectionStatus.description"
                show-icon
                :closable="false"
              />
            </div>
          </div>
        </div>
      </div>
      
      <!-- 右侧：对话历史 -->
      <div class="right-panel">
        <div class="panel-section">
          <div class="section-header">
            <h3 class="section-title">对话历史</h3>
            <div class="header-actions">
              <el-button type="info" size="small" @click="exportHistory">
                <el-icon><Download /></el-icon>
                导出
              </el-button>
            </div>
          </div>
          
          <div class="conversation-history">
            <div v-if="conversationHistory.length === 0" class="empty-state">
              <el-icon size="48" color="#c0c4cc"><ChatDotRound /></el-icon>
              <p>暂无对话记录</p>
              <p class="empty-hint">点击"开始录音"开始语音对话</p>
            </div>
            
            <div v-else class="history-list">
              <div
                v-for="(item, index) in conversationHistory"
                :key="index"
                class="history-item"
              >
                <div class="message user-message" v-if="item.type === 'user'">
                  <div class="message-avatar">
                    <el-icon><User /></el-icon>
                  </div>
                  <div class="message-content">
                    <div class="message-text">
                      <el-icon><Microphone /></el-icon>
                      <span>语音消息</span>
                    </div>
                    <div class="message-time">{{ formatTime(item.timestamp) }}</div>
                  </div>
                </div>
                
                <div class="message assistant-message" v-if="item.type === 'assistant'">
                  <div class="message-avatar">
                    <el-icon><Avatar /></el-icon>
                  </div>
                  <div class="message-content">
                    <div class="message-text">
                      <el-icon><VideoPlay /></el-icon>
                      <span>语音回复</span>
                      <el-button
                        type="text"
                        size="small"
                        @click="playAudio(item.audioData)"
                        :disabled="isPlaying"
                      >
                        {{ isPlaying ? '播放中...' : '播放' }}
                      </el-button>
                    </div>
                    <div class="message-time">{{ formatTime(item.timestamp) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Delete, 
  Plus, 
  Microphone, 
  Download, 
  ChatDotRound, 
  User, 
  Avatar, 
  VideoPlay,
  VideoPause,
  Star,
  ChatLineRound
} from '@element-plus/icons-vue'

// 响应式数据
const isConnected = ref(false)
const isRecording = ref(false)
const isListening = ref(false)
const isSpeaking = ref(false)
const isPlaying = ref(false)
const selectedVoice = ref('alloy')
const volume = ref(50)
const conversationHistory = ref<Array<{
  type: 'user' | 'assistant'
  timestamp: Date
  audioData?: string
  text?: string
}>>([])

// 语音选项
const voiceOptions = ref([
  { id: 'alloy', name: 'Alloy', description: '自然女声' },
  { id: 'echo', name: 'Echo', description: '清晰男声' },
  { id: 'fable', name: 'Fable', description: '温暖女声' },
  { id: 'onyx', name: 'Onyx', description: '深沉男声' },
  { id: 'nova', name: 'Nova', description: '年轻女声' },
  { id: 'shimmer', name: 'Shimmer', description: '柔和女声' }
])

// 连接状态
const connectionStatus = reactive({
  title: '未连接',
  type: 'info' as 'success' | 'warning' | 'info' | 'error',
  description: '正在连接语音服务...'
})

// WebSocket连接
let websocket: WebSocket | null = null
let mediaRecorder: MediaRecorder | null = null
let audioContext: AudioContext | null = null
let audioChunks: Blob[] = []

// 生命周期
onMounted(() => {
  initAudioContext()
  connectWebSocket()
  loadHistoryFromLocal()
})

onUnmounted(() => {
  disconnectWebSocket()
  if (mediaRecorder && mediaRecorder.state === 'recording') {
    mediaRecorder.stop()
  }
})

// 初始化音频上下文
const initAudioContext = () => {
  try {
    audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
  } catch (error) {
    console.error('初始化音频上下文失败:', error)
    ElMessage.error('音频初始化失败，请检查浏览器权限')
  }
}

  // 连接WebSocket
  const connectWebSocket = () => {
    try {
      // 使用后端服务的WebSocket端点
      const wsUrl = `ws://117.50.198.126:8000/v1/voice/voice-chat?user_id=default`
    
    websocket = new WebSocket(wsUrl)
    
    websocket.onopen = () => {
      isConnected.value = true
      connectionStatus.title = '已连接'
      connectionStatus.type = 'success'
      connectionStatus.description = '语音服务连接正常'
      ElMessage.success('语音服务连接成功')
    }
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      handleWebSocketMessage(data)
    }
    
    websocket.onclose = () => {
      isConnected.value = false
      connectionStatus.title = '连接断开'
      connectionStatus.type = 'error'
      connectionStatus.description = '语音服务连接已断开'
      ElMessage.warning('语音服务连接断开')
    }
    
    websocket.onerror = (error) => {
      console.error('WebSocket错误:', error)
      connectionStatus.title = '连接错误'
      connectionStatus.type = 'error'
      connectionStatus.description = '语音服务连接失败'
      ElMessage.error('语音服务连接失败')
    }
    
  } catch (error) {
    console.error('WebSocket连接失败:', error)
    ElMessage.error('无法连接到语音服务')
  }
}

// 断开WebSocket
const disconnectWebSocket = () => {
  if (websocket) {
    websocket.close()
    websocket = null
  }
}

// 处理WebSocket消息
const handleWebSocketMessage = (data: any) => {
  switch (data.type) {
    case 'recording_started':
      isListening.value = true
      break
    case 'recording_stopped':
      isListening.value = false
      break
    case 'audio_response':
      isSpeaking.value = true
      // 播放AI回复的音频
      playAudioResponse(data.audio)
      // 添加到历史记录
      conversationHistory.value.push({
        type: 'assistant',
        timestamp: new Date(),
        audioData: data.audio
      })
      break
    case 'response_done':
      isSpeaking.value = false
      break
    case 'error':
      ElMessage.error(data.message)
      break
  }
}

// 开始语音输入（按住说话）
const startVoiceInput = async (event: Event) => {
  event.preventDefault()
  
  if (!isConnected.value) {
    ElMessage.warning('请先连接语音服务')
    return
  }
  
  if (isRecording.value || isSpeaking.value) {
    return
  }
  
  await startRecording()
}

// 停止语音输入（松手发送）
const stopVoiceInput = (event: Event) => {
  event.preventDefault()
  
  if (isRecording.value) {
    stopRecording()
  }
}

// 开始录音
const startRecording = async () => {
  try {
    // 检查浏览器兼容性
    console.log('检查浏览器兼容性...')
    console.log('navigator.mediaDevices:', navigator.mediaDevices)
    console.log('navigator.mediaDevices.getUserMedia:', navigator.mediaDevices?.getUserMedia)
    console.log('当前协议:', window.location.protocol)
    console.log('当前域名:', window.location.hostname)
    
    if (!navigator.mediaDevices) {
      ElMessage.error('您的浏览器不支持MediaDevices API，请使用Chrome、Firefox或Safari浏览器')
      return
    }
    
    if (!navigator.mediaDevices.getUserMedia) {
      ElMessage.error('您的浏览器不支持getUserMedia API，请使用Chrome、Firefox或Safari浏览器')
      return
    }
    
    // 检查是否为HTTP环境
    if (window.location.protocol === 'http:' && window.location.hostname !== 'localhost') {
      ElMessage.error('HTTP环境下无法使用麦克风，请使用HTTPS访问或联系管理员配置SSL证书')
      return
    }
    
    // 检查麦克风权限状态
    try {
      const permissionStatus = await navigator.permissions.query({ name: 'microphone' as PermissionName })
      console.log('麦克风权限状态:', permissionStatus.state)
      
      if (permissionStatus.state === 'denied') {
        ElMessage.error('麦克风权限被拒绝，请在浏览器设置中允许此网站访问麦克风')
        return
      }
    } catch (error) {
      console.warn('无法检查权限状态:', error)
    }
    
    // 检查是否有可用的音频设备（兼容性处理）
    let audioInputs = []
    try {
      const devices = await navigator.mediaDevices.enumerateDevices()
      audioInputs = devices.filter(device => device.kind === 'audioinput')
      console.log('可用的音频输入设备:', audioInputs)
    } catch (error) {
      console.warn('无法枚举设备，但继续尝试录音:', error)
    }
    
    // 尝试获取用户媒体，使用更宽松的约束
    console.log('正在请求麦克风权限...')
    const stream = await navigator.mediaDevices.getUserMedia({ 
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true
      }
    })
    console.log('麦克风权限获取成功，音频流:', stream)
    
    mediaRecorder = new MediaRecorder(stream, {
      mimeType: 'audio/webm;codecs=opus'
    })
    
    audioChunks = []
    
    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data)
      }
    }
    
    mediaRecorder.onstop = () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
      sendAudioToServer(audioBlob)
      stream.getTracks().forEach(track => track.stop())
    }
    
    mediaRecorder.start(100) // 每100ms收集一次数据
    isRecording.value = true
    
    // 发送开始录音消息
    if (websocket) {
      websocket.send(JSON.stringify({ type: 'start_recording' }))
    }
    
    // 添加到历史记录
    conversationHistory.value.push({
      type: 'user',
      timestamp: new Date()
    })
    
    // 不显示开始录音提示，因为用户已经按住按钮了
    
  } catch (error: any) {
    console.error('录音失败:', error)
    
    // 检测浏览器类型
    const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent)
    const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0
    
    // 根据不同的错误类型给出具体的提示
    if (error.name === 'NotFoundError') {
      ElMessage.error('未找到麦克风设备，请检查：1. 耳机是否正确插入 2. 麦克风是否被其他应用占用')
    } else if (error.name === 'NotAllowedError') {
      if (isSafari && isMac) {
        ElMessage.error('Safari浏览器需要HTTPS才能使用麦克风，或者请在Safari偏好设置中允许此网站访问麦克风')
      } else {
        ElMessage.error('麦克风权限被拒绝，请在浏览器设置中允许麦克风访问')
      }
    } else if (error.name === 'NotReadableError') {
      ElMessage.error('麦克风被其他应用占用，请关闭其他使用麦克风的程序')
    } else if (error.message && error.message.includes('enumerateDevices')) {
      if (isSafari) {
        ElMessage.error('Safari浏览器兼容性问题，建议使用Chrome或Firefox浏览器')
      } else {
        ElMessage.error('浏览器兼容性问题，请尝试使用Chrome或Firefox浏览器')
      }
    } else {
      ElMessage.error(`录音失败: ${error.message}`)
    }
  }
}

// 停止录音
const stopRecording = () => {
  if (mediaRecorder && mediaRecorder.state === 'recording') {
    mediaRecorder.stop()
    isRecording.value = false
    
    // 发送停止录音消息
    if (websocket) {
      websocket.send(JSON.stringify({ type: 'stop_recording' }))
    }
    
    ElMessage.success('语音已发送')
  }
}

// 发送音频到服务器
const sendAudioToServer = async (audioBlob: Blob) => {
  try {
    const arrayBuffer = await audioBlob.arrayBuffer()
    const uint8Array = new Uint8Array(arrayBuffer)
    
    // 使用更安全的方式转换base64，避免栈溢出
    let binary = ''
    const chunkSize = 8192 // 分块处理，避免栈溢出
    
    for (let i = 0; i < uint8Array.length; i += chunkSize) {
      const chunk = uint8Array.slice(i, i + chunkSize)
      binary += String.fromCharCode.apply(null, Array.from(chunk))
    }
    
    const base64Audio = btoa(binary)
    
    if (websocket && websocket.readyState === WebSocket.OPEN) {
      websocket.send(JSON.stringify({
        type: 'audio_data',
        audio: base64Audio
      }))
      console.log('音频数据发送成功，大小:', base64Audio.length, '字符')
    } else {
      console.warn('WebSocket未连接，无法发送音频数据')
    }
  } catch (error) {
    console.error('发送音频失败:', error)
    ElMessage.error('发送音频失败')
  }
}

// 播放AI回复音频
const playAudioResponse = (audioBase64: string) => {
  try {
    if (!audioBase64) {
      console.warn('没有音频数据可播放')
      return
    }
    
    const audioData = atob(audioBase64)
    const audioBuffer = new Uint8Array(audioData.length)
    for (let i = 0; i < audioData.length; i++) {
      audioBuffer[i] = audioData.charCodeAt(i)
    }
    
    const blob = new Blob([audioBuffer], { type: 'audio/wav' })
    const audioUrl = URL.createObjectURL(blob)
    const audio = new Audio(audioUrl)
    
    audio.onended = () => {
      isSpeaking.value = false
      URL.revokeObjectURL(audioUrl)
    }
    
    audio.onerror = (error) => {
      console.error('音频播放错误:', error)
      isSpeaking.value = false
      URL.revokeObjectURL(audioUrl)
    }
    
    audio.volume = volume.value / 100
    audio.play()
    
    console.log('开始播放音频回复，大小:', audioData.length, '字节')
    
  } catch (error) {
    console.error('播放音频失败:', error)
    ElMessage.error('播放音频失败')
  }
}

// 播放历史音频
const playAudio = (audioBase64: string | undefined) => {
  if (!audioBase64) return
  isPlaying.value = true
  playAudioResponse(audioBase64)
  setTimeout(() => {
    isPlaying.value = false
  }, 3000) // 假设音频长度约3秒
}

// 更新音量
const updateVolume = (newVolume: number | number[]) => {
  volume.value = Array.isArray(newVolume) ? newVolume[0] : newVolume
}

// 获取状态文本
const getStatusText = () => {
  if (!isConnected.value) return '离线'
  if (isRecording.value) return '正在录音...'
  if (isListening.value) return '正在聆听...'
  if (isSpeaking.value) return '正在回复...'
  return '在线服务中'
}

// 获取语音按钮文本
const getVoiceButtonText = () => {
  if (!isConnected.value) return '未连接'
  if (isRecording.value) return '松手发送'
  if (isSpeaking.value) return '正在播放'
  return '按住说话'
}

// 获取语音提示
const getVoiceHint = () => {
  if (!isConnected.value) return '请先连接语音服务'
  if (isRecording.value) return '正在录音，松手即可发送'
  if (isSpeaking.value) return 'AI正在回复，请稍候'
  return '按住按钮说话，松手发送语音'
}

// 清空历史
const clearHistory = async () => {
  try {
    await ElMessageBox.confirm('确定要清空所有对话历史吗？', '确认清空', {
      type: 'warning'
    })
    conversationHistory.value = []
    saveHistoryToLocal()
    ElMessage.success('历史记录已清空')
  } catch {
    // 用户取消
  }
}

// 新建会话
const startNewSession = () => {
  if (isRecording.value) {
    stopRecording()
  }
  ElMessage.success('开始新的语音会话')
}

// 导出历史
const exportHistory = () => {
  if (conversationHistory.value.length === 0) {
    ElMessage.warning('暂无对话记录可导出')
    return
  }
  
  const dataStr = JSON.stringify(conversationHistory.value, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  
  const link = document.createElement('a')
  link.href = url
  link.download = `voice_conversation_${new Date().toISOString().split('T')[0]}.json`
  link.click()
  
  URL.revokeObjectURL(url)
  ElMessage.success('对话历史已导出')
}

// 格式化时间
const formatTime = (date: Date) => {
  return date.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

// 保存历史到本地
const saveHistoryToLocal = () => {
  localStorage.setItem('voiceConversationHistory', JSON.stringify(conversationHistory.value))
}

// 从本地加载历史
const loadHistoryFromLocal = () => {
  try {
    const saved = localStorage.getItem('voiceConversationHistory')
    if (saved) {
      conversationHistory.value = JSON.parse(saved)
    }
  } catch (error) {
    console.error('加载历史记录失败:', error)
  }
}
</script>

<style scoped>
.voice-interaction-page {
  height: 100vh;
  background: #f5f7fa;
  overflow: hidden;
}

.content-layout {
  display: flex;
  height: 100%;
  gap: 20px;
  padding: 20px;
}

.left-panel, .right-panel {
  flex: 1;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.panel-section {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
  background: #fafafa;
}

.section-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.voice-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.voice-assistant-section {
  text-align: center;
  margin-bottom: 30px;
}

.assistant-avatar {
  display: inline-block;
}

.avatar-container {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  transition: all 0.3s ease;
}

.avatar-container.speaking {
  animation: pulse 1s infinite;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
}

.avatar-container.listening {
  animation: pulse 1s infinite;
  background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.status-indicator {
  position: absolute;
  bottom: 5px;
  right: 5px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #f56c6c;
  border: 3px solid white;
}

.status-indicator.online {
  background: #67c23a;
}

.status-text {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.voice-controls {
  margin-bottom: 30px;
}

.control-section {
  margin-bottom: 25px;
}

.control-section h4 {
  margin: 0 0 15px 0;
  font-size: 16px;
  color: #303133;
}

.voice-options {
  margin-bottom: 15px;
}

.voice-interaction-controls {
  text-align: center;
  padding: 20px 0;
}

.voice-button {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  user-select: none;
}

.voice-button:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.voice-button.recording {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  animation: pulse 1s infinite;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.6);
}

.voice-button.speaking {
  background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
  animation: pulse 1s infinite;
  box-shadow: 0 4px 15px rgba(78, 205, 196, 0.6);
}

.voice-button.disabled {
  background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%);
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 2px 8px rgba(149, 165, 166, 0.3);
}

.voice-button-inner {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
}

.voice-button-text {
  color: white;
  font-size: 12px;
  font-weight: 600;
  text-align: center;
  line-height: 1.2;
}

.voice-hint {
  color: #606266;
  font-size: 14px;
  margin-top: 10px;
  text-align: center;
  min-height: 20px;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.volume-controls {
  display: flex;
  align-items: center;
  gap: 15px;
}

.volume-text {
  min-width: 40px;
  text-align: center;
  color: #606266;
  font-size: 14px;
}

.connection-status {
  margin-top: 20px;
}

.conversation-history {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #909399;
}

.empty-hint {
  font-size: 14px;
  margin-top: 10px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.history-item {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.message {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
}

.user-message .message-avatar {
  background: #409eff;
}

.assistant-message .message-avatar {
  background: #67c23a;
}

.message-content {
  flex: 1;
  background: #f5f7fa;
  padding: 12px 16px;
  border-radius: 12px;
  max-width: 80%;
}

.message-text {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #303133;
  font-size: 14px;
}

.message-time {
  margin-top: 5px;
  font-size: 12px;
  color: #909399;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-layout {
    flex-direction: column;
    padding: 10px;
  }
  
  .left-panel, .right-panel {
    flex: none;
    height: 50vh;
  }
}
</style>