<template>
	<!-- 优先获取 nodeType当前配置项的width，如果没有则用全局配置 -->
	<div
		class="border bg-white cursor-default shadow hover:shadow-lg pb-4"
		:style="{
			width: data.nodeType?.width || flowConfig.width,
			borderRadius: flowConfig.borderRadius,
			borderColor:
				data.opt.curActive == props.node?.id ? globalColors.btnActive : '',
		}"
		@click.stop="handleActive"
	>
		<!-- 顶部可抓取区 -->
		<div class="border-b p-4 py-2 cursor-move">
			<!-- 标题栏 -->
			<div class="flex items-center gap-2">
				<!-- 类型图标 -->
				<Icon
					:icon="data.nodeType?.icon"
					:color="data.nodeType?.iconColor"
					width="24"
				/>

				<!-- 标题 -->
				<div class="grow text-ellipsis overflow-hidden">
					<span v-if="!data.opt.flagChangingName">
						{{ props.node?.label || data.nodeType?.label }}
					</span>
					<!-- 修改名称 -->
					<template v-else>
						<n-input
							ref="refLabel"
							v-model:value="data.form.label"
							size="small"
							placeholder="搜索"
							@blur="handleChangeNameBlur"
						/>
					</template>
				</div>

				<!-- 更多操作 -->
				<template v-if="!props.node?.undeletable">
					<NDropdown
						trigger="hover"
						:options="data.opt.dropdownMenu"
						@select="(key) => handleMenuSelect(key)"
					>
						<button
							text
							class="transition text-neutral-300 hover:text-neutral-800 dark:hover:text-neutral-200"
						>
							<Icon icon="ri:more-fill" width="20" color="#111824" />
						</button>
					</NDropdown>
				</template>
			</div>
			<!-- 描述 -->
			<span class="text-[grey] text-[12px]">
				{{ data.nodeType?.desc }}
			</span>
		</div>

		<!-- 内容区 -->
		<!-- 处理鼠标进入内容区阻止可拖动，离开内容区恢复可拖动 -->
		<div
			class="w-full h-full"
			@mouseenter.stop="setDraggable(false)"
			@mouseleave.stop="setDraggable(true)"
			@mousedown.stop="(e) => stopDraggable(e)"
			@touchstart.stop="
				(e) => {
					setDraggable(false);
					stopDraggable(e);
				}
			"
			@touchend.stop="setDraggable(true)"
		>
			<slot></slot>
		</div>
	</div>
</template>

<script setup lang="ts">
import { useIconRender } from "@/hooks/useIconRender";
import {
	flowConfig,
	getFlowNodeType,
} from "@/views/application/vueFlow/flowConfig.ts";
import { Icon } from "@iconify/vue";
import { reactive, defineEmits, onMounted, ref, nextTick, computed } from "vue";
import { Handle, useVueFlow } from "@vue-flow/core";
import { setDraggable, stopDraggable } from "@/utils/flow";
import { useDialog } from "naive-ui";
import { useFlowStore } from "@/store";
import { globalColors } from "@/hooks/useTheme";

const { iconRender } = useIconRender();
const { updateNode } = useVueFlow();
const dialog = useDialog();
const flowStore = useFlowStore();

const emits = defineEmits(["duplicate", "deleteNode"]);
const props = defineProps({
	node: {
		type: Object,
		default: {},
	},
});

const refLabel = ref();
const data = reactive({
	nodeType: getFlowNodeType(props.node?.type),
	form: {
		label:
			props.node?.label?.length > 0
				? props.node?.label
				: getFlowNodeType(props.node?.type).label,
	},
	opt: {
		curActive: computed(() => flowStore.curActive),
		flagChangingName: false,
		dropdownMenu: [
			{
				label: "重命名",
				key: "rename",
				icon: iconRender({ icon: "akar-icons:edit" }),
			},
			{
				label: "复制", 
				key: "duplicate",
				icon: iconRender({ icon: "ph:copy-duotone" }),
			},
			{
				label: "删除",
				key: "delete",
				icon: iconRender({ icon: "ri:delete-bin-line" }),
			},
		],
	},
});

// 下拉菜单 选择
const handleMenuSelect = (key: string | number) => {
	switch (key) {
		// 重命名
		case "rename":
			// 显示输入框
			data.opt.flagChangingName = true;
			// 自动聚焦
			nextTick(() => {
				refLabel.value?.focus();
			});
			break;

		// 复制
		case "duplicate":
			emits("duplicate", props.node);
			break;

		// 删除
		case "delete":
			emits("deleteNode", props.node?.id);
			break;
	}
};

// 修改名称输入框失焦时
const handleChangeNameBlur = () => {
	// 更新节点
	updateNode(props.node.id, { label: data.form.label });

	data.opt.flagChangingName = false;
};

// 激活当前组件
const handleActive = () => {
	flowStore.setActiveComponent(props.node.id);
};

const init = () => {
	data.node = props?.node;
};

onMounted(() => {
	init();
});
</script>

<style lang="less" scoped></style>
