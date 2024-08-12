<script setup lang='ts'>
import { computed, useAttrs } from 'vue'
import { Icon } from '@iconify/vue'

// 定义组件的 Props 接口
interface Props {
  icon?: string // 可选的图标属性
}

// 使用 defineProps 定义组件的 Props
defineProps<Props>()

// 获取组件的所有属性
const attrs = useAttrs()

// 计算属性，用于绑定 class 和 style
const bindAttrs = computed<{ class: string; style: string }>(() => ({
  class: (attrs.class as string) || '', // 获取 class 属性，如果没有则为空字符串
  style: (attrs.style as string) || '', // 获取 style 属性，如果没有则为空字符串
}))
</script>

<template>
  <!-- Icon 组件，绑定传入的 icon 属性和计算的 class、style 属性 -->
  <Icon :icon="icon" v-bind="bindAttrs" />
</template>