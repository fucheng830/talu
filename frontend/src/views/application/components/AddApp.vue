<template>
	<m-modal
		ref="refModal"
		title="创建属于你的 AI 应用"
		style="
			max-width: 600px;
			width: 90%;
			border-radius: 30px;
			position: fixed;
			top: 5%;
			left: 50%;
			transform: translate(-50%, 0);
		"
	>
		<div class="flex flex-col gap-4 mt-6">
			<!-- 头像、名称 包围 -->
			<div class="flex flex-col">
				<p class="font-bold">取个名字</p>
				<div class="flex items-center gap-4">
					<div class="pt-3">
						<!-- 提示框 -->
						<n-popover
							placement="bottom"
							trigger="hover"
							:keep-alive-on-hover="false"
						>
							<template #trigger>
								<!-- 上传 -->
								<n-upload
									action="https://www.mocky.io/v2/5e4bafc63100007100d8b70f"
								>
									<!-- 头像 -->
									<n-avatar round size="medium" :src="data.form.avatar" />
								</n-upload>
							</template>
							点击设置头像
						</n-popover>
					</div>

					<!-- 名称 -->
					<div class="flex-1">
						<n-input
							v-model:value="data.form.name"
							type="text"
							placeholder=""
						/>
					</div>
				</div>
			</div>

			<!-- 从模板中选择 -->
			<div class="flex flex-col gap-2">
				<p class="font-bold">从模板中选择</p>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
					<template v-for="item in data.opt.appTemplate" :key="item.type">
						<div
							@click="changeCurType(item)"
							class="border rounded-lg shadow-sm hover:shadow-md px-3 py-2 cursor-pointer select-none"
							:class="[data.curType === item.type ? `bg-[#F4F6F8]` : '']"
						>
							<div class="flex items-center gap-2">
								<Icon :icon="item.icon" width="24" color="grey" />
								<span class="font-bold">{{ item.label }}</span>
							</div>

							<span class="text-[12px]">{{ item.desc }}</span>
						</div>
					</template>
				</div>
			</div>
		</div>
	</m-modal>
</template>

<script setup lang="ts">
import mModal from "@/components/common/mModal/index.vue";
import { reactive, ref } from "vue";
import { Icon } from "@iconify/vue";
import { globalColors } from "@/hooks/useTheme";

const refModal = ref();
const data = reactive({
	form: {
		avatar: "https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg", // 应用头像
		name: "", // 应用名称
	},
	curType: "simpleChat", // 当前模板类型
	opt: {
		// 模板类型
		appTemplate: [
			{
				type: "simpleChat",
				label: "简单的对话",
				desc: "一个极其简单的 AI 对话应用",
				icon: "material-symbols:person-apron-outline",
			},
			{
				type: "knowledge_chatGuide",
				label: "知识库 + 对话引导",
				desc: "每次提问时进行一次知识库搜索，将搜索结果注入 LLM 模型进行参考回答",
				icon: "solar:cloud-storage-bold-duotone",
			},
			{
				type: "chatGuide_variable",
				label: "对话引导 + 变量",
				desc: "可以在对话开始发送一段提示，或者让用户填写一些内容，作为本次对话的变量",
				icon: "ri:kakao-talk-fill",
			},
			{
				type: "questionClassify_knowledge",
				label: "问题分类 + 知识库",
				desc: "先对用户的问题进行分类，再根据不同类型问题，执行不同的操作",
				icon: "mdi:head-idea",
			},
		],
	},
});

// 改变当前模板类型
const changeCurType = (item) => {
	data.curType = item.type;
};

defineExpose({
	changeModalShow: () => refModal.value?.toggleModal(),
});
</script>

<style lang="less" scoped></style>
