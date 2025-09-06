<template>
  <div class="his-page">
    <div class="content-layout">
      <!-- 左侧：医院HIS接口 -->
      <div class="left-panel">
        <div class="panel-section">
          <div class="section-header">
            <h3 class="section-title">医院HIS接口</h3>
            <div class="update-info">更新日期: 2025-01-20</div>
          </div>
          
          <div class="medical-report">
            <div class="report-header">
              <h4>首都医科大学附属北京同仁医院 医学影像诊断报告书</h4>
            </div>
            
            <div class="report-content">
              <div class="patient-info">
                <div class="info-row">
                  <span class="label">姓名:</span>
                  <span class="value">张南</span>
                  <span class="label">性别:</span>
                  <span class="value">男</span>
                  <span class="label">年龄:</span>
                  <span class="value">48岁</span>
                </div>
                <div class="info-row">
                  <span class="label">检查日期:</span>
                  <span class="value">2025-01-24</span>
                  <span class="label">检查类型:</span>
                  <span class="value">MR 下肢</span>
                </div>
              </div>
              
              <div class="report-section">
                <h5>影像所见:</h5>
                <p>右足踝关节MR平扫示：右足踝关节骨质结构完整，关节间隙正常，关节面光滑，周围软组织未见明显异常信号。</p>
              </div>
              
              <div class="report-section">
                <h5>诊断结论:</h5>
                <p>右足踝关节MR平扫未见明显异常。</p>
              </div>
              
              <div class="medical-images">
                <div class="image-container">
                  <div class="image-placeholder">影像1</div>
                </div>
                <div class="image-container">
                  <div class="image-placeholder">影像2</div>
                </div>
                <div class="image-container">
                  <div class="image-placeholder">影像3</div>
                </div>
              </div>
              
              <div class="data-cards">
                <div class="data-card">
                  <div class="card-content">
                    <div class="card-item">20210523</div>
                    <div class="card-item">Feng Hua Xin Qiao Orthopedice Hospital</div>
                    <div class="card-item">PID: 83627</div>
                    <div class="card-item">序列: 1</div>
                    <div class="card-item">影像: 1/2</div>
                    <div class="card-item">倍率: 0.73</div>
                  </div>
                </div>
                <div class="data-card">
                  <div class="card-content">
                    <div class="card-item">20210523</div>
                    <div class="card-item">Feng Hua Xin Qiao Orthopedice Hospital</div>
                    <div class="card-item">PID: 83627</div>
                    <div class="card-item">序列: 1</div>
                    <div class="card-item">影像: 1/2</div>
                    <div class="card-item">倍率: 0.73</div>
                  </div>
                </div>
              </div>
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
import { useHistory } from '@/composables/useHistory'
import HistoryDetailDialog from '@/components/HistoryDetailDialog.vue'
import type { HistoryRecord } from '@/types/history'

const { getHistoryByType, deleteHistoryRecord } = useHistory()

// 获取HIS接口历史记录
const historyRecords = getHistoryByType('his')

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
.his-page {
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

.update-info {
  font-size: 0.9rem;
  color: #666;
}

.medical-report {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 20px;
  margin-bottom: 20px;
}

.report-header h4 {
  margin: 0 0 20px 0;
  color: #333;
  font-weight: 600;
  text-align: center;
}

.patient-info {
  margin-bottom: 20px;
}

.info-row {
  display: flex;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.label {
  font-weight: 600;
  color: #333;
  margin-right: 8px;
  min-width: 80px;
}

.value {
  color: #666;
  margin-right: 20px;
}

.report-section {
  margin-bottom: 20px;
}

.report-section h5 {
  margin: 0 0 10px 0;
  color: #333;
  font-weight: 600;
}

.report-section p {
  margin: 0;
  line-height: 1.6;
  color: #666;
}

.medical-images {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.image-container {
  flex: 1;
  height: 80px;
  background: #e9ecef;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-placeholder {
  color: #999;
  font-size: 0.9rem;
}

.data-cards {
  display: flex;
  gap: 10px;
}

.data-card {
  flex: 1;
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  padding: 15px;
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.card-item {
  font-size: 0.8rem;
  color: #666;
  line-height: 1.4;
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