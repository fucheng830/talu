<template>
  <div class="flex flex-col flex-1 h-full">
    <n-input
      v-model:value="data.txtInput"
      type="textarea"
      round
      size="large"
      :autosize="{
        minRows: 1,
        maxRows: 5,
      }"
      :placeholder="placeholder"
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
            <!-- 发送按钮 -->
            <Icon icon="entypo:paper-plane" width="28" />
          </div>
        </div>
      </template>
    </n-input>
  </div>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";
import { defineProps, defineEmits } from "vue";
import { useBasicLayout } from "@/hooks/useBasicLayout";
// 定义组件的 Props 接口
interface Props {
  placeholder: string; // 输入框的占位符文本
  showUpload: boolean; // 是否显示上传按钮
  showMic: boolean; // 是否显示麦克风按钮
  data: any; // 传入的数据
}

const { isMobile } = useBasicLayout();
// 使用 defineProps 定义组件的 Props
const props = defineProps<Props>();

// 定义组件的 emits
const emit = defineEmits(["send"]);

// 输入框回车处理函数
const handleInputEnter = (event: KeyboardEvent) => {
	// 移动端
	if (isMobile.value) {
		if (event.key === "Enter" && event.ctrlKey) {
			handleSend();
		}
		return;
	}

	// 非移动端
	// shift + enter 换行
	if (event.key === "Enter" && event.shiftKey) {
		props.data.txtInput += "\n";
		return;
	}
	handleSend();
};

// 发送按钮点击处理函数
const handleSend = () => {
  emit("send");
};

// 上传按钮点击处理函数
const handleUpload = () => {
  // 上传处理逻辑
};
</script>

<style scoped lang="less">
/* 样式定义 */
</style>