<template>
	<div class="flex items-center gap-2 text-[12px]">
		<span>{{ props.label }}</span>
		<div class="px-2 py-[.2rem] text-[#1c1f2399] bg-[#e6e8eac2] rounded">
			{{ props.tagLabel }}
		</div>
	</div>
</template>

<script setup lang="ts">
const props = defineProps({
	label: {
		type: String,
		default: "",
	},
	tagLabel: {
		type: String,
		default: "",
	},
});
</script>

<style lang="less" scoped></style>
