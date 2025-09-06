<template>
  <div class="not-found-page">
    <div class="not-found-content">
      <h1>404</h1>
      <h2>页面未找到</h2>
      <p>抱歉，您访问的页面不存在</p>
      <el-button type="primary" @click="$router.push('/')">
        返回首页
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
// 404页面逻辑
</script>

<style scoped>
.not-found-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  text-align: center;
}

.not-found-content h1 {
  font-size: 6rem;
  margin: 0;
  font-weight: bold;
}

.not-found-content h2 {
  font-size: 2rem;
  margin: 20px 0;
}

.not-found-content p {
  font-size: 1.2rem;
  margin-bottom: 30px;
  opacity: 0.8;
}
</style> 