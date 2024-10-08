<template>
	<div>
		<!-- 角色列表 -->
		<div
			class="font-bold leading-tight slogan break-all px-2 text-center mt-[4rem]"
			:class="[isMobile ? 'text-[37px]' : 'text-[60px]']"
		>
			Qu Chat
		</div>
		<div
			class="pb-[24px] pt-[6px] px-[24px] font-bold text-center leading-[1.1] break-all"
			:class="[isMobile ? 'text-[19px]' : 'text-[40px]']"
		>
			{{ $t("setting.menu.subTitle5") }}
		</div>

		<!-- 搜索栏 -->
		<div class="w-full flex justify-center">
			<div class="w-[90%] max-w-[40rem]">
				<n-input
					round
					size="large"
					:placeholder="$t('square.placeholderSearch')"
					@keypress.prevent.enter="handleSearch"
					clearable
				>
					<template #suffix>
						<n-button
							text
							@click="handleSearch"
							style="margin-left: 0.5rem"
						>
							<template v-if="data.isSearching">
								<Icon icon="line-md:loading-twotone-loop" width="24" />
							</template>
							<template v-else>
								<Icon icon="mingcute:search-line" width="24" />
							</template>
						</n-button>
					</template>
				</n-input>
			</div>
		</div>

		<!-- 标签列表 -->
		<div
			class="mt-[56px] min-h-[32px] mb-0 overflow-hidden max-w-full"
			:class="[isMobile ? 'px-[1rem]' : 'px-[40px]']"
		>
			<div
				ref="refTagList"
				class="w-full overflow-y-hidden overflow-x-auto no-scrollbar"
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
									item == data.curTagActive
										? theme.primaryColor
										: 'white',
							}"
						>
							{{ item }}
						</li>
					</template>
				</ul>
			</div>
		</div>

		<!-- 分类列表 -->
		<div class="w-full mb-[100px]">
			<template v-for="tag in data.dataList" :key="tag.label">
				<div class="w-full max-w-[2100px] px-[24px]">
					<h3
						class="mt-[32px] mb-[14px] font-bold flex items-center text-[18px]"
					>
						{{ tag.label }}
					</h3>

					<n-grid :cols="data.curCols" :x-gap="20" :y-gap="20">
						<template v-for="item in tag.children" :key="item.title">
							<n-gi>
								<div
									class="rounded-[16px] robot relative bg-white cursor-pointer flex flex-col items-center leading-none overflow-hidden p-[24px] h-[180px] animation rounded-tr-[8px] duration-200 hover:-translate-y-2 hover:shadow-lg"
									@click="handleGoChat(item)"
								>
									<div
										v-if="item.isplus"
										class="flex items-center text-white absolute right-0 top-0 rounded-bl-[8px] bg-[#6f55f2] h-[22px] text-[12px] px-[6px] leading-[17px]"
									>
										{{ $t("vip.proEdition") }}
									</div>
									<div class="relative">
										<div class="relative flex">
											<NImage
												:src="item.avatar"
												:preview-disabled="true"
												lazy
												class="group-hover:scale-[130%] duration-300 shrink-0 overflow-hidden bg-base object-cover rounded-full w-[56px] h-[56px]"
											>
												<template #placeholder>
													<div
														class="w-full h-full justify-center items-center flex"
													>
														<Icon
															icon="line-md:downloading-loop"
															class="text-[60px] text-green-300"
														></Icon>
													</div>
												</template>
											</NImage>
											<img
												v-if="item.authPath"
												src="@/assets/images/square/icon_authPass.svg"
												alt=""
												class="absolute bottom-[-3px] right-[-3px] w-[24px] h-[24px]"
											/>
										</div>
									</div>
									<div
										class="text-[16px] pb-[8px] pt-[16px] font-bold text-overflow text-center"
									>
										{{ item.name }}
									</div>
									<div
										class="text-[12px] text-[gray] text-overflow-l2 leading-tight text-center"
									>
										{{ item.description }}
									</div>
								</div>
							</n-gi>
						</template>
					</n-grid>
				</div>
			</template>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { useAgentStore } from "@/store";
import { Icon } from "@iconify/vue";
import { NImage } from "naive-ui";
import { useThemeVars } from "naive-ui";
import { api } from "@/api/common";

const agentsStore = useAgentStore();
const theme = useThemeVars();
const { isMobile } = useBasicLayout();
const router = useRouter();

const refTagList = ref();
const data = reactive({
	curTagActive: "推荐",
	tagList: computed(() => agentsStore.$state.categories),
	curCols: 7,
	dataList: [],
	dataListBackup: computed(() => agentsStore.$state.agents),
	isSearching: false,
});

function handleGoChat(item: any) {
	router.push("/chat/" + item.id);
}

const handleSearch = async () => {
	if (data.isSearching) return;

	data.isSearching = true;
	res = await api.search_agent({ keyword: "GPT" });
	console.log(res);

	setTimeout(() => {
		data.isSearching = false;
	}, 2000);
};

const handleWheelHorizontal = (event) => {
	let left = -event.wheelDelta || event.deltaY / 2;
	refTagList.value.scrollLeft += left;
};

const handleTagChange = (item: any) => {
	data.curTagActive = item;
};

const handleColChange = () => {
	const curWidth = window.innerWidth;
	if (curWidth < 600) return (data.curCols = 2);
	if (curWidth < 860) return (data.curCols = 3);
	if (curWidth < 1200) return (data.curCols = 4);
	if (curWidth < 1400) return (data.curCols = 5);
	if (curWidth < 1580) return (data.curCols = 6);
	data.curCols = 7;
};

watch(
	() => data.curTagActive,
	(val) => {
		const tar = data.tagList.find((item) => {
			return item === val;
		});
		if (val === "推荐") return (data.dataList = data.dataListBackup);
		data.dataList = data.dataListBackup.filter((item) => item.label === tar);
	}
);

window.onresize = (e) => {
	handleColChange();
};
handleColChange();
</script>

<style scoped>
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
