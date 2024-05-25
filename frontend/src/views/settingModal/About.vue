<template>
	<!-- 平台描述 -->
	<div class="border-b py-[24px] flex items-center text-primary">
		<!-- 头像 -->
		<div class="w-[76px] h-[76px]">
			<n-image width="100" src="/avatar.jpg" object-fit="contain" lazy />
		</div>
		<!-- 右侧 文字 -->
		<div class="ml-[16px]">
			<h3 class="font-bold text-[20px]">QuChat</h3>
			{{ $t("setting.menu.subTitle5") }}
		</div>
	</div>

	<!-- 其他信息 -->
	<div class="py-[16px]">
		<h3 class="font-bold pb-[16px]">
			{{ $t("setting.menu.otherInformation") }}
		</h3>
		<p>{{ $t("setting.menu.Email") }}: {{ data.opt.email }}</p>
	</div>
	<div>
		<a href="https://work.weixin.qq.com/kfid/kfcf34773bc3f87c4f1">
			<NButton block>
				<Icon icon="ri:customer-service-2-line" />
				<span class="ml-1">{{
					$t("setting.menu.contactCustomerService")
				}}</span>
			</NButton>
		</a>
	</div>
</template>

<script setup lang="ts">
import { reactive } from "vue";
// 平台logo

const data = reactive({
	opt: {
		email: "fucheng@123qiming.com", // 联系邮箱
	},
});
</script>

<style></style>
