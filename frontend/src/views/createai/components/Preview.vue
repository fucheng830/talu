<template>
	<!-- 遮罩层，现不在内部加 @click.stop，点任何区域都可以关闭预览 -->
	<div
		class="flex"
		:class="[
			isMobile && data.isCollapsedRight ? 'w-0' : 'w-full',
			isMobile && 'h-full absolute bg-black/40 z-40',
		]"
		@click="changeCollapsedRight"
	>
		<!-- 右侧预览页 -->
		<div
			class="flex h-full bg-[white] hover:cursor-not-allowed select-none duration-500 overflow-hidden"
			:class="[
				isMobile ? 'fixed right-0' : 'flex-1 p-3 relative',
				isMobile && data.isCollapsedRight ? 'w-0' : 'w-[300px] p-3',
			]"
		>
			<main
				class="h-full overflow-hidden flex robot-playground flex-1 rounded-t-md bg-white shadow-sm rounded-[24px]"
			>
				<div class="flex flex-col h-full flex-1 w-full">
					<!-- 顶部栏 -->
					<header
						class="flex-none h-[56px] font-bold text-[16px] flex items-center px-3 relative justify-center border-b"
					>
						<div
							class="flex flex-col items-center justify-center font-bold leading-none"
						>
							{{ roleName == "" ? "未命名角色" : roleName }}
						</div>
					</header>
					<!-- 聊天区 -->
					<div class="w-full flex justify-center h-full overflow-hidden">
						<div
							class="h-full overflow-hidden overflow-y-auto flex-1 max-w-screen-xl"
						>
							<div class="w-full max-w-screen-xl m-auto dark:bg-[#101014] p-4">
								<div class="flex w-full mb-6 overflow-hidden items-start">
									<!-- 头像 -->
									<div
										class="flex items-center justify-center overflow-hidden rounded-full flex-none mr-2"
									>
										<Icon icon="uil:robot" width="26" />
									</div>

									<div class="overflow-hidden text-[15px] flex-1 items-start">
										<!-- 时间 -->
										<p class="text-xs text-[#b4bbc4] text-left">
											{{ data.curTime }}
										</p>
										<!-- 聊天内容 -->
										<div class="flex items-end gap-1 mt-2 flex-row">
											<div
												class="text-primary message-text text-wrap min-w-[20px] rounded-2xl px-[14px] py-[10px] bg-[white] dark:bg-[#1e1e20] message-reply text-primary"
											>
												<div class="leading-relaxed break-words">
													<p>
														{{
															chatPrologue == ""
																? "还未设置你角色的开场白…"
																: chatPrologue
														}}
													</p>
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<!-- 底部输入栏 -->
					<footer class="px-4 py-[12px]">
						<div class="w-full max-w-screen-xl m-auto">
							<div class="flex items-end justify-between space-x-2">
								<div class="flex flex-col flex-1">
									<n-input
										v-model:value="data.txtInput"
										round
										size="large"
										:autosize="{
											minRows: 1,
											maxRows: 5,
										}"
										:placeholder="$t('chat.placeholderMobile')"
									>
										<!-- 发送按钮 -->
										<template #suffix>
											<div
												class="pl-[2px] border-l cursor-pointer"
												@click="handleSend"
											>
												<Icon
													icon="entypo:paper-plane"
													width="22"
													color="#d2c4fc"
												/>
											</div>
										</template>
									</n-input>
								</div>
							</div>
						</div>
					</footer>
				</div>
			</main>

			<!-- 内部遮罩层 -->
			<div
				v-if="data.isShowMask"
				class="absolute top-0 left-0 bg-[rgba(17,14,34,0.15)] w-full h-full z-50 select-none flex justify-center items-center"
			>
				<div
					class="w-[192px] h-[140px] bg-[rgba(17,14,34,0.08)] rounded-2xl text-[#F9F9FA] text-[12px] flex justify-center items-center flex-col leading-none"
				>
					<div
						class="flex justify-center items-center w-[64px] h-[64px] bg-[rgba(255,255,255,0.1)] rounded-full"
					>
						<Icon
							icon="ph:identification-badge-light"
							width="48"
							color="white"
						/>
					</div>
					<p class="font-bold pt-[6px] px-[10px] text-center leading-normal">
						完成角色设定 即可预览调试
					</p>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { onMounted, reactive } from "vue";
import { Icon } from "@iconify/vue";
import { useBasicLayout } from "@/hooks/useBasicLayout";

const { isMobile } = useBasicLayout();

const props = defineProps({
	isCollapsedRight: {
		type: Boolean,
		default: false,
	},
	roleName: {
		type: String,
		default: "",
	},
	chatPrologue: {
		type: String,
		default: "",
	},
});

const data = reactive({
	curTime: "",
	isShowMask: true,
	isCollapsedRight: true,
});

// 修改当前右侧预览部分的折叠状态
const changeCollapsedRight = () => {
	data.isCollapsedRight = !data.isCollapsedRight;
};

onMounted(() => {
	// 第一条消息显示当前页加载时的时间
	const date = new Date();
	data.curTime = `${date.getMonth()}/${date.getDate()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
});

defineExpose({
	changeCollapsedRight,
});
</script>

<style lang="less" scoped>
// 取消折叠过程中因空间不足导致的自动换行
* {
	white-space: nowrap;
	flex-wrap: nowrap;
}
</style>
