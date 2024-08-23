<template>
	<div class="flex flex-col py-4">
		<!-- 邀请框 -->
		<div
			class="text-primary text-sm border p-4 rounded-md flex-col flex-center"
		>
			<div class="pb-2">
				{{ $t("share.invite") }}
				<span :style="{ color: theme.primaryColor }">
					{{ data.opt.inviteCount }}
				</span>
				{{ $t("share.invite2") }}
				<span :style="{ color: theme.primaryColor }">
					{{ data.opt.inviteChat }}
				</span>
				{{ $t("share.invite3") }}
			</div>
			<n-button type="primary" size="small" ghost @click="copyInviteUrl">
				<span class="p-5">{{ $t("share.inviteFriend") }}</span>
			</n-button>
		</div>

		<!-- 邀请记录 -->
		<div class="flex flex-col text-primary mt-4 mb-1 text-sm">
			<span class="mb-2">{{ $t("setting.menu.inviteHistory") }}</span>

			<n-data-table :columns="data.table.columns" :data="data.table.data" />
		</div>
	</div>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import { useMessage } from "naive-ui";
import { t } from "@/locales";
import { useThemeVars } from "naive-ui";

const theme = useThemeVars();
const msg = useMessage();

const data = reactive({
	opt: {
		inviteCount: 1,
		inviteChat: 50,
		inviteUrl: "www.baidu.com",
	},
	table: {
		data: [
			//   {
			//     username: "张三",
			//     account: "zhangsan",
			//     registerTime: "2022-01-01 00:00:00",
			//     award: "50",
			//   },
		],
		columns: [
			{
				title: t("common.username"),
				key: "username",
				fixed: "left",
				align: "center",
			},
			{
				title: t("common.account"),
				key: "account",
				align: "center",
			},
			{
				title: t("setting.menu.registerTime"),
				key: "registerTime",
				align: "center",
			},
			{
				title: t("setting.menu.award"),
				key: "award",
				align: "center",
				width: 80,
			},
		],
	},
});

// 复制邀请链接
const copyInviteUrl = () => {
	navigator.clipboard.writeText(data.opt.inviteUrl);
	msg.success(t("share.copyedGoShare"));
};
</script>

<style></style>
