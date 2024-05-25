<template>
	<Handle
		:id="id"
		:type="type"
		:connectable="true"
		:position="props.type === 'target' ? 'left' : 'right'"
		:style="{
			width: props.width,
			height: props.height,
			backgroundColor: props.color,
			position: 'absolute',
			top: '50%',
		}"
	/>
</template>

<script setup lang="ts">
/**
 * flow 连线点
    !tip 需在style中覆盖原有样式，class优先级比原配置更低(部分样式会无法生效)
          且必须使用top、left (覆盖flow组件中定义的)
    需配合父组件的relative样式
 */
import { Handle } from "@vue-flow/core";
import { v4 as uuidv4 } from "uuid";

const props = defineProps({
	id: {
		type: String,
		default: () => uuidv4(),
	},
	// 连线点类型
	type: {
		type: String, //  target(接收连接 左侧) | source(发起连接 右侧)
		default: "target",
	},
	width: {
		type: String,
		default: "14px",
	},
	height: {
		type: String,
		default: "14px",
	},
	color: {
		type: String,
		default: "",
	},
});
</script>

<style lang="less" scoped>
// :root {
// 	--transform-scale-rate: 1.5;
// 	--translate-position: props.type;
// 	// "props.type === "target" ? "-30%, 30%": "30%, -30%"
// }

// .vue-flow__handle {
// 	transform-origin: center center;
// 	transition: all 0.3s;

// 	&:hover {
// 		// transform: scale(1.5) translate(var(--translate-position));
// 	}
// }

// .vue-flow__handle:hover when (var(--translate-position) = "target") {
// 	transform: scale(var(--transform-scale-rate)) translate(-30%, 30%);
// }

// .vue-flow__handle:hover when (var(--translate-position) = "source") {
// 	transform: scale(var(--transform-scale-rate)) translate(30%, -30%);
// }
</style>
