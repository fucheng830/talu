<template>
    <div class="flex flex-col items-center">
      <img src="@/assets/logo.png" alt="" class="w-[44px]" />
      <span class="text-sm font-bold truncate max-w-[68px] mt-2">{{ logoName }}</span>
    </div>
  </template>
  
  <script setup lang="ts">
  import { defineProps } from 'vue';
  
  defineProps({
    logoName: {
      type: String,
      required: true
    }
  });
  </script>
  
  <style scoped>
  /* 你可以在这里添加额外的样式 */
  </style>