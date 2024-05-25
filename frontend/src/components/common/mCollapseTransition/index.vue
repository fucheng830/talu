<template>
	<!-- 折叠组件 -->
	<div class="w-full">
		<div class="grid grid-cols-[1fr_2rem]">
			<slot name="header" :changeCollapsed="changeCollapsed"></slot>

			<!-- 右侧展开按钮 -->
			<div class="flex justify-center items-center" @click="changeCollapsed">
				<Icon
					icon="mingcute:right-fill"
					width="44"
					:color="data.isCollapsed ? globalColors.btnActive : undefined"
					:style="{
						transition: 'all .3s',
						transform: `rotate(${data.isCollapsed ? 90 : 0}deg)`,
					}"
				/>
			</div>
		</div>

		<n-collapse-transition :show="data.isCollapsed">
			<slot>
				<div>暂无数据</div>
			</slot>
		</n-collapse-transition>
	</div>
</template>

<script setup lang="ts">
import { isBoolean } from "@/utils/is";
import { onMounted, reactive } from "vue";
import { Icon } from "@iconify/vue";
import { globalColors } from "@/hooks/useTheme";

const props = defineProps({
	defaultCollapsed: {
		type: Boolean,
		default: true,
	},
});

const data = reactive({
	isCollapsed: true,
});

onMounted(() => {
	data.isCollapsed = props.defaultCollapsed;
});

// 改变折叠状态
const changeCollapsed = (show: boolean | undefined = undefined) => {
	if (isBoolean(show)) return (data.isCollapsed = show);
	data.isCollapsed = !data.isCollapsed;
};
</script>

<style lang="less" scoped></style>
