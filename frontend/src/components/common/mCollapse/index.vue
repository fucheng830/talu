<template>
	<n-collapse
		:display-directive="displayDirective"
		:default-expanded-names="[title]"
	>
		<template #header-extra v-if="!hideBtn">
			<slot name="extra">
				<n-button
					quaternary
					@click.stop="handleDelete"
					style="padding: 0 0.8em"
				>
					<Icon :icon="icon" :width="iconWidth" />
				</n-button>
			</slot>
		</template>

		<n-collapse-item :title="title" :name="title">
			<slot></slot>
		</n-collapse-item>
	</n-collapse>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";

const emits = defineEmits("onDelete");
const props = defineProps({
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
		// 隐藏右侧
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

// 默认删除按钮
const handleDelete = () => {
	emits("onDelete");
};
</script>

<style lang="less" scoped></style>
