<template>
	<n-tooltip
		:trigger="trigger"
		:style="{
			'max-width': wrapMaxWidth,
		}"
	>
		<template #trigger>
			<Icon :icon="icon" :width="width" :color="color" />
		</template>

		{{ msg }}
		<slot></slot>
	</n-tooltip>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";

const props = defineProps({
	wrapMaxWidth: {
		type: String,
		default: "300px",
	},
	icon: {
		type: String,
		default: "ph:question",
	},
	msg: {
		type: String,
		default: "",
	},
	trigger: {
		type: String,
		default: "hover",
	},
	width: {
		type: String,
		default: "",
	},
	color: {
		type: String,
		default: "",
	},
});
</script>

<style></style>
