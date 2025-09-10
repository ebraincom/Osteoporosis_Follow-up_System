import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Welcome',
      component: () => import('@/views/Welcome.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/Register.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('@/views/Dashboard.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'Home',
          component: () => import('@/views/dashboard/Home.vue')
        },
        {
          path: 'data-collection',
          name: 'DataCollection',
          redirect: '/dashboard/data-collection/his',
          children: [
            {
              path: 'his',
              name: 'HIS',
              component: () => import('@/views/dashboard/data-collection/HIS.vue')
            },
            {
              path: 'validation',
              name: 'Validation',
              component: () => import('@/views/dashboard/data-collection/Validation.vue')
            },
            {
              path: 'voice',
              name: 'Voice',
              component: () => import('@/views/dashboard/data-collection/Voice.vue')
            },
            {
              path: 'diet',
              name: 'Diet',
              component: () => import('@/views/dashboard/data-collection/Diet.vue')
            }
          ]
        },
        {
          path: 'followup',
          name: 'Followup',
          redirect: '/dashboard/followup/search',
          children: [
            {
              path: 'search',
              name: 'FollowupSearch',
              component: () => import('@/views/dashboard/followup/Search.vue')
            },
            {
              path: 'records',
              name: 'FollowupRecords',
              component: () => import('@/views/dashboard/followup/Records.vue')
            },
            {
              path: 'response',
              name: 'FollowupResponse',
              component: () => import('@/views/dashboard/followup/Response.vue')
            },
            {
              path: 'settings',
              name: 'FollowupSettings',
              component: () => import('@/views/dashboard/followup/Settings.vue')
            }
          ]
        },
        // 个人用户随访跟踪路由
        {
          path: 'personal-followup',
          name: 'PersonalFollowup',
          redirect: '/dashboard/personal-followup/my-records',
          children: [
            {
              path: 'my-records',
              name: 'PersonalFollowupRecords',
              component: () => import('@/views/dashboard/personal-followup/MyRecords.vue')
            },
            {
              path: 'my-schedule',
              name: 'PersonalFollowupSchedule',
              component: () => import('@/views/dashboard/personal-followup/MySchedule.vue')
            },
            {
              path: 'my-reminders',
              name: 'PersonalFollowupReminders',
              component: () => import('@/views/dashboard/personal-followup/MyReminders.vue')
            },
            {
              path: 'my-responses',
              name: 'PersonalFollowupResponses',
              component: () => import('@/views/dashboard/personal-followup/MyResponses.vue')
            }
          ]
        },
        {
          path: 'ai',
          name: 'AI',
          redirect: '/dashboard/ai/voice-interaction',
          children: [
            {
              path: 'voice-interaction',
              name: 'VoiceInteraction',
              component: () => import('@/views/dashboard/ai/VoiceInteraction.vue')
            },
            {
              path: 'intelligent-qa',
              name: 'IntelligentQA',
              component: () => import('@/views/dashboard/ai/IntelligentQA.vue')
            },
            {
              path: 'analysis-decision',
              name: 'AnalysisDecision',
              component: () => import('@/views/dashboard/ai/AnalysisDecision.vue')
            },
            {
              path: 'digital-companion',
              name: 'DigitalCompanion',
              component: () => import('@/views/dashboard/ai/DigitalCompanion.vue')
            },
            {
              path: 'fall-warning',
              name: 'FallWarning',
              component: () => import('@/views/dashboard/ai/FallWarning.vue')
            }
          ]
        },
        {
          path: 'settings',
          name: 'Settings',
          redirect: '/dashboard/settings/profile',
          children: [
            {
              path: 'profile',
              name: 'Profile',
              component: () => import('@/views/dashboard/settings/Profile.vue')
            },
            {
              path: 'privacy',
              name: 'Privacy',
              component: () => import('@/views/dashboard/settings/Privacy.vue')
            },
            {
              path: 'version',
              name: 'Version',
              component: () => import('@/views/dashboard/settings/Version.vue')
            },
            {
              path: 'help',
              name: 'Help',
              component: () => import('@/views/dashboard/settings/Help.vue')
            }
          ]
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/NotFound.vue')
    }
  ]
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  console.log('路由守卫执行:', {
    to: to.path,
    from: from.path,
    isInitialized: userStore.isInitialized,
    hasToken: !!userStore.token,
    isAuthenticated: userStore.isAuthenticated,
    tokenValue: userStore.token ? userStore.token.substring(0, 20) + '...' : null,
    localStorageToken: localStorage.getItem('token') ? localStorage.getItem('token')?.substring(0, 20) + '...' : null
  })
  
  // 如果还没有初始化，先初始化
  if (!userStore.isInitialized) {
    console.log('路由守卫：用户状态未初始化，开始初始化...')
    userStore.initializeAuth()
  }
  
  // 等待用户状态初始化完成
  if (!userStore.isInitialized) {
    console.log('路由守卫：等待用户状态初始化完成...')
    next(false) // 阻止导航，等待初始化
    return
  }
  
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    console.log('路由守卫：用户未认证，跳转到登录页')
    console.log('路由守卫：认证状态详情:', {
      requiresAuth: to.meta.requiresAuth,
      isAuthenticated: userStore.isAuthenticated,
      hasToken: !!userStore.token,
      tokenValue: userStore.token
    })
    next('/login')
  } else if (to.path === '/login' && userStore.isAuthenticated) {
    console.log('路由守卫：用户已认证，跳转到仪表板')
    next('/dashboard')
  } else {
    console.log('路由守卫：允许导航到', to.path)
    next()
  }
})

export default router 