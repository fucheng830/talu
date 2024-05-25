<template>
	<!-- 内容区 -->
	<div class="relative px-4 mt-4 flex justify-end">
		<span>用户问题</span>

		<MyHandle type="source" color="#36ADEF" />
	</div>
</template>

<script setup lang="ts">
import { useIconRender } from "@/hooks/useIconRender";
import {
	flowConfig,
	getFlowNodeType,
} from "@/views/application/vueFlow/flowConfig.ts";
import { Icon } from "@iconify/vue";
import { reactive } from "vue";
import MyHandle from "@/views/application/vueFlow/components/MyHandle.vue";

const { iconRender } = useIconRender();

const props = defineProps({
	node: Object,
	default: {},
});

const data = reactive({
	nodeType: getFlowNodeType("chatEntrance"),
	opt: {
		dropdownMenu: [
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
		// 删除
		case "delete":
			// handleDeleteApp(props.id);
			console.log("delete", props);
			data.showModalDeleteApp = true;
			data.curDeleteUUID = item.uuid;
	}
};
</script>

<style lang="less" scoped></style>
