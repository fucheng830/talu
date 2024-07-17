<template>
	<div class="w-full h-full flex flex-col gap-4 py-6 px-8">
		<div>
			<n-upload
				ref="refUpload"
				directory-dnd
				multiple
				:action="upload_endpoint"
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
							:color="globalColors.btnActive"
							width="32"
						/>
					</div>
					<div class="font-bold">{{ $t("knowledge.uploadFileTitle") }}</div>
					<div class="text-[grey] text-[12px]">
						<p>
							{{
								$t("knowledge.uploadFileSubtitle", {
									msg: ".txt, .docx, .csv, .pdf, .md, .html",
								})
							}}
						</p>
						<p>
							{{ $t("knowledge.uploadFileSubtitle2", { msg: 1000, msg2: 30 }) }}
						</p>
					</div>
				</n-upload-dragger>
			</n-upload>

			<!-- step1 底部按钮栏 -->
			<div class="flex justify-end">
				<n-button
					:disabled="data.btnNextDisabled"
					:color="globalColors.btnActive"
					style="border-radius: 8px"
					@click="handleNext"
				>
					<span class="px-1">
						<span v-if="data.upload.fileListLength > 0"
							>{{
								$t("knowledge.totalFiles", { msg: data.upload.fileListLength })
							}}
							|
						</span>
						{{ $t("common.nextStep") }}
					</span>
				</n-button>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { globalColors } from "@/hooks/useTheme";
import { Icon } from "@iconify/vue";
import { UploadFileInfo } from "naive-ui";
import { useUserStore } from "@/store";
import { api } from "@/api/common";
import { useKnowledgeStore } from "@/store";

const route = useRoute();
const router = useRouter();
const refUpload = ref();
const userStore = useUserStore();
const KnowledgeStore = useKnowledgeStore();

const upload_endpoint = import.meta.env.VITE_GLOB_API_URL+"/load_file";
const token = userStore.$state.userInfo?.access_token;

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

const data = reactive({
	curProgress: "process", // 当前进度 'process' | 'finish' | 'error' | 'wait'
	btnNextDisabled: computed(() => data.upload.fileListLength < 1), // 下一步按钮 禁用
	// step1
	upload: {
		fileList: [],
		fileListLength: 0,
	},
	// 上传以后返回的文档数据
	docs: [],
});

// step1 上传文件 列表改变
const handleUploadChange = async (options: { fileList: UploadFileInfo[] }) => {
	const { file } = options;

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
	// 更新列表文件个数
	data.upload.fileListLength = options.fileList.length;
};

const handleUploadFinish = (options: {
	file: UploadFileInfo;
	event?: ProgressEvent;
}) => {
	const { file, event } = options;

	const docText = JSON.parse(event.currentTarget?.response);

	const newDoc = {
		name: file.name,
		content: docText[0]?.page_content,
		length: docText.length,
	};
	data.docs.push(newDoc);
	KnowledgeStore.setDocs(data.docs);
};

// 进入切割页面
const handleNext = () => {
	router.replace({
		name: "KnowledgeDetails_dataset_split",
		params: {
			id: route.params?.id,
		},
	});
};

// 点击左上角返回时，因返回按钮在此页面外，使用传值给router-view外的布局组件
// 对应 @/views/knowledge/details/index.vue
const onClickBack = () => {
	router.replace({
		name: "KnowledgeDetails_dataset",
		params: {
			id: route.params?.id,
		},
	});
	return true;
};

defineExpose({
	onClickBack,
});
</script>

<style lang="less" scoped></style>
