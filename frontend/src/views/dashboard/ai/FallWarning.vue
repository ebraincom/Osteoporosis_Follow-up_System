<template>
  <div class="fall-warning-page">
    <div class="content-layout">
      <!-- 左侧：跌倒预警 -->
      <div class="left-panel">
        <div class="panel-section">
          <div class="section-header">
            <h3 class="section-title">跌倒预警</h3>
            <div class="device-status">
              <el-icon size="20" color="#67c23a"><Monitor /></el-icon>
              <span>85% 设备已连接</span>
            </div>
          </div>
          
          <div class="warning-content">
            <!-- 当前安全状态 -->
            <div class="safety-status-section">
              <h4>当前状态</h4>
              <div class="safety-status-panel">
                <div class="status-icon">
                  <el-icon size="60" color="#409eff"><ShieldCheck /></el-icon>
                </div>
                <div class="status-text">安全</div>
              </div>
            </div>
            
            <!-- 健康指标卡片 -->
            <div class="health-metrics">
              <div class="metric-card">
                <div class="metric-icon">
                  <el-icon size="24" color="#409eff"><Footprints /></el-icon>
                </div>
                <div class="metric-content">
                  <div class="metric-title">今日步数</div>
                  <div class="metric-value">2,345</div>
                </div>
              </div>
              
              <div class="metric-card">
                <div class="metric-icon">
                  <el-icon size="24" color="#f56c6c"><Heart /></el-icon>
                </div>
                <div class="metric-content">
                  <div class="metric-title">今日心率</div>
                  <div class="metric-value">72次/分钟</div>
                </div>
              </div>
              
              <div class="metric-card">
                <div class="metric-icon">
                  <el-icon size="24" color="#67c23a"><Temperature /></el-icon>
                </div>
                <div class="metric-content">
                  <div class="metric-title">今日血压</div>
                  <div class="metric-value">
                    <div>收缩压: 120-150 mmHg</div>
                    <div>舒张压: 70-85 mmHg</div>
                  </div>
                </div>
              </div>
              
              <div class="metric-card">
                <div class="metric-icon">
                  <el-icon size="24" color="#e6a23c"><Lightning /></el-icon>
                </div>
                <div class="metric-content">
                  <div class="metric-title">血氧饱和度</div>
                  <div class="metric-value">95%-99%</div>
                </div>
              </div>
            </div>
            
            <!-- 求助按钮 -->
            <div class="help-section">
              <el-button type="danger" size="large" class="help-btn">
                <el-icon size="20"><Warning /></el-icon>
                求助
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：预警历史 -->
      <div class="right-panel">
        <div class="panel-section">
          <h3 class="section-title">预警历史</h3>
          <div class="warning-history">
            <div class="history-item" v-for="item in warningHistory" :key="item.id">
              <div class="history-icon" :class="item.type">
                <el-icon size="20">
                  <component :is="item.icon" />
                </el-icon>
              </div>
              <div class="history-content">
                <div class="history-title">{{ item.title }}</div>
                <div class="history-time">{{ item.time }}</div>
                <div class="history-description">{{ item.description }}</div>
              </div>
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
  Monitor, 
  ShieldCheck, 
  Footprints, 
  Heart, 
  Temperature, 
  Lightning, 
  Warning,
  Bell
} from '@element-plus/icons-vue'

// 预警历史数据
const warningHistory = ref([
  {
    id: 1,
    type: 'warning',
    icon: 'Bell',
    title: '异常活动检测',
    time: '2025-01-20 14:30',
    description: '检测到异常活动模式，建议检查身体状况'
  },
  {
    id: 2,
    type: 'info',
    icon: 'ShieldCheck',
    title: '设备连接正常',
    time: '2025-01-20 12:00',
    description: '监测设备连接状态良好，数据正常传输'
  },
  {
    id: 3,
    type: 'success',
    icon: 'ShieldCheck',
    title: '安全状态确认',
    time: '2025-01-20 10:15',
    description: '所有健康指标正常，安全状态良好'
  }
])
</script>

<style scoped>
.fall-warning-page {
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

.device-status {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #67c23a;
  font-size: 0.9rem;
}

.warning-content {
  display: flex;
  flex-direction: column;
  height: calc(100% - 80px);
  gap: 30px;
}

.safety-status-section h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-weight: 600;
}

.safety-status-panel {
  background: #f0f9ff;
  border: 2px solid #409eff;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.status-icon {
  margin-bottom: 10px;
}

.status-text {
  font-size: 2rem;
  font-weight: bold;
  color: #409eff;
}

.health-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.metric-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  border-left: 4px solid #667eea;
}

.metric-icon {
  flex-shrink: 0;
}

.metric-content {
  flex: 1;
}

.metric-title {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 5px;
}

.metric-value {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  line-height: 1.4;
}

.help-section {
  text-align: center;
  margin-top: auto;
}

.help-btn {
  padding: 15px 40px;
  font-size: 1.2rem;
  border-radius: 50px;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 auto;
  box-shadow: 0 4px 15px rgba(245, 108, 108, 0.3);
  transition: all 0.3s ease;
}

.help-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(245, 108, 108, 0.4);
}

.warning-history {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.history-item {
  display: flex;
  gap: 15px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.history-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.history-icon.warning {
  background: #e6a23c;
}

.history-icon.info {
  background: #409eff;
}

.history-icon.success {
  background: #67c23a;
}

.history-content {
  flex: 1;
}

.history-title {
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.history-time {
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 5px;
}

.history-description {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
}
</style> 