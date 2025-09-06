<template>
  <div class="patient-detail-view">
    <div class="content-layout">
      <!-- 左侧：患者信息区域 -->
      <div class="left-panel">
        <div class="panel-section">
          <h3 class="section-title">患者基本信息</h3>
          <div class="patient-basic-info">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="患者姓名">{{ patient.name }}</el-descriptions-item>
              <el-descriptions-item label="年龄">{{ patient.age }}岁</el-descriptions-item>
              <el-descriptions-item label="性别">{{ patient.gender === 'male' ? '男' : '女' }}</el-descriptions-item>
              <el-descriptions-item label="联系电话">{{ patient.phone }}</el-descriptions-item>
              <el-descriptions-item label="身份证号">{{ patient.idCard }}</el-descriptions-item>
              <el-descriptions-item label="随访等级">
                <el-tag :type="getFollowUpLevelColor(patient.followUpLevel)">
                  {{ getFollowUpLevelText(patient.followUpLevel) }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="登记日期">{{ patient.registrationDate }}</el-descriptions-item>
              <el-descriptions-item label="最后就诊">{{ patient.lastVisitDate }}</el-descriptions-item>
              <el-descriptions-item label="下次随访">{{ patient.nextVisitDate }}</el-descriptions-item>
              <el-descriptions-item label="家庭住址" :span="2">{{ patient.address }}</el-descriptions-item>
              <el-descriptions-item label="紧急联系人">{{ patient.emergencyContact }}</el-descriptions-item>
              <el-descriptions-item label="紧急联系电话">{{ patient.emergencyPhone }}</el-descriptions-item>
            </el-descriptions>
          </div>
        </div>

        <div class="panel-section">
          <h3 class="section-title">重要指标展示</h3>
          <div class="indicators-display">
            <el-table :data="indicatorsData" border stripe>
              <el-table-column prop="indicator" label="指标" width="150" />
              <el-table-column prop="value" label="数值" width="100" />
              <el-table-column prop="unit" label="单位" width="80" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.status === '正常' ? 'success' : 'warning'">
                    {{ scope.row.status }}
                  </el-tag>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>

        <div class="panel-section">
          <h3 class="section-title">病例信息</h3>
          <div class="case-info">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="主诉">
                {{ patient.chiefComplaint }}
              </el-descriptions-item>
              <el-descriptions-item label="现病史">
                {{ patient.presentIllness }}
              </el-descriptions-item>
              <el-descriptions-item label="既往史">
                {{ patient.pastHistory }}
              </el-descriptions-item>
              <el-descriptions-item label="个人史">
                {{ patient.personalHistory }}
              </el-descriptions-item>
              <el-descriptions-item label="家族史">
                {{ patient.familyHistory }}
              </el-descriptions-item>
              <el-descriptions-item label="诊断">
                {{ patient.diagnosis }}
              </el-descriptions-item>
              <el-descriptions-item label="治疗方案">
                {{ patient.treatmentPlan }}
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </div>
      </div>

      <!-- 右侧：随访医嘱区域 -->
      <div class="right-panel">
        <div class="panel-section">
          <h3 class="section-title">随访医嘱</h3>
          <div class="followup-tabs">
            <el-tabs v-model="activeTab" type="card">
              <el-tab-pane label="随访医嘱" name="advice">
                <div class="advice-content">
                  <div class="latest-advice" v-if="latestFollowUpRecord">
                    <h4>最新医嘱 ({{ latestFollowUpRecord.date }})</h4>
                    <div class="advice-text">
                      <p><strong>症状评估：</strong>{{ latestFollowUpRecord.symptoms }}</p>
                      <p><strong>用药依从性：</strong>{{ latestFollowUpRecord.medicationAdherence }}</p>
                      <p><strong>运动情况：</strong>{{ latestFollowUpRecord.exercise }}</p>
                      <p><strong>不良反应：</strong>{{ latestFollowUpRecord.adverseReactions || '无' }}</p>
                      <p><strong>医生评估：</strong>{{ latestFollowUpRecord.assessment }}</p>
                      <p><strong>下一步计划：</strong>{{ latestFollowUpRecord.nextPlan }}</p>
                    </div>
                  </div>
                  
                  <div class="history-records" v-if="patient.followUpRecords.length > 0">
                    <h4>历史记录</h4>
                    <el-timeline>
                      <el-timeline-item
                        v-for="(record, index) in patient.followUpRecords"
                        :key="record.id"
                        :timestamp="record.date"
                        placement="top"
                      >
                        <div class="record-content">
                          <p><strong>医生：</strong>{{ record.doctor }}</p>
                          <p><strong>症状：</strong>{{ record.symptoms }}</p>
                          <p><strong>评估：</strong>{{ record.assessment }}</p>
                          <p><strong>计划：</strong>{{ record.nextPlan }}</p>
                        </div>
                      </el-timeline-item>
                    </el-timeline>
                  </div>
                </div>
              </el-tab-pane>
              
              <el-tab-pane label="重要日期" name="dates">
                <div class="important-dates">
                  <el-calendar v-model="currentDate">
                    <template #dateCell="{ data }">
                      <div class="calendar-cell">
                        <span>{{ data.day.split('-').slice(2).join('') }}</span>
                        <div v-if="data.day in importantDates" class="date-marker">
                          <el-tag size="small" type="warning">{{ importantDates[data.day] }}</el-tag>
                        </div>
                      </div>
                    </template>
                  </el-calendar>
                </div>
              </el-tab-pane>
              
              <el-tab-pane label="随访应答" name="response">
                <div class="followup-response">
                  <el-form :model="responseForm" label-width="120px">
                    <el-form-item label="症状改善情况">
                      <el-radio-group v-model="responseForm.symptomImprovement">
                        <el-radio label="明显改善">明显改善</el-radio>
                        <el-radio label="轻微改善">轻微改善</el-radio>
                        <el-radio label="无变化">无变化</el-radio>
                        <el-radio label="加重">加重</el-radio>
                      </el-radio-group>
                    </el-form-item>
                    
                    <el-form-item label="用药依从性">
                      <el-radio-group v-model="responseForm.medicationAdherence">
                        <el-radio label="完全按医嘱">完全按医嘱</el-radio>
                        <el-radio label="基本按医嘱">基本按医嘱</el-radio>
                        <el-radio label="偶尔漏服">偶尔漏服</el-radio>
                        <el-radio label="经常漏服">经常漏服</el-radio>
                      </el-radio-group>
                    </el-form-item>
                    
                    <el-form-item label="运动情况">
                      <el-input
                        v-model="responseForm.exercise"
                        type="textarea"
                        :rows="3"
                        placeholder="请描述运动情况..."
                      />
                    </el-form-item>
                    
                    <el-form-item label="不良反应">
                      <el-input
                        v-model="responseForm.adverseReactions"
                        type="textarea"
                        :rows="3"
                        placeholder="如有不良反应请详细描述..."
                      />
                    </el-form-item>
                    
                    <el-form-item>
                      <el-button type="primary" @click="submitResponse">提交随访应答</el-button>
                    </el-form-item>
                  </el-form>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>
        </div>
      </div>
    </div>

    <!-- 关闭按钮 -->
    <div v-if="showClose" class="close-button">
      <el-button @click="$emit('close')">关闭</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import type { PatientDetailInfo } from '@/types/patient'
import { FollowUpLevelText, FollowUpLevelColor } from '@/types/patient'

interface Props {
  patient: PatientDetailInfo
  showClose?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showClose: true
})

const emit = defineEmits<{
  close: []
}>()

const activeTab = ref('advice')
const currentDate = ref(new Date())

// 计算属性：重要指标数据
const indicatorsData = computed(() => [
  { indicator: '身高', value: patient.height.toString(), unit: 'cm', status: '正常' },
  { indicator: '体重', value: patient.weight.toString(), unit: 'kg', status: '正常' },
  { indicator: 'BMI', value: patient.bmi.toFixed(1), unit: 'kg/m²', status: '正常' },
  { indicator: '腰椎T值', value: patient.lumbarTScore.toString(), unit: '', status: patient.lumbarTScore < -2.5 ? '异常' : '正常' },
  { indicator: '股骨颈T值', value: patient.femoralNeckTScore.toString(), unit: '', status: patient.femoralNeckTScore < -2.5 ? '异常' : '正常' },
  { indicator: '血钙', value: patient.bloodCalcium.toString(), unit: 'mmol/L', status: patient.bloodCalcium < 2.2 ? '偏低' : '正常' },
  { indicator: '血磷', value: patient.bloodPhosphorus.toString(), unit: 'mmol/L', status: '正常' },
  { indicator: '25-羟维生素D', value: patient.vitaminD.toString(), unit: 'ng/ml', status: patient.vitaminD < 20 ? '不足' : '正常' },
  { indicator: '甲状旁腺激素', value: patient.parathyroidHormone.toString(), unit: 'pg/ml', status: '正常' }
])

// 计算属性：最新随访记录
const latestFollowUpRecord = computed(() => {
  if (patient.followUpRecords.length === 0) return null
  return patient.followUpRecords[0] // 假设按日期排序，最新的在前面
})

// 重要日期
const importantDates = computed(() => ({
  [patient.nextVisitDate]: '下次随访',
  [patient.lastVisitDate]: '最后就诊'
}))

// 随访应答表单
const responseForm = ref({
  symptomImprovement: '',
  medicationAdherence: '',
  exercise: '',
  adverseReactions: ''
})

// 获取随访等级文本
const getFollowUpLevelText = (level: string) => {
  return FollowUpLevelText[level as keyof typeof FollowUpLevelText] || level
}

// 获取随访等级颜色
const getFollowUpLevelColor = (level: string) => {
  return FollowUpLevelColor[level as keyof typeof FollowUpLevelColor] || 'info'
}

// 提交随访应答
const submitResponse = () => {
  ElMessage.success('随访应答提交成功！')
  // 这里可以添加提交到后端的逻辑
}
</script>

<style scoped>
.patient-detail-view {
  height: 100%;
  position: relative;
}

.content-layout {
  display: flex;
  gap: 20px;
  height: 100%;
}

.left-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
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
}

.section-title {
  margin: 0 0 20px 0;
  font-size: 1.2rem;
  color: #333;
  font-weight: 600;
  border-bottom: 2px solid #667eea;
  padding-bottom: 8px;
}

.patient-basic-info,
.indicators-display,
.case-info {
  margin-top: 15px;
}

.followup-tabs {
  height: 100%;
}

.advice-content {
  max-height: 600px;
  overflow-y: auto;
}

.latest-advice {
  margin-bottom: 30px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #667eea;
}

.latest-advice h4 {
  margin: 0 0 15px 0;
  color: #667eea;
  font-weight: 600;
}

.advice-text p {
  margin: 8px 0;
  line-height: 1.6;
}

.history-records h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-weight: 600;
}

.record-content {
  padding: 10px;
  background: #f8f9fa;
  border-radius: 4px;
}

.record-content p {
  margin: 5px 0;
  line-height: 1.5;
}

.important-dates {
  padding: 15px;
}

.calendar-cell {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}

.date-marker {
  position: absolute;
  bottom: 2px;
  left: 50%;
  transform: translateX(-50%);
}

.followup-response {
  padding: 15px;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-radio-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.el-radio {
  margin-right: 0;
  margin-bottom: 8px;
}

.close-button {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 10;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-layout {
    flex-direction: column;
  }
  
  .left-panel,
  .right-panel {
    flex: none;
  }
}
</style> 