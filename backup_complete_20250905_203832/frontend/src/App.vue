<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

onMounted(async () => {
  console.log('App.vue: 开始初始化用户状态')
  
  // 同步初始化用户状态
  userStore.initializeAuth()
  console.log('App.vue: 用户状态初始化完成', {
    isInitialized: userStore.isInitialized,
    hasToken: !!userStore.token,
    isAuthenticated: userStore.isAuthenticated
  })
  
  // 异步验证用户状态（如果需要）
  if (userStore.token && !userStore.user) {
    console.log('App.vue: 开始验证用户状态')
    try {
      await userStore.checkAuthStatus()
      console.log('App.vue: 用户状态验证完成', {
        hasUser: !!userStore.user,
        isAuthenticated: userStore.isAuthenticated
      })
    } catch (error) {
      console.error('App.vue: 用户状态验证失败', error)
    }
  }
})
</script>

<style>
#app {
  height: 100vh;
  font-family: 'Microsoft YaHei', Arial, sans-serif;
}
</style> 