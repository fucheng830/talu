<template>
	<div class="w-60 rounded-lg p-4 text-sm">
		<div class="mb-2 text-sm text-[grey]">
			{{ $t("createai.checkPermission") }}
		</div>

		<div class="flex flex-col gap-3 text-sm">
			<n-radio-group v-model:value="data.form.permission" name="permission">
				<n-space vertical>
					<n-radio
						v-for="item in data.opt.permission"
						:key="item.value"
						:value="item.value"
					>
						<span>{{ item.label }}</span>
					</n-radio>
				</n-space>
			</n-radio-group>

			<!-- 仅限邀请、所有人 -->
			<template v-if="data.form.permission != 'only_me'">
				<div
					class="relative flex w-full flex-col items-center justify-stretch rounded-lg p-4"
				>
					<div class="absolute right-4 top-3 text-xs text-token-text-tertiary">
						<Icon icon="tdesign:edit" width="18" color="grey" />
					</div>

					<!-- 头像 -->
					<n-avatar round :src="chatInfo?.avatar" />
					<!-- 名称 -->
					<div class="mt-1 text-center text-[13px] font-medium">
						<span>{{ chatInfo?.name }}</span>
					</div>
					<!-- 作者 -->
					<div
						class="mt-1 flex flex-row items-center space-x-1 text-[grey] text-[12px]"
					>
						<span>{{ $t("createai.from") }} {{ data.opt.userInfo?.name }}</span>
					</div>
				</div>
			</template>

			<!-- 所有人 -->
			<!-- <template v-if="data.form.permission == 'public'">
				<div class="flex items-center justify-between text-sm text-[grey]">
					<span> 种类 </span>

					<IconTip msg="该GPT可能会公开在广场的角色列表中" />
				</div>

				<n-select
					v-model:value="data.form.category"
					:options="data.opt.category"
				/>
			</template> -->
		</div>

		<div class="w-full mt-4">
			<n-button block type="primary" @click="handleSubmit">
				{{ $t("common.confirm") }}
			</n-button>
		</div>
	</div>
</template>

<script setup lang="ts">
import { reactive, computed } from "vue";
import { Icon } from "@iconify/vue";
import { useUserStore } from "@/store";
import { defineEmits } from "vue";
import { t } from "@/locales";

const emits = defineEmits(["saveForm", "emitForm"]);

const userStore = useUserStore();

const data = reactive({
	form: {
		permission: "only_me",
		// category: "other",
	},
	opt: {
		userInfo: computed(() => userStore.userInfo),
		permission: [
			{
				label: t("createai.private"),
				value: "only_me",
			},
			{
				label: t("createai.inviteOnly"),
				value: "share",
			},
			{
				label: t("createai.everyone"),
				value: "public",
			},
		],
		// category: [
		// 	{
		// 		label: "DALL·E",
		// 		value: "dall_e",
		// 	},
		// 	{
		// 		label: "Other",
		// 		value: "other",
		// 	},
		// ],
	},
});

// 确认 保存
const handleSubmit = () => {
	emits("saveForm", data.form);
	emits("emitForm");
};
</script>

<style lang="less" scoped></style>
