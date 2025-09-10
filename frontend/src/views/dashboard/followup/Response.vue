<template>
  <div class="followup-response">

    <!-- 顶部概览卡片 -->
    <div class="overview-cards">
      <div class="overview-card low-risk">
        <div class="card-content">
          <div class="card-title">低危</div>
          <div class="card-subtitle">患者人数</div>
          <div class="card-number">{{ statistics.low }}人</div>
        </div>
      </div>
      <div class="overview-card medium-risk">
        <div class="card-content">
          <div class="card-title">中危</div>
          <div class="card-subtitle">患者人数</div>
          <div class="card-number">{{ statistics.medium }}人</div>
        </div>
      </div>
      <div class="overview-card high-risk">
        <div class="card-content">
          <div class="card-title">高危</div>
          <div class="card-subtitle">患者人数</div>
          <div class="card-number">{{ statistics.high }}人</div>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧患者列表 -->
      <div class="left-panel">
        <!-- 患者列表表格 -->
        <div class="table-section">
          <div class="table-header">
            <h3>患者列表</h3>
            <el-button type="primary" @click="loadPatients" :loading="loading">
              刷新数据
            </el-button>
          </div>
          <el-table
            :data="patients"
            style="width: 100%"
            @row-click="handlePatientClick"
            :row-class-name="getRowClassName"
            highlight-current-row
            v-loading="loading"
          >
            <el-table-column prop="patient_id" label="档案编号" width="100" show-overflow-tooltip />
            <el-table-column prop="name" label="患者姓名" width="100" />
            <el-table-column prop="age" label="年龄" width="60" align="center" />
            <el-table-column prop="gender" label="性别" width="60" align="center">
              <template #default="{ row }">
                {{ row.gender === 'male' ? '男' : '女' }}
              </template>
            </el-table-column>
            <el-table-column label="风险等级" width="80" align="center">
              <template #default="{ row }">
                <el-tag 
                  :type="getLevelType(row.risk_level)"
                  size="small"
                >
                  {{ getLevelText(row.risk_level) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="phone" label="联系电话" width="120" show-overflow-tooltip />
            <el-table-column label="操作" width="180">
              <template #default="{ row }">
                <div style="display: flex; gap: 4px; flex-wrap: nowrap;">
                  <el-button type="primary" size="small" @click.stop="viewDetails(row)">
                    查看回复
                  </el-button>
                  <el-button type="success" size="small" @click.stop="createFollowupRecord(row)">
                    创建随访
                  </el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>

      <!-- 右侧患者应答详情 -->
      <div class="right-panel">
        <div v-if="selectedPatient" class="response-detail">
          <div class="detail-header">
            <h3>随访应答-{{ selectedPatient.name }}</h3>
            <el-button type="primary" @click="loadPatientResponses(selectedPatient.id)" :loading="responseLoading">
              刷新回复
            </el-button>
          </div>

          <!-- 患者基本信息 -->
          <div class="patient-info">
            <div class="info-grid">
              <div class="info-item">
                <span class="label">姓名:</span>
                <span class="value">{{ selectedPatient.name }}</span>
              </div>
              <div class="info-item">
                <span class="label">性别:</span>
                <span class="value">{{ selectedPatient.gender === 'male' ? '男' : '女' }}</span>
              </div>
              <div class="info-item">
                <span class="label">年龄:</span>
                <span class="value">{{ selectedPatient.age }}岁</span>
              </div>
              <div class="info-item">
                <span class="label">联系电话:</span>
                <span class="value">{{ selectedPatient.phone }}</span>
              </div>
            </div>
            <div class="risk-level">
              <el-tag :type="getLevelType(selectedPatient.risk_level)" size="small">
                {{ getLevelText(selectedPatient.risk_level) }}
              </el-tag>
            </div>
          </div>

          <!-- 关键指标 -->
          <div class="key-indicators">
            <h4>关键指标 (骨密度)</h4>
            <div class="indicators-content">
              <div class="indicator-item">
                <span class="label">T值:</span>
                <span class="value">{{ selectedPatient.t_score || '未检测' }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">Z值:</span>
                <span class="value">{{ selectedPatient.z_score || '未检测' }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">身高:</span>
                <span class="value">{{ selectedPatient.height ? selectedPatient.height + 'cm' : '未填写' }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">体重:</span>
                <span class="value">{{ selectedPatient.weight ? selectedPatient.weight + 'kg' : '未填写' }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">BMI:</span>
                <span class="value">{{ selectedPatient.bmi || '未计算' }}</span>
              </div>
            </div>
          </div>

          <!-- 随访应答列表 -->
          <div class="response-section">
            <h4>随访应答记录 ({{ patientResponses.length }}条)</h4>
            <div v-if="patientResponses.length === 0" class="empty-responses">
              <el-empty description="暂无随访应答记录" />
            </div>
            <div v-else class="responses-table">
              <el-table :data="patientResponses" style="width: 100%" v-loading="responseLoading" stripe>
                <el-table-column prop="id" label="应答ID" width="70" align="center" />
                <el-table-column label="回复时间" width="140" align="center">
                  <template #default="{ row }">
                    {{ formatDate(row.response_time) }}
                  </template>
                </el-table-column>
                <el-table-column label="状态" width="80" align="center">
                  <template #default="{ row }">
                    <el-tag :type="row.is_completed ? 'success' : 'warning'" size="small">
                      {{ row.is_completed ? '已完成' : '未完成' }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="overall_feeling" label="总体感受" width="90" show-overflow-tooltip />
                <el-table-column prop="improvement_level" label="改善程度" width="90" show-overflow-tooltip />
                <el-table-column label="操作" width="90" align="center">
                  <template #default="{ row }">
                    <el-button type="primary" size="small" @click="viewResponseDetail(row)">
                      查看详情
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>
        </div>

        <div v-else class="no-patient-selected">
          <el-empty description="请选择患者查看应答详情" />
        </div>
      </div>
    </div>

    <!-- 随访应答详情弹窗 -->
    <el-dialog
      v-model="responseDetailVisible"
      title="随访应答详情"
      width="800px"
      :before-close="handleCloseResponseDetail"
    >
      <div v-if="selectedResponse" class="response-detail">
        <div class="detail-header">
          <div class="detail-info">
            <span class="label">应答ID:</span>
            <span class="value">{{ selectedResponse.id }}</span>
          </div>
          <div class="detail-info">
            <span class="label">回复时间:</span>
            <span class="value">{{ formatDate(selectedResponse.response_time) }}</span>
          </div>
          <div class="detail-info">
            <span class="label">状态:</span>
            <el-tag :type="selectedResponse.is_completed ? 'success' : 'warning'" size="small">
              {{ selectedResponse.is_completed ? '已完成' : '未完成' }}
            </el-tag>
          </div>
        </div>
        
        <div class="detail-content">
          <div class="detail-section">
            <h5>基本信息</h5>
            <div class="detail-grid">
              <div class="detail-field">
                <span class="label">总体感受:</span>
                <span class="value">{{ selectedResponse.overall_feeling || '未填写' }}</span>
              </div>
              <div class="detail-field">
                <span class="label">改善程度:</span>
                <span class="value">{{ selectedResponse.improvement_level || '未填写' }}</span>
              </div>
              <div class="detail-field">
                <span class="label">用药依从性:</span>
                <span class="value">{{ selectedResponse.medication_adherence || '未填写' }}</span>
              </div>
              <div class="detail-field">
                <span class="label">运动量:</span>
                <span class="value">{{ selectedResponse.exercise_volume || '未填写' }}</span>
              </div>
              <div class="detail-field">
                <span class="label">饮食调整:</span>
                <span class="value">{{ selectedResponse.diet_adjustment || '未填写' }}</span>
              </div>
              <div class="detail-field">
                <span class="label">疼痛程度:</span>
                <span class="value">{{ selectedResponse.pain_level ? selectedResponse.pain_level + '分' : '未填写' }}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h5>生活状态</h5>
            <div class="detail-grid">
              <div class="detail-field">
                <span class="label">睡眠质量:</span>
                <span class="value">{{ selectedResponse.sleep_quality || '未填写' }}</span>
              </div>
              <div class="detail-field">
                <span class="label">日常活动:</span>
                <span class="value">{{ selectedResponse.daily_activity || '未填写' }}</span>
              </div>
              <div class="detail-field">
                <span class="label">情绪状态:</span>
                <span class="value">{{ selectedResponse.mood_status || '未填写' }}</span>
              </div>
              <div class="detail-field">
                <span class="label">社交活动:</span>
                <span class="value">{{ selectedResponse.social_activity || '未填写' }}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h5>其他信息</h5>
            <div class="detail-grid">
              <div class="detail-field">
                <span class="label">副作用:</span>
                <span class="value">{{ selectedResponse.side_effects || '无' }}</span>
              </div>
              <div class="detail-field">
                <span class="label">担忧:</span>
                <span class="value">{{ selectedResponse.concerns || '无' }}</span>
              </div>
              <div class="detail-field">
                <span class="label">建议:</span>
                <span class="value">{{ selectedResponse.suggestions || '无' }}</span>
              </div>
              <div class="detail-field full-width">
                <span class="label">其他信息:</span>
                <span class="value">{{ selectedResponse.additional_info || '无' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="responseDetailVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, h } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { patientApi } from '@/api/patient'
import { followupResponseApi } from '@/api/followupResponse'
import { followupApi } from '@/api/followup'
import { useUserStore } from '@/stores/user'
import axios from 'axios'

// 用户状态
const userStore = useUserStore()

// 响应式数据
const selectedPatient = ref<any>(null)
const patients = ref<any[]>([])
const patientResponses = ref<any[]>([])
const loading = ref(false)
const responseLoading = ref(false)

// 详情弹窗相关
const responseDetailVisible = ref(false)
const selectedResponse = ref<any>(null)

// 统计数据
const statistics = ref({
  low: 0,
  medium: 0,
  high: 0
})

// 方法

const loadPatients = async () => {
  try {
    loading.value = true
    const response = await patientApi.getPatients()
    patients.value = response?.patients || []
    
    // 计算统计数据
    statistics.value = {
      low: patients.value.filter(p => p.risk_level === 'low').length,
      medium: patients.value.filter(p => p.risk_level === 'medium').length,
      high: patients.value.filter(p => p.risk_level === 'high').length
    }
    
    // 默认选中第一个患者
    if (patients.value.length > 0) {
      selectedPatient.value = patients.value[0]
      await loadPatientResponses(patients.value[0].id)
    }
  } catch (error) {
    console.error('加载患者列表失败:', error)
    ElMessage.error('加载患者列表失败')
  } finally {
    loading.value = false
  }
}

const loadPatientResponses = async (patientId: number) => {
  try {
    responseLoading.value = true
    const response = await followupResponseApi.getPatientResponses(patientId)
    console.log('患者应答API响应:', response)
    patientResponses.value = response || []
  } catch (error) {
    console.error('加载患者应答失败:', error)
    ElMessage.error('加载患者应答失败')
  } finally {
    responseLoading.value = false
  }
}

const handlePatientClick = async (row: any) => {
  selectedPatient.value = row
  await loadPatientResponses(row.id)
  ElMessage.info(`已选择患者: ${row.name}`)
}

const viewDetails = async (patient: any) => {
  selectedPatient.value = patient
  await loadPatientResponses(patient.id)
  ElMessage.info(`查看患者: ${patient.name} 的应答详情`)
}

const createFollowupRecord = async (patient: any) => {
  try {
    // 创建随访表单数据
    const formData = ref({
      patient_id: patient.id,
      time: new Date().toISOString().slice(0, 16), // 格式化为 datetime-local 格式
      method: '电话随访',
      location: '医院',
      details: '',
      patient_status: '待回复',
      recommendations: ''
    })

    // 使用 ElMessageBox 创建自定义表单
    const result = await ElMessageBox({
      title: `为患者 ${patient.name} 创建随访记录`,
      message: h('div', { class: 'patient-detail-form' }, [
        // 患者基本信息
        h('div', { class: 'patient-info-section' }, [
          h('h3', { class: 'section-title' }, '患者基本信息'),
          h('div', { class: 'info-grid' }, [
            h('div', { class: 'info-item' }, [
              h('span', { class: 'info-label' }, '姓名:'),
              h('span', { class: 'info-value' }, patient.name)
            ]),
            h('div', { class: 'info-item' }, [
              h('span', { class: 'info-label' }, '性别:'),
              h('span', { class: 'info-value' }, patient.gender === 'male' ? '男' : '女')
            ]),
            h('div', { class: 'info-item' }, [
              h('span', { class: 'info-label' }, '年龄:'),
              h('span', { class: 'info-value' }, `${patient.age}岁`)
            ]),
            h('div', { class: 'info-item' }, [
              h('span', { class: 'info-label' }, '联系电话:'),
              h('span', { class: 'info-value' }, patient.phone)
            ]),
            h('div', { class: 'info-item' }, [
              h('span', { class: 'info-label' }, '风险等级:'),
              h('span', { class: 'info-value' }, [
                h('span', { 
                  class: `risk-tag ${getLevelType(patient.risk_level)}` 
                }, getLevelText(patient.risk_level))
              ])
            ]),
            h('div', { class: 'info-item' }, [
              h('span', { class: 'info-label' }, '档案编号:'),
              h('span', { class: 'info-value' }, patient.patient_id)
            ])
          ])
        ]),
        
        // 随访信息
        h('div', { class: 'followup-info-section' }, [
          h('h3', { class: 'section-title' }, '随访信息'),
          h('div', { class: 'info-grid' }, [
            h('div', { class: 'info-item' }, [
              h('span', { class: 'info-label' }, '随访时间 *:'),
              h('input', {
                type: 'datetime-local',
                value: formData.value.time,
                onInput: (e: any) => formData.value.time = e.target.value,
                class: 'info-input'
              })
            ]),
            h('div', { class: 'info-item' }, [
              h('span', { class: 'info-label' }, '随访方式:'),
              h('select', {
                value: formData.value.method,
                onChange: (e: any) => formData.value.method = e.target.value,
                class: 'info-select'
              }, [
                h('option', { value: '电话随访' }, '电话随访'),
                h('option', { value: '门诊随访' }, '门诊随访'),
                h('option', { value: '视频随访' }, '视频随访'),
                h('option', { value: '上门随访' }, '上门随访')
              ])
            ]),
            h('div', { class: 'info-item' }, [
              h('span', { class: 'info-label' }, '随访地点:'),
              h('input', {
                type: 'text',
                value: formData.value.location,
                onInput: (e: any) => formData.value.location = e.target.value,
                placeholder: '请输入随访地点',
                class: 'info-input'
              })
            ]),
            h('div', { class: 'info-item' }, [
              h('span', { class: 'info-label' }, '患者状态:'),
              h('select', {
                value: formData.value.patient_status,
                onChange: (e: any) => formData.value.patient_status = e.target.value,
                class: 'info-select'
              }, [
                h('option', { value: '待回复' }, '待回复'),
                h('option', { value: '已回复' }, '已回复'),
                h('option', { value: '失联' }, '失联'),
                h('option', { value: '拒绝随访' }, '拒绝随访')
              ])
            ])
          ])
        ]),
        
        // 随访内容
        h('div', { class: 'followup-content-section' }, [
          h('h3', { class: 'section-title' }, '随访内容'),
          h('div', { class: 'content-item' }, [
            h('span', { class: 'content-label' }, '随访详情 *:'),
            h('textarea', {
              value: formData.value.details,
              onInput: (e: any) => formData.value.details = e.target.value,
              placeholder: '请详细描述随访内容，包括患者主诉、检查结果、用药情况、症状变化等...',
              rows: 4,
              class: 'content-textarea'
            })
          ]),
          h('div', { class: 'content-item' }, [
            h('span', { class: 'content-label' }, '医生建议:'),
            h('textarea', {
              value: formData.value.recommendations,
              onInput: (e: any) => formData.value.recommendations = e.target.value,
              placeholder: '请输入医生的建议和指导，包括用药调整、复查安排、注意事项等...',
              rows: 3,
              class: 'content-textarea'
            })
          ])
        ])
      ]),
      showCancelButton: true,
      confirmButtonText: '创建随访记录',
      cancelButtonText: '取消',
      customClass: 'patient-detail-dialog',
      beforeClose: (action: string, instance: any, done: any) => {
        if (action === 'confirm') {
          // 验证必填字段
          if (!formData.value.details.trim()) {
            ElMessage.error('请填写随访内容')
            return
          }
          if (!formData.value.time) {
            ElMessage.error('请选择随访时间')
            return
          }
          
          // 创建随访数据
          const followupData = {
            patient_id: formData.value.patient_id,
            time: new Date(formData.value.time).toISOString(),
            method: formData.value.method,
            location: formData.value.location,
            details: formData.value.details,
            patient_status: formData.value.patient_status,
            recommendations: formData.value.recommendations
          }
          
          // 调用API创建随访
          followupApi.createFollowup(followupData).then(() => {
            ElMessage.success('随访记录创建成功')
            // 重新加载患者应答
            loadPatientResponses(patient.id)
            done()
          }).catch((error) => {
            console.error('创建随访记录失败:', error)
            ElMessage.error('创建随访记录失败')
          })
        } else {
          done()
        }
      }
    })
  } catch (error) {
    if (error !== 'cancel') {
      console.error('创建随访记录失败:', error)
      ElMessage.error('创建随访记录失败')
    }
  }
}

const getLevelType = (level: string) => {
  switch (level) {
    case 'low': return 'success'
    case 'medium': return 'warning'
    case 'high': return 'danger'
    default: return 'info'
  }
}

const getLevelText = (level: string) => {
  switch (level) {
    case 'low': return '低危'
    case 'medium': return '中危'
    case 'high': return '高危'
    default: return '未知'
  }
}

const getRowClassName = ({ row }: { row: any }) => {
  return selectedPatient.value?.id === row.id ? 'selected-row' : ''
}

// 查看随访应答详情
const viewResponseDetail = (response: any) => {
  selectedResponse.value = response
  responseDetailVisible.value = true
}

// 关闭详情弹窗
const handleCloseResponseDetail = () => {
  responseDetailVisible.value = false
  selectedResponse.value = null
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadPatients()
})
</script>

<style scoped>
.followup-response {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 概览卡片样式 */
.overview-cards {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.overview-card {
  flex: 1;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.overview-card:hover {
  transform: translateY(-2px);
}

.overview-card.low-risk {
  background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
  border-left: 4px solid #28a745;
}

.overview-card.medium-risk {
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
  border-left: 4px solid #ffc107;
}

.overview-card.high-risk {
  background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
  border-left: 4px solid #dc3545;
}

.card-content {
  text-align: center;
}

.card-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 8px;
}

.card-subtitle {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.card-number {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

/* 主要内容区域 */
.main-content {
  flex: 1;
  display: flex;
  gap: 20px;
  min-height: 0;
}

/* 左侧面板 */
.left-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 500px;
}

.table-section {
  flex: 1;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* 右侧面板 */
.right-panel {
  flex: 1;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: auto;
  min-width: 500px;
}

.response-detail {
  padding: 20px;
}

.detail-header {
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 15px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-header h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
}

/* 患者基本信息 */
.patient-info {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 20px;
  position: relative;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.label {
  font-weight: bold;
  color: #333;
  min-width: 60px;
  white-space: nowrap;
}

.value {
  color: #666;
  flex: 1;
}

.risk-level {
  position: absolute;
  top: 15px;
  right: 15px;
}

/* 关键指标 */
.key-indicators {
  border: 1px solid #e9ecef;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 20px;
}

.key-indicators h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 16px;
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 8px;
}

.indicators-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.indicator-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.indicator-item.full-width {
  flex-direction: column;
  gap: 5px;
}

.indicator-item .label {
  font-weight: bold;
  color: #333;
  min-width: 80px;
  white-space: nowrap;
}

.indicator-item .value {
  color: #666;
  flex: 1;
}

/* 回访应答 */
.response-section {
  border: 1px solid #e9ecef;
  border-radius: 6px;
  padding: 15px;
}

.response-section h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 16px;
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 8px;
}

.response-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.response-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 4px;
}

.response-item .label {
  font-weight: bold;
  color: #333;
  min-width: 80px;
  white-space: nowrap;
}

.response-item .value {
  color: #666;
  flex: 1;
  line-height: 1.5;
}

.no-patient-selected {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
}

/* 表格样式 */
.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 0 10px;
}

.table-header h3 {
  margin: 0;
  color: #333;
}

:deep(.el-table) {
  border-radius: 8px;
}

:deep(.el-table th) {
  background-color: #f8f9fa;
  color: #333;
  font-weight: bold;
}

:deep(.selected-row) {
  background-color: #e3f2fd !important;
}

:deep(.el-table__row:hover) {
  background-color: #f5f5f5;
}

/* 应答列表样式 */
.responses-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.response-item {
  border: 1px solid #e9ecef;
  border-radius: 6px;
  padding: 15px;
  background: #f8f9fa;
}

.response-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e9ecef;
}

.response-time {
  font-weight: bold;
  color: #333;
}

.response-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.response-field {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.response-field .label {
  font-weight: bold;
  color: #333;
  min-width: 80px;
  white-space: nowrap;
}

.response-field .value {
  color: #666;
  flex: 1;
  line-height: 1.5;
}

.empty-responses {
  text-align: center;
  padding: 40px 0;
}

/* 患者详情表单样式 */
.patient-detail-form {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 0;
}

.patient-info-section,
.followup-info-section,
.followup-content-section {
  margin-bottom: 24px;
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  overflow: hidden;
}

.section-title {
  background-color: #f8f9fa;
  margin: 0;
  padding: 12px 16px;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  border-bottom: 1px solid #e1e5e9;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  padding: 0;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  min-height: 48px;
}

.info-item:nth-child(odd) {
  border-right: 1px solid #f0f0f0;
}

.info-item:last-child,
.info-item:nth-last-child(2) {
  border-bottom: none;
}

.info-label {
  font-weight: 500;
  color: #666;
  min-width: 80px;
  margin-right: 12px;
  font-size: 14px;
}

.info-value {
  color: #333;
  font-size: 14px;
  flex: 1;
}

.risk-tag {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.risk-tag.success {
  background-color: #f0f9ff;
  color: #0369a1;
  border: 1px solid #bae6fd;
}

.risk-tag.warning {
  background-color: #fffbeb;
  color: #d97706;
  border: 1px solid #fed7aa;
}

.risk-tag.danger {
  background-color: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.info-input,
.info-select {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 14px;
  background-color: #fff;
  transition: border-color 0.2s;
}

.info-input:focus,
.info-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

.info-select {
  cursor: pointer;
}

.content-item {
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.content-item:last-child {
  border-bottom: none;
}

.content-label {
  display: block;
  font-weight: 500;
  color: #666;
  margin-bottom: 8px;
  font-size: 14px;
}

.content-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
  line-height: 1.5;
  resize: vertical;
  background-color: #fff;
  transition: border-color 0.2s;
}

.content-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

/* 对话框样式 */
:deep(.patient-detail-dialog) {
  width: 90% !important;
  max-width: 900px !important;
}

:deep(.patient-detail-dialog .el-message-box__content) {
  padding: 0 !important;
}

:deep(.patient-detail-dialog .el-message-box__header) {
  padding: 16px 20px;
  border-bottom: 1px solid #e1e5e9;
  background-color: #f8f9fa;
}

:deep(.patient-detail-dialog .el-message-box__title) {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

:deep(.patient-detail-dialog .el-message-box__btns) {
  padding: 16px 20px;
  border-top: 1px solid #e1e5e9;
  background-color: #f8f9fa;
}

:deep(.patient-detail-dialog .el-button) {
  padding: 10px 20px;
  font-size: 14px;
  border-radius: 4px;
  font-weight: 500;
}

:deep(.patient-detail-dialog .el-button--primary) {
  background-color: #3b82f6;
  border-color: #3b82f6;
}

:deep(.patient-detail-dialog .el-button--primary:hover) {
  background-color: #2563eb;
  border-color: #2563eb;
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .main-content {
    flex-direction: column;
  }
  
  .left-panel,
  .right-panel {
    flex: none;
    min-width: auto;
  }
  
  .overview-cards {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .indicators-content {
    gap: 8px;
  }
  
  .response-content {
    gap: 8px;
  }
  
  .followup-form {
    max-width: 100%;
  }
}

/* 随访应答详情弹窗样式 */
.response-detail {
  .detail-header {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin-bottom: 24px;
    padding: 16px;
    background: #f8f9fa;
    border-radius: 8px;
    
    .detail-info {
      display: flex;
      align-items: center;
      gap: 8px;
      
      .label {
        font-weight: 600;
        color: #606266;
        min-width: 80px;
      }
      
      .value {
        color: #303133;
      }
    }
  }
  
  .detail-content {
    .detail-section {
      margin-bottom: 24px;
      
      h5 {
        margin: 0 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #e4e7ed;
        color: #303133;
        font-size: 16px;
        font-weight: 600;
      }
      
      .detail-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 16px;
        
        .detail-field {
          display: flex;
          align-items: flex-start;
          gap: 8px;
          
          &.full-width {
            grid-column: 1 / -1;
          }
          
          .label {
            font-weight: 600;
            color: #606266;
            min-width: 100px;
            flex-shrink: 0;
          }
          
          .value {
            color: #303133;
            line-height: 1.5;
            word-break: break-word;
          }
        }
      }
    }
  }
}

.responses-table {
  margin-top: 16px;
}

.responses-table .el-table {
  border-radius: 8px;
  overflow: hidden;
}

.responses-table .el-button {
  margin: 0;
}
</style>