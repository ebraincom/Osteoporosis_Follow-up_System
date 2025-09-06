<template>
  <div class="help-page">
    <div class="help-content">
      <h2 class="page-title">帮助中心</h2>
      
      <!-- 快速导航 -->
      <div class="quick-nav">
        <h3>快速导航</h3>
        <div class="nav-grid">
          <div class="nav-item" @click="scrollToSection('getting-started')">
            <el-icon><Document /></el-icon>
            <span>快速开始</span>
          </div>
          <div class="nav-item" @click="scrollToSection('data-collection')">
            <el-icon><Check /></el-icon>
            <span>数据采集</span>
          </div>
          <div class="nav-item" @click="scrollToSection('ai-assistant')">
            <el-icon><ChatDotRound /></el-icon>
            <span>AI辅助</span>
          </div>
          <div class="nav-item" @click="scrollToSection('settings')">
            <el-icon><UserFilled /></el-icon>
            <span>系统设置</span>
          </div>
          <div class="nav-item" @click="scrollToSection('faq')">
            <el-icon><QuestionFilled /></el-icon>
            <span>常见问题</span>
          </div>
          <div class="nav-item" @click="scrollToSection('contact')">
            <el-icon><Connection /></el-icon>
            <span>联系我们</span>
          </div>
        </div>
      </div>

      <!-- 帮助内容 -->
      <div class="help-sections">
        <!-- 快速开始 -->
        <div id="getting-started" class="help-section">
          <h3>快速开始</h3>
          <div class="section-content">
            <div class="step-item">
              <div class="step-number">1</div>
              <div class="step-content">
                <h4>注册账号</h4>
                <p>首次使用需要注册账号，选择用户类型（机构用户或个人用户），填写基本信息。</p>
              </div>
            </div>
            <div class="step-item">
              <div class="step-number">2</div>
              <div class="step-content">
                <h4>登录系统</h4>
                <p>使用注册的用户名和密码登录系统，进入主界面。</p>
              </div>
            </div>
            <div class="step-item">
              <div class="step-number">3</div>
              <div class="step-content">
                <h4>完善个人信息</h4>
                <p>在"我的设置"中完善个人信息，包括基本信息、联系方式等。</p>
              </div>
            </div>
            <div class="step-item">
              <div class="step-number">4</div>
              <div class="step-content">
                <h4>开始使用</h4>
                <p>根据需求选择相应功能模块，开始使用系统的各项功能。</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 常见问题 -->
        <div id="faq" class="help-section">
          <h3>常见问题</h3>
          <div class="section-content">
            <div class="faq-item">
              <h4>如何修改密码？</h4>
              <p>进入"我的设置" → "个人信息"，点击密码字段旁的"修改"按钮，输入新密码并确认。</p>
            </div>
            <div class="faq-item">
              <h4>忘记密码怎么办？</h4>
              <p>在登录页面点击"忘记密码"，通过注册邮箱或手机号进行密码重置。</p>
            </div>
            <div class="faq-item">
              <h4>如何导出数据？</h4>
              <p>在相应功能页面点击"导出"按钮，选择导出格式（Excel、PDF等）即可下载。</p>
            </div>
            <div class="faq-item">
              <h4>系统支持哪些浏览器？</h4>
              <p>建议使用Chrome、Firefox、Safari、Edge等现代浏览器，版本要求IE11以上。</p>
            </div>
          </div>
        </div>

        <!-- 联系我们 -->
        <div id="contact" class="help-section">
          <h3>联系我们</h3>
          <div class="section-content">
            <div class="contact-grid">
              <div class="contact-item">
                <h4>技术支持</h4>
                <p>邮箱：support@osteoporosis-system.com</p>
                <p>电话：400-123-4567</p>
                <p>工作时间：周一至周五 9:00-18:00</p>
              </div>
              <div class="contact-item">
                <h4>产品反馈</h4>
                <p>邮箱：feedback@osteoporosis-system.com</p>
                <p>在线反馈：系统内"意见反馈"功能</p>
                <p>响应时间：24小时内</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Document, Check, ChatDotRound, UserFilled, QuestionFilled, Connection } from '@element-plus/icons-vue'

const scrollToSection = (sectionId: string) => {
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<style scoped>
.help-page {
  height: 100%;
  padding: 20px;
  background: #f5f5f5;
  overflow-y: auto;
}

.help-content {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  max-width: 1000px;
  margin: 0 auto;
}

.page-title {
  text-align: center;
  color: #333;
  font-size: 1.8rem;
  margin-bottom: 30px;
  font-weight: 600;
}

.quick-nav {
  margin-bottom: 40px;
}

.quick-nav h3 {
  color: #333;
  font-size: 1.3rem;
  margin-bottom: 20px;
  font-weight: 600;
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.nav-item:hover {
  background: #e3f2fd;
  border-color: #667eea;
  transform: translateY(-2px);
}

.nav-item .el-icon {
  font-size: 2rem;
  color: #667eea;
  margin-bottom: 10px;
}

.nav-item span {
  color: #333;
  font-weight: 500;
}

.help-sections {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.help-section {
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 30px;
}

.help-section:last-child {
  border-bottom: none;
}

.help-section h3 {
  color: #333;
  font-size: 1.4rem;
  margin-bottom: 20px;
  font-weight: 600;
  padding-bottom: 10px;
  border-bottom: 2px solid #667eea;
}

.section-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.step-number {
  background: #667eea;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  flex-shrink: 0;
}

.step-content h4 {
  color: #333;
  font-size: 1.1rem;
  margin: 0 0 8px 0;
  font-weight: 600;
}

.step-content p {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.faq-item {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 15px;
}

.faq-item h4 {
  color: #333;
  font-size: 1.1rem;
  margin: 0 0 10px 0;
  font-weight: 600;
}

.faq-item p {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.contact-item {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  text-align: center;
}

.contact-item h4 {
  color: #333;
  font-size: 1.1rem;
  margin: 0 0 15px 0;
  font-weight: 600;
}

.contact-item p {
  color: #666;
  line-height: 1.6;
  margin: 0 0 8px 0;
}

.contact-item p:last-child {
  margin-bottom: 0;
}
</style> 