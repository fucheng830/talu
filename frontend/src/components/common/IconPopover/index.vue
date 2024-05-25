<template>
	<n-popover
		:trigger="trigger"
		:placement="placement"
		:keep-alive-on-hover="false"
		:style="{
			'max-width': wrapMaxWidth,
		}"
	>
		<template #trigger>
			<div class="flex justify-center items-center">
				<Icon :icon="icon" :width="width" :color="color" />
				<slot name="text"></slot>
			</div>
		</template>

		<slot></slot>
	</n-popover>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";

const props = defineProps({
	placement: {
		type: String,
		default: "bottom",
	},
	icon: {
		type: String,
		default: "ph:question",
	},
	trigger: {
		type: String,
		default: "hover",
	},
	width: {
		type: String,
		default: "18",
	},
	color: {
		type: String,
		default: "",
	},
	wrapMaxWidth: {
		type: String,
		default: "300px",
	},
});
</script>

<style></style>
