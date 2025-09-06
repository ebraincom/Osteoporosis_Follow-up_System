<template>
  <div class="followup-settings-page">
    <div class="settings-container">
      <!-- 页面标题 -->
      <div class="page-header">
        <h2>随访设置</h2>
        <p>配置随访相关的系统参数和规则</p>
      </div>

      <!-- 设置内容 -->
      <div class="settings-content">
        <!-- 基本设置 -->
        <div class="settings-section">
          <h3>基本设置</h3>
          <div class="settings-form">
            <div class="form-item">
              <label>默认随访间隔 (天)</label>
              <el-input-number 
                v-model="basicSettings.defaultInterval" 
                :min="1" 
                :max="365"
                controls-position="right"
              />
            </div>
            <div class="form-item">
              <label>随访提醒提前天数</label>
              <el-input-number 
                v-model="basicSettings.reminderDays" 
                :min="1" 
                :max="30"
                controls-position="right"
              />
            </div>
            <div class="form-item">
              <label>自动随访开关</label>
              <el-switch v-model="basicSettings.autoFollowup" />
            </div>
          </div>
        </div>

        <!-- 风险等级设置 -->
        <div class="settings-section">
          <h3>风险等级设置</h3>
          <div class="risk-settings">
            <div class="risk-level-item">
              <div class="risk-header">
                <el-tag type="success" size="large">低危</el-tag>
                <span class="risk-description">骨密度正常或轻度降低</span>
              </div>
              <div class="risk-config">
                <div class="config-item">
                  <label>随访间隔:</label>
                  <el-input-number 
                    v-model="riskSettings.low.interval" 
                    :min="30" 
                    :max="365"
                    controls-position="right"
                  />
                  <span class="unit">天</span>
                </div>
                <div class="config-item">
                  <label>提醒方式:</label>
                  <el-select v-model="riskSettings.low.reminderType" placeholder="选择提醒方式">
                    <el-option label="短信" value="sms" />
                    <el-option label="电话" value="phone" />
                    <el-option label="微信" value="wechat" />
                    <el-option label="邮件" value="email" />
                  </el-select>
                </div>
              </div>
            </div>

            <div class="risk-level-item">
              <div class="risk-header">
                <el-tag type="warning" size="large">中危</el-tag>
                <span class="risk-description">骨密度中度降低</span>
              </div>
              <div class="risk-config">
                <div class="config-item">
                  <label>随访间隔:</label>
                  <el-input-number 
                    v-model="riskSettings.medium.interval" 
                    :min="15" 
                    :max="180"
                    controls-position="right"
                  />
                  <span class="unit">天</span>
                </div>
                <div class="config-item">
                  <label>提醒方式:</label>
                  <el-select v-model="riskSettings.medium.reminderType" placeholder="选择提醒方式">
                    <el-option label="短信" value="sms" />
                    <el-option label="电话" value="phone" />
                    <el-option label="微信" value="wechat" />
                    <el-option label="邮件" value="email" />
                  </el-select>
                </div>
              </div>
            </div>

            <div class="risk-level-item">
              <div class="risk-header">
                <el-tag type="danger" size="large">高危</el-tag>
                <span class="risk-description">骨密度严重降低，有骨折风险</span>
              </div>
              <div class="risk-config">
                <div class="config-item">
                  <label>随访间隔:</label>
                  <el-input-number 
                    v-model="riskSettings.high.interval" 
                    :min="7" 
                    :max="90"
                    controls-position="right"
                  />
                  <span class="unit">天</span>
                </div>
                <div class="config-item">
                  <label>提醒方式:</label>
                  <el-select v-model="riskSettings.high.reminderType" placeholder="选择提醒方式">
                    <el-option label="短信" value="sms" />
                    <el-option label="电话" value="phone" />
                    <el-option label="微信" value="wechat" />
                    <el-option label="邮件" value="email" />
                  </el-select>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 通知设置 -->
        <div class="settings-section">
          <h3>通知设置</h3>
          <div class="notification-settings">
            <div class="notification-item">
              <div class="notification-info">
                <h4>随访提醒</h4>
                <p>在随访日期前发送提醒通知</p>
              </div>
              <el-switch v-model="notificationSettings.followupReminder" />
            </div>
            <div class="notification-item">
              <div class="notification-info">
                <h4>逾期提醒</h4>
                <p>随访逾期后发送提醒通知</p>
              </div>
              <el-switch v-model="notificationSettings.overdueReminder" />
            </div>
            <div class="notification-item">
              <div class="notification-info">
                <h4>异常提醒</h4>
                <p>检测到异常情况时发送提醒</p>
              </div>
              <el-switch v-model="notificationSettings.abnormalReminder" />
            </div>
            <div class="notification-item">
              <div class="notification-info">
                <h4>统计报告</h4>
                <p>定期发送随访统计报告</p>
              </div>
              <el-switch v-model="notificationSettings.statisticsReport" />
            </div>
          </div>
        </div>

        <!-- 模板设置 -->
        <div class="settings-section">
          <h3>消息模板设置</h3>
          <div class="template-settings">
            <div class="template-item">
              <label>随访提醒模板</label>
              <el-input
                v-model="templateSettings.followupReminder"
                type="textarea"
                :rows="3"
                placeholder="请输入随访提醒消息模板"
              />
              <div class="template-variables">
                <span class="variable-tip">可用变量: {{name}}, {{date}}, {{hospital}}</span>
              </div>
            </div>
            <div class="template-item">
              <label>逾期提醒模板</label>
              <el-input
                v-model="templateSettings.overdueReminder"
                type="textarea"
                :rows="3"
                placeholder="请输入逾期提醒消息模板"
              />
              <div class="template-variables">
                <span class="variable-tip">可用变量: {{name}}, {{date}}, {{hospital}}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="settings-actions">
          <el-button type="primary" @click="saveSettings" :loading="saving">
            保存设置
          </el-button>
          <el-button @click="resetSettings">
            重置默认
          </el-button>
          <el-button @click="testNotification">
            测试通知
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

// 响应式数据
const saving = ref(false)

// 基本设置
const basicSettings = reactive({
  defaultInterval: 90,
  reminderDays: 3,
  autoFollowup: true
})

// 风险等级设置
const riskSettings = reactive({
  low: {
    interval: 180,
    reminderType: 'sms'
  },
  medium: {
    interval: 90,
    reminderType: 'phone'
  },
  high: {
    interval: 30,
    reminderType: 'phone'
  }
})

// 通知设置
const notificationSettings = reactive({
  followupReminder: true,
  overdueReminder: true,
  abnormalReminder: true,
  statisticsReport: false
})

// 模板设置
const templateSettings = reactive({
  followupReminder: '尊敬的{{name}}，您预约的随访时间为{{date}}，请按时到{{hospital}}就诊。如有疑问，请及时联系。',
  overdueReminder: '尊敬的{{name}}，您的随访时间已逾期，请尽快到{{hospital}}就诊。如有疑问，请及时联系。'
})

// 方法
const saveSettings = async () => {
  saving.value = true
  
  try {
    // 模拟保存
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success('设置保存成功')
  } catch (error) {
    ElMessage.error('保存失败，请重试')
  } finally {
    saving.value = false
  }
}

const resetSettings = () => {
  // 重置为默认值
  basicSettings.defaultInterval = 90
  basicSettings.reminderDays = 3
  basicSettings.autoFollowup = true
  
  riskSettings.low.interval = 180
  riskSettings.low.reminderType = 'sms'
  riskSettings.medium.interval = 90
  riskSettings.medium.reminderType = 'phone'
  riskSettings.high.interval = 30
  riskSettings.high.reminderType = 'phone'
  
  notificationSettings.followupReminder = true
  notificationSettings.overdueReminder = true
  notificationSettings.abnormalReminder = true
  notificationSettings.statisticsReport = false
  
  templateSettings.followupReminder = '尊敬的{{name}}，您预约的随访时间为{{date}}，请按时到{{hospital}}就诊。如有疑问，请及时联系。'
  templateSettings.overdueReminder = '尊敬的{{name}}，您的随访时间已逾期，请尽快到{{hospital}}就诊。如有疑问，请及时联系。'
  
  ElMessage.success('设置已重置为默认值')
}

const testNotification = () => {
  ElMessage.success('测试通知已发送')
}
</script>

<style scoped>
.followup-settings-page {
  padding: 20px;
  height: 100%;
  background: #f5f7fa;
}

.settings-container {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 30px;
  text-align: center;
}

.page-header h2 {
  margin: 0 0 10px 0;
  font-size: 24px;
  font-weight: bold;
}

.page-header p {
  margin: 0;
  opacity: 0.9;
  font-size: 14px;
}

.settings-content {
  padding: 30px;
}

.settings-section {
  margin-bottom: 40px;
}

.settings-section h3 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 18px;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 10px;
}

/* 基本设置 */
.settings-form {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-item label {
  font-weight: bold;
  color: #333;
}

/* 风险等级设置 */
.risk-settings {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.risk-level-item {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 20px;
  background: #f8f9fa;
}

.risk-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.risk-description {
  color: #666;
  font-size: 14px;
}

.risk-config {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.config-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.config-item label {
  font-weight: bold;
  color: #333;
  min-width: 80px;
}

.unit {
  color: #666;
  font-size: 14px;
}

/* 通知设置 */
.notification-settings {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.notification-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  background: #f8f9fa;
}

.notification-info h4 {
  margin: 0 0 5px 0;
  color: #333;
  font-size: 16px;
}

.notification-info p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

/* 模板设置 */
.template-settings {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.template-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.template-item label {
  font-weight: bold;
  color: #333;
}

.template-variables {
  margin-top: 5px;
}

.variable-tip {
  color: #999;
  font-size: 12px;
  font-style: italic;
}

/* 操作按钮 */
.settings-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 40px;
  padding-top: 30px;
  border-top: 1px solid #e9ecef;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .settings-content {
    padding: 20px;
  }
  
  .settings-form {
    grid-template-columns: 1fr;
  }
  
  .risk-config {
    grid-template-columns: 1fr;
  }
  
  .notification-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .settings-actions {
    flex-direction: column;
    align-items: center;
  }
}
</style> 