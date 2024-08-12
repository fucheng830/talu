<template>
  <!-- n-button 组件，带有颜色、圆角和点击事件 -->
  <n-button :color="bgcolor" round @click="emits('emit')">
    <!-- 自定义图标插槽 -->
    <template #icon>
      <!-- Icon 组件，显示传入的图标 -->
      <Icon :icon="icon" />
    </template>
    <!-- 按钮文本 -->
    <span> {{ label }} </span>
  </n-button>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";

// 定义组件的 props
defineProps({
  label: {
    type: String,
    default: "AI一键生成", // 默认按钮文本
  },
  icon: {
    type: String,
    default: "mingcute:bling-line", // 默认图标
  },
  bgcolor: {
    type: String, // 按钮背景颜色
  },
});

// 定义组件的 emits
const emits = defineEmits(["emit"]);
</script>

<style></style>