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
		<template #header>
			<div class="modal-header">{{ title }}</div>
		</template>

		<slot></slot>

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
	// 显示方式	if/show
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

const emits = defineEmits([
	"onPositiveClick", // 点击 确认
	"onNegativeClick", // 点击 取消
	"onClose", // 模态框关闭时
	"onShowChange", // 模态框显示变化时
]);

const showModal = ref(false);

// Event handlers
const handleClose = (isShow: boolean) => {
	emits("onClose");
	showModal.value = isShow;
};
const emitPositiveClick = () => emits("onPositiveClick");
const handleNegativeAction = () => {
	emits("onNegativeClick");
	showModal.value = false;
};

const handleMaskClick = () => {
	showModal.value = false;
};

const changeModalShow = (show: boolean | undefined = undefined) => {
	if (isBoolean(show)) return (showModal.value = show);
	showModal.value = !showModal.value;
};

// 当模态框显示变化时
watch(
	() => showModal.value,
	(val) => {
		emits("onShowChange", val);
	}
);

// Expose the showModal toggle method to the parent component
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
