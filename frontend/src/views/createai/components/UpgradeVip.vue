<template>
  <n-modal v-model:show="data.showModal" preset="dialog" title="Dialog">
    <template #header>
      <div>提示</div>
    </template>

    创建应用为专业版功能，开通专业版后即可使用

    <template #action>
      <n-button ghost size="small" @click="changeModalShow">
        <span> 取消</span>
      </n-button>
      <n-button color="blue" size="small" @click="router.push('/vipPay')">
        <span> 前往开通 </span>
      </n-button>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const data = reactive({
  showModal: false,
});

// 改变显示状态
const changeModalShow = () => {
  data.showModal = !data.showModal;
};

// 暴露方法给父组件
defineExpose({
  changeModalShow,
});
</script>

<style></style>
