<template>
    <!-- n-tooltip 组件，设置触发方式和最大宽度 -->
    <n-tooltip
        :trigger="trigger"
        :style="{
            'max-width': wrapMaxWidth,
        }"
    >
        <!-- 触发器插槽 -->
        <template #trigger>
            <!-- Icon 组件，设置图标、宽度和颜色 -->
            <Icon :icon="icon" :width="width" :color="color" />
        </template>

        <!-- 显示消息内容 -->
        {{ msg }}
        <!-- 默认插槽，用于显示额外内容 -->
        <slot></slot>
    </n-tooltip>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";

// 定义组件的 props
defineProps({
    wrapMaxWidth: {
        type: String,
        default: "300px",
    },
    icon: {
        type: String,
        default: "ph:question",
    },
    msg: {
        type: String,
        default: "",
    },
    trigger: {
        type: String,
        default: "hover",
    },
    width: {
        type: String,
        default: "",
    },
    color: {
        type: String,
        default: "",
    },
});
</script>

<style></style>