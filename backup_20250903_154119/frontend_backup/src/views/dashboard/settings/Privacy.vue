<template>
  <div class="privacy-page">
    <div class="privacy-content">
      <h2 class="page-title">隐私条款</h2>
      
      <!-- 隐私政策列表 -->
      <div class="policy-list">
        <div 
          v-for="policy in privacyPolicies" 
          :key="policy.id"
          class="policy-item"
          @click="viewPolicy(policy)"
        >
          <div class="policy-info">
            <h3 class="policy-title">{{ policy.title }}</h3>
            <p class="policy-description">{{ policy.description }}</p>
            <div class="policy-meta">
              <span class="policy-date">更新日期: {{ policy.updateDate }}</span>
              <span class="policy-version">版本: {{ policy.version }}</span>
            </div>
          </div>
          <div class="policy-actions">
            <el-button type="primary" size="small">查看详情</el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 政策详情对话框 -->
    <el-dialog 
      v-model="policyDialogVisible" 
      :title="selectedPolicy?.title" 
      width="800px"
      class="policy-dialog"
    >
      <div v-if="selectedPolicy" class="policy-detail">
        <div class="policy-header">
          <div class="policy-meta-info">
            <p><strong>版本:</strong> {{ selectedPolicy.version }}</p>
            <p><strong>更新日期:</strong> {{ selectedPolicy.updateDate }}</p>
            <p><strong>生效日期:</strong> {{ selectedPolicy.effectiveDate }}</p>
          </div>
        </div>
        
        <div class="policy-content">
          <div v-for="section in selectedPolicy.sections" :key="section.id" class="policy-section">
            <h4>{{ section.title }}</h4>
            <div v-html="section.content"></div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="policyDialogVisible = false">关闭</el-button>
          <el-button type="primary" @click="downloadPolicy">下载PDF</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

// 隐私政策数据
const privacyPolicies = ref([
  {
    id: 1,
    title: '患者基本信息与病史登记管理条例',
    description: '规范患者基本信息和病史的收集、存储、使用和保护，确保患者隐私安全。',
    version: 'v2.1',
    updateDate: '2025-01-15',
    effectiveDate: '2025-02-01',
    sections: [
      {
        id: 1,
        title: '第一章 总则',
        content: `
          <p><strong>第一条</strong> 为规范患者基本信息和病史的收集、存储、使用和保护，保护患者隐私权，根据《中华人民共和国个人信息保护法》等相关法律法规，制定本条例。</p>
          <p><strong>第二条</strong> 本条例适用于骨质疏松症跟踪随访系统中患者基本信息和病史的登记管理活动。</p>
          <p><strong>第三条</strong> 患者基本信息和病史的收集、使用应当遵循合法、正当、必要的原则，不得过度收集个人信息。</p>
        `
      },
      {
        id: 2,
        title: '第二章 信息收集',
        content: `
          <p><strong>第四条</strong> 收集患者基本信息应当取得患者的明确同意，并告知收集目的、使用范围、保存期限等事项。</p>
          <p><strong>第五条</strong> 收集的病史信息应当真实、准确、完整，不得虚假记录或遗漏重要信息。</p>
          <p><strong>第六条</strong> 收集敏感个人信息时，应当取得患者的单独同意。</p>
        `
      },
      {
        id: 3,
        title: '第三章 信息保护',
        content: `
          <p><strong>第七条</strong> 应当采取技术措施和其他必要措施，确保患者信息安全。</p>
          <p><strong>第八条</strong> 未经患者同意，不得向第三方提供患者个人信息。</p>
          <p><strong>第九条</strong> 发生个人信息泄露事件时，应当立即采取补救措施，并通知患者。</p>
        `
      }
    ]
  },
  {
    id: 2,
    title: '骨密度检测结果录入与追踪规范',
    description: '规范骨密度检测结果的录入、存储、追踪和使用流程，确保数据准确性和安全性。',
    version: 'v1.8',
    updateDate: '2025-01-10',
    effectiveDate: '2025-01-25',
    sections: [
      {
        id: 1,
        title: '检测结果录入规范',
        content: `
          <p><strong>第一条</strong> 骨密度检测结果应当由专业医务人员录入系统，确保数据的准确性和完整性。</p>
          <p><strong>第二条</strong> 录入的检测结果应当包括检测日期、检测部位、检测方法、检测结果等关键信息。</p>
          <p><strong>第三条</strong> 对于异常检测结果，应当进行标记并记录相关说明。</p>
        `
      },
      {
        id: 2,
        title: '数据追踪管理',
        content: `
          <p><strong>第四条</strong> 系统应当记录检测结果的所有操作历史，包括录入、修改、删除等操作。</p>
          <p><strong>第五条</strong> 定期对检测数据进行质量检查和统计分析。</p>
        `
      }
    ]
  },
  {
    id: 3,
    title: '骨折风险综合评估与预警机制条例',
    description: '建立骨折风险综合评估体系，制定预警机制，及时识别高风险患者。',
    version: 'v1.5',
    updateDate: '2025-01-08',
    effectiveDate: '2025-01-20',
    sections: [
      {
        id: 1,
        title: '风险评估体系',
        content: `
          <p><strong>第一条</strong> 建立基于多因素的骨折风险评估体系，包括骨密度、年龄、性别、既往骨折史等。</p>
          <p><strong>第二条</strong> 定期更新风险评估模型，提高预测准确性。</p>
        `
      },
      {
        id: 2,
        title: '预警机制',
        content: `
          <p><strong>第三条</strong> 对于高风险患者，系统应当自动生成预警信息。</p>
          <p><strong>第四条</strong> 预警信息应当及时通知相关医务人员和患者。</p>
        `
      }
    ]
  },
  {
    id: 4,
    title: '药物治疗方案依从性跟踪管理规定',
    description: '规范药物治疗方案的制定、跟踪和管理，提高患者治疗依从性。',
    version: 'v1.3',
    updateDate: '2025-01-05',
    effectiveDate: '2025-01-15',
    sections: [
      {
        id: 1,
        title: '治疗方案制定',
        content: `
          <p><strong>第一条</strong> 治疗方案应当根据患者具体情况制定，考虑患者年龄、病情、经济状况等因素。</p>
          <p><strong>第二条</strong> 治疗方案应当明确用药剂量、频次、疗程等关键信息。</p>
        `
      },
      {
        id: 2,
        title: '依从性跟踪',
        content: `
          <p><strong>第三条</strong> 定期跟踪患者用药情况，记录用药依从性数据。</p>
          <p><strong>第四条</strong> 对于依从性较差的患者，应当及时干预和指导。</p>
        `
      }
    ]
  },
  {
    id: 5,
    title: '系统数据安全与隐私保护条例',
    description: '确保系统数据安全，保护患者隐私，防止数据泄露和滥用。',
    version: 'v2.0',
    updateDate: '2025-01-20',
    effectiveDate: '2025-02-01',
    sections: [
      {
        id: 1,
        title: '数据安全措施',
        content: `
          <p><strong>第一条</strong> 采用加密技术保护数据传输和存储安全。</p>
          <p><strong>第二条</strong> 建立访问控制机制，限制数据访问权限。</p>
          <p><strong>第三条</strong> 定期进行安全审计和漏洞扫描。</p>
        `
      },
      {
        id: 2,
        title: '隐私保护',
        content: `
          <p><strong>第四条</strong> 严格保护患者隐私信息，不得用于非医疗目的。</p>
          <p><strong>第五条</strong> 建立数据泄露应急响应机制。</p>
        `
      }
    ]
  }
])

// 对话框控制
const policyDialogVisible = ref(false)
const selectedPolicy = ref(null)

// 查看政策详情
const viewPolicy = (policy: any) => {
  selectedPolicy.value = policy
  policyDialogVisible.value = true
}

// 下载政策PDF
const downloadPolicy = () => {
  ElMessage.success('PDF下载功能开发中...')
}
</script>

<style scoped>
.privacy-page {
  height: 100%;
  padding: 20px;
  background: #f5f5f5;
}

.privacy-content {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  max-width: 900px;
  margin: 0 auto;
}

.page-title {
  text-align: center;
  color: #333;
  font-size: 1.5rem;
  margin-bottom: 30px;
  font-weight: 600;
}

.policy-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.policy-item {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.policy-item:hover {
  border-color: #667eea;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
  transform: translateY(-2px);
}

.policy-info {
  flex: 1;
}

.policy-title {
  color: #333;
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.policy-description {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0 0 10px 0;
}

.policy-meta {
  display: flex;
  gap: 20px;
  font-size: 0.8rem;
  color: #999;
}

.policy-actions {
  flex-shrink: 0;
}

.policy-dialog :deep(.el-dialog__body) {
  max-height: 60vh;
  overflow-y: auto;
}

.policy-detail {
  line-height: 1.6;
}

.policy-header {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 20px;
}

.policy-meta-info p {
  margin: 5px 0;
  color: #666;
}

.policy-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.policy-section {
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 15px;
}

.policy-section:last-child {
  border-bottom: none;
}

.policy-section h4 {
  color: #333;
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 10px 0;
}

.policy-section p {
  margin: 8px 0;
  color: #555;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 