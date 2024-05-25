<template>
    <NModal :show="props.show" style="width: 90%; max-width: 640px">
      <div class="p-10 bg-white rounded dark:bg-slate-800">
        <div class="flex items-center px-[24px] justify-end">
            <Icon
            icon="simple-line-icons:close"
                width="22"
                color="#4D5052"
                @click="emit('closeModal')"
            />
        </div>
        <div class="space-y-4">
          <header class="space-y-2">
            <h2 class="text-2xl font-bold text-center text-slate-800 dark:text-neutral-200">
              微信扫码支付
            </h2>
          </header>
          <div>
            <div class="w-full flex items-center justify-center h-full">
              <canvas ref="canvas" />
            </div>
            <div class="w-full text-center">{{ checkMsg }}</div>
          </div>
          <div>
            <div class="text-center text-gray-500">
              <span>支付即代表您已阅读并同意</span>
              <a href="/#/content" target="_blank" class="text-blue-500">《隐私政策》</a>
              <span>和</span>
              <a href="/#/content/rule" target="_blank" class="text-blue-500">《服务条款》</a>
            </div>
          </div>
          <div>
            <div class="text-center text-gray-500">
              <span>支付遇到问题？</span>
              <a href="https://work.weixin.qq.com/kfid/kfcf34773bc3f87c4f1" target="_blank" class="text-blue-500">联系客服</a>
            </div>
          </div>
        </div>
      </div>
    </NModal>
  </template>
  
  <script setup lang="ts">
  import { ref, watch, defineProps, defineEmits } from 'vue'
  import { NModal, useMessage } from 'naive-ui'
  import { Icon } from "@iconify/vue";
  import { useUserStore } from '@/store'
  import { api } from '@/api/common'
  import QRCode from 'qrcode'
  
  const props = defineProps({
    orderId: Number,
    QrUrl: String,
    show: Boolean
  })
  const emit = defineEmits(['closeModal'])
  
  const userStore = useUserStore()
  const message = useMessage()
  
  const checkMsg = ref('')
  const canvas = ref<HTMLElement | null>(null)
  
  const generateQRCode = () => {
    if (canvas.value) {
      QRCode.toCanvas(canvas.value,  props.QrUrl, (error: any) => {
        if (error) console.error(error)
      })
    }
  }
  
  const waitPay = () => {
    let countDown = 60
    checkMsg.value = `二维码将在${countDown}秒后失效`
    const timer = setInterval(() => {
      if (countDown <= 0) {
        clearInterval(timer)
      } else {
        countDown--
        checkMsg.value = `二维码将在${countDown}秒后失效`
        if (countDown % 4 === 0) {
          api.check_order({order_id:props.orderId}).then((response) => {
            if (response?.status === 'paid') {
              message.success('购买成功')
              userStore.updateUserInfo({ vip_end_time: response?.vip_end_time, 'plan': response?.plan})
              // 触发事件关闭弹窗
              emit('closeModal')
              clearInterval(timer)
              window.location.reload()
            }
          }).catch((err) => {
            console.log('订单未支付', err.message)
          })
        }
      }
    }, 1000)
  }

  
  watch(() => props.show, (newVal) => {
  if (newVal) {
    waitPay()
  }
})
watch(canvas, (newVal) => {
  if (newVal)
    generateQRCode()
})
  </script>
  
  
  <style scoped>
  </style>
  