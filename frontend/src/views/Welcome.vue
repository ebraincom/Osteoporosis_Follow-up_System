<template>
  <div class="welcome-page">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="logo">
        <el-icon class="logo-icon"><Monitor /></el-icon>
        骨质疏松症跟踪随访系统
      </div>
      <div class="nav-actions">
        <el-button type="primary" @click="$router.push('/login')" class="gradient-btn">
          登录
        </el-button>
        <el-button @click="$router.push('/register')" class="outline-btn">
          注册
        </el-button>
      </div>
    </nav>

    <!-- 主要内容 -->
    <div class="welcome-content">
      <div class="hero-section">
        <h1 class="hero-title fade-in-up">
          基于LLM大模型的骨质疏松症患者跟踪随访系统
        </h1>
        <p class="hero-subtitle fade-in-up">
          高效管理，科学干预，降低骨折风险
        </p>
        <div class="hero-actions fade-in-up">
          <el-button type="primary" size="large" @click="$router.push('/register')" class="gradient-btn">
            立即开始
          </el-button>
          <el-button size="large" @click="showFeatures = true" class="outline-btn">
            了解更多
          </el-button>
        </div>
      </div>

      <!-- 特性展示 -->
      <div class="features-section">
        <div class="features-grid">
          <div class="feature-card glass-card" v-for="feature in features" :key="feature.title">
            <el-icon class="feature-icon" :size="48">
              <component :is="feature.icon" />
            </el-icon>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 页脚 -->
    <footer class="footer">
      <p>北京智芸数据提供技术支持</p>
    </footer>

    <!-- 特性详情弹窗 -->
    <el-dialog v-model="showFeatures" title="系统特性" width="60%" class="features-dialog">
      <div class="features-detail">
        <el-tabs>
          <el-tab-pane label="智能管理" name="management">
            <div class="feature-detail-content">
              <h4>患者信息智能管理</h4>
              <ul>
                <li>骨密度指标实时监测</li>
                <li>骨折风险评估分析</li>
                <li>电子病历无缝对接</li>
                <li>报告智能解析</li>
              </ul>
            </div>
          </el-tab-pane>
          <el-tab-pane label="AI辅助" name="ai">
            <div class="feature-detail-content">
              <h4>AI智能辅助诊断</h4>
              <ul>
                <li>基于LLM的智能分析</li>
                <li>个性化治疗建议</li>
                <li>风险预警系统</li>
                <li>医学证据支持</li>
              </ul>
            </div>
          </el-tab-pane>
          <el-tab-pane label="随访管理" name="followup">
            <div class="feature-detail-content">
              <h4>科学随访管理</h4>
              <ul>
                <li>自动化随访计划</li>
                <li>智能提醒系统</li>
                <li>随访记录追踪</li>
                <li>治疗效果评估</li>
              </ul>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {
  Monitor,
  User,
  DataAnalysis,
  Bell,
  Document,
  TrendCharts
} from '@element-plus/icons-vue'

const showFeatures = ref(false)

const features = [
  {
    icon: 'User',
    title: '患者管理',
    description: '全面的患者信息管理，支持机构和个人用户'
  },
  {
    icon: 'DataAnalysis',
    title: '数据分析',
    description: '基于AI的智能数据分析，提供精准的医学建议'
  },
  {
    icon: 'Bell',
    title: '智能提醒',
    description: '自动化随访提醒，确保治疗计划执行'
  },
  {
    icon: 'Document',
    title: '报告管理',
    description: '支持多种医学报告格式，智能解析和存储'
  },
  {
    icon: 'TrendCharts',
    title: '趋势分析',
    description: '长期数据趋势分析，评估治疗效果'
  },
  {
    icon: 'Monitor',
    title: '实时监控',
    description: '实时监控患者状态，及时发现风险'
  }
]
</script>

<style scoped>
.welcome-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 40px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: bold;
  color: #667eea;
}

.logo-icon {
  margin-right: 10px;
  font-size: 2rem;
}

.nav-actions {
  display: flex;
  gap: 15px;
}

.outline-btn {
  border: 2px solid #667eea;
  color: #667eea;
  background: transparent;
}

.outline-btn:hover {
  background: #667eea;
  color: white;
}

.welcome-content {
  padding: 60px 40px;
}

.hero-section {
  text-align: center;
  color: white;
  margin-bottom: 80px;
}

.hero-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 20px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.hero-subtitle {
  font-size: 1.3rem;
  margin-bottom: 40px;
  opacity: 0.9;
}

.hero-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.features-section {
  margin-bottom: 60px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  padding: 40px 30px;
  text-align: center;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
}

.feature-icon {
  color: #667eea;
  margin-bottom: 20px;
}

.feature-card h3 {
  font-size: 1.3rem;
  margin-bottom: 15px;
  color: #333;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}

.footer {
  text-align: center;
  padding: 30px;
  color: rgba(255, 255, 255, 0.8);
  background: rgba(0, 0, 0, 0.1);
}

.features-dialog :deep(.el-dialog) {
  border-radius: 20px;
}

.feature-detail-content h4 {
  color: #667eea;
  margin-bottom: 15px;
  font-size: 1.2rem;
}

.feature-detail-content ul {
  list-style: none;
  padding: 0;
}

.feature-detail-content li {
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
  color: #666;
}

.feature-detail-content li:before {
  content: "✓";
  color: #667eea;
  font-weight: bold;
  margin-right: 10px;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .navbar {
    padding: 15px 20px;
  }
  
  .welcome-content {
    padding: 40px 20px;
  }
}
</style> 