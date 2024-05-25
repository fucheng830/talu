<template>
  <m-modal
    ref="refModal"
    title="激活码激活会员"
    txtConfirm="激活"
    @onPositiveClick="onPositiveClick"
    @onNegativeClick="onNegativeClick"
  >
    <div class="mt-8">
      <n-input
        v-model:value="data.form.activateKey"
        type="text"
        placeholder="请输入激活码激活会员"
      />
    </div>
  </m-modal>
</template>

<script setup lang="ts">
import mModal from "@/components/common/mModal/index.vue";
import { reactive, ref } from "vue";

const refModal = ref();
const data = reactive({
  form: {
    activateKey: "",
  },
});

// 激活 激活码
const onPositiveClick = () => {
  console.log("activateKey", data.form.activateKey);
};

// 取消
const onNegativeClick = () => {
  changeModalShow();
};

// 改变模态框显示
const changeModalShow = () => {
  if (refModal.value && refModal.value.showModal) {
    refModal.value.showModal = !refModal.value.showModal; // 假设showModal是控制显示的reactive property
  } else {
    console.error('Modal component is not properly referenced');
  }
};

// 暴露方法给父组件
defineExpose({
  changeModalShow,
});
</script>

<style></style>
