<template>
  <div class="voice-page">
    <div class="content-layout">
      <!-- 左侧：语音自述 -->
      <div class="left-panel">
        <div class="panel-section">
          <div class="section-header">
            <h3 class="section-title">语音自述</h3>
            <el-button type="primary" class="create-btn">+创建新对话</el-button>
          </div>
          
          <div class="voice-content">
            <!-- 对话历史 -->
            <div class="conversation-history">
              <div class="message user-message">
                <div class="message-content">
                  今天早上起床翻身的时候,突然右边腰那里像针扎一样疼,完全不敢动,缓了几分钟才能慢慢起来,这是怎么回事?
                </div>
              </div>
              
              <div class="message ai-message">
                <div class="message-content">
                  根据您描述的症状，最可能的原因是急性腰扭伤或腰椎小关节紊乱。突然的翻身动作可能导致肌肉、韧带拉伤或关节卡压，引起剧烈疼痛和活动受限。
                  <br><br>
                  <strong>建议立即处理：</strong>
                  <br>1. 立即停止引起疼痛的动作
                  <br>2. 采取舒适体位休息（如侧卧位，屈膝）
                  <br>3. 冷敷（冰袋包裹毛巾，每次15-20分钟）
                  <br>4. 24小时内避免热敷、按摩或强行拉伸
                </div>
              </div>
              
              <div class="message user-message">
                <div class="message-content">
                  谢谢。那我需要马上去医院吗?还是可以先在家观察一下?
                </div>
              </div>
              
              <div class="message ai-message">
                <div class="message-content">
                  <strong>建议就医的情况：</strong>
                  <br>1. 疼痛持续加重，休息后无缓解
                  <br>2. 伴有下肢放射痛、麻木或无力（疼痛从臀部延伸至大腿、小腿甚至脚趾）
                  <br>3. 大小便控制困难或异常感觉（如鞍区麻木）
                  <br>4. 伴有发热或不明原因体重减轻
                  <br><br>
                  如无上述严重情况，建议严格休息和冷敷观察24小时。如疼痛明显改善，可后续预约复诊；如疼痛持续无改善或非常担心，建议到医院（骨科、康复科或疼痛科）进行专业检查（如触诊、活动度评估，必要时X线检查）以排除腰椎间盘突出等问题，这是最安全的做法。
                </div>
              </div>
            </div>
            
            <!-- 语音输入区域 -->
            <div class="voice-input-area">
              <el-button type="primary" size="large" class="speak-btn">
                按住说话
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：历史记录 -->
      <div class="right-panel">
        <div class="panel-section">
          <h3 class="section-title">历史记录</h3>
                     <div class="history-list">
             <div class="history-item" v-for="record in historyRecords" :key="record.id">
               <div class="record-info">
                 <div class="record-title">{{ record.title }}</div>
                 <div class="record-date">{{ record.date }}</div>
                 <div class="record-summary">{{ record.summary }}</div>
               </div>
               <el-button type="primary" size="small" class="view-btn" @click="viewHistory(record)">查看</el-button>
             </div>
           </div>
        </div>
             </div>
     </div>
   </div>

   <!-- 历史记录详情对话框 -->
   <HistoryDetailDialog
     v-model="showHistoryDialog"
     :record="selectedRecord"
     @delete="handleDeleteHistory"
   />
 </template>

<script setup lang="ts">
import { ref } from 'vue'
import { Document } from '@element-plus/icons-vue'
import { useHistory } from '@/composables/useHistory'
import HistoryDetailDialog from '@/components/HistoryDetailDialog.vue'
import type { HistoryRecord } from '@/types/history'

const { getHistoryByType, deleteHistoryRecord } = useHistory()

// 获取语音自述历史记录
const historyRecords = getHistoryByType('voice')

// 历史记录详情对话框
const showHistoryDialog = ref(false)
const selectedRecord = ref<HistoryRecord | null>(null)

// 查看历史记录详情
const viewHistory = (record: HistoryRecord) => {
  selectedRecord.value = record
  showHistoryDialog.value = true
}

// 删除历史记录
const handleDeleteHistory = (id: string) => {
  deleteHistoryRecord(id)
}
</script>

<style scoped>
.voice-page {
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

.voice-content {
  display: flex;
  flex-direction: column;
  height: calc(100% - 80px);
}

.conversation-history {
  flex: 1;
  overflow-y: auto;
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message {
  max-width: 80%;
  margin-bottom: 10px;
}

.user-message {
  align-self: flex-end;
}

.ai-message {
  align-self: flex-start;
}

.message-content {
  padding: 15px 20px;
  border-radius: 18px;
  line-height: 1.6;
  word-wrap: break-word;
}

.user-message .message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom-right-radius: 4px;
}

.ai-message .message-content {
  background: #f8f9fa;
  color: #333;
  border: 1px solid #e9ecef;
  border-bottom-left-radius: 4px;
}

.voice-input-area {
  padding: 20px 0;
  text-align: center;
  border-top: 1px solid #e9ecef;
  margin-top: auto;
}

.speak-btn {
  padding: 15px 40px;
  font-size: 1.1rem;
  border-radius: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
}

.speak-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #667eea;
}

.record-info {
  flex: 1;
}

.record-title {
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
  font-size: 1rem;
}

.record-date {
  color: #666;
  font-size: 0.8rem;
  margin-bottom: 5px;
}

.record-summary {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
}

.view-btn {
  margin-left: 10px;
}
</style> 