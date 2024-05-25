<script setup lang="ts">
import { defineProps, onMounted, ref, watch } from 'vue'
import QRCode from 'qrcode'

const props = defineProps(['url'])

const canvas = ref(null)

const generateQRCode = () => {
  QRCode.toCanvas(canvas.value, props.url, (error: any) => {
    if (error)
      console.error(error)
  })
}

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
  <div class="w-full flex items-center justify-center w-full h-full">
    <canvas ref="canvas" />
  </div>
</template>
