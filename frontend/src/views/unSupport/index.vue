<template>
  <div class="w-full h-full bg-[#F5F4F7]">
    <BgTopBar :showAvatar="false" class="pl-3 pt-2">
      <div
        class="w-full h-full pb-[140px] flex justify-center items-center flex-col"
      >
        <img :src="iconUnSupport" alt="" width="230" />
        <div class="mt-[24px] flex flex-col text-[20px] leading-[28px]">
          暂不支持移动端使用
        </div>
        <div class="mt-[4px] text-[#93909F] text-[18px] leading-[26px]">
          请用电脑使用知识库功能
        </div>
      </div>
    </BgTopBar>
  </div>
</template>

<script setup lang="ts">
import iconUnSupport from "@/assets/images/knowledge/un-support.png";
import BgTopBar from "@/views/layout/BgTopBar.vue";
</script>

<style></style>
