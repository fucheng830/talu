<template>
	<m-modal
		ref="refModal"
		:title="title"
		:show-footer="false"
		style="border-radius: 10px"
	>
		<div class="mt-6">
			<!-- 邀请码 -->
			<n-input-group>
				<n-input v-model:value="data.inviteUrl" readonly placeholder="" />
				<n-button ghost @click="copyInviteUrl">
					<span> {{ $t("common.copy") }} </span>
				</n-button>
			</n-input-group>
		</div>
	</m-modal>
</template>

<script setup lang="ts">
import mModal from "@/components/common/mModal/index.vue";
import { computed, onMounted, reactive, ref } from "vue";
import { globalColors } from "@/hooks/useTheme";
import { useMessage } from "naive-ui";
import { t } from "@/locales";

const props = defineProps({
	title: {
		type: String,
		default: "",
	},
	urlCopy: {
		type: String,
		default: "",
	},
});

const msg = useMessage();

const refModal = ref();
const data = reactive({
	// 当前域名
	inviteUrl: computed(() => `${location.host}/#/${props.urlCopy}`),
});

// 复制 邀请链接
const copyInviteUrl = () => {
	navigator.clipboard.writeText(data.inviteUrl);
	msg.success(t("share.copyedGoShare"));
};

// 改变模态框显示
const changeModalShow = () => {
	if (refModal.value) {
		refModal.value.toggleModal();
	}
};

// 暴露方法给父组件
defineExpose({
	changeModalShow,
});
</script>

<style></style>
