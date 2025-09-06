<template>
  <div class="followup-response">
    <!-- 顶部概览卡片 -->
    <div class="overview-cards">
      <div class="overview-card low-risk">
        <div class="card-content">
          <div class="card-title">低危</div>
          <div class="card-subtitle">待随访人数</div>
          <div class="card-number">30人</div>
        </div>
      </div>
      <div class="overview-card medium-risk">
        <div class="card-content">
          <div class="card-title">中危</div>
          <div class="card-subtitle">待随访人数</div>
          <div class="card-number">20人</div>
        </div>
      </div>
      <div class="overview-card high-risk">
        <div class="card-content">
          <div class="card-title">高危</div>
          <div class="card-subtitle">待随访人数</div>
          <div class="card-number">12人</div>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧患者列表 -->
      <div class="left-panel">
        <!-- 患者列表表格 -->
        <div class="table-section">
          <el-table
            :data="patients"
            style="width: 100%"
            @row-click="handlePatientClick"
            :row-class-name="getRowClassName"
            highlight-current-row
          >
            <el-table-column prop="id" label="序号" width="80" />
            <el-table-column prop="name" label="用户名称" width="120" />
            <el-table-column label="病人等级" width="120">
              <template #default="{ row }">
                <el-tag 
                  :type="getLevelType(row.level)"
                  size="small"
                >
                  {{ getLevelText(row.level) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="responseTime" label="应答时间" width="180" />
            <el-table-column label="详细信息" width="120">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click.stop="viewDetails(row)">
                  点击查看
                </el-button>
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
                <span class="value">{{ selectedPatient.gender }}</span>
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
              <el-tag :type="getLevelType(selectedPatient.level)" size="small">
                {{ getLevelText(selectedPatient.level) }}
              </el-tag>
            </div>
          </div>

          <!-- 关键指标 -->
          <div class="key-indicators">
            <h4>关键指标 (骨密度) - {{ selectedPatient.boneDensity.date }}检测</h4>
            <div class="indicators-content">
              <div class="indicator-item">
                <span class="label">检测方法:</span>
                <span class="value">{{ selectedPatient.boneDensity.method }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">检测部位:</span>
                <span class="value">{{ selectedPatient.boneDensity.site }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">T值:</span>
                <span class="value">{{ selectedPatient.boneDensity.tScore }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">Z值:</span>
                <span class="value">{{ selectedPatient.boneDensity.zScore }}</span>
              </div>
              <div class="indicator-item full-width">
                <span class="label">结论:</span>
                <span class="value">{{ selectedPatient.boneDensity.conclusion }}</span>
              </div>
            </div>
          </div>

          <!-- 回访应答 -->
          <div class="response-section">
            <h4>回访应答 - {{ selectedPatient.response.time }}</h4>
            <div class="response-content">
              <div class="response-item">
                <span class="label">总体感受:</span>
                <span class="value">{{ selectedPatient.response.overallFeeling }}</span>
              </div>
              <div class="response-item">
                <span class="label">状况改善:</span>
                <span class="value">{{ selectedPatient.response.improvement }}</span>
              </div>
              <div class="response-item">
                <span class="label">用药依从性:</span>
                <span class="value">{{ selectedPatient.response.medicationAdherence }}</span>
              </div>
              <div class="response-item">
                <span class="label">运动量:</span>
                <span class="value">{{ selectedPatient.response.exerciseVolume }}</span>
              </div>
              <div class="response-item">
                <span class="label">饮食调整:</span>
                <span class="value">{{ selectedPatient.response.dietAdjustment }}</span>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="no-patient-selected">
          <el-empty description="请选择患者查看应答详情" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 响应式数据
const selectedPatient = ref<any>(null)

// 模拟患者数据
const patients = ref([
  {
    id: 1,
    name: '张伟',
    level: 'low',
    responseTime: '2025/8/15 13:00',
    gender: '男',
    age: 45,
    phone: '138****1234',
    boneDensity: {
      date: '2024年05月20日',
      method: '双能X线吸收检测法(DXA)',
      site: '腰椎(L1-L4)',
      tScore: '-0.8 (处于正常骨量范围下限)',
      zScore: '+0.2',
      conclusion: '骨密度在正常范围内,但接近骨量减少临界值,需关注生活方式干预。'
    },
    response: {
      time: '2025/8/15 13:00',
      overallFeeling: '良好',
      improvement: '明显改善',
      medicationAdherence: '完全按照医嘱',
      exerciseVolume: '每周能完成2次30分钟以上的快走',
      dietAdjustment: '每日早餐必喝一杯牛奶或酸奶'
    }
  },
  {
    id: 2,
    name: '李娜',
    level: 'medium',
    responseTime: '2025/8/13 13:00',
    gender: '女',
    age: 62,
    phone: '136****2345',
    boneDensity: {
      date: '2024年05月21日',
      method: '双能X线吸收检测法(DXA)',
      site: '腰椎(L1-L4)及左侧股骨颈',
      tScore: '-1.9 (骨量减少)',
      zScore: '-1.2',
      conclusion: '骨密度明显低于峰值骨量，符合中度骨质疏松症标准。'
    },
    response: {
      time: '2025/8/13 13:00',
      overallFeeling: '一般',
      improvement: '有所改善',
      medicationAdherence: '基本按照医嘱',
      exerciseVolume: '每周能完成1次30分钟的快走',
      dietAdjustment: '增加了钙质摄入，每日喝牛奶'
    }
  },
  {
    id: 3,
    name: '王建国',
    level: 'high',
    responseTime: '2025/8/13 13:00',
    gender: '男',
    age: 78,
    phone: '138****3456',
    boneDensity: {
      date: '2024年05月24日',
      method: '双能X线吸收检测法(DXA)',
      site: '腰椎(L1-L4)及左侧股骨颈',
      tScore: '-3.2 (重度骨质疏松)',
      zScore: '-2.1',
      conclusion: '骨密度显著低于峰值骨量，符合重度骨质疏松症标准。'
    },
    response: {
      time: '2025/8/13 13:00',
      overallFeeling: '较差',
      improvement: '改善不明显',
      medicationAdherence: '有时忘记服药',
      exerciseVolume: '因身体原因，运动量较少',
      dietAdjustment: '尽量增加钙质摄入，但食欲不佳'
    }
  }
])

// 方法
const handlePatientClick = (row: any) => {
  selectedPatient.value = row
  ElMessage.info(`已选择患者: ${row.name}`)
}

const viewDetails = (patient: any) => {
  selectedPatient.value = patient
  ElMessage.info(`查看患者: ${patient.name} 的应答详情`)
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

onMounted(() => {
  // 默认选中第一个患者
  if (patients.value.length > 0) {
    selectedPatient.value = patients.value[0]
  }
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
  flex: 2;
  display: flex;
  flex-direction: column;
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
}

.response-detail {
  padding: 20px;
}

.detail-header {
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 15px;
  margin-bottom: 20px;
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

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-content {
    flex-direction: column;
  }
  
  .left-panel,
  .right-panel {
    flex: none;
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
}
</style> 