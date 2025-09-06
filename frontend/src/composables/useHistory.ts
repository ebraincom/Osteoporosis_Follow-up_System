import { ref, computed } from 'vue'
import type { HistoryRecord, VoiceHistoryRecord, DietHistoryRecord, HISHistoryRecord, ValidationHistoryRecord } from '@/types/history'

// 历史记录存储
const historyRecords = ref<HistoryRecord[]>([])

// 初始化一些示例数据
const initializeSampleData = () => {
  // 语音自述历史记录
  const voiceHistory: VoiceHistoryRecord = {
    id: 'voice-001',
    date: '2025-01-20',
    title: '腰部疼痛咨询',
    type: 'voice',
    summary: '今天翻身时腰像针扎一样疼，咨询了急性腰扭伤的处理方法',
    conversations: [
      {
        role: 'user',
        content: '今天早上起床翻身的时候,突然右边腰那里像针扎一样疼,完全不敢动,缓了几分钟才能慢慢起来,这是怎么回事?',
        timestamp: '2025-01-20 09:30:00'
      },
      {
        role: 'ai',
        content: '根据您描述的症状，最可能的原因是急性腰扭伤或腰椎小关节紊乱。突然的翻身动作可能导致肌肉、韧带拉伤或关节卡压，引起剧烈疼痛和活动受限。\n\n建议立即处理：\n1. 立即停止引起疼痛的动作\n2. 采取舒适体位休息（如侧卧位，屈膝）\n3. 冷敷（冰袋包裹毛巾，每次15-20分钟）\n4. 24小时内避免热敷、按摩或强行拉伸',
        timestamp: '2025-01-20 09:30:15'
      },
      {
        role: 'user',
        content: '谢谢。那我需要马上去医院吗?还是可以先在家观察一下?',
        timestamp: '2025-01-20 09:31:00'
      },
      {
        role: 'ai',
        content: '建议就医的情况：\n1. 疼痛持续加重，休息后无缓解\n2. 伴有下肢放射痛、麻木或无力\n3. 大小便控制困难或异常感觉\n4. 伴有发热或不明原因体重减轻\n\n如无上述严重情况，建议严格休息和冷敷观察24小时。',
        timestamp: '2025-01-20 09:31:20'
      }
    ],
    duration: 120
  }

  // 饮食识别历史记录
  const dietHistory: DietHistoryRecord = {
    id: 'diet-001',
    date: '2025-01-20',
    title: '牛奶营养分析',
    type: 'diet',
    summary: '识别了500ml纯牛奶，分析了钙含量和蛋白质等营养成分',
    foodImage: '/images/milk.jpg',
    nutritionData: {
      calories: 240,
      protein: 16,
      fat: 8,
      carbohydrates: 12,
      calcium: 600,
      vitaminD: 2.5,
      otherNutrients: {
        '维生素B2': 0.4,
        '磷': 200,
        '钾': 400
      }
    },
    benefits: [
      '骨骼与牙齿的"建筑师"',
      '优质蛋白"补给站"',
      '神经系统的"稳定剂"',
      '身体的"综合维护师"'
    ],
    recommendations: [
      '建议每日饮用300-500ml牛奶',
      '配合维生素D补充剂效果更佳',
      '避免空腹饮用，可搭配全谷物'
    ]
  }

  // HIS接口历史记录
  const hisHistory: HISHistoryRecord = {
    id: 'his-001',
    date: '2025-01-20',
    title: '张南 - MR下肢检查报告',
    type: 'his',
    summary: '首都医科大学附属北京同仁医院医学影像诊断报告',
    hospital: '首都医科大学附属北京同仁医院',
    patientInfo: {
      name: '张南',
      gender: '男',
      age: 48,
      examDate: '2025-01-24',
      examType: 'MR 下肢'
    },
    reportContent: '右足踝关节MR平扫示：右足踝关节骨质结构完整，关节间隙正常，关节面光滑，周围软组织未见明显异常信号。\n\n诊断结论：右足踝关节MR平扫未见明显异常。',
    images: ['/images/mr1.jpg', '/images/mr2.jpg', '/images/mr3.jpg']
  }

  // 校验规则历史记录
  const validationHistory: ValidationHistoryRecord = {
    id: 'validation-001',
    date: '2025-01-20',
    title: '数据校验规则检查',
    type: 'validation',
    summary: '检查了患者数据的完整性和准确性',
    status: 'passed',
    rules: [
      {
        name: '患者基本信息完整性',
        description: '检查姓名、性别、年龄等基本信息是否完整',
        status: 'passed',
        details: '所有基本信息字段都已填写完整'
      },
      {
        name: '检查日期有效性',
        description: '验证检查日期是否为有效日期',
        status: 'passed',
        details: '检查日期2025-01-24为有效日期'
      },
      {
        name: '影像数据完整性',
        description: '检查影像文件是否存在且可访问',
        status: 'warning',
        details: '发现1个影像文件路径可能存在问题，建议重新上传'
      }
    ]
  }

  historyRecords.value = [voiceHistory, dietHistory, hisHistory, validationHistory]
}

// 获取指定类型的历史记录
const getHistoryByType = (type: string) => {
  return computed(() => historyRecords.value.filter(record => record.type === type))
}

// 获取指定ID的历史记录
const getHistoryById = (id: string) => {
  return computed(() => historyRecords.value.find(record => record.id === id))
}

// 添加新的历史记录
const addHistoryRecord = (record: HistoryRecord) => {
  historyRecords.value.unshift(record)
}

// 删除历史记录
const deleteHistoryRecord = (id: string) => {
  const index = historyRecords.value.findIndex(record => record.id === id)
  if (index !== -1) {
    historyRecords.value.splice(index, 1)
  }
}

// 初始化数据
initializeSampleData()

export function useHistory() {
  return {
    historyRecords: computed(() => historyRecords.value),
    getHistoryByType,
    getHistoryById,
    addHistoryRecord,
    deleteHistoryRecord
  }
} 