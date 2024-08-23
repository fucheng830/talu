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
import { computed, reactive, ref } from "vue";
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
	inviteUrl: computed(() => {
		if (!props.urlCopy) {
			return "https://example.com"; // 默认值或错误提示
		}
		return `${location.protocol}//${location.host}/#/${props.urlCopy}`;
	}),
});

// 复制 邀请链接
const copyInviteUrl = () => {
	if (navigator.clipboard && window.isSecureContext) {
		navigator.clipboard.writeText(data.inviteUrl)
			.then(() => {
				msg.success(t("share.copyedGoShare"));
			})
			.catch(err => {
				console.error('Failed to copy text: ', err);
				fallbackCopyTextToClipboard(data.inviteUrl);
			});
	} else {
		fallbackCopyTextToClipboard(data.inviteUrl);
	}
};

// 备用的复制方法
const fallbackCopyTextToClipboard = (text: string) => {
	const textArea = document.createElement("textarea");
	textArea.value = text;
	textArea.style.position = 'fixed';  // 避免在页面滚动时影响用户体验
	textArea.style.opacity = '0';  // 隐藏文本区域
	document.body.appendChild(textArea);
	textArea.focus();
	textArea.select();
	try {
		const successful = document.execCommand('copy');
		if (successful) {
			msg.success(t("share.copyedGoShare"));
		} else {
			console.error('Fallback: Copying text command was unsuccessful');
		}
	} catch (err) {
		console.error('Fallback: Oops, unable to copy', err);
	}
	document.body.removeChild(textArea);
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
