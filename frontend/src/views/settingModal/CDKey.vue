<template>
	<div>
		<n-form ref="refForm" :model="data.form" class="pt-4 max-w-[480px]">
			<n-form-item :label="$t('setting.menu.activateVIP')" path="inviteKey">
				<n-input-group style="border-radius: 20px">
					<n-input
						v-model="data.form.inviteKey"
						:placeholder="$t('setting.menu.placeholderActivateVIP')"
					/>
					<n-button type="primary" @click="handleActivate">
						{{ $t("setting.menu.activate") }}
					</n-button>
				</n-input-group>
			</n-form-item>
		</n-form>
		<span class="font-bold"> {{ $t("setting.menu.activatedHistory") }} </span>
		<div class="mt-2">
			<n-data-table :columns="data.table.columns" :data="data.table.data" />
		</div>
	</div>
</template>

<script setup lang="ts">
import { t } from "@/locales";
import { reactive, ref } from "vue";

const refForm = ref();
const data = reactive({
	form: {
		inviteKey: "",
	},
	table: {
		data: [
			//   {
			//     activateKey: "123456",
			//     vipSet: "VIP套餐一",
			//     activateDate: "2022-01-01 00:00:00",
			//   },
		],
		columns: [
			{
				title: t("setting.menu.CDKey"),
				key: "activateKey",
				fixed: "left",
				align: "center",
			},
			{
				title: t("setting.menu.bindSet"),
				key: "vipSet",
				align: "center",
			},
			{
				title: t("setting.menu.activateDate"),
				key: "activateDate",
				align: "center",
			},
		],
	},
});

// 激活 激活码
const handleActivate = () => {
	console.log("inviteKey", data.form.inviteKey);
};
</script>

<style lang="less" scoped>
:deep(.n-form-item-label) {
	font-weight: bold;
}
</style>
