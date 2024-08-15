<template>
  <div class="flex flex-col flex-1 h-full" @paste="handlePaste">
    <!-- 缩略图展示区域 -->
    <div class="mb-1 flex flex-item"> <!-- 使用 grid 布局支持多图展示 -->
      <div v-for="(item, index) in fileData" :key="index" class="upload-preview mr-1">
        <img v-if="item.type.startsWith('image/')" :src="item.url ?? ''" class="thumbnail w-12 h-12 object-cover rounded" />
        <video v-else-if="item.type.startsWith('video/')" :src="item.url ?? ''" class="thumbnail w-12 h-12 object-cover rounded" controls />
        <audio v-else-if="item.type.startsWith('audio/')" :src="item.url ?? ''" class="thumbnail w-12 h-12 object-cover rounded" controls />
        <div class="w-12 h-1 bg-gray-200 relative bottom-2" v-if="item.progress < 100">
          <div class="h-full bg-green-500 transition-all duration-200" :style="{ width: `${item.progress}%` }"></div>
        </div>
        <div class="absolute top-0 right-0">
          <Icon icon="mdi:close-circle" class="text-red-500 cursor-pointer" width="18" @click="removeFile(index)" />
        </div>
      </div>
    </div>
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
import { defineProps, defineEmits, ref, withDefaults } from "vue";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { useUserStore } from "@/store/modules/user";
import axios from 'axios';

interface Props {
  placeholder: string; // 输入框的占位符文本
  showUpload: boolean; // 是否显示上传按钮
  showMic: boolean; // 是否显示麦克风按钮
  fileTypes: string[]; // 可接受的文件类型
}

// 使用 defineProps 和 withDefaults 设置默认值
const props = withDefaults(defineProps<Props>(), {
  fileTypes: ['image/png', 'image/jpeg', 'image/gif', 'application/pdf', 'video/mp4', 'audio/mpeg'] // 默认支持的文件类型
});

const userStore = useUserStore();
const { isMobile } = useBasicLayout();
const emit = defineEmits(["send"]);

// 组件内的状态
const txtInput = ref('');
const fileData = ref<Chat.FileData[]>([]);

// 输入框回车处理函数
const handleInputEnter = (event: KeyboardEvent) => {
  if (isMobile.value) {
    if (event.key === "Enter" && event.ctrlKey) {
      handleSend();
    }
    return;
  }

  if (event.key === "Enter" && event.shiftKey) {
    txtInput.value += "\n";
    return;
  }
  handleSend();
};

// 发送按钮点击处理函数
const handleSend = () => {
  if (txtInput.value.trim() === "") return;
  emit("send", txtInput.value, fileData.value);
  // 清空输入框数据
  txtInput.value = "";
  fileData.value = [];
};

// 上传按钮点击处理函数
const handleUpload = () => {
  // 上传处理逻辑
};

// 处理粘贴事件
const handlePaste = (event: ClipboardEvent) => {
  const items = event.clipboardData?.items;
  if (items) {
    for (const item of items) {
      const type = item.type;
      if (props.fileTypes.includes(type)) { // 检查文件类型
        const file = item.getAsFile();
        if (file) {
          showFilePreview(file);
        }
      }
    }
  }
};

// 显示文件预览并上传文件
const showFilePreview = (file: File) => {
  const reader = new FileReader();
  reader.onload = (e) => {
    const newFileData = {
      url: e.target?.result as string,
      type: file.type,
      progress: 0,
      file_id: '',
    };
    const currentIndex = fileData.value.length; // 新文件的索引
    fileData.value.push(newFileData);
    
    // 上传文件并传递索引
    uploadFile(file, currentIndex); 
  };
  reader.readAsDataURL(file);
};

// 上传文件到服务
const uploadFile = async (file: File, currentIndex: number) => {
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
        // 更新上传进度
        if (currentIndex >= 0 && currentIndex < fileData.value.length) {
          fileData.value[currentIndex].progress = Math.round((event.loaded / event.total) * 100);
        }
      }
    });

    if (response.status !== 200) {
      throw new Error(`上传失败: ${response.statusText}`);
    }

    const result = response.data;

    // 在这里检查当前索引的有效性
    if (currentIndex >= 0 && currentIndex < fileData.value.length) {
      fileData.value[currentIndex].file_id = result.data.file_id; // 处理服务器返回的数据
    } else {
      console.warn('文件已被移除，无法设置 file_id');
    }
  } catch (error) {
    console.error('文件上传失败:', error);
  }
};

// 移除文件函数
const removeFile = (index: number) => {
  fileData.value.splice(index, 1);
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