<template>
	<!-- 智能体 -->
	<div class="w-full h-full py-4 px-[5%]">
		<!-- 顶部按钮栏 -->
		<div class="w-full flex justify-end">
			<n-button color="#13A47F" class="btn-radius">
				<Icon icon="ic:baseline-plus" />
				创建GPT
			</n-button>
		</div>

		<!-- 我的 -->
		<div class="w-full">
			<span class="">我的</span>
		</div>

		<!-- 市场 -->
		<div class="w-full mt-[10rem]">
			<span class="">市场</span>

			<!-- 搜索栏 -->
			<n-input
				v-model:value="value"
				type="text"
				placeholder="搜索"
				class="btn-radius mt-4"
			/>

			<!-- 内容区 包围 -->
			<div
				class="w-full mt-2 p-2"
			>
				<!-- 筛选条 -->
				<div class="w-full flex gap-2">
					<!-- 单个筛选 -->
					<template v-for="tag in data.filterList" :key="tag">
						<div
							class="px-2 py-1 rounded cursor-pointer animation duration-200 ease-in"
							:class="[
								data.curFilter == tag
									? `bg-[#4F55E6] text-[white]`
									: `bg-[white]`,
							]"
							@click="changeFilter(tag)"
						>
							<span>{{ tag }}</span>
						</div>
					</template>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import { Icon } from "@iconify/vue";
import { globalConfig } from "@/hooks/useTheme";

const data = reactive({
	myList: [], // 我的 列表
	curFilter: "全部", // 当前筛选
	filterList: ["全部", "工具", "娱乐", "生活方式", "咨询", "创意", "学习"], // 筛选列表
});

// 切换筛选
const changeFilter = (tag) => {
	data.curFilter = tag;
};
</script>

<style lang="less" scoped>
.btn-radius {
	border-radius: v-bind("globalConfig.btnRadius");
}
</style>
