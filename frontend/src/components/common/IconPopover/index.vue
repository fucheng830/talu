<template>
    <!-- n-popover 组件，设置触发方式、位置、保持悬停状态和最大宽度 -->
    <n-popover
        :trigger="trigger"
        :placement="placement"
        :keep-alive-on-hover="false"
        :style="{
            'max-width': wrapMaxWidth,
        }"
    >
        <!-- 触发器插槽 -->
        <template #trigger>
            <div class="flex justify-center items-center">
                <!-- Icon 组件，设置图标、宽度和颜色 -->
                <Icon :icon="icon" :width="width" :color="color" />
                <!-- 插槽，用于显示文本 -->
                <slot name="text"></slot>
            </div>
        </template>

        <!-- 默认插槽，用于显示弹出内容 -->
        <slot></slot>
    </n-popover>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";

// 定义组件的 props
defineProps({
    placement: {
        type: String,
        default: "bottom",
    },
    icon: {
        type: String,
        default: "ph:question",
    },
    trigger: {
        type: String,
        default: "hover",
    },
    width: {
        type: String,
        default: "18",
    },
    color: {
        type: String,
        default: "",
    },
    wrapMaxWidth: {
        type: String,
        default: "300px",
    },
});
</script>

<style></style>