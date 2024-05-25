<template>
	<div class="w-full h-full flex flex-col">
		<!-- 顶部栏 -->
		<div class="flex justify-between items-center px-6 py-3 border shadow-sm">
			<div class="flex items-center gap-3 cursor-pointer">
				<!-- 返回图标 箭头 左 -->
				<div
					@click="handleGoBack"
					class="p-1 rounded-full border hover:shadow"
					:style="{ 'box-shadow': '1px 1px 9px rgba(0,0,0,.15)' }"
				>
					<Icon
						icon="gravity-ui:arrow-left"
						:color="globalColors.btnActive"
						width="18"
					/>
				</div>
				<span class="text-[18px]">{{ data.curAppName }}</span>
			</div>

			<!-- 右侧按钮组 -->
			<div class="flex items-center gap-6">
				<n-dropdown
					trigger="click"
					:options="data.opt.dropdown"
					@select="dropdownSelect"
				>
					<n-button-group>
						<n-button @click.stop="handleTestFlow">测试流程</n-button>
						<!-- 下拉按钮 -->
						<n-button style="padding: 0 0.4rem">
							<Icon icon="icon-park-solid:down-one" width="18" />
						</n-button>
					</n-button-group>
				</n-dropdown>

				<n-button type="primary">发布</n-button>

				<n-popover placement="bottom" :keep-alive-on-hover="false">
					<template #trigger>
						<n-button>
							<Icon icon="ph:copy-duotone" width="18" />
						</n-button>
					</template>
					<span>复制</span>
				</n-popover>
			</div>
		</div>

		<!-- 内容 主视图区 -->
		<div class="relative w-full h-full">
			<div
				class="absolute flex flex-col z-[10]"
				:class="[data.showAddComponent ? 'w-[90%] max-w-[360px] h-full' : '']"
			>
				<!-- 添加组件 按钮 -->
				<div class="mt-4 ml-4">
					<n-button
						circle
						size="large"
						:color="globalColors.btnActive"
						@click="changeShowAddComponent"
					>
						<Icon
							icon="fa-solid:plus"
							width="18"
							color="white"
							class="transition-all transition-200"
							:style="{
								transform: data.showAddComponent ? 'rotate(-135deg)' : '',
							}"
						/>
					</n-button>
				</div>

				<!-- 组件列表 包围 外层 -->
				<div
					class="grow"
					:class="[data.showAddComponent ? 'mt-4 pb-[2rem]' : '']"
				>
					<n-collapse-transition
						:show="data.showAddComponent"
						style="height: 100%; display: flex; flex-direction: column"
					>
						<!-- 组件列表 包围 -->
						<div
							class="flex flex-col grow rounded-[1.5rem] py-2 bg-white"
							style="box-shadow: 3px 0 20px 0 rgba(0, 0, 0, 0.2)"
						>
							<n-scrollbar style="flex: 1 0 0">
								<!-- 组件列表 -->
								<div class="w-full flex flex-col gap-2 px-4 py-2 select-none">
									<!-- 分组 -->
									<template v-for="item in data.opt.compList" :key="item.key">
										<!-- <div class="flex flex-col">
											<span class="font-bold">{{ curGroup.label }}</span> -->

										<!-- 单个组件 -->
										<!-- <template
												v-for="item in curGroup.children"
												:key="item.key"
											> -->
										<div
											class="flex gap-4 p-4 hover:bg-[#F4F6F8] hover:shadow-lg cursor-pointer"
											:draggable="true"
											@dragend="(e) => onDragEnd(e, item)"
										>
											<!-- 图标 -->
											<div
												class="min-w-[32px] flex justify-center items-center"
											>
												<Icon
													:icon="item.icon"
													:color="item?.iconColor ? item.iconColor : ''"
													width="32"
												/>
											</div>
											<!-- 右侧信息 -->
											<div class="grow flex flex-col">
												<!-- 名称 -->
												<span class="text-[14px]">
													{{ item.label }}
												</span>
												<!-- 描述 -->
												<span class="text-[grey] text-[12px]">
													{{ item.desc }}
												</span>
											</div>
										</div>
										<!-- </template> -->
										<!-- </div> -->
									</template>
								</div>
							</n-scrollbar>
						</div>
					</n-collapse-transition>
				</div>
			</div>

			<!-- vue flow 组件 -->
			<myFlow ref="refMyFlow" />
		</div>
	</div>
</template>

<script setup lang="ts">
import myFlow from "@/views/application/vueFlow/index.vue";
import { reactive, ref } from "vue";
import { Icon } from "@iconify/vue";
import { globalColors } from "@/hooks/useTheme";
import { useRoute, useRouter } from "vue-router";
import { flowNodeType } from "@/views/application/vueFlow/flowConfig.ts";

const route = useRoute();
const router = useRouter();

const refMyFlow = ref();
const data = reactive({
	curAppName: "myAI", // 当前应用名
	showAddComponent: false, // 是否展开显示 添加组件
	opt: {
		compList: flowNodeType,
		dropdown: [
			{
				label: "管理测试集",
				key: "manageTestset",
			},
		],
	},
});

// 顶部栏下拉选择
const dropdownSelect = (key: string) => {
	switch (key) {
		case "manageTestset":
			// todo 管理测试集逻辑
			console.log("manageTestset");
			break;
	}
};

// 测试流程
const handleTestFlow = () => {
	// todo 测试流程逻辑
	console.log("handleTestFlow");
};

// 切换显示 添加组件
const changeShowAddComponent = () => {
	data.showAddComponent = !data.showAddComponent;
};

// 拖放松开，添加组件
const onDragEnd = (e: Event, item: any) => {
	const { layerX, layerY } = e;

	refMyFlow.value.addFlowNode({
		type: item?.key,
		x: layerX,
		y: layerY,
	});
};

const handleGoBack = () => {
	// router.go(-1);
	router.push({
		name: "Createai",
	});
};
</script>

<style lang="less" scoped></style>
