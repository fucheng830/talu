<script setup lang="ts">
import { defineProps, onMounted, ref, watch } from 'vue'
import QRCode from 'qrcode'

// 定义组件的 props，接收一个 url 参数
const props = defineProps(['url'])

// 创建一个对 canvas 元素的引用
const canvas = ref(null)

// 生成二维码的函数
const generateQRCode = () => {
  QRCode.toCanvas(canvas.value, props.url, (error: any) => {
    if (error)
      console.error(error) // 如果生成二维码时发生错误，打印错误信息
  })
}

// 在组件挂载时生成二维码
onMounted(() => {
  if (canvas.value)
    generateQRCode()
})

// 监听 canvas 引用的变化，当 canvas 被赋值后生成二维码
watch(canvas, (newVal) => {
  if (newVal)
    generateQRCode()
})
</script>

<template>
  <!-- 布局容器，居中对齐 -->
  <div class="w-full flex items-center justify-center w-full h-full">
    <!-- canvas 元素，用于绘制二维码 -->
    <canvas ref="canvas" />
  </div>
</template>