<template>
	<m-modal
		ref="refModal"
		:title="title"
		:show-footer="false"
		style="border-radius: 10px"
	>
		<div class="mb-2 text-[16px]">
			{{ $t("share.invite") }}
			<!-- 邀请数 -->
			<span :style="{ color: globalColors.btnActive }">
				{{ data.opt.inviteCount }}
			</span>
			{{ $t("share.invite2") }}

			<!-- 对话奖励 -->
			<span :style="{ color: globalColors.btnActive }">
				{{ data.opt.chatAward }}
			</span>
			{{ $t("share.invite3") }}
		</div>

		<!-- 邀请码 -->
		<n-input-group>
			<n-input v-model:value="data.inviteUrl" readonly placeholder="" />
			<n-button ghost @click="copyInviteUrl">
				<span> {{ $t("share.copyLink") }} </span>
			</n-button>
		</n-input-group>
	</m-modal>
</template>

<script setup lang="ts">
import mModal from "@/components/common/mModal/index.vue";
import { computed, onMounted, reactive, ref } from "vue";
import { globalColors } from "@/hooks/useTheme";
import { useMessage } from "naive-ui";

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
	inviteUrl: computed(() => `${location.host}/${props.urlCopy}`),
	opt: {
		inviteCount: 1, // 邀请数
		chatAward: 50, // 对话奖励
	},
});

// 复制 邀请链接
const copyInviteUrl = () => {
	navigator.clipboard.writeText(data.inviteUrl);
	msg.success("链接已复制，快分享给你的好友吧！");
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
