<template>
  <n-button :color="bgcolor" round @click="emits('emit')">
    <template #icon>
      <Icon :icon="icon" />
    </template>
    <span> {{ label }} </span>
  </n-button>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";

defineProps({
  label: {
    type: String,
    default: "AI一键生成",
  },
  icon: {
    type: String,
    default: "mingcute:bling-line",
  },
  bgcolor: {
    type: String,
  },
});

const emits = defineEmits(["emit"]);
</script>

<style></style>
