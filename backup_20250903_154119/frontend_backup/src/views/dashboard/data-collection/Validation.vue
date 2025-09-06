<template>
  <div class="validation-page">
    <div class="content-layout">
      <!-- 左侧：校验规则 -->
      <div class="left-panel">
        <div class="panel-section">
          <h3 class="section-title">校验规则</h3>
          <div class="validation-content">
            <p>这里将展示数据校验规则和配置。</p>
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
import { useHistory } from '@/composables/useHistory'
import HistoryDetailDialog from '@/components/HistoryDetailDialog.vue'
import type { HistoryRecord } from '@/types/history'

const { getHistoryByType, deleteHistoryRecord } = useHistory()

// 获取校验规则历史记录
const historyRecords = getHistoryByType('validation')

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
.validation-page {
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

.section-title {
  margin: 0 0 20px 0;
  font-size: 1.2rem;
  color: #333;
  font-weight: 600;
  border-bottom: 2px solid #667eea;
  padding-bottom: 8px;
}

.validation-content {
  padding: 20px;
  text-align: center;
  color: #666;
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