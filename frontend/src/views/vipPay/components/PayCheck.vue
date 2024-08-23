<template>
  <n-modal :show="props.show" style="width: 90%; max-width: 640px">
    <div class="p-10 bg-white rounded dark:bg-slate-800">
      <div class="space-y-4">
        <header class="space-y-2">
          <h2 class="font-bold text-center text-slate-800 dark:text-neutral-200">
            请确认微信支付是否完成
          </h2>
        </header>
        <div class="completed-payment font-bold text-center text-blue-500 cursor-pointer">
          <span @click="checkOrder">已完成支付</span>
        </div>
        <div class="text-center text-gray-500">
          <span>支付遇到问题？</span>
        </div>
      </div>
    </div>
  </n-modal>
</template>

<script lang="ts" setup>
import { api } from '@/api/common'
import { useUserStore } from '@/store'
import { useMessage } from 'naive-ui'

const props = defineProps({
  orderId: Number,
  show: Boolean
});

  
const userStore = useUserStore()
  const message = useMessage()

const checkOrder = async () => {
  // Check if the order is paid
  const response = await api.check_order({order_id:props.orderId})
  if (response?.status === 'paid') {
    message.success('购买成功')
    userStore.updateUserInfo({ vip_end_time: response?.vip_end_time, 'plan': response?.plan})
    // 触发事件关闭弹窗
    emit('close')
    window.location.reload()
  }

};

const emit = defineEmits(['close']);
</script>

<style scoped>

</style>
