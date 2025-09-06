<template>
  <div class="diet-page">
    <div class="content-layout">
      <!-- 左侧：饮食照片AI识别 -->
      <div class="left-panel">
        <div class="panel-section">
          <div class="section-header">
            <h3 class="section-title">饮食照片AI识别</h3>
            <el-button type="primary" class="create-btn">+创建新对话</el-button>
          </div>
          
          <div class="diet-content">
            <!-- 食物图片展示 -->
            <div class="food-image-section">
              <div class="food-image">
                <div class="image-placeholder">
                  <el-icon size="60" color="#667eea"><Picture /></el-icon>
                  <p>牛奶图片</p>
                </div>
              </div>
            </div>
            
            <!-- 分析结果 -->
            <div class="analysis-result">
              <div class="result-header">
                <h4>识别成功!这是一杯约500ml的纯牛奶,为您分析如下:</h4>
              </div>
              
              <div class="nutrition-data">
                <h5>1. 核心营养数据速览</h5>
                <ul>
                  <li><strong>钙含量:</strong> 约600毫克(基于每100ml牛奶含120mg钙计算)</li>
                  <li><strong>蛋白质:</strong> 约15-17克(相当于2-3个鸡蛋的蛋白质量)</li>
                  <li><strong>其他关键营养素:</strong> 维生素D、维生素B2(核黄素)、磷、钾。</li>
                </ul>
              </div>
              
              <div class="benefits-section">
                <h5>2. 对您的好处</h5>
                <div class="benefit-items">
                  <div class="benefit-item">
                    <h6>骨骼与牙齿的"建筑师"</h6>
                    <p>钙质是维持骨密度的重要元素，对预防骨质疏松症有重要作用，特别适合各年龄段人群。</p>
                  </div>
                  <div class="benefit-item">
                    <h6>优质蛋白"补给站"</h6>
                    <p>牛奶含有完整的蛋白质，包含所有必需氨基酸，有助于肌肉修复和身体恢复。</p>
                  </div>
                  <div class="benefit-item">
                    <h6>神经系统的"稳定剂"</h6>
                    <p>钙和镁元素有助于舒缓神经，改善睡眠质量，缓解压力。</p>
                  </div>
                  <div class="benefit-item">
                    <h6>身体的"综合维护师"</h6>
                    <p>B族维生素促进能量代谢，维生素D帮助钙吸收，钾元素稳定血压。</p>
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
import { Picture, Camera } from '@element-plus/icons-vue'
import { useHistory } from '@/composables/useHistory'
import HistoryDetailDialog from '@/components/HistoryDetailDialog.vue'
import type { HistoryRecord } from '@/types/history'

const { getHistoryByType, deleteHistoryRecord } = useHistory()

// 获取饮食识别历史记录
const historyRecords = getHistoryByType('diet')

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
.diet-page {
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

.diet-content {
  height: calc(100% - 80px);
  overflow-y: auto;
  padding: 20px 0;
}

.food-image-section {
  text-align: center;
  margin-bottom: 30px;
}

.food-image {
  display: inline-block;
  width: 200px;
  height: 200px;
  border: 2px dashed #667eea;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f8ff;
}

.image-placeholder {
  text-align: center;
  color: #667eea;
}

.image-placeholder p {
  margin-top: 10px;
  font-weight: 500;
}

.analysis-result {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 20px;
}

.result-header h4 {
  margin: 0 0 20px 0;
  color: #333;
  font-weight: 600;
  text-align: center;
}

.nutrition-data {
  margin-bottom: 25px;
}

.nutrition-data h5 {
  margin: 0 0 15px 0;
  color: #667eea;
  font-weight: 600;
}

.nutrition-data ul {
  margin: 0;
  padding-left: 20px;
}

.nutrition-data li {
  margin-bottom: 8px;
  line-height: 1.6;
  color: #666;
}

.benefits-section h5 {
  margin: 0 0 20px 0;
  color: #667eea;
  font-weight: 600;
}

.benefit-items {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.benefit-item {
  background: white;
  border-radius: 8px;
  padding: 20px;
  border-left: 4px solid #667eea;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.benefit-item h6 {
  margin: 0 0 10px 0;
  color: #333;
  font-weight: 600;
  font-size: 1rem;
}

.benefit-item p {
  margin: 0;
  color: #666;
  line-height: 1.6;
  font-size: 0.9rem;
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