<template>
	<div class="h-full flex justify-end items-center gap-2">
		<n-button
			v-if="props.row?.children"
			type="primary"
			quaternary
			@click.stop="emits('add', row)"
		>
			<Icon icon="ph:plus" :width="iconWidth" />
		</n-button>

		<n-button
			type="primary"
			quaternary
			:disabled="btnDisabled || row?.disabled"
			@click.stop="emits('delete', row)"
		>
			<Icon icon="nimbus:stop" :width="iconWidth" color="grey" />
		</n-button>
	</div>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";
import { defineProps } from "vue";

// 使用h函数时需要加on前缀，比如onAdd
const emits = defineEmits(["add", "delete"]);
const props = defineProps({
	// 当前表格行数据
	row: {
		type: Object,
		default: () => {},
	},
	// 图标宽度
	iconWidth: {
		type: String,
		default: "16",
	},
	btnDisabled: {
		type: Boolean,
		default: false,
	},
});
</script>

<style lang="less" scoped></style>
