<!-- 通用的模态框 -->
<template>
    <n-modal
        v-model:show="showModal"
        preset="dialog"
        :title="title"
        :closable="showCloseIcon"
        :show-icon="false"
        :display-directive="displayDirective"
        :auto-focus="autoFocus"
        class="modal-wrap"
        :on-update:show="handleClose"
        :on-mask-click="handleMaskClick"
    >
        <!-- 自定义头部 -->
        <template #header>
            <div class="modal-header">{{ title }}</div>
        </template>

        <!-- 默认插槽，用于显示模态框内容 -->
        <slot></slot>

        <!-- 底部操作按钮 -->
        <template #action v-if="showFooter">
            <n-button
                type="tertiary"
                :size="footerBtnSize"
                @click="handleNegativeAction"
            >
                {{ txtCancel }}
            </n-button>
            <n-button
                :type="footerConfirmBtnType"
                :size="footerBtnSize"
                :disabled="comfirmDisabled"
                :loading="comfirmLoading"
                @click="emitPositiveClick"
            >
                {{ txtConfirm }}
            </n-button>
        </template>
    </n-modal>
</template>

<script setup lang="ts">
import { isBoolean } from "@/utils/is";
import { ref, watch } from "vue";

// 定义组件的 props
const props = defineProps({
    title: String,
    // 取消按钮文本
    txtCancel: {
        type: String,
        default: "取消",
    },
    // 确认按钮文本
    txtConfirm: {
        type: String,
        default: "确定",
    },
    // 显示底部按钮栏
    showFooter: {
        type: Boolean,
        default: true,
    },
    // 是否显示右上角关闭按钮
    showCloseIcon: {
        type: Boolean,
        default: false,
    },
    // 显示方式 if/show
    displayDirective: {
        type: String,
        default: "if",
    },
    // 底部按钮大小
    footerBtnSize: {
        type: String,
        default: "large",
    },
    // 确认按钮类型
    footerConfirmBtnType: {
        type: String,
        default: "primary",
    },
    // 确认按钮是否禁用
    comfirmDisabled: {
        type: Boolean,
        default: false,
    },
    // 确认按钮是否加载中
    comfirmLoading: {
        type: Boolean,
        default: false,
    },
    // 是否自动聚焦
    autoFocus: {
        type: Boolean,
        default: true,
    },
});

// 定义组件的 emits
const emits = defineEmits([
    "onPositiveClick", // 点击 确认
    "onNegativeClick", // 点击 取消
    "onClose", // 模态框关闭时
    "onShowChange", // 模态框显示变化时
]);

// 定义模态框显示状态
const showModal = ref(false);

// 处理模态框关闭事件
const handleClose = (isShow: boolean) => {
    emits("onClose");
    showModal.value = isShow;
};

// 处理确认按钮点击事件
const emitPositiveClick = () => emits("onPositiveClick");

// 处理取消按钮点击事件
const handleNegativeAction = () => {
    emits("onNegativeClick");
    showModal.value = false;
};

// 处理遮罩点击事件
const handleMaskClick = () => {
    showModal.value = false;
};

// 改变模态框显示状态
const changeModalShow = (show: boolean | undefined = undefined) => {
    if (isBoolean(show)) return (showModal.value = show);
    showModal.value = !showModal.value;
};

// 监听模态框显示状态变化
watch(
    () => showModal.value,
    (val) => {
        emits("onShowChange", val);
    }
);

// 向父组件暴露 toggleModal 方法
defineExpose({
    toggleModal: changeModalShow,
});
</script>

<style lang="less" scoped>
.modal-wrap {
    border-radius: 30px !important;
}

.modal-header {
    font-weight: 600;
    font-size: 16px;
}
</style>