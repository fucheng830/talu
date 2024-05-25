<template>
	<!-- 单个模块，输入、输出 等 -->
	<div class="bg-[#F7F7F7] rounded-lg p-2 pb-4">
		<mCollapse :title="title" :hideBtn="hideBtn">
			<!-- 右侧添加按钮 -->
			<template #extra>
				<slot name="extra">
					<n-button
						quaternary
						style="padding: 0.4rem"
						@click.stop="emits('add')"
					>
						<Icon icon="ph:plus" width="24" :color="globalColors.btnActive" />
					</n-button>
				</slot>
			</template>

			<template v-if="useGrid">
				<div class="grid grid-cols-[30%_1fr] gap-y-2 gap-x-2">
					<span class="text-[#1c1d2359] pl-2">{{ firstText }}</span>
					<span class="text-[#1c1d2359] pl-2">值</span>

					<slot></slot>
				</div>
			</template>

			<slot v-else></slot>
		</mCollapse>
	</div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import mCollapse from "@/components/common/mCollapse/index.vue";
import { globalColors } from "@/hooks/useTheme";
import { Icon } from "@iconify/vue";

const emits = defineEmits(["add"]);
const props = defineProps({
	title: {
		type: String,
		default: "输入",
	},
	hideBtn: {
		type: Boolean,
		default: false,
	},
	useGrid: {
		type: Boolean,
		default: true,
	},
	firstText: {
		type: String,
		default: "名称",
	},
});
</script>

<style lang="less" scoped></style>
