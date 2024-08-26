<template>
	<div class="w-full h-full p-4">
		<div class="flex justify-end gap-4">
			<!-- 排序 -->
			<n-dropdown
				trigger="click"
				:options="data.opt.sort"
				@select="handleSortSelect"
			>
				<n-button quaternary>
					<span class="text-[grey]">排序：</span>
					<span class="font-bold"> {{ data.curSortLabel }} </span>
				</n-button>
			</n-dropdown>

			<!-- 搜索 -->
			<div class="flex items-center gap-4">
				<n-input
					v-model:value="data.txtSearch"
					type="text"
					placeholder="搜索"
					clearable
				>
					<template #prefix>
						<Icon icon="iconamoon:search" width="18" color="#74737A" />
					</template>
				</n-input>
				<n-button type="primary">创建插件</n-button>
			</div>
		</div>

		<!-- 标签列表 -->
		<div
			class="mt-[1rem] min-h-[32px] mb-0 overflow-hidden max-w-full"
			:class="[!isMobile && 'px-[40px]']"
		>
			<div
				ref="refTagList"
				class="no-scrollbar w-full overflow-y-hidden overflow-x-auto"
				@wheel.prevent="handleWheelHorizontal"
			>
				<ul class="flex">
					<template v-for="item in data.tagList" :key="item">
						<li
							v-if="item"
							@click="handleTagChange(item)"
							class="tab flex-shrink-0 cursor-pointer"
							:class="[
								item == data.curTagActive ? `text-white` : 'text-gray-DEEP',
							]"
							:style="{
								'background-color':
									item == data.curTagActive ? theme.primaryColor : 'white',
							}"
						>
							{{ item }}
						</li>
					</template>
				</ul>
			</div>
		</div>

		<!-- 插件列表 包围 -->
		<div
			class="mt-[2rem] grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5"
		>
			<!-- 单个插件 -->
			<template v-for="item in data.pluginList" :key="item?.id">
				<div
					class="flex flex-col p-4 bg-white rounded-lg shadow-[0_6px_8px_0_rgba(28,31,35,.06)] cursor-pointer m-2"
				>
					<!-- 头像 -->
					<n-avatar
						:size="36"
						:src="item.avatar" 
					/>

					<!-- 名称 -->
					<div class="text-[24px] text-[#383743] mt-2">
						{{ item?.name }}
					</div>

					<!-- 作者 -->
					<div class="text-[14px] text-[grey]">{{ item.author }}</div>

					<!-- 描述 -->
					<div class="text-[14px] text-[grey] mt-2">{{ item.description }}</div> <!-- 修改为 description -->

					<!-- 底部栏 -->
					<div
						class="flex items-center gap-4 mt-[3rem] text-[12px] text-[#383743]/[.35]"
					>
						<!-- 使用次数 -->
						<!-- 这个部分可以根据需要来决定是否显示 -->
						<!-- <div class="flex items-center gap-1">
							<Icon
								icon="material-symbols:person-outline"
								width="16"
								color="rgba(56, 55, 67, 0.35)"
							/>
							<span>{{ item.used }}</span>
						</div> -->
					</div>
				</div>
			</template>
		</div>
	</div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { renderIcon } from "@/utils/functions";
import { Icon } from "@iconify/vue";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { useThemeVars } from "naive-ui";
import { useSettingStore } from "@/store";

const theme = useThemeVars();
const { isMobile } = useBasicLayout();
const settingStore = useSettingStore();
const rootUrl = "@/assets/images/";
const refTagList = ref();
const data = reactive({
	sort: "popular", // 当前排序方式
	// 当前排序 文本
	curSortLabel: computed(
		() => data?.opt?.sort.find((item) => item.key == data.sort)?.label
	),
	txtSearch: "", // 搜索关键词
	curTagActive: "推荐", // 当前筛选
	tagList: ["推荐", "照片"], // 筛选栏
	pluginList: computed(()=>settingStore.$state.toolsConfig), // 插件列表
	opt: {
		sort: [
			{
				label: "热度",
				key: "popular",
				icon: () =>
					data?.sort == "popular"
						? renderIcon({
								icon: "typcn:tick",
								width: 18,
								color: theme.primaryColor,
						  })
						: undefined,
			},
			{
				label: "最新",
				key: "recent",
				icon: () =>
					data?.sort == "recent"
						? renderIcon({
								icon: "typcn:tick",
								width: 18,
								color: theme.primaryColor,
						  })
						: undefined,
			},
		],
	},
});

// 改变排序方式
const handleSortSelect = (key: string, opt: DropdownOption) => {
	data.sort = key;
	// todo 对接接口，搜索当前相关插件
	// data.pluginList=
};

// 切换标签激活状态
const handleTagChange = (item: any) => {
	data.curTagActive = item;
};

// 处理垂直滚动转为横向滚动
// 需要处理阻止默认事件，这里在调用时使用.prevent后缀
const handleWheelHorizontal = (event) => {
	let left = -event.wheelDelta || event.deltaY / 2;
	refTagList.value.scrollLeft += left;
};

onMounted(() => {
	settingStore.fetchToolsConfig();
});
</script>

<style lang="less" scoped>
.tab {
	margin-right: 10px;
	padding: 0 20px;
	min-width: 96px;
	height: 32px;
	line-height: 32px;
	text-align: center;
	border-radius: 16px;
	transition: all 0.4s;
}
</style>
