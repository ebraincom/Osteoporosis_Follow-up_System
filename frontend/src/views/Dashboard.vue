<template>
  <div class="dashboard">
    <!-- 顶部导航栏 -->
    <el-header class="header">
      <div class="header-left">
        <h1 class="system-title">骨质疏松症跟踪随访系统</h1>
      </div>
             <div class="header-center">
         <div class="top-nav">
           <el-button 
             type="text" 
             class="nav-btn" 
             :class="{ 'active': isHomeActive }"
             @click="navigateToHome"
           >
             首页
           </el-button>
           <el-button 
             type="text" 
             class="nav-btn" 
             :class="{ 'active': isFollowupActive }"
             @click="navigateToFollowup"
           >
             随访跟踪
           </el-button>
           <el-button 
             type="text" 
             class="nav-btn" 
             :class="{ 'active': isDataCollectionActive }"
             @click="navigateToDataCollection"
           >
             数据采集
           </el-button>
           <el-button 
             type="text" 
             class="nav-btn" 
             :class="{ 'active': isAIActive }"
             @click="navigateToAI"
           >
             AI辅助
           </el-button>
           <el-button 
             type="text" 
             class="nav-btn" 
             :class="{ 'active': isSettingsActive }"
             @click="navigateToSettings"
           >
             我的设置
           </el-button>
         </div>
       </div>
      <div class="header-right">
        <div class="user-info">
          <span class="info-item">用户名: {{ userStore.user?.username }}</span>
          <span class="info-item">
            {{ userStore.user?.user_type === 'institutional' 
              ? `机构: ${userStore.user?.institution || '未知机构'}${userStore.user?.department ? ' - ' + userStore.user.department : ''}`
              : '个人用户'
            }}
          </span>
          <span class="info-item">登陆时间: {{ loginTime }}</span>
        </div>
        <el-button 
          type="danger" 
          size="small" 
          @click="handleLogout"
          class="logout-btn"
        >
          退出登录
        </el-button>
      </div>
    </el-header>

    <el-container class="main-container">
             <!-- 左侧边栏 -->
       <el-aside :width="isCollapse ? '64px' : '250px'" class="sidebar">
         <div class="sidebar-header">
           <h3 class="sidebar-title">{{ sidebarTitle }}</h3>
         </div>
         
         <el-menu
           :default-active="activeMenu"
           :collapse="isCollapse"
           router
           class="sidebar-menu"
         >
           <!-- 数据采集菜单 -->
           <template v-if="isDataCollectionActive">
             <el-menu-item index="/dashboard/data-collection/his">
               <el-icon><User /></el-icon>
               <template #title>医院HIS接口</template>
             </el-menu-item>

             <el-menu-item index="/dashboard/data-collection/validation">
               <el-icon><Check /></el-icon>
               <template #title>校验规则</template>
             </el-menu-item>

             <el-menu-item index="/dashboard/data-collection/voice">
               <el-icon><Document /></el-icon>
               <template #title>语音录入</template>
             </el-menu-item>

             <el-menu-item index="/dashboard/data-collection/diet">
               <el-icon><Food /></el-icon>
               <template #title>饮食记录</template>
             </el-menu-item>
           </template>

           <!-- 随访跟踪菜单 - 根据用户类型显示 -->
           <template v-if="isFollowupActive">
             <!-- 机构用户菜单 -->
             <template v-if="userStore.user?.user_type === 'institutional'">
               <el-menu-item index="/dashboard/followup/search">
                 <el-icon><Search /></el-icon>
                 <template #title>患者检索</template>
               </el-menu-item>

               <el-menu-item index="/dashboard/followup/records">
                 <el-icon><Document /></el-icon>
                 <template #title>随访记录</template>
               </el-menu-item>

               <el-menu-item index="/dashboard/followup/response">
                 <el-icon><ChatDotRound /></el-icon>
                 <template #title>随访回复</template>
               </el-menu-item>

               <el-menu-item index="/dashboard/followup/settings">
                 <el-icon><Setting /></el-icon>
                 <template #title>随访设置</template>
               </el-menu-item>
             </template>

             <!-- 个人用户菜单 -->
             <template v-else>
               <el-menu-item index="/dashboard/personal-followup/my-records">
                 <el-icon><Document /></el-icon>
                 <template #title>我的随访记录</template>
               </el-menu-item>

               <el-menu-item index="/dashboard/personal-followup/my-schedule">
                 <el-icon><Calendar /></el-icon>
                 <template #title>随访计划</template>
               </el-menu-item>

               <el-menu-item index="/dashboard/personal-followup/my-reminders">
                 <el-icon><Bell /></el-icon>
                 <template #title>随访提醒</template>
               </el-menu-item>

               <el-menu-item index="/dashboard/personal-followup/my-responses">
                 <el-icon><ChatDotRound /></el-icon>
                 <template #title>随访回复</template>
               </el-menu-item>
             </template>
           </template>

            <!-- AI辅助菜单 -->
            <template v-if="isAIActive">
              <el-menu-item index="/dashboard/ai/voice-interaction">
                <el-icon><Microphone /></el-icon>
                <template #title>语音交互</template>
              </el-menu-item>

              <el-menu-item index="/dashboard/ai/intelligent-qa">
                <el-icon><ChatDotRound /></el-icon>
                <template #title>智能问答</template>
              </el-menu-item>

              <el-menu-item index="/dashboard/ai/analysis-decision">
                <el-icon><TrendCharts /></el-icon>
                <template #title>分析与决策</template>
              </el-menu-item>

              <el-menu-item index="/dashboard/ai/digital-companion">
                <el-icon><UserFilled /></el-icon>
                <template #title>数字人情感陪伴</template>
              </el-menu-item>

              <el-menu-item index="/dashboard/ai/fall-warning">
                <el-icon><Bell /></el-icon>
                <template #title>跌倒预警</template>
              </el-menu-item>
            </template>

            <!-- 我的设置菜单 -->
            <template v-if="isSettingsActive">
              <el-menu-item index="/dashboard/settings/profile">
                <el-icon><User /></el-icon>
                <template #title>个人信息</template>
              </el-menu-item>

              <el-menu-item index="/dashboard/settings/privacy">
                <el-icon><Check /></el-icon>
                <template #title>隐私条款</template>
              </el-menu-item>

              <el-menu-item index="/dashboard/settings/version">
                <el-icon><Document /></el-icon>
                <template #title>版本号</template>
              </el-menu-item>

              <el-menu-item index="/dashboard/settings/help">
                <el-icon><QuestionFilled /></el-icon>
                <template #title>帮助</template>
              </el-menu-item>
            </template>
         </el-menu>
       </el-aside>

      <!-- 主内容区 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import {
  User,
  Check,
  Document,
  Picture,
  Monitor,
  Microphone,
  ChatDotRound,
  TrendCharts,
  UserFilled,
  Bell,
  QuestionFilled,
  Search,
  Setting,
  Calendar,
  Food
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isCollapse = ref(false)
const loginTime = ref('')

const activeMenu = computed(() => route.path)

// 判断当前路由的计算属性
const isHomeActive = computed(() => route.path === '/dashboard')
const isDataCollectionActive = computed(() => route.path.startsWith('/dashboard/data-collection'))
const isAIActive = computed(() => route.path.startsWith('/dashboard/ai'))
const isSettingsActive = computed(() => route.path.startsWith('/dashboard/settings'))
const isFollowupActive = computed(() => route.path.startsWith('/dashboard/followup') || route.path.startsWith('/dashboard/personal-followup'))

// 侧边栏标题
const sidebarTitle = computed(() => {
  if (isDataCollectionActive.value) return '数据采集'
  if (isAIActive.value) return 'AI辅助'
  if (isSettingsActive.value) return '我的设置'
  if (isFollowupActive.value) return '跟踪随访'
  return '系统导航'
})

const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value
}

// 导航方法
const navigateToHome = () => {
  router.push('/dashboard')
}

const navigateToDataCollection = () => {
  router.push('/dashboard/data-collection')
}

const navigateToAI = () => {
  router.push('/dashboard/ai')
}

const navigateToSettings = () => {
  router.push('/dashboard/settings')
}

const navigateToFollowup = () => {
  router.push('/dashboard/followup')
}

const handleUserCommand = async (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/dashboard/settings')
      break
    case 'settings':
      router.push('/dashboard/settings')
      break
    case 'logout':
      try {
        await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        userStore.logout()
        router.push('/login')
      } catch {
        // 用户取消
      }
      break
  }
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    userStore.logout()
    router.push('/login')
  } catch {
    // 用户取消
  }
}

onMounted(() => {
  // 设置登录时间
  const now = new Date()
  loginTime.value = now.toLocaleString('zh-CN')
})
</script>

<style scoped>
.dashboard {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header-left {
  flex: 1;
  display: flex;
  align-items: center;
}

.system-title {
  font-size: 1.5rem;
  margin: 0;
  font-weight: bold;
}

.header-center {
  flex: 2;
  display: flex;
  justify-content: center;
  align-items: center;
}

.top-nav {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 400px;
}

.nav-btn {
  color: white;
  font-size: 0.9rem;
  padding: 8px 16px;
  flex: 1;
  margin: 0 4px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.nav-btn:hover {
  background: rgba(255,255,255,0.1);
  transform: translateY(-1px);
}

.nav-btn.active {
  background: rgba(255,255,255,0.2);
  font-weight: 600;
  border-bottom: 2px solid white;
}

.header-right {
  flex: 1;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 20px;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}

.info-item {
  font-size: 0.8rem;
  opacity: 0.9;
  max-width: 200px;
  word-wrap: break-word;
  text-align: left;
}

.logout-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-1px);
}

.main-container {
  flex: 1;
  overflow: hidden;
}

.sidebar {
  background: #f8f9fa;
  border-right: 1px solid #e9ecef;
  transition: width 0.3s;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #e9ecef;
}

.sidebar-title {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
  font-weight: 600;
}

.sidebar-menu {
  border: none;
  background: transparent;
}

.main-content {
  padding: 0;
  background: #f5f5f5;
  overflow: auto;
}
</style> 