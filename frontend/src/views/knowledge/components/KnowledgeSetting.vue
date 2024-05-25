<template>
	<m-modal
		ref="refModal"
		:title="$t('knowledge.createNewKnowledge')"
		:comfirmDisabled="data.form.name?.length <= 0"
		style="width: 700px; border-radius: 30px"
		@onPositiveClick="createKnowledge"
	>
		<div class="flex flex-col mt-[24px]">
			<div class="flex width-full gap-[12px]" :class="[isMobile && 'flex-col']">
				<!-- 分段方式 单选 -->
				<template v-for="item in data.arrSegmentType" :key="item.key">
					<div
						@click="changeSegmentType(item.key)"
						class="flex-1 flex flex-col rounded-[8px] bg border hover:cursor-pointer hover:bg-white p-2"
						:class="[
							`hover:border-[blue]`,
							data.knowledgeType == item.key
								? 'border-[blue] bg-white'
								: 'bg-[#F5F5F5]',
						]"
					>
						<div class="h-full flex items-center pl-[16px] pr-[16px]">
							<div class="rounded flex items-center mr-[16px]">
								<!-- 图标 -->
								<Icon :icon="item.icon" width="36" />
							</div>

							<!-- 分割线 -->
							<div class="w-0 h-[40px] border-r mr-[16px]"></div>

							<!-- 右侧字样 -->
							<div class="flex flex-col flex-1">
								<div class="flex-col justify-center">
									<!-- 标题 -->
									<span
										class="text text-primary w-full flex justify-between font-bold text-[14px] leading-[20px]"
									>
										{{ item.title }}

										<!-- radio 单选 -->
										<n-radio
											:checked="data.knowledgeType === item.key"
											:value="item.key"
											name="segmentType"
										/>
									</span>

									<!-- 描述 -->
									<span
										class="text-[12px] leading-[17px] mt-[4px] text-[#999999]"
									>
										{{ item.desc }}
									</span>
								</div>
							</div>
						</div>
					</div>
				</template>
			</div>
		</div>

		<!-- 名字输入框 -->
		<n-form-item :label="$t('knowledge.nameOfKnowledge')" class="mt-[24px]">
			<n-input
				v-model:value="data.form.name"
				:placeholder="$t('knowledge.placeholderNameOfKnowledge')"
			/>
		</n-form-item>
	</m-modal>
</template>

<script setup lang="ts">
import mModal from "@/components/common/mModal/index.vue";
import { reactive, ref } from "vue";
import { Icon } from "@iconify/vue";
import { useMessage } from "naive-ui";
import { useKnowledgeStore } from "@/store";
import { router } from "@/router"; // Import the router object from the appropriate package
import { useRouter } from "vue-router";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { t } from "@/locales";
const { isMobile } = useBasicLayout();

const refModal = ref();
const msg = useMessage();
const router = useRouter();

const knowledgeStore = useKnowledgeStore();

const data = reactive({
	// 当前
	knowledgeType: "normal",
	form: {
		name: "",
	},
	// 分段方式
	arrSegmentType: [
		{
			key: "normal",
			title: t("knowledge.commonKnowledge"),
			desc: t("knowledge.subscriptionFromWebsideDesc"),
			icon: "mdi:refresh-auto",
		},
		{
			key: "website-subscription",
			title: t("knowledge.subscriptionFromWebside"),
			desc: t("knowledge.subscriptionFromWebsideDesc"),
			icon: "tabler:circle-letter-m",
		},
	],
});

// 改变分段选项
const changeSegmentType = (key: string) => {
	data.knowledgeType = key;
};

const createKnowledge = () => {
	// 获取 Pinia store 实例

	// 创建知识项数据结构
	const knowledgeItem = {
		name: data.form.name,
		type: data.knowledgeType,
	};

	// 使用store中定义的addKnowledge方法
	knowledgeStore
		.addKnowledge(knowledgeItem)
		.then((res) => {
			// 提示创建成功
			msg.success("创建成功");
			// 关闭模态框，确保refModal是一个 ref 并且包含 toggleModal 方法
			if (refModal.value) {
				refModal.value.toggleModal();
			}
			// 如果你需要跳转到知识库详情页，这里假定res.data包含必要的uuid
			// 你可以根据你的实际情况修改这一部分
			console.log("返回的知识库uuid", res);

			router.push(`knowledgeDetails/dataset/${res}`);
		})
		.catch((error) => {
			// 如果有错误发生，处理它们（例如显示错误消息）
			console.error(`知识库创建失败：`, error);
			msg.error(`${t("knowledge.createFail")}`);
		});
};

defineExpose({
	changeModalShow: () => refModal.value?.toggleModal(),
});
</script>

<style lang="less" scoped>
// 自定义分段(选项表单) > 标题行
:deep(.n-form-item-label__text) {
	font-weight: bold;
}
</style>
