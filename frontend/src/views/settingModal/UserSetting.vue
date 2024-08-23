<template>
	<div class="h-full overflow-y-auto flex flex-col">
		<div class="flex-1 max-w-[380px] mt-[10px]">
			<n-form
				ref="refForm"
				:model="data.form"
				:rules="data.rules"
				label-placement="left"
				label-align="left"
				label-width="auto"
				require-mark-placement="right-hanging"
				:style="{
					maxWidth: '640px',
				}"
			>
				<n-form-item :label="$t('setting.menu.avatar')" path="avator">
					<n-upload
						action="https://www.mocky.io/v2/5e4bafc63100007100d8b70f"
						:default-file-list="data.arrAvator"
						list-type="image-card"
						:max="1"
						:show-retry-button="false"
						:trigger-style="{
							width: '48px',
							height: '48px',
							'border-radius': '999px',
						}"
					>
						<Icon icon="bytesize:plus" width="14" color="inherit" />
					</n-upload>
				</n-form-item>

				<n-form-item :label="$t('setting.menu.nickname')" path="username">
					<n-input
						v-model:value="data.form.username"
						type="text"
						:placeholder="$t('setting.menu.placeholderNickname')"
					/>
				</n-form-item>

				<!-- <n-form-item label="剩余聊天条数" path="username">
					<div class="flex gap-2">
						<span>{{ data.opt.chatCount }} </span>
						<n-button text type="primary"> 开通VIP </n-button>
					</div>
				</n-form-item>

				<n-form-item label="我的角色" path="myRole">
					<div class="flex gap-2">
						<span>{{ data.opt.myRole }} / {{ data.opt.myRoleMax }} </span>
						<n-button text type="primary"> 更多角色 </n-button>
					</div>
				</n-form-item>

				<n-form-item label="知识库" path="knowledge">
					<div class="flex gap-2">
						<span>{{ data.opt.knowledge }} / {{ data.opt.knowledgeMax }} </span>
					</div>
				</n-form-item> -->

				<n-form-item :label="$t('setting.menu.theme')" path="sysTheme">
					<div class="flex gap-4">
						<template v-for="item in data.opt.sysTheme" :key="item.value">
							<n-button type="primary" @click="changeTheme(item)">
								<Icon :icon="item.icon" width="18" color="inherit" />
								<span class="ml-2">{{ item.label }}</span>
							</n-button>
						</template>
					</div>
				</n-form-item>

				<n-form-item :label="$t('setting.menu.lang')" path="lang">
					<n-select v-model:value="data.form.lang" :options="data.opt.lang" />
					<!-- @update:value="changeLang" -->
				</n-form-item>
			</n-form>
		</div>

		<footer class="w-full" :class="[!isMobile && 'px-[32px]']">
			<div class="border-t w-full flex items-center justify-between">
				<div>
					<template v-if="isMobile">
						<n-button
							ghost
							:size="isMobile && 'small'"
							@click="handleLogoutMobile"
						>
							<Icon icon="line-md:log-out" :width="20" />
							<span class="ml-1"> 退出登录 </span>
						</n-button>
					</template>
				</div>
				<div class="h-[64px] flex items-center gap-4">
					<n-button type="primary" :size="isMobile && 'small'">
						<span class="px-4"> 保存</span>
					</n-button>
					<n-button type="tertiary" :size="isMobile && 'small'">
						<span class="px-4"> 取消</span>
					</n-button>
				</div>
			</div>
		</footer>
	</div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import { Icon } from "@iconify/vue";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { useAppStore, useUserStore } from "@/store";
import { t } from "@/locales";


const { isMobile } = useBasicLayout();

const emit = defineEmits(["handleLogout"]);

const appStore = useAppStore();
const userStore = useUserStore();
const userInfo = computed(() => userStore.$state.userInfo);
// console.log(userInfo.value);

const refForm = ref();
const data = reactive({
	form: {
		avator: userInfo.value?.avatar, // 头像
		username: userInfo.value?.name, // 昵称
		theme: "light", // 主题
		lang: computed({
			get() {
				return appStore.language;
			},
			set(value: Language) {
				appStore.setLanguage(value);
			},
		}), // 语言
	},
	arrAvator: [], // 头像上传列表
	opt: {
		chatCount: 10, // 剩余聊天条数
		myRole: 0, // 我的角色
		myRoleMax: 1, // 我的角色 最多限制
		knowledge: 0, // 知识库
		knowledgeMax: 0, // 知识库 最多限制
		// 系统主题
		sysTheme: [
			{
				label: t("setting.menu.themeDay"),
				value: "light",
				icon: "entypo:light-up",
			},
			//   {
			// 		 label: t("setting.menu.themeNight"),
			//     value: "night",
			//     icon: "tdesign:fog-night",
			//   },
		],
		lang: [
			{
				label: t("setting.menu.langZhCN"),
				value: "zh-CN",
			},
			{
				label: t("setting.menu.langEn"),
				value: "en-US",
			},
		],
	},
	//   校验规则
	rules: {},
});

// 改变主题
const changeTheme = (item) => {
	data.form.theme = item.value;
};

// 改变语言
// const changeLang = (value: string, option: SelectOption) => {
// 	console.log(value, option);
// };

// 退出登录
const handleLogoutMobile = () => {
	emit("handleLogout");
};
// 保存用户资料设置
</script>

<style lang="less" scoped>
// 上传按钮 圆边框
:deep(.n-upload-dragger) {
	border-radius: 999px;
}

// 表单左侧label 粗体
:deep(.n-form-item-label__text) {
	font-weight: bold;
}
</style>
