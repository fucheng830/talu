<template>
  <div class="upload-container">
    <!-- 使用NaiveUI的n-upload组件进行文件上传 -->
    <n-upload
      list-type="image-card"
      action="http://192.168.2.152:8003/upload_image"
      :on-finish="handleUploadFinish"
      :default-file-list="fileList"
    >
      Click to Upload Image
    </n-upload>
  </div>
</template>

<script setup lang="ts">
import { defineComponent, ref, reactive } from 'vue';
import { UploadFileInfo } from 'naive-ui';
import axios from 'axios';

// 变量来跟踪上传的文件列表
const fileList = ref<UploadFileInfo[]>([]);

// 上传完成后调用此函数
function handleUploadFinish({ file }: { file: File }) {
  // FormData用于构建一个与HTML表单相同的数据集
  console.log('Uploading file:', file);
  const formData = new FormData();
  formData.append('file', file);
}
</script>

<style>
.upload-container {
  /* 样式、布局调整，如居中对齐等 */
}
</style>