<template>
  <div class="version-page">
    <div class="version-content">
      <h2 class="page-title">骨质疏松症跟踪随访系统</h2>
      <div class="version-info">
        <h3 class="version-number">版本号 1.0.0</h3>
      </div>
      
      <!-- 版本详细信息 -->
      <div class="version-details">
        <div class="detail-section">
          <h4>系统信息</h4>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">系统名称:</span>
              <span class="value">骨质疏松症跟踪随访系统</span>
            </div>
            <div class="info-item">
              <span class="label">当前版本:</span>
              <span class="value">1.0.0</span>
            </div>
            <div class="info-item">
              <span class="label">发布日期:</span>
              <span class="value">2025-09-07</span>
            </div>
            <div class="info-item">
              <span class="label">构建编号:</span>
              <span class="value">Build-20250907-001</span>
            </div>
            <div class="info-item">
              <span class="label">系统运行时间:</span>
              <span class="value">{{ systemUptime }}</span>
            </div>
            <div class="info-item">
              <span class="label">当前时间:</span>
              <span class="value">{{ currentTime }}</span>
            </div>
            <div class="info-item">
              <span class="label">系统状态:</span>
              <span class="value">
                <el-tag :type="systemStatus.type" size="small">
                  {{ systemStatus.text }}
                </el-tag>
              </span>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4>技术栈</h4>
          <div class="tech-stack">
            <div class="tech-item">
              <span class="tech-label">前端框架:</span>
              <span class="tech-value">Vue 3.4.0</span>
            </div>
            <div class="tech-item">
              <span class="tech-label">UI组件库:</span>
              <span class="tech-value">Element Plus 2.4.0</span>
            </div>
            <div class="tech-item">
              <span class="tech-label">构建工具:</span>
              <span class="tech-value">Vite 5.0.0</span>
            </div>
            <div class="tech-item">
              <span class="tech-label">后端框架:</span>
              <span class="tech-value">FastAPI 0.104.0</span>
            </div>
            <div class="tech-item">
              <span class="tech-label">数据库:</span>
              <span class="tech-value">SQLite 3.45.0</span>
            </div>
            <div class="tech-item">
              <span class="tech-label">Python版本:</span>
              <span class="tech-value">Python 3.11.0</span>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4>更新日志</h4>
          <div class="changelog">
            <div class="changelog-item">
              <div class="changelog-header">
                <span class="version-tag">v1.0.0</span>
                <span class="release-date">2025-01-20</span>
              </div>
              <div class="changelog-content">
                <h5>新功能</h5>
                <ul>
                  <li>用户注册和登录系统</li>
                  <li>患者信息管理</li>
                  <li>骨密度数据录入和追踪</li>
                  <li>AI辅助诊断功能</li>
                  <li>数据采集模块</li>
                  <li>隐私条款和设置管理</li>
                </ul>
                <h5>优化</h5>
                <ul>
                  <li>界面响应式设计优化</li>
                  <li>数据加载性能提升</li>
                  <li>用户体验改进</li>
                </ul>
                <h5>修复</h5>
                <ul>
                  <li>修复登录状态保持问题</li>
                  <li>修复数据验证错误</li>
                  <li>修复界面显示异常</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4>开发团队</h4>
          <div class="team-info">
            <div class="team-item">
              <span class="team-label">产品经理:</span>
              <span class="team-value">张医生</span>
            </div>
            <div class="team-item">
              <span class="team-label">技术负责人:</span>
              <span class="team-value">李工程师</span>
            </div>
            <div class="team-item">
              <span class="team-label">前端开发:</span>
              <span class="team-value">王开发</span>
            </div>
            <div class="team-item">
              <span class="team-label">后端开发:</span>
              <span class="team-value">陈开发</span>
            </div>
            <div class="team-item">
              <span class="team-label">测试工程师:</span>
              <span class="team-value">刘测试</span>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4>联系方式</h4>
          <div class="contact-info">
            <div class="contact-item">
              <span class="contact-label">技术支持:</span>
              <span class="contact-value">support@osteoporosis-system.com</span>
            </div>
            <div class="contact-item">
              <span class="contact-label">产品反馈:</span>
              <span class="contact-value">feedback@osteoporosis-system.com</span>
            </div>
            <div class="contact-item">
              <span class="contact-label">紧急联系:</span>
              <span class="contact-value">400-123-4567</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

// 系统运行时间
const systemUptime = ref('')
const currentTime = ref('')
let timeInterval: NodeJS.Timeout | null = null

// 系统状态
const systemStatus = ref({
  type: 'success',
  text: '正常运行'
})

// 计算系统运行时间
const calculateUptime = () => {
  const startTime = new Date('2025-09-07T18:00:00Z') // 假设系统启动时间
  const now = new Date()
  const diff = now.getTime() - startTime.getTime()
  
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  
  systemUptime.value = `${days}天 ${hours}小时 ${minutes}分钟`
}

// 更新当前时间
const updateCurrentTime = () => {
  currentTime.value = new Date().toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

onMounted(() => {
  calculateUptime()
  updateCurrentTime()
  
  // 每秒更新一次时间
  timeInterval = setInterval(() => {
    updateCurrentTime()
    calculateUptime()
  }, 1000)
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})
</script>

<style scoped>
.version-page {
  height: 100%;
  padding: 20px;
  background: #f5f5f5;
}

.version-content {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  max-width: 800px;
  margin: 0 auto;
}

.page-title {
  text-align: center;
  color: #333;
  font-size: 1.8rem;
  margin-bottom: 10px;
  font-weight: 600;
}

.version-info {
  text-align: center;
  margin-bottom: 40px;
}

.version-number {
  color: #667eea;
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

.version-details {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.detail-section {
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 20px;
}

.detail-section:last-child {
  border-bottom: none;
}

.detail-section h4 {
  color: #333;
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0 0 15px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #667eea;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background: #f8f9fa;
  border-radius: 6px;
}

.label {
  font-weight: 600;
  color: #333;
}

.value {
  color: #666;
}

.tech-stack {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.tech-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #f0f8ff;
  border-radius: 4px;
  border-left: 3px solid #667eea;
}

.tech-label {
  font-weight: 600;
  color: #333;
}

.tech-value {
  color: #667eea;
  font-weight: 500;
}

.changelog {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.changelog-item {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  border-left: 4px solid #667eea;
}

.changelog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.version-tag {
  background: #667eea;
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
}

.release-date {
  color: #666;
  font-size: 0.9rem;
}

.changelog-content h5 {
  color: #333;
  font-size: 1rem;
  font-weight: 600;
  margin: 15px 0 8px 0;
}

.changelog-content h5:first-child {
  margin-top: 0;
}

.changelog-content ul {
  margin: 0 0 15px 0;
  padding-left: 20px;
}

.changelog-content li {
  color: #555;
  line-height: 1.6;
  margin-bottom: 4px;
}

.team-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.team-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 4px;
}

.team-label {
  font-weight: 600;
  color: #333;
}

.team-value {
  color: #666;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.contact-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background: #f8f9fa;
  border-radius: 6px;
}

.contact-label {
  font-weight: 600;
  color: #333;
}

.contact-value {
  color: #667eea;
  font-weight: 500;
}
</style> 