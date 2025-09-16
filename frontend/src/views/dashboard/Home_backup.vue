<template>
  <div class="home-container">
    <!-- 机构用户首页：患者信息列表 -->
    <div v-if="userStore.user?.user_type === 'institutional'" class="institutional-home">
      <!-- 主内容区 -->
      <div class="main-content">
        <!-- 左侧：患者列表 -->
        <div class="left-panel">
          <div class="search-section">
            <div class="search-header">
              <span class="search-title">分类查找:</span>
              <div class="filter-buttons">
                <el-button 
                  :type="currentFilter === 'all' ? 'primary' : 'default'"
                  size="small"
                  @click="setFilter('all')"
                >
                  展示全部
                </el-button>
                <el-button 
                  :type="currentFilter === 'high' ? 'primary' : 'default'"
                  size="small"
                  @click="setFilter('high')"
                >
                  高危
                </el-button>
                <el-button 
                  :type="currentFilter === 'medium' ? 'primary' : 'default'"
                  size="small"
                  @click="setFilter('medium')"
                >
                  中危
                </el-button>
                <el-button 
                  :type="currentFilter === 'low' ? 'primary' : 'default'"
                  size="small"
                  @click="setFilter('low')"
                >
                  低危
                </el-button>
              </div>
            </div>
            <div class="search-input-section">
              <el-input
                v-model="searchKeyword"
                placeholder="输入想要查找的名称"
                class="search-input"
                clearable
              />
              <el-button type="primary" @click="handleSearch" class="search-button">
                点击搜索
              </el-button>
            </div>
          </div>

          <!-- 患者表格 -->
          <div class="patient-table-section">
            <el-table
              :data="filteredPatients"
              style="width: 100%"
              @row-click="handlePatientClick"
              :row-class-name="getRowClassName"
              highlight-current-row
            >
              <el-table-column prop="name" label="用户名称" width="120" />
              <el-table-column prop="level" label="病人等级" width="100">
                <template #default="{ row }">
                  <el-tag
                    :type="getLevelType(row.level)"
                    size="small"
                  >
                    {{ getLevelText(row.level) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="age" label="年龄" width="80" />
              <el-table-column prop="gender" label="性别" width="80" />
              <el-table-column prop="keyIndicator" label="关键指标" width="100" />
              <el-table-column prop="hospital" label="就医机构" min-width="150" />
              <el-table-column label="操作" width="120" fixed="right">
                <template #default="{ row }">
                  <el-button 
                    type="primary" 
                    size="small" 
                    @click.stop="viewPatient(row)"
                    :class="{ 'is-selected': selectedPatient?.id === row.id }"
                  >
                    {{ selectedPatient?.id === row.id ? '已选中' : '查看' }}
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>

        <!-- 右侧：患者详情 -->
        <div class="right-panel">
          <div v-if="selectedPatient" class="patient-detail">
            <div class="detail-header">
              <h2>患者综合信息档案-{{ selectedPatient.name }}</h2>
              <div class="file-info">
                <span>档案编号: {{ selectedPatient.fileNo }}</span>
                <span>生成日期: {{ selectedPatient.generateDate }}</span>
              </div>
            </div>

            <div class="detail-content">
              <!-- 基本信息 -->
              <div class="info-section">
                <h3>一、基本信息</h3>
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
                  <div class="info-item">
                    <span class="label">身份证号:</span>
                    <span class="value">{{ selectedPatient.idCard }}</span>
                  </div>
                  <div class="info-item">
                    <span class="label">地址:</span>
                    <span class="value">{{ selectedPatient.address }}</span>
                  </div>
                  <div class="info-item">
                    <span class="label">紧急联系人:</span>
                    <span class="value">{{ selectedPatient.emergencyContact }}</span>
                  </div>
                </div>
              </div>

              <!-- 临床诊断信息 -->
              <div class="info-section">
                <h3>二、临床诊断信息</h3>
                <div class="info-grid">
                  <div class="info-item">
                    <span class="label">主要诊断:</span>
                    <span class="value">{{ selectedPatient.diagnosis }}</span>
                  </div>
                  <div class="info-item">
                    <span class="label">患者等级:</span>
                    <el-tag :type="getLevelType(selectedPatient.level)" size="small">
                      {{ getLevelText(selectedPatient.level) }}
                    </el-tag>
                  </div>
                  <div class="info-item">
                    <span class="label">关键指标:</span>
                    <span class="value">{{ selectedPatient.keyIndicator }}</span>
                  </div>
                </div>
                <div class="bone-density-info">
                  <h4>骨密度详情</h4>
                  <div class="info-grid">
                    <div class="info-item">
                      <span class="label">检测方法:</span>
                      <span class="value">{{ selectedPatient.boneDensity.method }}</span>
                    </div>
                    <div class="info-item">
                      <span class="label">检测部位:</span>
                      <span class="value">{{ selectedPatient.boneDensity.site }}</span>
                    </div>
                    <div class="info-item">
                      <span class="label">T值:</span>
                      <span class="value">{{ selectedPatient.boneDensity.tScore }}</span>
                    </div>
                    <div class="info-item">
                      <span class="label">Z值:</span>
                      <span class="value">{{ selectedPatient.boneDensity.zScore }}</span>
                    </div>
                    <div class="info-item full-width">
                      <span class="label">结论:</span>
                      <span class="value">{{ selectedPatient.boneDensity.conclusion }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 病史与风险因素 -->
              <div class="info-section">
                <h3>三、病史与风险因素</h3>
                <div class="history-item">
                  <h4>现病史</h4>
                  <p>{{ selectedPatient.currentHistory }}</p>
                </div>
                <div class="history-item">
                  <h4>既往史</h4>
                  <p>{{ selectedPatient.pastHistory }}</p>
                </div>
                <div class="history-item">
                  <h4>个人史</h4>
                  <p>{{ selectedPatient.personalHistory }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <div v-else class="no-patient-selected">
            <el-empty description="请选择患者查看详细信息" />
          </div>
        </div>
      </div>

      <!-- 右侧历史记录栏 -->
      <div class="right-sidebar">
        <div class="sidebar-header">
          <h3>历史记录</h3>
        </div>
        <div class="history-list">
          <div v-if="historyRecords.length > 0">
            <div v-for="record in historyRecords" :key="record.id" class="history-item">
              <div class="history-content">
                <div class="history-title">{{ record.patientName }} - {{ record.action }}</div>
                <div class="history-date">{{ formatDate(record.timestamp) }}</div>
                <div class="history-desc">{{ record.description }}</div>
              </div>
              <el-button size="small" type="primary" @click="viewHistoryDetail(record)">查看</el-button>
            </div>
          </div>
          <div v-else class="no-history">
            <el-empty description="暂无历史记录" :image-size="60" />
          </div>
        </div>
      </div>
    </div>

    <!-- 个人用户首页：个人信息展示和患者档案 -->
    <div v-else class="personal-home">
      <!-- 主内容区 -->
      <div class="main-content">
        <!-- 左侧：个人信息展示 -->
        <div class="left-panel">
          <!-- 个人信息展示 -->
          <div class="personal-info-section">
            <div class="info-header">
              <h3>个人信息</h3>
              <p>以下是您的基本信息</p>
            </div>
            
            <!-- 个人信息卡片 -->
            <div class="personal-info-card">
              <div class="info-grid">
                <div class="info-item">
                  <label>姓名</label>
                  <span>{{ personalUserInfo.name || '未设置' }}</span>
                </div>
                <div class="info-item">
                  <label>年龄</label>
                  <span>{{ personalUserInfo.age || '未设置' }}</span>
                </div>
                <div class="info-item">
                  <label>性别</label>
                  <span>{{ personalUserInfo.gender === 'FEMALE' ? '女' : personalUserInfo.gender === 'MALE' ? '男' : '未设置' }}</span>
                </div>
                <div class="info-item">
                  <label>联系电话</label>
                  <span>{{ personalUserInfo.phone || '未设置' }}</span>
                </div>
                <div class="info-item">
                  <label>邮箱</label>
                  <span>{{ personalUserInfo.email || '未设置' }}</span>
                </div>
                <div class="info-item">
                  <label>地址</label>
                  <span>{{ personalUserInfo.address || '未设置' }}</span>
                </div>
                <div class="info-item">
                  <label>身高</label>
                  <span>{{ personalUserInfo.height ? personalUserInfo.height + 'cm' : '未设置' }}</span>
                </div>
                <div class="info-item">
                  <label>体重</label>
                  <span>{{ personalUserInfo.weight ? personalUserInfo.weight + 'kg' : '未设置' }}</span>
                </div>
                <div class="info-item">
                  <label>T值</label>
                  <span>{{ personalUserInfo.t_score || '未设置' }}</span>
                </div>
                <div class="info-item">
                  <label>Z值</label>
                  <span>{{ personalUserInfo.z_score || '未设置' }}</span>
                </div>
                <div class="info-item">
                  <label>风险等级</label>
                  <el-tag :type="getRiskLevelType(personalUserInfo.risk_level)" size="small">
                    {{ getRiskLevelText(personalUserInfo.risk_level) }}
                  </el-tag>
                </div>
              </div>
              
              <!-- 添加详情按钮 -->
              <div class="action-buttons">
                <el-button type="primary" @click="showAddDetailsDialog">
                  <el-icon><Plus /></el-icon>
                  添加详情
                </el-button>
                <el-button type="success" @click="showEditInfoDialog">
                  <el-icon><Edit /></el-icon>
                  编辑信息
                </el-button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 右侧：患者档案信息 -->
        <div class="right-panel">
          <div class="patient-files-section">
            <div class="files-header">
              <h3>我的患者档案</h3>
              <p>以下是您的患者档案信息</p>
            </div>
            
            <!-- 患者档案列表 -->
            <div class="patient-files-list">
              <div v-if="patientFiles.length === 0" class="no-files">
                <el-empty description="暂无患者档案" />
              </div>
              <div v-else>
                <div 
                  v-for="file in patientFiles" 
                  :key="file.id"
                  class="patient-file-item"
                  @click="selectPatientFile(file)"
                >
                  <div class="file-header">
                    <span class="file-id">{{ file.patient_id }}</span>
                    <el-tag :type="getRiskLevelType(file.risk_level)" size="small">
                      {{ getRiskLevelText(file.risk_level) }}
                    </el-tag>
                  </div>
                  <div class="file-info">
                    <p><strong>姓名:</strong> {{ file.name }}</p>
                    <p><strong>年龄:</strong> {{ file.age }}岁</p>
                    <p><strong>性别:</strong> {{ file.gender === 'female' ? '女' : '男' }}</p>
                    <p><strong>电话:</strong> {{ file.phone }}</p>
                    <p v-if="file.address"><strong>地址:</strong> {{ file.address }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
            
    <!-- 添加详情弹窗 -->
    <el-dialog
      v-model="addDetailsDialogVisible"
      title="添加详情信息"
      width="60%"
      :close-on-click-modal="false"
    >
      <el-form
        ref="addDetailsFormRef"
        :model="addDetailsForm"
        :rules="addDetailsRules"
        label-width="120px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="地址" prop="address">
              <el-input v-model="addDetailsForm.address" placeholder="请输入详细地址" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="身高(cm)" prop="height">
              <el-input-number v-model="addDetailsForm.height" :min="100" :max="250" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="体重(kg)" prop="weight">
              <el-input-number v-model="addDetailsForm.weight" :min="20" :max="200" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="T值" prop="t_score">
              <el-input-number v-model="addDetailsForm.t_score" :min="-5" :max="5" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Z值" prop="z_score">
              <el-input-number v-model="addDetailsForm.z_score" :min="-5" :max="5" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="风险等级" prop="risk_level">
              <el-select v-model="addDetailsForm.risk_level" placeholder="请选择风险等级" style="width: 100%">
                <el-option label="低危" value="low" />
                <el-option label="中危" value="medium" />
                <el-option label="高危" value="high" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="现病史" prop="medical_history">
              <el-input v-model="addDetailsForm.medical_history" type="textarea" :rows="3" placeholder="请描述您的现病史" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="家族史" prop="family_history">
              <el-input v-model="addDetailsForm.family_history" type="textarea" :rows="3" placeholder="请描述您的家族史" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="用药史" prop="medications">
              <el-input v-model="addDetailsForm.medications" type="textarea" :rows="3" placeholder="请输入用药史" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addDetailsDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAddDetails" :loading="submittingDetails">
            {{ submittingDetails ? '提交中...' : '确认添加' }}
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑信息弹窗 -->
    <el-dialog
      v-model="editInfoDialogVisible"
      title="编辑个人信息"
      width="60%"
      :close-on-click-modal="false"
    >
      <el-form
        ref="editInfoFormRef"
        :model="editInfoForm"
        :rules="editInfoRules"
        label-width="120px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="editInfoForm.name" placeholder="请输入姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="年龄" prop="age">
              <el-input-number v-model="editInfoForm.age" :min="1" :max="120" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="editInfoForm.gender" placeholder="请选择性别" style="width: 100%">
                <el-option label="男" value="MALE" />
                <el-option label="女" value="FEMALE" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="editInfoForm.phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="editInfoForm.email" placeholder="请输入邮箱" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editInfoDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitEditInfo" :loading="submittingEdit">
            {{ submittingEdit ? '保存中...' : '保存修改' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="档案编号" prop="patient_id">
                    <el-input 
                      v-model="patientForm.patient_id" 
                      placeholder="系统自动生成" 
                      readonly
                      disabled
                      class="auto-generated-field"
                    >
                      <template #prepend>
                        <el-tooltip 
                          content="档案编号由系统自动生成" 
                          placement="top"
                        >
                          <el-icon><InfoFilled /></el-icon>
                        </el-tooltip>
                      </template>
                      <template #append>
                        <el-tooltip content="重新生成档案编号" placement="top">
                          <el-button 
                            type="text" 
                            size="small" 
                            @click="regeneratePatientId"
                            class="regenerate-btn"
                          >
                            <el-icon><Refresh /></el-icon>
                          </el-button>
                        </el-tooltip>
                      </template>
                    </el-input>
                    <div class="field-hint">
                      <el-icon><InfoFilled /></el-icon>
                      <span>档案编号由系统自动生成</span>
                    </div>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="姓名" prop="name">
                    <el-input v-model="patientForm.name" placeholder="请输入姓名" />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="年龄" prop="age">
                    <el-input v-model="patientForm.age" type="number" placeholder="请输入年龄" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="性别" prop="gender">
                    <el-select v-model="patientForm.gender" placeholder="请选择性别" style="width: 100%">
                      <el-option label="男" value="male" />
                      <el-option label="女" value="female" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="联系电话" prop="phone">
                    <el-input v-model="patientForm.phone" placeholder="请输入联系电话" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="邮箱" prop="email">
                    <el-input v-model="patientForm.email" placeholder="请输入邮箱（可选）" />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="身高(cm)" prop="height">
                    <el-input v-model="patientForm.height" type="number" placeholder="请输入身高" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="体重(kg)" prop="weight">
                    <el-input v-model="patientForm.weight" type="number" placeholder="请输入体重" />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="T值" prop="t_score">
                    <el-input v-model="patientForm.t_score" type="number" step="0.1" placeholder="请输入T值" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="Z值" prop="z_score">
                    <el-input v-model="patientForm.z_score" type="number" step="0.1" placeholder="请输入Z值" />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="风险等级" prop="risk_level">
                    <el-select v-model="patientForm.risk_level" placeholder="请选择风险等级" style="width: 100%">
                      <el-option label="低危" value="low" />
                      <el-option label="中危" value="medium" />
                      <el-option label="高危" value="high" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="地址" prop="address">
                    <el-input v-model="patientForm.address" placeholder="请输入详细地址" />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-row :gutter="20">
                <el-col :span="24">
                  <el-form-item label="现病史" prop="medical_history">
                    <el-input 
                      v-model="patientForm.medical_history" 
                      type="textarea" 
                      :rows="3"
                      placeholder="请描述您的现病史（可选）" 
                    />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-row :gutter="20">
                <el-col :span="24">
                  <el-form-item label="家族史" prop="family_history">
                    <el-input 
                      v-model="patientForm.family_history" 
                      type="textarea" 
                      :rows="3"
                      placeholder="请描述您的家族史（可选）" 
                    />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-row :gutter="20">
                <el-col :span="24">
                  <el-form-item label="用药史" prop="medications">
                    <el-input 
                      v-model="patientForm.medications" 
                      type="textarea" 
                      :rows="3" 
                      placeholder="请输入用药史（可选）" 
                    />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <!-- 表单操作按钮 -->
              <div class="form-actions">
                <el-button 
                  type="primary" 
                  size="large" 
                  @click="submitPatientForm" 
                  :loading="submitting"
                  :disabled="submitting"
                >
                  <el-icon><Check /></el-icon>
                  {{ submitting ? '提交中...' : '提交个人信息' }}
                </el-button>
                <el-button 
                  size="large" 
                  @click="resetPatientForm"
                  :disabled="submitting"
                >
                  <el-icon><Refresh /></el-icon>
                  重置表单
                </el-button>
              </div>
            </el-form>
          </div>

          <!-- 患者表格 -->
          <div class="patient-table-section">
            <div class="table-header">
              <h3>我的患者档案</h3>
              <p>以下是您的患者档案信息</p>
            </div>
            
            <el-table
              :data="filteredPatients"
              style="width: 100%"
              @row-click="handlePatientClick"
              :row-class-name="getRowClassName"
              highlight-current-row
            >
              <el-table-column prop="name" label="用户名称" width="120" />
              <el-table-column prop="level" label="病人等级" width="100">
                <template #default="{ row }">
                  <el-tag
                    :type="getLevelType(row.level)"
                    size="small"
                  >
                    {{ getLevelText(row.level) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="age" label="年龄" width="80" />
              <el-table-column prop="gender" label="性别" width="80" />
              <el-table-column prop="keyIndicator" label="关键指标" width="100" />
              <el-table-column prop="hospital" label="就医机构" min-width="150" />
              <el-table-column label="操作" width="120" fixed="right">
                <template #default="{ row }">
                  <el-button 
                    type="primary" 
                    size="small" 
                    @click.stop="viewPatient(row)"
                    :class="{ 'is-selected': selectedPatient?.id === row.id }"
                  >
                    {{ selectedPatient?.id === row.id ? '已选中' : '查看' }}
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>

        <!-- 右侧：患者详情 -->
        <div class="right-panel">
          <div v-if="selectedPatient" class="patient-detail">
            <div class="detail-header">
              <h2>患者综合信息档案-{{ selectedPatient.name }}</h2>
              <div class="file-info">
                <span>档案编号: {{ selectedPatient.fileNo }}</span>
                <span>生成日期: {{ selectedPatient.generateDate }}</span>
              </div>
            </div>

            <div class="detail-content">
              <!-- 基本信息 -->
              <div class="info-section">
                <h3>一、基本信息</h3>
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
                  <div class="info-item">
                    <span class="label">身份证号:</span>
                    <span class="value">{{ selectedPatient.idCard }}</span>
                  </div>
                  <div class="info-item">
                    <span class="label">地址:</span>
                    <span class="value">{{ selectedPatient.address }}</span>
                  </div>
                  <div class="info-item">
                    <span class="label">紧急联系人:</span>
                    <span class="value">{{ selectedPatient.emergencyContact }}</span>
                  </div>
                </div>
              </div>

              <!-- 临床诊断信息 -->
              <div class="info-section">
                <h3>二、临床诊断信息</h3>
                <div class="info-grid">
                  <div class="info-item">
                    <span class="label">主要诊断:</span>
                    <span class="value">{{ selectedPatient.diagnosis }}</span>
                  </div>
                  <div class="info-item">
                    <span class="label">患者等级:</span>
                    <el-tag :type="getLevelType(selectedPatient.level)" size="small">
                      {{ getLevelText(selectedPatient.level) }}
                    </el-tag>
                  </div>
                  <div class="info-item">
                    <span class="label">关键指标:</span>
                    <span class="value">{{ selectedPatient.keyIndicator }}</span>
                  </div>
                </div>
                <div class="bone-density-info">
                  <h4>骨密度详情</h4>
                  <div class="info-grid">
                    <div class="info-item">
                      <span class="label">检测方法:</span>
                      <span class="value">{{ selectedPatient.boneDensity.method }}</span>
                    </div>
                    <div class="info-item">
                      <span class="label">检测部位:</span>
                      <span class="value">{{ selectedPatient.boneDensity.site }}</span>
                    </div>
                    <div class="info-item">
                      <span class="label">T值:</span>
                      <span class="value">{{ selectedPatient.boneDensity.tScore }}</span>
                    </div>
                    <div class="info-item">
                      <span class="label">Z值:</span>
                      <span class="value">{{ selectedPatient.boneDensity.zScore }}</span>
                    </div>
                    <div class="info-item full-width">
                      <span class="label">结论:</span>
                      <span class="value">{{ selectedPatient.boneDensity.conclusion }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 病史与风险因素 -->
              <div class="info-section">
                <h3>三、病史与风险因素</h3>
                <div class="history-item">
                  <h4>现病史</h4>
                  <p>{{ selectedPatient.currentHistory }}</p>
                </div>
                <div class="history-item">
                  <h4>既往史</h4>
                  <p>{{ selectedPatient.pastHistory }}</p>
                </div>
                <div class="history-item">
                  <h4>个人史</h4>
                  <p>{{ selectedPatient.personalHistory }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <div v-else class="no-patient-selected">
            <el-empty description="请选择患者查看详细信息" />
          </div>
        </div>
      </div>

      <!-- 右侧历史记录栏 -->
      <div class="right-sidebar">
        <div class="sidebar-header">
          <h3>历史记录</h3>
        </div>
        <div class="history-list">
          <div v-if="historyRecords.length > 0">
            <div v-for="record in historyRecords" :key="record.id" class="history-item">
              <div class="history-content">
                <div class="history-title">{{ record.patientName }} - {{ record.action }}</div>
                <div class="history-date">{{ formatDate(record.timestamp) }}</div>
                <div class="history-desc">{{ record.description }}</div>
              </div>
              <el-button size="small" type="primary" @click="viewHistoryDetail(record)">查看</el-button>
            </div>
          </div>
          <div v-else class="no-history">
            <el-empty description="暂无历史记录" :image-size="60" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import { useUserStore } from '@/stores/user'
import { ElAlert, ElTooltip, ElIcon, ElInput, ElButton, ElSelect, ElOption, ElRow, ElCol, ElForm, ElFormItem, ElTable, ElTableColumn, ElTag, ElEmpty } from 'element-plus'
import { InfoFilled, Refresh, Check } from '@element-plus/icons-vue'

// 响应式数据
const userStore = useUserStore()
const selectedPatient = ref<any>(null)
const currentFilter = ref('all')
const searchKeyword = ref('')
const currentDate = ref(new Date())

// 历史记录数组
const historyRecords = ref<any[]>([])

// 真实患者数据（从API获取）
const patients = ref<any[]>([])

// 表单数据
const patientForm = ref({
  patient_id: '',
  name: '',
  age: '',
  gender: '',
  phone: '',
  email: '',
  height: '',
  weight: '',
  t_score: '',
  z_score: '',
  risk_level: 'low',
  address: '',
  medical_history: '',
  family_history: '',
  medications: '',
  created_at: ''
})

const patientFormRef = ref<any>(null)
const submitting = ref(false)
const submitSuccess = ref(false)

const patientFormRules = {
  patient_id: [{ required: true, message: '请输入档案编号', trigger: 'blur' }],
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  age: [{ required: true, message: '请输入年龄', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
  t_score: [{ required: true, message: '请输入T值', trigger: 'blur' }],
  z_score: [{ required: true, message: '请输入Z值', trigger: 'blur' }],
  risk_level: [{ required: true, message: '请选择风险等级', trigger: 'change' }],
  address: [{ required: true, message: '请输入地址', trigger: 'blur' }],
}

// 计算属性
const filteredPatients = computed(() => {
  let result = patients.value

  // 等级筛选
  if (currentFilter.value !== 'all') {
    result = result.filter(patient => patient.level === currentFilter.value)
  }

  // 关键词搜索
  if (searchKeyword.value.trim()) {
    const keyword = searchKeyword.value.toLowerCase().trim()
    result = result.filter(patient => 
      patient.name.toLowerCase().includes(keyword) ||
      patient.hospital?.toLowerCase().includes(keyword) ||
      patient.fileNo?.toLowerCase().includes(keyword)
    )
  }

  return result
})

// 获取患者数据
const fetchPatients = async () => {
  try {
    console.log('首页开始获取患者数据...')
    const response = await request.get('/v1/patients/')
    console.log('首页API响应:', response)
    console.log('response类型:', typeof response)
    console.log('response.data类型:', typeof response?.data)
    console.log('response.data内容:', response?.data)
    console.log('response.data.patients存在:', !!(response?.data as any)?.patients)
    
    let patientData: any[] = []
    
    // 兼容不同的API响应格式
    if (response && ((response as any).patients || response.data?.patients || Array.isArray(response) || Array.isArray(response.data))) {
      console.log('首页响应数据结构:', {
        hasPatients: !!((response as any).patients || response.data?.patients),
        patientsType: typeof ((response as any).patients || response.data?.patients),
        isArray: Array.isArray((response as any).patients || response.data?.patients),
        responseKeys: Object.keys(response),
        dataKeys: response.data ? Object.keys(response.data) : []
      })
      
      // 优先检查response.patients，然后检查response.data.patients
      const patientsData = (response as any).patients || response.data?.patients
      
      if (patientsData && Array.isArray(patientsData)) {
        // 标准格式：{ patients: [...], total: 3, page: 1, size: 10 }
        patientData = patientsData
        console.log('首页使用标准格式数据，患者数量:', patientData.length)
      } else if (Array.isArray(response) || Array.isArray(response.data)) {
        // 直接返回数组格式：[...]
        patientData = Array.isArray(response) ? response : response.data
        console.log('首页使用直接数组格式数据，患者数量:', patientData.length)
      } else {
        console.warn('首页响应数据结构不符合预期:', response)
        patientData = []
      }
    } else {
      console.warn('首页响应数据为空:', response)
      console.warn('response存在:', !!response)
      console.warn('response.patients存在:', !!(response as any)?.patients)
      console.warn('response.data存在:', !!response?.data)
      console.warn('response.data.patients存在:', !!(response?.data as any)?.patients)
      console.warn('response.data值:', response?.data)
      patientData = []
    }
    
    if (patientData.length > 0) {
      // 将后端数据格式转换为前端使用的格式
      patients.value = patientData.map((patient: any) => ({
        id: patient.id,
        name: patient.name,
        level: patient.risk_level || 'medium', // 映射风险等级
        age: patient.age,
        gender: patient.gender === 'male' ? '男' : '女',
        keyIndicator: patient.t_score || 0,
        hospital: '北京潞河医院', // 默认医院，可以从用户信息获取
        // 详细信息
        fileNo: patient.patient_id,
        generateDate: new Date(patient.created_at).toLocaleDateString('zh-CN'),
        phone: patient.phone || '未填写',
        idCard: '未填写', // 后端没有身份证字段
        address: patient.address || '未填写',
        emergencyContact: '未填写', // 后端没有紧急联系人字段
        diagnosis: '骨质疏松症', // 根据风险等级判断
        boneDensity: {
          method: 'DXA',
          site: '腰椎L1-L4及左股骨颈',
          tScore: patient.t_score || 0,
          zScore: patient.z_score || 0,
          conclusion: getBoneDensityConclusion(patient.t_score)
        },
        currentHistory: patient.medical_history || '无特殊症状',
        pastHistory: patient.family_history || '无重大疾病史',
        personalHistory: patient.medications || '无特殊个人史'
      }))
      
      // 默认选中第一个患者
      if (patients.value.length > 0) {
        const firstPatient = patients.value[0]
        selectedPatient.value = firstPatient
        addHistoryRecord(firstPatient)
        ElMessage.info(`已自动选择患者: ${firstPatient.name}`)
        console.log('首页成功加载患者数据，选中患者:', firstPatient.name)
      }
    } else {
      console.log('首页未获取到患者数据')
      patients.value = []
    }
    
  } catch (error: any) {
    console.error('获取患者数据失败:', error)
    ElMessage.error('获取患者数据失败，请检查网络连接')
    patients.value = []
  }
}

// 根据T值获取骨密度结论
const getBoneDensityConclusion = (tScore: number) => {
  if (tScore >= -1.0) return '骨密度正常'
  if (tScore >= -2.5) return '骨密度偏低，符合轻度骨质疏松症标准'
  if (tScore >= -3.0) return '骨密度明显偏低，符合中度骨质疏松症标准'
  return '骨密度显著偏低，符合重度骨质疏松症标准'
}

// 方法
const setFilter = (filter: string) => {
  currentFilter.value = filter
}

const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    ElMessage.success(`搜索"${searchKeyword.value}"完成，找到${filteredPatients.value.length}条记录`)
  } else {
    ElMessage.info('请输入搜索关键词')
  }
}

const handlePatientClick = (row: any) => {
  selectedPatient.value = row
  // 添加历史记录
  addHistoryRecord(row)
}

const addHistoryRecord = (patient: any) => {
  const record = {
    id: Date.now(),
    patientName: patient.name,
    patientId: patient.id,
    action: '查看患者信息',
    timestamp: new Date(),
    description: `查看了患者${patient.name}的基本信息`
  }
  
  // 检查是否已存在相同记录，避免重复
  const existingRecord = historyRecords.value.find(r => 
    r.patientId === patient.id && r.action === '查看患者信息'
  )
  
  if (!existingRecord) {
    historyRecords.value.unshift(record)
    // 限制历史记录数量，保留最近20条
    if (historyRecords.value.length > 20) {
      historyRecords.value = historyRecords.value.slice(0, 20)
    }
  }
}

const getRowClassName = ({ row }: { row: any }) => {
  return selectedPatient.value?.id === row.id ? 'selected-row' : ''
}

const getLevelType = (level: string) => {
  switch (level) {
    case 'high': return 'danger'
    case 'medium': return 'warning'
    case 'low': return 'success'
    default: return 'info'
  }
}

const getLevelText = (level: string) => {
  switch (level) {
    case 'high': return '高危'
    case 'medium': return '中危'
    case 'low': return '低危'
    default: return '未知'
  }
}

const viewPatient = (patient: any) => {
  selectedPatient.value = patient
  ElMessage.info(`已选择患者: ${patient.name}`)
  addHistoryRecord(patient)
}

const viewHistoryDetail = (record: any) => {
  // 根据历史记录找到对应的患者
  const patient = patients.value.find(p => p.id === record.patientId)
  if (patient) {
    selectedPatient.value = patient
    ElMessage.success(`已切换到患者${patient.name}的详细信息`)
  } else {
    ElMessage.error('患者信息不存在')
  }
}

// 格式化日期
const formatDate = (date: Date) => {
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 重新生成档案编号
const regeneratePatientId = () => {
  patientForm.value.patient_id = `PAT${Date.now().toString().slice(-6)}`
  ElMessage.success('档案编号已重新生成')
}

// 提交个人信息
const submitPatientForm = async () => {
  if (!patientFormRef.value) return

  await patientFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      submitting.value = true
      try {
        const response = await request.post('/v1/patients/', patientForm.value)
        console.log('提交个人信息成功:', response)
        ElMessage.success('个人信息提交成功！')
        submitSuccess.value = true
        // 刷新患者列表，以便新患者立即显示
        await fetchPatients()
        // 自动选中新患者
        if (patients.value.length > 0) {
          selectedPatient.value = patients.value[0]
          addHistoryRecord(patients.value[0])
        }
      } catch (error: any) {
        console.error('提交个人信息失败:', error)
        ElMessage.error('提交个人信息失败，请稍后再试')
      } finally {
        submitting.value = false
      }
    } else {
      ElMessage.error('请检查表单填写是否完整')
    }
  })
}

// 重置表单
const resetPatientForm = () => {
  if (patientFormRef.value) {
    patientFormRef.value.resetFields()
    submitSuccess.value = false
    ElMessage.info('表单已重置')
  }
}

// 生命周期
onMounted(async () => {
  // 只对机构用户获取患者数据，个人用户不需要
  if (userStore.user?.user_type === 'institutional') {
    await fetchPatients()
  } else {
    console.log('个人用户登录，跳过患者数据获取')
  }
})
</script>

<style scoped>
.home-container {
  display: flex;
  height: 100vh;
  background-color: #f5f5f5;
}

.institutional-home {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.personal-home {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.main-content {
  display: flex;
  gap: 20px;
  padding: 20px;
}

.left-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.right-panel {
  flex: 1;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 20px;
  overflow-y: auto;
}

.right-sidebar {
  width: 300px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin: 20px 20px 20px 0;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.search-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.patient-table-section {
  flex: 1;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.search-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.search-title {
  font-weight: 600;
  color: #333;
}

.filter-buttons {
  display: flex;
  gap: 8px;
}

.search-input-section {
  display: flex;
  gap: 10px;
  align-items: center;
}

.search-input {
  flex: 1;
}

.search-button {
  white-space: nowrap;
}

.detail-header {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.detail-header h2 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 20px;
  font-weight: 600;
}

.file-info {
  display: flex;
  gap: 20px;
  font-size: 14px;
  color: #666;
}

.info-section {
  margin-bottom: 25px;
}

.info-section h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
  border-left: 3px solid #667eea;
  padding-left: 10px;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-item.full-width {
  grid-column: 1 / -1;
}

.info-item .label {
  font-weight: 600;
  color: #333;
  min-width: 80px;
}

.info-item .value {
  color: #666;
  flex: 1;
}

.bone-density-info {
  margin-top: 15px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
}

.bone-density-info h4 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 14px;
  font-weight: 600;
}

.history-item {
  margin-bottom: 15px;
}

.history-item h4 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 14px;
  font-weight: 600;
}

.history-item p {
  margin: 0;
  color: #666;
  line-height: 1.5;
}

.selected-row {
  background-color: #e6f7ff !important;
}

.selected-row:hover {
  background-color: #d4f1ff !important;
}

/* 选中按钮样式 */
.el-button.is-selected {
  background: linear-gradient(135deg, #52c41a 0%, #389e0d 100%) !important;
  border-color: #52c41a !important;
  color: white !important;
  box-shadow: 0 2px 8px rgba(82, 196, 26, 0.3) !important;
}

.el-button.is-selected:hover {
  background: linear-gradient(135deg, #389e0d 0%, #237804 100%) !important;
  box-shadow: 0 4px 12px rgba(82, 196, 26, 0.4) !important;
  transform: translateY(-1px);
}

.no-patient-selected {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
}

.sidebar-header h3 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
  border-bottom: 2px solid #667eea;
  padding-bottom: 8px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.history-item {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 3px solid #667eea;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.history-content {
  flex: 1;
}

.history-title {
  font-weight: 600;
  color: #333;
  font-size: 15px;
  margin-bottom: 5px;
}

.history-date {
  font-size: 13px;
  color: #666;
  margin-bottom: 5px;
}

.history-desc {
  font-size: 13px;
  color: #999;
  margin-bottom: 10px;
}

.no-history {
  padding: 60px 20px;
  text-align: center;
}

/* 按钮样式 */
.el-button {
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.el-button--primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.el-button--primary:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  transform: translateY(-1px);
}

.el-button--default {
  border: 1px solid #dcdfe6;
  background: white;
  color: #606266;
}

.el-button--default:hover {
  border-color: #667eea;
  color: #667eea;
  background: #f8f9ff;
}

/* 表格样式 */
:deep(.el-table) {
  border-radius: 8px;
}

:deep(.el-table th) {
  background-color: #fafafa;
  color: #333;
  font-weight: 600;
}

.patient-row {
  cursor: pointer;
  transition: background-color 0.3s;
}

.patient-row:hover {
  background-color: #f5f7fa;
}

.form-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.form-header {
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.form-header h3 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.form-header p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.submit-success {
  margin-bottom: 20px;
  padding: 15px;
  background: #f0f9eb;
  border: 1px solid #e1f3d8;
  border-radius: 6px;
  color: #67c23a;
  font-size: 14px;
}

.patient-form {
  max-width: 800px;
  margin: 0 auto;
}

.auto-generated-field .el-input__inner {
  color: #909399;
  font-style: italic;
}

.field-hint {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-top: 5px;
  color: #909399;
  font-size: 12px;
}

.regenerate-btn {
  color: #409eff;
  font-size: 14px;
}

.regenerate-btn:hover {
  color: #66b1ff;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style> 