<script setup lang="ts">
import { defineComponent, h } from 'vue'
import {
  NDialogProvider,
  NLoadingBarProvider,
  NMessageProvider,
  NNotificationProvider,
  useDialog,
  useLoadingBar,
  useMessage,
  useNotification,
} from 'naive-ui'

// 注册 Naive UI 工具到全局 window 对象
function registerNaiveTools() {
  window.$loadingBar = useLoadingBar()
  window.$dialog = useDialog()
  window.$message = useMessage()
  window.$notification = useNotification()
}

// 定义 NaiveProviderContent 组件
const NaiveProviderContent = defineComponent({
  name: 'NaiveProviderContent',
  setup() {
    // 在 setup 阶段注册 Naive UI 工具
    registerNaiveTools()
  },
  render() {
    // 渲染一个空的 div 元素
    return h('div')
  },
})
</script>

<template>
  <!-- 提供 Naive UI 的 LoadingBar 功能 -->
  <NLoadingBarProvider>
    <!-- 提供 Naive UI 的 Dialog 功能 -->
    <NDialogProvider>
      <!-- 提供 Naive UI 的 Notification 功能 -->
      <NNotificationProvider>
        <!-- 提供 Naive UI 的 Message 功能 -->
        <NMessageProvider>
          <!-- 插槽，用于嵌入子组件 -->
          <slot />
          <!-- 渲染 NaiveProviderContent 组件 -->
          <NaiveProviderContent />
        </NMessageProvider>
      </NNotificationProvider>
    </NDialogProvider>
  </NLoadingBarProvider>
</template>