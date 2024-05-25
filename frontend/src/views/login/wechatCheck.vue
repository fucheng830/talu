<template>
    <div class="wechat-login-callback-page">
      <!-- 这里可以放置一些登录状态提示信息或者加载动画 -->
      <p v-if="loading">正在登录，请稍候...</p>
      <p v-else-if="error">登录失败，请重试。</p>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import { api } from "@/api/common"; // 假设你的API模块已经设置好了相关接口
  import { useUserStore } from "@/store"; // 假设你的Vuex store中有一个userStore模块
  import { useMessage } from "naive-ui"; // 使用naive-ui的消息提示功能
  
  const loading = ref(true);
  const error = ref(false);
  const router = useRouter();
  const userStore = useUserStore();
  const msg = useMessage();
  const referee = userStore.$state.invitecode; // 假设你的userStore中有一个referee状态
  
  onMounted(async () => {
    try {
      const url = new URL(window.location.href);
      const params = new URLSearchParams(url.search);
      const code = params.get('code');
      const state = params.get('state');
  
      if (code && state) {
        // 调用API进行微信登录
        const response = await api.wechat_login({ code, referee });
        // 更新user_info
        if (response.data) {
          userStore.updateUserInfo(response.data);
        }
        msg.success('登录成功');
        // 登录成功后重定向到首页
        router.replace('/');
      } else {
        throw new Error('授权码或状态码缺失');
      }
    } catch (e) {
      console.error('登录失败', e);
      msg.error('登录失败');
      error.value = true;
    } finally {
      loading.value = false;
    }
  });
  </script>
  
  <style scoped>
  .wechat-login-callback-page {
    /* 在这里添加你的样式 */
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    text-align: center;
  }
  
  /* 根据需要添加更多样式 */
  </style>