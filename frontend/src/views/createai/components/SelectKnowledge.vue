<template>
	<mModal
		ref="refModal"
		:title="$t('createai.selectKnowledge')"
		:showFooter="false"
		:showCloseIcon="true"
		@onShowChange="onShowChange"
		style="width: 90vw; max-width: 600px"
	>
		<!-- style="position: fixed; top: 10%; left: 50%; transform: translate(-50%, 0)" -->
		<div class="w-full h-[80vh] flex flex-col overflow-y-auto">
			<template v-for="(item, i) in data.knowledgeList" :key="i">
				<div class="border-b hover:border-none">
					<div
						class="flex justify-between items-center gap-2 p-4 hover:bg-[#ECECF0] rounded-xl"
					>
						<div class="flex-1 flex items-center gap-4">
							<!-- 图标 -->
							<Icon icon="tdesign:data" width="36" />

							<!-- 中间信息 -->
							<div class="flex-1 flex flex-col">
								<span
									class="text-[18px] font-bold overflow-hidden text-ellipsis whitespace-nowrap"
									>{{ item.name }}</span
								>
							</div>
						</div>

						<!-- 添加按钮 -->
						<n-button tertiary size="small" @click="handleActive(item)">
							<div class="active-wrap w-[4rem] font-bold">
								<!-- 激活时，鼠标悬浮隐藏 -->
								<span :class="[item.isActive && `opacity-40 activated-hide`]">
									{{ item.isActive ? $t("common.added") : $t("common.add") }}
								</span>

								<!-- 激活时，鼠标悬浮显示 -->
								<span
									v-if="item.isActive"
									class="text-[red]"
									:class="item.isActive && 'activated'"
									>{{ $t("common.remove") }}</span
								>
							</div>
						</n-button>
					</div>
				</div>
			</template>

			<!-- 到底 -->
			<div class="flex justify-center text-[grey] mt-4">
				{{ $t("common.end") }}
			</div>
		</div>
	</mModal>
</template>

<script setup lang="ts">
import mModal from "@/components/common/mModal/index.vue";
import { useKnowledgeStore } from "@/store";
import { computed, reactive, ref, watch } from "vue";
import { Icon } from "@iconify/vue";

const emits = defineEmits(["saveForm"]);
const props = defineProps({
	knowledgeList: {
		type: Array,
		default: [],
	},
});

const knowledgeStore = useKnowledgeStore();

const refModal = ref();
const data = reactive({
	knowledgeList: [],
	rawKnowledgeList: computed(() => knowledgeStore.listKnowledge),
});

// 添加/移除
const handleActive = (item) => {
	data.knowledgeList.find((i) => i.uuid === item.uuid).isActive =
		!item.isActive;

	saveForm();
};

// 模态框显示状态 变化时
const onShowChange = (isShow: boolean) => {
	// 关闭模态框时
	if (!isShow) return;

	// 获取所有知识库
	const rawList = data.rawKnowledgeList.map((item) => ({
		...item,
		isActive: false,
	}));

	// 当前已引用知识库
	const arrPropsKnowledgeList = props.knowledgeList.map((i) => i.uuid);

	// 激活当前已引用知识库
	rawList.forEach((item) => {
		arrPropsKnowledgeList.includes(item.uuid) && (item.isActive = true);
	});

	data.knowledgeList = rawList;
};

// 提交修改
const saveForm = () => {
	const activeList = data.knowledgeList.filter((item) => item.isActive);
	emits("saveForm", activeList);
};

// 改变模态框显示
const changeModalShow = (show: boolean = undefined) => {
	refModal.value.toggleModal(show);
};

// watch(
// 	() => data.knowledgeList,
// 	() => {
// 		const activeList = data.knowledgeList.filter((item) => item.isActive);
// 		emits("saveForm", activeList);
// 	},
// 	{ deep: true }
// );

defineExpose({
	changeModalShow,
});
</script>

<style lang="less" scoped>
.active-wrap {
	.activated {
		display: none;
	}

	&:hover {
		.activated {
			display: block;
		}

		.activated-hide {
			display: none;
		}
	}
}
</style>
