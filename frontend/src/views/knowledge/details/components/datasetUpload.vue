<template>
	<div class="w-full h-full flex flex-col gap-4 py-6 px-8">
		<div class="flex">
			<!-- 第一步时 返回 知识库首页 -->
			<template v-if="data.curStep === 1">
				<div
					class="flex items-center gap-3 cursor-pointer"
					@click="handleGoKnowledgeDetail()"
				>
					<!-- 返回图标 箭头 左 -->
					<div
						class="p-1 rounded-full"
						:style="{ 'box-shadow': '1px 1px 9px rgba(0,0,0,.15)' }"
					>
						<Icon
							icon="gravity-ui:arrow-left"
							:color="theme.primaryColor"
							width="22"
						/>
					</div>
					<span>退出</span>
				</div>
			</template>
			<!-- 非第一步时，返回上一步 -->
			<template v-else>
				<n-button style="border-radius: 8px">
					<div
						class="flex items-center gap-3 cursor-pointer"
						@click="data.curStep -= 1"
					>
						<!-- 返回图标 箭头 左 -->
						<Icon icon="gravity-ui:arrow-left" width="22" />
						<span>上一步</span>
					</div>
				</n-button>
			</template>
		</div>

		<!-- 顶部步骤栏 -->
		<div class="px-8 py-2 bg-[#F7F8FA] border rounded-lg">
			<n-steps :current="data.curStep" :status="data.curProgress" :size="small">
				<n-step title="上传文件" />
				<n-step title="数据切分" />
				<n-step title="数据索引" />
			</n-steps>
		</div>

		<!-- step1 选择文件 -->
		<div v-show="data.curStep === 1">
			<n-upload
				ref="refUpload"
				directory-dnd
				multiple
				:action=upload_endpoint
				:headers="{ Authorization: 'Bearer ' + token }"
				:max="1000"
				:default-upload="true"
				@change="handleUploadChange"
				@finish="handleUploadFinish"
			>
				<n-upload-dragger>
					<div class="flex justify-center">
						<Icon
							icon="ion:cloud-upload"
							:color="theme.primaryColor"
							width="32"
						/>
					</div>
					<div class="font-bold">点击或者拖动文件到该区域来上传</div>
					<div class="text-[grey] text-[12px]">
						<p>支持 .txt, .docx, .csv, .pdf, .md, .html 类型文件</p>
						<p>最多支持 1000 个文件。单个文件最大 30 MB</p>
					</div>
				</n-upload-dragger>
			</n-upload>

			<!-- step1 底部按钮栏 -->
			<div class="flex justify-end">
				<n-button
					:disabled="data.btnNextDisabled"
					:color="theme.primaryColor"
					style="border-radius: 8px"
					@click="handleNextStep(2)"
				>
					<span class="px-1">
						<span v-if="data.upload.fileListLength > 0"
							>共 {{ data.upload.fileListLength }} 个文件 |
						</span>
						下一步
					</span>
				</n-button>
			</div>
		</div>

		<!-- step2 数据处理 -->
		<div v-show="data.curStep === 2" class="flex-1 w-full h-full flex gap-4">
			<!-- 左侧表单 -->
			<div class="flex-1 flex flex-col overflow-auto">
				<!-- 标题 -->
				<p class="flex items-center gap-1 mb-2">
					<Icon icon="uil:setting" width="22" />
					<span class="font-bold text-[16px]">数据处理参数</span>
				</p>

				<!-- 处理方式 -->
				<n-form-item
					label="内容切分"
					label-placement="left"
					label-align="left"
					label-width="100px"
				>
					<!-- 处理方式 单选 -->
					<n-radio-group
						v-model:value="data.formDataHandle.curSplitType"
						name="searchType"
						style="width: 100%"
					>
						<div class="flex flex-col gap-4">
							<template
								v-for="item in data.formDataHandle.opt.splitType"
								:key="item.value"
							>
								<div
									@click="changeSplitType(item)"
									class="flex justify-between items-center border p-2 rounded-lg cursor-pointer select-none hover:border-[#0653FF]"
									:style="{
										'border-color':
											data.formDataHandle.curSplitType == item.value
												? theme.primaryColor
												: '',
										'box-shadow':
											data.formDataHandle.curSplitType == item.value
												? '0 0 3px 0 #0653FF'
												: '',
									}"
								>
									<div class="w-full flex gap-4">
										<n-radio :value="item.value"></n-radio>
										<div class="w-full flex flex-col">
											<span>{{ item.label }}</span>
											<span class="text-[grey] text-[12px]">{{
												item.desc
											}}</span>

											<!-- 更多 表单 -->
											<div
												v-show="
													item.hasForm &&
													data.formDataHandle.curSplitType == 'custom'
												"
												class="flex flex-col gap-4 mt-4"
											>
												<!-- 理想分块长度 -->
												<div class="flex flex-col">
													<span class="flex items-center gap-1">
														理想分块长度
														<n-popover
															trigger="hover"
															:width="300"
															placement="bottom"
															:keep-alive-on-hover="false"
														>
															<template #trigger>
																<Icon
																	icon="ph:question"
																	color="grey"
																	width="18"
																/>
															</template>

															<p>
																按借宿符号进行分段。我们建议您的文档应合理地使用标点符号，以确保
																每个完整的句子长度不要超过该值
															</p>
															<p>中文文档建议400~1000</p>
															<p>英文文档建议600~1200</p>
														</n-popover>
													</span>
													<n-input-number
														v-model:value="data.formDataHandle.splitterParams.chunk_size"
														:step="100"
													/>
												</div>

												<!-- 自定义分隔符 -->
												<div class="flex flex-col">
													<span class="flex items-center gap-1">
														自定义分隔符
														<n-popover
															trigger="hover"
															:width="300"
															placement="bottom"
															:keep-alive-on-hover="false"
														>
															<template #trigger>
																<Icon
																	icon="ph:question"
																	color="grey"
																	width="18"
																/>
															</template>

															<span
																>允许你根据自定义的分隔符进行分块。通常用于已处理好的数据，使用特定的分隔符来精确分块。</span
															>
														</n-popover>
													</span>
													<n-input
														v-model:value="data.formDataHandle.splitterParams.separator"
														type="text"
														placeholder="\n;======;==SPLIT=="
														clearable
													/>
												</div>
											</div>
										</div>
									</div>
								</div>
							</template>
						</div>
					</n-radio-group>
				</n-form-item>


	
				<!-- 处理方式 -->
				<n-form-item
					label="信息抽取"
					label-placement="left"
					label-align="left"
					label-width="100px"
				>
					<!-- 处理方式 单选 -->
					<n-radio-group
						v-model:value="data.formDataHandle.curDrillMode"
						name="searchType"
						style="width: 100%"
					>
						<div class="flex flex-col gap-4">
							<template
								v-for="item in data.formDataHandle.opt.extractInfo"
								:key="item.value"
							>
								<div
									@click="changeDrillMode(item)"
									class="flex justify-between items-center border p-2 rounded-lg cursor-pointer select-none hover:border-[#0653FF]"
									:style="{
										'border-color':
											data.formDataHandle.curDrillMode == item.value
												? theme.primaryColor
												: '',
										'box-shadow':
											data.formDataHandle.curDrillMode == item.value
												? '0 0 3px 0 #0653FF'
												: '',
									}"
								>
									<div class="w-full flex gap-4">
										<n-radio :value="item.value"></n-radio>
										<div class="w-full flex flex-col">
											<span>{{ item.label }}</span>
											<span class="text-[grey] text-[12px]">{{
												item.desc
											}}</span>

											<!-- 更多 表单 -->
											<div
												v-show="
													item.hasForm &&
													data.formDataHandle.curDrillMode == 'custom'
												"
												class="flex flex-col gap-4 mt-4"
											>
												<!-- 理想分块长度 -->
												<div class="flex flex-col">
													<span class="flex items-center gap-1">
														理想分块长度
														<n-popover
															trigger="hover"
															:width="300"
															placement="bottom"
															:keep-alive-on-hover="false"
														>
															<template #trigger>
																<Icon
																	icon="ph:question"
																	color="grey"
																	width="18"
																/>
															</template>

															<p>
																按借宿符号进行分段。我们建议您的文档应合理地使用标点符号，以确保
																每个完整的句子长度不要超过该值
															</p>
															<p>中文文档建议400~1000</p>
															<p>英文文档建议600~1200</p>
														</n-popover>
													</span>
													<n-input-number
														v-model:value="data.formDataHandle.splitterParams.chunk_size"
														:step="100"
													/>
												</div>

												<!-- 自定义分隔符 -->
												<div class="flex flex-col">
													<span class="flex items-center gap-1">
														自定义分隔符
														<n-popover
															trigger="hover"
															:width="300"
															placement="bottom"
															:keep-alive-on-hover="false"
														>
															<template #trigger>
																<Icon
																	icon="ph:question"
																	color="grey"
																	width="18"
																/>
															</template>

															<span
																>允许你根据自定义的分隔符进行分块。通常用于已处理好的数据，使用特定的分隔符来精确分块。</span
															>
														</n-popover>
													</span>
													<n-input
														v-model:value="data.formDataHandle.splitterParams.separator"
														type="text"
														placeholder="\n;======;==SPLIT=="
														clearable
													/>
												</div>
											</div>
										</div>
									</div>
								</div>
							</template>
						</div>
					</n-radio-group>
				</n-form-item>

				<!-- step2 左侧 底部tag -->
				<n-form-item
					label=" "
					label-placement="left"
					label-align="left"
					label-width="100px"
				>
					<div class="w-full flex gap-4 items-center">
						<div
							class="py-[2px] px-3 bg-[#F7F8FA] border rounded-lg text-[12px] text-[#383F50]"
						>
							总分段：{{ data.formDataHandle.totalSegment }}
						</div>
						<div
							class="py-[2px] px-3 bg-[#F7F8FA] border rounded-lg text-[12px] text-[#383F50]"
						>
							总字数：{{ data.formDataHandle.totalLength }}
						</div>
					</div>
				</n-form-item>

				<!-- 底部按钮栏 -->
				<div class="flex justify-end gap-4">
					<n-button style="border-radius: 8px" @click="regenerate">
						<span class="px-1"> 重新生成预览 </span>
					</n-button>

					<n-button
						:color="theme.primaryColor"
						style="border-radius: 8px"
						@click="handleNextStep(3)"
					>
						<span class="px-1"> 下一步 </span>
					</n-button>
				</div>
			</div>

			<!-- step2 右侧预览 -->
			<div class="h-full flex-1 flex flex-col">
				<!-- 预览切换 -->
				<div class="max-w-[12rem]">
					<n-tabs
						type="segment"
						animated
						:on-update:value="(val) => (data.formDataHandle.curPreview = val)"
						default-value="segment"
					>
						<!-- 分段预览 -->
						<n-tab name="segment">
							<Icon
								icon="mdi:eye-outline"
								width="12"
								:color="
									data.formDataHandle.curPreview === 'segment'
										? theme.primaryColor
										: ''
								"
							/>
							<span
								class="ml-1"
								:style="{
									color:
										data.formDataHandle.curPreview === 'segment'
											? theme.primaryColor
											: '',
								}"
								>分段预览</span
							>
						</n-tab>
						<!-- 来源列表 -->
						<n-tab name="source">
							<Icon
								icon="ri:file-list-2-line"
								width="12"
								:color="
									data.formDataHandle.curPreview === 'source'
										? theme.primaryColor
										: ''
								"
							/>
							<span
								class="ml-1"
								:style="{
									color:
										data.formDataHandle.curPreview === 'source'
											? theme.primaryColor
											: '',
								}"
								>抽取预览</span
							>
						</n-tab>
					</n-tabs>
				</div>

				<!-- 分段预览 -->
				<template v-if="data.formDataHandle.curPreview === 'segment'">
					<n-scrollbar style="flex: 1 0 0">
						<div class="flex flex-col mt-3 overflow-auto">
							<!-- 单个文件预览 -->
							<template v-for="(item, index) in data.formDataHandle.segmentPreview.txtPreview" :key="item?.id">
								<div class="w-full border mb-3 p-4 shadow rounded-lg">
									<div class="flex items-center gap-2 text-[12px]">
									<!-- 排序标号 -->
									<n-tag type="info" size="small" style="border-radius: 6px">
										# {{ index + 1 }}
									</n-tag>
									<div class="flex items-center">
										<!-- 文件类型 图标 -->
										<Icon icon="bxs:file" width="18" color="#99B7D2" />
										<!-- 标题 -->
										<span class="font-bold">{{ item.metadata.file_name }}</span>

									</div>
									</div>

									<div
									v-text="item.page_content"
									class="whitespace-pre-line text-[12px]"
									></div>
									<div class="mt-3">
										<n-tag
											size="tiny"
											type="success"
											class="font-bold text-[12px]"
										>
											字数: {{ item.page_content.length }}
										</n-tag>
										</div>
								</div>
								</template>
						</div>
					</n-scrollbar>
				</template>

				<!-- 抽取预览 -->
				<template v-else>
					<div class="flex flex-col">
						<template v-for="item in data.formDataHandle.segmentPreview.extractPreview" :key="item?.id">
							<div
								class="gap-2 mt-3 p-3 border shadow-sm rounded-lg"
							>
								<div class="flex items-center mb-2">
									<!-- 文件类型 图标 -->
									<Icon icon="bxs:file" width="18" color="#99B7D2" />
									<!-- 标题 -->
									<span>{{ item.file_name }}</span>
								</div>

								<div v-if="item.summary">摘要: {{ item.summary }}</div>
								<div v-if="item.qa" class="p-6 bg-gray-50 rounded-lg shadow-md">
								<h2 class="text-xl font-semibold mb-4">问答:</h2>
								<div class="space-y-4">
									<div v-for="qa in item.qa.qa_list" :key="qa.id" class="p-4 bg-white rounded-md border border-gray-200">
									<div class="font-bold text-gray-800">
										问题: {{ qa.question }}
									</div>
									<div class="mt-2 text-gray-600">
										答案: {{ qa.answer }}
									</div>
									</div>
								</div>
								</div>
							</div>
						</template>
					</div>
				</template>
			</div>
		</div>

		<!-- step3 上传数据 -->
		<div v-show="data.curStep === 3">
			<n-data-table
				:bordered="false"
				:columns="data.table.columns"
				:data="data.table.data"
				:pagination="data.table.pagination"
				:paginate-single-page="false"
			/>
			<!-- 底部按钮栏 -->
			<div class="flex justify-end mt-4">
				<n-button :color="theme.primaryColor" @click="handleUpload">
					共 {{ data.docs.length }} 个文件 | 开始上传
				</n-button>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { computed, h, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Icon } from "@iconify/vue";
import { NProgress, UploadFileInfo } from "naive-ui";
import { useUserStore } from "@/store";
import { api } from "@/api/common";
import { useThemeVars } from "naive-ui";

const theme = useThemeVars();

const route = useRoute();
const router = useRouter();
const refUpload = ref();
const userStore = useUserStore();

const upload_endpoint = "http://192.168.2.152:8003/load_file";
const token = userStore.$state.userInfo?.access_token;




const data = reactive({
	curStep: 1, // 当前步骤
	curProgress: "process", // 当前进度 'process' | 'finish' | 'error' | 'wait'
	btnNextDisabled: computed(() => data.upload.fileListLength < 1), // 下一步按钮 禁用

	// step1
	upload: {
		fileList: [
			// {
			// 	batchId: "4a700da0",
			// 	content: "新动能成长壮大。",
			// 	file: {
			// 		lastModified: 1709208903774,
			// 		lastModifiedDate: "Thu Feb 29 2024 20:15:03 GMT+0800 (中国标准时间) ",
			// 		name: "tmp.txt",
			// 		size: 1487,
			// 		type: "text/plain",
			// 		webkitRelativePath: "",
			// 	},
			// 	fullPath: "/tmp.txt",
			// 	id: "60ee5640",
			// 	name: "tmp.txt",
			// 	percentage: 0,
			// 	status: "pending",
			// 	thumbnailUrl: null,
			// 	type: "text/plain",
			// 	url: null,
			// },
		],
		fileListLength: 0,
	},
	// 上传以后返回的文档数据
	docs: [],

	// step2
	formDataHandle: {
		curDrillMode: "summary", // 当前信息抽取模式
		curSplitType: "auto", // 当前字符切分处理方式

		splitterParams: {
			// 自定义规则
			chunk_size: 512, // 理想分块长度
			chunk_overlap: 0, // 分块重叠
			separator: "\n\n", // 自定义分隔符
		},
		extracParams: {
		},

		splitChar: "", // 自定义分隔符

		// 左侧底部
		// 总分段
		totalSegment: 0,
		// 总字数
		totalLength: 0,
		// todo 计算消耗积分
		needPoint: 0, // 预估消耗积分

		// 右侧预览
		curPreview: "segment", // 当前预览
		segmentPreview: {
			txtPreview: [],
			extractPreview: [],
		},

		opt: {
			// 训练模式
			drillMode: [
				{
					label: "字符分割",
					value: "CharacterTextSplitter",
					desc: "文本按一定的规则进行分段处理后，转成可进行语义搜索的格式，适合绝大多数场景。不需要调用模型额外处理，成本低。",
				},
				{
					label: "增强处理",
					value: "enhance",
					desc: "通过子索引以及调用模型生成相关问题与摘要，来增加数据块的语义丰富度，更利于检索。需要消耗更多的储存空间和增加AI调用次数。",
				},
				{
					label: "问答拆分",
					value: "split",
					desc: "根据一定规则，将文本拆成一段较大的段落，调用AI为该段落生成问答对。有非常高的检索精度，但是会丢失很多内容细节。",
				},
			],
			// 处理方式
			splitType: [
				{
					label: "自动",
					value: "auto",
					desc: "自动设置分割和预处理规则",
				},
				{
					label: "自定义规则",
					value: "custom",
					desc: "自定义设置分制和预处理规则",
					hasForm: true,
				},
			],
			// 信息抽取
			extractInfo: [
				{
					label: "抽取摘要",
					value: "summary",
					desc: "自动抽取文本中的信息",
				},
				{
					label: "问答抽取",
					value: "qa",
					desc: "将文本转换成问答对",
				}
			],
		},
	},

	// step3
	table: {
		data: [
		],
		pagination: {
			pageSize: 10,
		},
		loading: false,
		columns: [
			{
				title: "来源名",
				key: "name",
				fixed: "left",
				width: 400,
				render(row) {
					return h(
						"div",
						{
							class: "flex items-center gap-2",
						},
						[
							// 图标外包一层div，防止被右侧文件名挤压图标大小
							h(
								"div",
								{
									class: "min-w-[18px] h-full",
								},
								// 图标 文件类型
								h(Icon, {
									icon: "bxs:file",
									width: 18,
									color: "#99B7D2",
									style: "height: 18px",
								})
							),
							// 文件名
							h("span", {}, row.name),
						]
					);
				},
			},
			{
				title: "内容索引数",
				key: "segmentNum",
				minWidth: 100,
				align: "center",
			},
			{
				title: "结构化索引数",
				key: "structureIndex",
				minWidth: 100,
				align: "center",
			},
		],
	},
});





// step1 上传文件 列表改变
const handleUploadChange = async (options: { fileList: UploadFileInfo[] }) => {
	const { file } = options;
	console.log(file.status);
	// 删除时
	if (file.status == "removed") {
		// 删除上传列表
		data.upload.fileList = data.upload.fileList.filter(
			(item) => item.id != file.id
		);
		// 删除表格数据
		data.table.data = data.table.data.filter((item) => item.id != file.id);
		return;
	}

	const reader = new FileReader();
	// 读取完毕后执行
	reader.onload = () => {
		handleReadFile(reader, options);
	};

	// 读取文件
	reader.readAsText(file.file);

	// 更新列表文件个数
	data.upload.fileListLength = options.fileList.length;
};

// 读取文件
const handleReadFile = (reader: FileReader, opt) => {
	const { file, fileList } = opt;

	switch (file.type) {
		// 文本类型
		case "text/plain":
			// // 同步表格数据
			// data.table.data = data.upload.fileList.map((item) => {
			// 	const trimSegmentNum = item.content
			// 		.split(/\r?\n/)
			// 		.filter((item) => item.trim() != "");

			// 	return {
			// 		name: item.name,
			// 		segmentNum: trimSegmentNum.length,
			// 		fileUploadProgress: 0,
			// 		dataUploadProgress: 0,
			// 	};
			// });

			// const trimSegmentNum = item.content
			// 	.split(/\r?\n/)
			// 	.filter((item) => item.trim() != "");

			// 去除内容的空行
			const trimSegmentNum = reader.result
				.split(/\r?\n/)
				.filter((item) => item.trim() != "");

			// 填充 step1 文件读取的内容
			data.upload.fileList.push({
				...file,
				content: reader.result,
				segmentNum: trimSegmentNum.length,
			});

			// 同步 step3 表格数据
			data.table.data.push({
				id: file.id,
				name: file.name,
				segmentNum: trimSegmentNum.length,
				fileUploadProgress: 0,
				dataUploadProgress: 0,
			});

			break;
	}
};


const handleUploadFinish = (options: { file: UploadFileInfo, event?: ProgressEvent }) => {
	const { file, event } = options;

	const docText = JSON.parse(event.currentTarget?.response);
	
	const newDoc = {
		name: file.name,
		content: docText[0]?.page_content,
		length: docText.length,
	};
	data.docs.push(newDoc);
};

// step2 切换训练模式
const changeDrillMode = (item) => {
	data.formDataHandle.curDrillMode = item.value;

};

// step2 切换处理方式
const changeSplitType = (item) => {
	data.formDataHandle.curSplitType = item.value;
};

// step2 重新生成预览
const regenerate = () => {
	console.log(data.formDataHandle.splitterParams);
	const spliter_name = 'CharacterTextSplitter'
	api.split_document({
		documents: data.docs,
		handler_name: spliter_name,
		params: data.formDataHandle.splitterParams,
	}).then((res) => {
		// 更新预览数据
		data.formDataHandle.segmentPreview.txtPreview = res?.splited_texts
		data.formDataHandle.totalSegment = res?.metadata?.total_segment
		data.formDataHandle.totalLength = res?.metadata?.total_length


	});

	api.extract_document({
		documents: data.docs,
		handler_name: data.formDataHandle.curDrillMode,
		params: {},
	}).then((res) => {
		data.formDataHandle.segmentPreview.extractPreview = res
	});


};

// 下一步
const handleNextStep = async (tarStep: number) => {
	data.curStep = tarStep;
	if (tarStep === 2) {
		// 进行分段处理
		regenerate();
	} else if (tarStep === 3) {
		handleUpload();
	}
};

// step3 上传文件
const handleUpload = () => {
	if (data.docs.length === 0) {
		console.error('No documents to upload.');
		return;
	} else {
		const docsDictionary = {};

		// 遍历docs数组，为每个文档创建字典条目
		data.docs.forEach((doc) => {
		// 使用文档名称作为键
		const key = doc.name;
		console.log(data.formDataHandle.segmentPreview)
		// 查找与当前文档名称匹配的split和extract数据
		const splits = data.formDataHandle.segmentPreview.txtPreview?.filter((item) => item.metadata.file_name === key);
		const extract = data.formDataHandle.segmentPreview.extractPreview?.find((item) => item.file_name === key);
		
		console.log(splits, extract)
		// 创建字典项内容
		const dictionaryItem = {
			name: doc.name,
			type: 'file',
			content_split: splits.map((split) => split.page_content), // 只提取分段的内容
			summary: extract ? extract.summary : '', // 如果extract信息存在，就添加摘要
			qa: extract ? extract.qa : '', // 如果extract信息存在，就添加qa
		};

			// 将字典项添加到字典对象中
			docsDictionary[key] = dictionaryItem;
		});
				
		// 转成列表
		const docsList = Object.values(docsDictionary);
		console.log(docsList);
		api.upload_data({
			data: docsList,
			knowledge_id: route.params?.id,
		}).then((res) => {
			console.log(res);
		});


	}
	
};

// 退出按钮 回到知识库详情 数据集页
const handleGoKnowledgeDetail = () => {
	router.replace({
		name: "KnowledgeDetails_dataset",
		params: {
			id: route.params?.id,
		},
	});
};
</script>

<style lang="less" scoped></style>
