<template>
    <!-- n-collapse 组件，设置显示指令和默认展开的名称 -->
    <n-collapse
        :display-directive="displayDirective"
        :default-expanded-names="[title]"
    >
        <!-- 额外的头部插槽，如果 hideBtn 为 false 则显示 -->
        <template #header-extra v-if="!hideBtn">
            <slot name="extra">
                <!-- n-button 组件，点击时触发 handleDelete 函数 -->
                <n-button
                    quaternary
                    @click.stop="handleDelete"
                    style="padding: 0 0.8em"
                >
                    <!-- Icon 组件，设置图标和宽度 -->
                    <Icon :icon="icon" :width="iconWidth" />
                </n-button>
            </slot>
        </template>

        <!-- n-collapse-item 组件，设置标题和名称 -->
        <n-collapse-item :title="title" :name="title">
            <!-- 默认插槽，用于显示内容 -->
            <slot></slot>
        </n-collapse-item>
    </n-collapse>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";

// 定义组件的 emits
const emits = defineEmits("onDelete");

// 定义组件的 props
defineProps({
    displayDirective: {
        type: String,
        default: "show", // "show" | "if"
    },
    title: {
        // 标题
        type: String,
        default: "",
    },
    hideBtn: {
        // 隐藏右侧按钮
        type: Boolean,
        default: false,
    },
    icon: {
        type: String,
        default: "nimbus:stop",
    },
    iconWidth: {
        type: String,
        default: "14",
    },
});

// 处理删除按钮点击事件的函数
const handleDelete = () => {
    emits("onDelete");
};
</script>

<style lang="less" scoped></style>