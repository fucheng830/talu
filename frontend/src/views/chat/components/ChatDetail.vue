<template>
	<!-- 遮罩层 -->
	<div
		class="flex max-w-[276px] transition-width"
		:class="[data.opt.collapseRight ? 'w-0 overflow-hidden' : 'w-full', isMobile ? 'h-full absolute bg-black/40 z-40' : 'transition-all duration-500']"
		@click="changeCollapseRight"
	>
		<div
			class="h-full transition-all flex-none overflow-hidden duration-500 bg-[#F5F7FA]"
			:class="[isMobile ? 'fixed right-0' : 'relative', isMobile && data.opt.collapseRight ? 'w-0' : 'w-[276px]']"
			@click.stop="() => {}"
		>
			<div class="h-full flex flex-col">
				<!-- 顶部 名称 信息 -->
				<div class="flex items-start justify-start py-4 px-3 mx-2 mb-2 border-b h-[100px]">
					<!-- 系统提示词 -->
					<div class="flex flex-col gap-y-1 text-xs ml-2 flex-1">
						<!-- 名称 -->
						<div class="flex-1 flex justify-between items-center text-[15px] font-bold text-[#1A1A1A]">
							<span>系统提示词</span>
							<Icon icon="lucide:edit" :width="12" @click="isEditing = !isEditing" />
						</div>
						<div class="text-regular text-[12px] line-height-[17px] h-[17px]">
							<div class="flex items-center">
								<n-input
									v-if="isEditing"
									v-model:value="systemPrompt"
									type="textarea"
									placeholder="输入系统提示词"
									@blur="saveSystemPrompt"
								/>
								<n-ellipsis v-else class="text-xs text-gray-500 ml-1" :line-clamp="4" style="max-width: 240px;">
									{{ data.chatInfo?.system_prompt }}
								</n-ellipsis>
							</div>
						</div>
					</div>
				</div>
			
				<!-- 模型设置 -->
				<div class="flex items-start justify-start py-4 px-3 mx-2 mb-2" v-if="data.chatInfo.llm">
					<!-- 模型设置内部 -->
					<div class="flex flex-col gap-y-1 text-xs ml-2 flex-1">
						<!-- 名称 -->
						<div class="flex-1 flex justify-between items-center text-[15px] font-bold text-[#1A1A1A]">
							<span>模型设置</span>
						</div>
						<div class="text-regular text-[12px] mt-4">
							<div class="max-w-4xl mx-auto">
								<!-- <div class="flex justify-between items-center mb-6">
									<div class="flex items-center space-x-4">
										<img alt="Model logo" class="rounded-full" height="40" src="https://oaidalleapiprodscus.blob.core.windows.net/private/org-cVasOiEuygIw9fXrYWxUwn9u/test/img-O5PKrkmc0xbR0tZAq1ZJaMbJ.png?st=2024-08-19T05%3A56%3A33Z&amp;se=2024-08-19T07%3A56%3A33Z&amp;sp=r&amp;sv=2024-08-04&amp;sr=b&amp;rscd=inline&amp;rsct=image/png&amp;skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&amp;sktid=a48cca56-e6da-484e-a814-9c849652bcb3&amp;skt=2024-08-19T02%3A58%3A03Z&amp;ske=2024-08-20T02%3A58%3A03Z&amp;sks=b&amp;skv=2024-08-04&amp;sig=RO755iEbxhTFBrZIskw1WkfA%2BLfEmoKLM/LcI5tNXfg%3D" width="40"/>
										<span class="text-purple-600 font-semibold">GPT-40 mini</span>
										<span class="bg-green-200 text-green-800 text-xs font-semibold px-2 py-1 rounded">128K</span>
									</div>
								</div> -->
								<div class="space-y-6">
									<div>
										<label class="block text-sm font-medium text-gray-700">随机性 
											<span class="bg-gray-200 text-gray-500 text-xs px-2 py-1 rounded">temperature</span>
										</label>
										<p class="text-xs text-gray-500 mt-1">值越大，回答越随机</p>
										<n-slider v-model:value="data.chatInfo.llm.temperature" :max="1" :min="0" :step="0.1" />
										<div class="text-right text-sm">{{ data.chatInfo.llm.temperature }}</div>
									</div>
									<div>
										<label class="block text-sm font-medium text-gray-700">核心性 
											<span class="bg-gray-200 text-gray-500 text-xs px-2 py-1 rounded">top_p</span>
										</label>
										<p class="text-xs text-gray-500 mt-1">与概率相关，但不要和随机性一起更改</p>
										<n-slider v-model:value="data.chatInfo.llm.top_p" :max="1" :min="0" :step="0.1" />
										<div class="text-right text-sm">{{ data.chatInfo.llm.top_p }}</div>
									</div>
									<div>
										<label class="block text-sm font-medium text-gray-700">提示惩罚性 
											<span class="bg-gray-200 text-gray-500 text-xs px-2 py-1 rounded">presence_penalty</span>
										</label>
										<p class="text-xs text-gray-500 mt-1">值越大，核心内容越受到惩罚</p>
										<n-slider v-model:value="data.chatInfo.llm.presence_penalty" :max="1" :min="0" :step="0.1" />
										<div class="text-right text-sm">{{ data.chatInfo.llm.presence_penalty }}</div>
									</div>
									<div>
										<label class="block text-sm font-medium text-gray-700">频率惩罚性 
											<span class="bg-gray-200 text-gray-500 text-xs px-2 py-1 rounded">frequency_penalty</span></label>
										<p class="text-xs text-gray-500 mt-1">值越大，核心内容越受到惩罚</p>
										<n-slider v-model:value="data.chatInfo.llm.frequency_penalty" :max="1" :min="0" :step="0.1" />
										<div class="text-right text-sm">{{ data.chatInfo.llm.frequency_penalty }}</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>

				<div class="flex items-start justify-start py-4 px-3 mx-2 mb-2 border-b" v-if="data.chatInfo.context">
					<!-- 上下文设置 -->
					<div class="flex flex-col gap-y-1 text-xs ml-2 flex-1">
						<!-- 名称 -->
						<div class="flex-1 flex justify-between items-center text-[15px] font-bold text-[#1A1A1A]">
							<span>上下文设置</span>
						</div>
						<div class="text-regular text-[12px] line-height-[17px] h-[17px]">
					
					<div class="mt-2">
						<label>上下文数量</label>
						<n-slider v-model:value="data.chatInfo.context.n" :max="30" :min="1" :step="1" />
						<div class="text-right text-sm">{{ data.chatInfo.context.n }}</div>
					</div>
					<div class="">
						<label>记忆回忆方式</label>
						<div class="mt-1">
							<n-select v-model:value="data.chatInfo.context.memory_recall" :options="memoryRecallOptions" />
						</div>
						
					</div>
						</div>
					</div>
				</div>

				
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { computed, reactive, watch, ref } from "vue";
import { Icon } from "@iconify/vue";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { useChatStore } from "@/store";

const { isMobile } = useBasicLayout();
const chatStore = useChatStore();


const data = reactive({
	chatInfo: computed(() => chatStore.currentAgent()),
	opt: {
		collapseRight: true,
	},
});
const systemPrompt = ref(data.chatInfo?.system_prompt || '');

// 保存系统提示词到原数据结构中
const saveSystemPrompt = () => {
    if (data.chatInfo) {
        data.chatInfo.system_prompt = systemPrompt.value;
    }
    isEditing.value = false;
}

// 编辑状态
const isEditing = ref(false);

const memoryRecallOptions = [
	{
		label: "keep_last",
		value: "keep_last",
	},
	{
		label: "summary",
		value: "summary",
	},
	{
		label: "rag",
		value: "rag",
	},
];
// 改变右侧栏 折叠
const changeCollapseRight = () => {
	data.opt.collapseRight = !data.opt.collapseRight;
};

// 移动端时自动隐藏右侧详情栏
watch(
    () => isMobile,
    (val) => {
        console.log('isMobile changed:', val.value);
        if (val.value) {
            data.opt.collapseRight = true;
        }
    },
    { deep: true, immediate: true }
);

// 暴露方法给父组件
defineExpose({
	collapseRight: computed(() => data.opt.collapseRight),
	changeCollapseRight,
});
</script>

<style lang="less" scoped>
.transition-width {
	transition: width 0.5s ease-in-out;
}
</style>