<template>
  <div class="analysis-decision-page">
    <div class="content-layout">
      <!-- 左侧：分析与决策 -->
      <div class="left-panel">
        <div class="panel-section">
          <div class="section-header">
            <h3 class="section-title">分析与决策</h3>
            <el-button type="primary" class="create-btn">+新建分析</el-button>
          </div>
          
          <div class="analysis-content">
            <!-- 分析类型选择 -->
            <div class="analysis-type-section">
              <h4>选择分析类型</h4>
              <div class="type-cards">
                <div 
                  v-for="type in analysisTypes" 
                  :key="type.id"
                  class="type-card"
                  :class="{ active: selectedType === type.id }"
                  @click="selectedType = type.id"
                >
                  <div class="type-icon">
                    <el-icon size="30" :color="type.color"><component :is="type.icon" /></el-icon>
                  </div>
                  <div class="type-info">
                    <div class="type-title">{{ type.title }}</div>
                    <div class="type-description">{{ type.description }}</div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 分析参数设置 -->
            <div class="analysis-params">
              <h4>分析参数</h4>
              <div class="param-group">
                <label>时间范围</label>
                <el-select v-model="timeRange" placeholder="选择时间范围">
                  <el-option label="最近7天" value="7days" />
                  <el-option label="最近30天" value="30days" />
                  <el-option label="最近3个月" value="3months" />
                  <el-option label="最近6个月" value="6months" />
                </el-select>
              </div>
              <div class="param-group">
                <label>分析深度</label>
                <el-select v-model="analysisDepth" placeholder="选择分析深度">
                  <el-option label="基础分析" value="basic" />
                  <el-option label="深度分析" value="deep" />
                  <el-option label="专家级分析" value="expert" />
                </el-select>
              </div>
            </div>
            
            <!-- 开始分析按钮 -->
            <div class="analysis-actions">
              <el-button type="primary" size="large" class="start-btn" @click="startAnalysis">
                开始分析
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：分析结果 -->
      <div class="right-panel">
        <div class="panel-section">
          <h3 class="section-title">分析结果</h3>
          <div class="result-content">
            <div v-if="isAnalyzing" class="analyzing-indicator">
              <el-icon class="is-loading"><Loading /></el-icon>
              <p>正在分析数据...</p>
            </div>
            <div v-else-if="analysisResult" class="result-display">
              <div class="result-summary">
                <h4>分析摘要</h4>
                <div class="summary-content">{{ analysisResult.summary }}</div>
              </div>
              
              <div class="result-details">
                <h4>详细分析</h4>
                <div class="detail-items">
                  <div v-for="detail in analysisResult.details" :key="detail.id" class="detail-item">
                    <div class="detail-title">{{ detail.title }}</div>
                    <div class="detail-content">{{ detail.content }}</div>
                  </div>
                </div>
              </div>
              
              <div class="result-recommendations">
                <h4>决策建议</h4>
                <div class="recommendation-list">
                  <div v-for="rec in analysisResult.recommendations" :key="rec.id" class="recommendation-item">
                    <div class="rec-icon">
                      <el-icon size="16" color="#67c23a"><Check /></el-icon>
                    </div>
                    <div class="rec-content">{{ rec.content }}</div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <el-icon size="60" color="#ccc"><TrendCharts /></el-icon>
              <p>等待分析开始...</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { 
  TrendCharts, 
  Loading, 
  Check,
  DataAnalysis,
  PieChart,
  Histogram,
  Connection
} from '@element-plus/icons-vue'

// 响应式数据
const selectedType = ref('trend')
const timeRange = ref('30days')
const analysisDepth = ref('deep')
const isAnalyzing = ref(false)
const analysisResult = ref(null)

// 分析类型
const analysisTypes = ref([
  {
    id: 'trend',
    title: '趋势分析',
    description: '分析数据变化趋势和模式',
    icon: 'TrendCharts',
    color: '#409eff'
  },
  {
    id: 'correlation',
    title: '相关性分析',
    description: '分析不同指标间的关联关系',
    icon: 'Connection',
    color: '#67c23a'
  },
  {
    id: 'distribution',
    title: '分布分析',
    description: '分析数据的分布特征',
    icon: 'Histogram',
    color: '#e6a23c'
  },
  {
    id: 'prediction',
    title: '预测分析',
    description: '基于历史数据预测未来趋势',
    icon: 'DataAnalysis',
    color: '#f56c6c'
  }
])

// 开始分析
const startAnalysis = () => {
  if (!selectedType.value) {
    return
  }
  
  isAnalyzing.value = true
  analysisResult.value = null
  
  // 模拟分析过程
  setTimeout(() => {
    const results = {
      trend: {
        summary: '根据最近30天的数据分析，您的骨密度指标呈现稳定趋势，但钙摄入量需要关注。',
        details: [
          {
            id: 1,
            title: '骨密度变化',
            content: 'T值从-1.3稳定在-1.2，变化幅度在正常范围内。'
          },
          {
            id: 2,
            title: '钙摄入情况',
            content: '日均钙摄入量约600mg，低于推荐值800-1200mg。'
          },
          {
            id: 3,
            title: '运动频率',
            content: '每周运动3-4次，运动强度适中，有助于骨密度维持。'
          }
        ],
        recommendations: [
          { id: 1, content: '增加钙质摄入，建议每日补充钙片或增加奶制品摄入' },
          { id: 2, content: '保持现有运动习惯，可适当增加负重运动' },
          { id: 3, content: '定期进行骨密度检查，建议每6个月复查一次' }
        ]
      },
      correlation: {
        summary: '钙摄入量与骨密度呈正相关，运动频率与骨密度改善显著相关。',
        details: [
          {
            id: 1,
            title: '钙摄入相关性',
            content: '钙摄入量与骨密度T值相关系数为0.72，呈强正相关。'
          },
          {
            id: 2,
            title: '运动影响',
            content: '运动频率与骨密度改善程度相关系数为0.65。'
          }
        ],
        recommendations: [
          { id: 1, content: '重点关注钙质补充，这是影响骨密度的关键因素' },
          { id: 2, content: '保持规律运动，特别是负重运动对骨密度有益' }
        ]
      }
    }
    
    analysisResult.value = results[selectedType.value] || results.trend
    isAnalyzing.value = false
  }, 3000)
}
</script>

<style scoped>
.analysis-decision-page {
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

.analysis-content {
  display: flex;
  flex-direction: column;
  height: calc(100% - 80px);
  gap: 30px;
}

.analysis-type-section h4,
.analysis-params h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-weight: 600;
}

.type-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.type-card {
  background: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 15px;
}

.type-card:hover {
  border-color: #667eea;
  transform: translateY(-2px);
}

.type-card.active {
  border-color: #667eea;
  background: #f0f8ff;
}

.type-icon {
  flex-shrink: 0;
}

.type-info {
  flex: 1;
}

.type-title {
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.type-description {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
}

.analysis-params {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.param-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.param-group label {
  font-weight: 600;
  color: #333;
}

.analysis-actions {
  margin-top: auto;
  text-align: center;
}

.start-btn {
  padding: 12px 40px;
  font-size: 1.1rem;
}

.result-content {
  flex: 1;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.analyzing-indicator {
  text-align: center;
  color: #667eea;
}

.analyzing-indicator .el-icon {
  font-size: 2rem;
  margin-bottom: 10px;
}

.result-display {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.result-summary,
.result-details,
.result-recommendations {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
}

.result-summary h4,
.result-details h4,
.result-recommendations h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-weight: 600;
}

.summary-content {
  line-height: 1.6;
  color: #333;
}

.detail-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.detail-item {
  border-left: 3px solid #667eea;
  padding-left: 15px;
}

.detail-title {
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.detail-content {
  color: #666;
  line-height: 1.5;
}

.recommendation-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.recommendation-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.rec-icon {
  flex-shrink: 0;
  margin-top: 2px;
}

.rec-content {
  color: #333;
  line-height: 1.5;
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