<template>
	<!-- 输出 -->
	<n-tree
		:data="props.outputList"
		default-expand-all
		block-line
		:show-line="true"
		:selectable="false"
		:render-label="renderTreeLabel"
	/>
</template>

<script setup lang="ts">
import SingleModule from "@/views/application/vueFlow/components/pages/components/SingleModule.vue";
import { TreeOption } from "naive-ui";
import { defineProps, h } from "vue";
import TreeLabel from '@/views/application/vueFlow/components/pages/components/knowledge/TreeLabel.vue';

// 数据结构参考
// {
//   label: "输出列表",
//   key: "outputList",
//   tag: "Array<Object>",
//   children: [
//     {
//       label: "输出",
//       key: "output",
//       tag: "String",
//     },
//   ],
// },

const props = defineProps({
	outputList: {
		type: Array,
		default: [],
	},
});

// 输出 渲染tree组件的label
const renderTreeLabel = ({ option }: { option: TreeOption }) => {
	return h(TreeLabel, {
		label: option.label,
		tagLabel: option.tag,
	});
};
</script>

<style lang="less" scoped></style>
