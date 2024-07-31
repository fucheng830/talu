<template>
    <div class="flex flex-col flex-1 h-full">
      <n-input
        v-model:value="txtInput"
        type="textarea"
        round
        size="large"
        :autosize="{
          minRows: 1,
          maxRows: 5,
        }"
        :placeholder="placeholder"
        @focus="handleInputFocus"
        @blur="handleInputBlur"
        @keypress.prevent.enter="handleInputEnter"
      >
        <!-- 左侧 前缀 上传插件按钮-->
        <template #prefix>
          <div
            v-if="showUpload"
            class="h-full pr-1 cursor-pointer flex flex-col justify-center"
            @click.stop="handleUpload"
          >
            <Icon icon="gg:attachment" width="22" />
          </div>
        </template>
  
        <!-- 发送按钮 -->
        <template #suffix>
          <div class="h-full flex items-center">
            <div
              v-if="showMic"
              class="pr-2 cursor-pointer flex flex-col justify-center"
            >
              <Icon icon="material-symbols:mic" width="22" color="#7e7e7e" />
            </div>
            <div
              class="pl-[2px] border-l cursor-pointer flex flex-col justify-center"
              @click="handleSend"
            >
              <!-- 语音输入 -->
              <Icon
                icon="entypo:paper-plane"
                width="28"
              />
            </div>
          </div>
        </template>
      </n-input>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref} from "vue";
  import { Icon } from "@iconify/vue";
  import { defineProps, defineEmits } from "vue";

  
  interface Props {
    placeholder: string;
    showUpload: boolean;
    showMic: boolean;
  }
  
  defineProps<Props>();
  
  const txtInput = ref("");
  const emit = defineEmits(["send"]);
  
  
  const handleInputEnter = (event: KeyboardEvent) => {
    // 输入框回车处理
  };
  
  const handleSend = () => {
    console.log(txtInput.value);
    if (!txtInput.value) return;
    // 发送消息处理
    emit("send", txtInput.value);
  };
  
  const handleUpload = () => {
    // 上传处理
  };
  </script>
  
  <style scoped lang="less">
  /* 样式定义 */
  </style>
  