<template>
  <div class="flex flex-col flex-1 h-full" @paste="handlePaste">
    <!-- 缩略图展示区域 -->
    <div class="mb-1 flex flex-item"> <!-- 使用 grid 布局支持多图展示 -->
      <div v-for="(img, index) in imageData" :key="index" class="upload-preview mr-1">
        <img :src="img.url" class="thumbnail w-12 h-12 object-cover rounded" />
        <div class="w-12 h-1 bg-gray-200 relative bottom-2" v-if="img.progress < 100">
          <div class="h-full bg-green-500 transition-all duration-200" :style="{ width: `${img.progress}%` }"></div>
        </div>
          <!-- 删除按钮 -->
          <div class="absolute top-0 right-0">
          <Icon icon="mdi:close-circle" class="text-red-500 cursor-pointer" width="18" @click="removeImage(index)" />
        </div>
      </div>
    </div>
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
import { defineProps, defineEmits, ref } from "vue";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { useUserStore } from "@/store/modules/user";
import axios from 'axios';

// 定义组件的 Props 接口
interface Props {
  placeholder: string; // 输入框的占位符文本
  showUpload: boolean; // 是否显示上传按钮
  showMic: boolean; // 是否显示麦克风按钮
  data: any; // 传入的数据
  imgData: any; // 图片数据
}

const userStore = useUserStore();
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

// 处理粘贴事件
const handlePaste = (event: ClipboardEvent) => {
  const items = event.clipboardData?.items;
  if (items) {
    for (let i = 0; i < items.length; i++) {
      const item = items[i];
      if (item.type.indexOf("image") !== -1) {
        const file = item.getAsFile();
        if (file) {
          showImagePreview(file);
          uploadImage(file);
        }
      }
    }
  }
};

// 显示图像预览
const imageData = ref<{ url: string | null, progress: number }[]>([]);
const showImagePreview = (file: File) => {
  const reader = new FileReader();
  reader.onload = (e) => {
    imageData.value.push({
      url: e.target?.result as string,
      progress: 0
    });
  };
  reader.readAsDataURL(file);
};

// 上传图片到服务
const uploadImage = async (file: File) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const baseURL: string = import.meta.env.VITE_GLOB_API_URL;
    const url = new URL('/upload_file', baseURL).toString();
    const token = userStore.$state.userInfo?.access_token;
    
    const response = await axios.post(url, formData, {
      headers: {
        Authorization: token ? `Bearer ${token}` : '',
      },
      onUploadProgress: (event) => {
      console.log(event); // 添加调试输出
      const index = imageData.value.length - 1;
      
      imageData.value[index].progress = (Math.round((event.loaded ) / event.total))*100;
      console.log(imageData.value[index].progress)
    }

    });
    
    if (response.status !== 200) {
      throw new Error(`上传失败: ${response.statusText}`);
    }

    const result = response.data;
    console.log('上传成功:', result);
    // 在这里你可以处理服务器返回的数据，例如将图片 URL 添加到输入框内容中
  } catch (error) {
    console.error('图片上传失败:', error);
  }
};
</script>

<style scoped lang="less">
.upload-preview {
  position: relative;
}
.ellipsis {
      width: 200px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
}
</style>
