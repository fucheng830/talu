<template>
	<mModal
		ref="refModal"
		title="更多设置"
		footerBtnSize="medium"
		footerComfirmBtnType="primary"
		txtCancel="关闭"
		txtConfirm="确认"
		@onShowChange="onShowChange"
		@onPositiveClick="handleComfirm"
		style="
			width: 600px;
			position: fixed;
			top: 10%;
			left: 50%;
			transform: translate(-50%, 0);
		"
	>
		<div class="flex flex-col gap-4 py-4">
			<div class="grid grid-cols-4 gap-y-2">
				<div class="mb-4">返回AI内容</div>
				<div class="col-span-3">
					<n-switch v-model:value="data.form.isReturnAIContent" />
				</div>

				<div>温度</div>
				<div class="col-span-3">
					<n-slider
						v-model:value="data.form.temperature"
						:marks="data.opt.temperature"
						:min="0"
						:max="10"
						:step="1"
					/>
				</div>

				<div>回复上限</div>
				<div class="col-span-3">
					<n-slider
						v-model:value="data.form.replyLimit"
						:marks="data.opt.replyLimit"
						:min="100"
						:max="4000"
						:step="50"
					/>
				</div>
			</div>

			<!-- 引用内容模板 -->
			<div class="flex flex-col">
				<div class="flex justify-between">
					<span class="flex items-center">
						引用内容模板
						<IconPopover>
							<div class="whitespace-pre-wrap">
								{{ data.opt.txtTemplatePlaceholder }}
							</div>
						</IconPopover>
					</span>

					<div>
						<n-button type="primary" text @click="changeModalSelectTemplateShow">
							选择模板
						</n-button>
					</div>
				</div>

				<n-input
					v-model:value="data.form.txtTemplate"
					type="textarea"
					:autosize="{
						minRows: 6,
						maxRows: 10,
					}"
					:placeholder="data.opt.txtTemplatePlaceholder"
					style="font-size: 12px"
				/>
			</div>

			<!-- 引用模板提示词 -->
			<div class="flex flex-col">
				<span class="flex items-center">
					引用模板提示词
					<IconPopover>
						<div class="whitespace-pre-wrap">
							{{ data.opt.txtTipPlaceholder }}
						</div>
					</IconPopover>
				</span>

				<n-input
					v-model:value="data.form.txtTip"
					type="textarea"
					:autosize="{
						minRows: 12,
						maxRows: 12,
					}"
					:placeholder="data.opt.txtTipPlaceholder"
					style="font-size: 12px"
				/>
			</div>
		</div>
	</mModal>

	<mModal
		ref="refModalSelectTemplate"
		title="选择引用提示模板"
		footerBtnSize="medium"
		footerComfirmBtnType="primary"
		txtCancel="关闭"
		txtConfirm="确认"
		@onShowChange="onSelectTemplateShowChange"
		@onPositiveClick="handleSelectTemplateComfirm"
		style="
			width: 600px;
			position: fixed;
			top: 10%;
			left: 50%;
			transform: translate(-50%, 0);
		"
	>
		<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
			<template v-for="item in dataTemplate.opt.templateList" :key="item.key">
				<div
					@click="handleSelectTemplate(item)"
					class="p-2 border rounded-xl cursor-pointer select-none"
					:class="[dataTemplate.curTemplate === item.key ? 'bg-[#F0F4FF]' : '']"
				>
					<p>{{ item.label }}</p>
					<span class="text-[grey] text-[12px]">{{ item.desc }}</span>
				</div>
			</template>
		</div>
	</mModal>
</template>

<script setup lang="ts">
import mModal from "@/components/common/mModal/index.vue";
import { reactive, ref } from "vue";
import IconPopover from "@/components/common/IconPopover/index.vue";

const refModal = ref();
const refModalSelectTemplate = ref();
const data = reactive({
	form: {
		isReturnAIContent: true, // 返回AI内容
		temperature: 0, // 温度
		replyLimit: 2000, // 引用内容模板
		txtTemplate: "", // 引用内容模板
		txtTip: "", // 引用模板提示词
	},
	formBackup: {}, // 表单备份，用于重置
	opt: {
		temperature: {
			0: "严谨",
			10: "发散",
		},
		replyLimit: {
			100: "100",
			4000: "4000",
		},
		txtTemplatePlaceholder: `该配置只有传入引用内容（知识库搜索）时生效。
可以自定义引用内容的结构,以更好的适配不同场景。可以使用一些变量来进行模板配置：
{{q}}-检索内容， {{a}}-预期内容, {{source}}-来源,{{sourceld}}-来源文件名
{{index}}-第n个引用,{{score}}-该引用的得分(0-1)，他们都是可选的，下面是默认值：
{{q}}
{{a}}`,
		// 模板中空行需留着
		txtTipPlaceholder: `该配置只在知识库搜索时生效。
可以用{{ quote }}来插入引用内容模板，使用{{question}}来插入问题。下面是默认值：
使用 <Data></Data> 标记中的内容作为你的知识:

<Data>
{{quote}}
</Data>

回答要求：
- 如果你不清楚答案，你需要澄清。
- 避免提及你是从 <Data></Data> 获取的知识。
- 保持答案与 <Data></Data> 中描述的一致。`,
	},
});

const dataTemplate = reactive({
	curTemplate: "",
	curTemplateBackup: "",
	opt: {
		templateList: [
			{
				label: "标准模板",
				key: "common",
				desc: "标准提示词，用于结构不固定的知识库。",
				txtTemplate: `{{q}}
{{a}}`,
				txtTip: `使用 <Data></Data> 标记中的内容作为你的知识:

<Data>
{{quote}}
</Data>

回答要求：
- 如果你不清楚答案，你需要澄清。
- 避免提及你是从 <Data></Data> 获取的知识。
- 保持答案与 <Data></Data> 中描述的一致。
- 使用 Markdown 语法优化回答格式。
- 使用与问题相同的语言回答。

问题:"""{{question}}"""`,
			},
			{
				label: "问答模板",
				key: "questionAnswer",
				desc: "适合 QA 问答结构的知识库，可以让AI较为严格的按预设内容回答",
				txtTemplate: `<Question>
{{q}}
</Question>
<Answer>
{{a}}
</Answer>`,
				txtTip: `使用 <QA></QA> 标记中的问答对进行回答。

<QA>
{{quote}}
</QA>

回答要求：
- 选择其中一个或多个问答对进行回答。
- 回答的内容应尽可能与 <答案></答案> 中的内容一致。
- 如果没有相关的问答对，你需要澄清。
- 避免提及你是从 QA 获取的知识，只需要回复答案。

问题:"""{{question}}"""`,
			},
			{
				label: "标准严格模板",
				key: "commonStrict",
				desc: "在标准模板基础上，对模型的回答做更严格的要求。",
				txtTemplate: `{{q}}
{{a}}`,
				txtTip: `忘记你已有的知识，仅使用 <Data></Data> 标记中的内容作为你的知识:

<Data>
{{quote}}
</Data>

思考流程：
1. 判断问题是否与 <Data></Data> 标记中的内容有关。
2. 如果有关，你按下面的要求回答。
3. 如果无关，你直接拒绝回答本次问题。

回答要求：
- 避免提及你是从 <Data></Data> 获取的知识。
- 保持答案与 <Data></Data> 中描述的一致。
- 使用 Markdown 语法优化回答格式。
- 使用与问题相同的语言回答。

问题:"""{{question}}"""`,
			},
			{
				label: "严格问答模板",
				key: "questionAnswerStrict",
				desc: "在问答模板基础上，对模型的回答做更严格的要求。",
				txtTemplate: `<Question>
{{q}}
</Question>
<Answer>
{{a}}
</Answer>`,
				txtTip: `忘记你已有的知识，仅使用 <QA></QA> 标记中的问答对进行回答。

<QA>
{{quote}}
</QA>}

思考流程：
1. 判断问题是否与 <QA></QA> 标记中的内容有关。
2. 如果无关，你直接拒绝回答本次问题。
3. 判断是否有相近或相同的问题。
4. 如果有相同的问题，直接输出对应答案。
5. 如果只有相近的问题，请把相近的问题和答案一起输出。

最后，避免提及你是从 QA 获取的知识，只需要回复答案。

问题:"""{{question}}"""`,
			},
		],
	},
});

// 确认
const handleComfirm = () => {
	console.log("commit");
	// todo 提交配置更改
};

// 重置表单
const resetForm = () => {
	data.form = { ...data.form, ...data.formBackup };
};

// 模态框显示状态 变化时
const onShowChange = (isShow: boolean) => {
	// 关闭模态框时
	if (!isShow) return resetForm();

	// 备份表单，用于重置
	data.formBackup = JSON.parse(JSON.stringify(data.form));
};

// 改变模态框显示
const changeModalShow = () => {
	refModal.value.toggleModal();
};

// 改变选择模板模态框显示
const changeModalSelectTemplateShow = () => {
	refModalSelectTemplate.value.toggleModal();
};

// 选择模板
const handleSelectTemplate = (item) => {
	dataTemplate.curTemplate = item.key;
};

// 确认选择模板
const handleSelectTemplateComfirm = () => {
	const { txtTemplate, txtTip } = dataTemplate.opt.templateList.find(
		(item) => item.key === dataTemplate.curTemplate
	);
	data.form.txtTemplate = txtTemplate;
	data.form.txtTip = txtTip;
	changeModalSelectTemplateShow();
};

// 模态框显示状态 变化时
const onSelectTemplateShowChange = (isShow: boolean) => {
	// 关闭模态框时
	if (!isShow) dataTemplate.curTemplate = "";
};

defineExpose({
	changeModalShow,
});
</script>

<style lang="less" scoped></style>
