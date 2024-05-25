<template>
	<div class="mt-2">
		<n-data-table :columns="data.table.columns" :data="data.table.data" />
	</div>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import { useMessage } from "naive-ui";
import { t } from "@/locales";

const msg = useMessage();

const data = reactive({
	table: {
		data: [
			//   {
			//     orderID: "123456",
			//     vipSet: "VIP套餐一",
			//     money: "100",
			//     payTime: "2022-01-01 00:00:00",
			//     expire: "2022-01-01 00:00:00",
			//   },
		],
		columns: [
			{
				title: t("setting.menu.orderNumber"),
				key: "orderID",
				fixed: "left",
				align: "center",
			},
			{
				title: t("setting.menu.vipSet"),
				key: "vipSet",
				align: "center",
			},
			{
				title: t("setting.menu.money"),
				key: "money",
				align: "center",
			},
			{
				title: t("setting.menu.payTime"),
				key: "payTime",
				align: "center",
			},
			{
				title: t("setting.menu.expire"),
				key: "expire",
				align: "center",
			},
		],
	},
});
</script>

<style></style>
