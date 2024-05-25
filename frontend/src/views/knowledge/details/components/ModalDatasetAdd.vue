<template>
	<div>
		<mModal
			ref="refModal"
			footerBtnSize="medium"
			footerComfirmBtnType="primary"
			:txtCancel="$t('common.cancel')"
			:txtConfirm="$t('common.confirm')"
			@onShowChange="onShowChange"
			@onPositiveClick="handleComfirm"
			style="
				position: fixed;
				top: 10%;
				left: 50%;
				transform: translate(-50%, 0);
			"
		>
			<div class="flex items-center text-[18px] mb-4">
				<span>{{ data.title }}</span>
			</div>

			<!-- 根据选择显示不同的提示文字 -->
			<div class="text-[grey] mb-2">
				{{ data.manualDatasetDescription }}
			</div>

			<!-- 相应地改变输入框的placeholder -->
			<div class="w-full">
				<n-input
					v-model:value="data.txtFolderManual"
					type="text"
					:placeholder="data.inputPlaceholder"
				/>
			</div>

			<div class="w-full pt-3" v-if="data.curAddType?.key === 'datasetTxt'">
				<n-input
					v-model:value="data.txtContent"
					type="textarea"
					:placeholder="$t('knowledge.placeholderInputTxt')"
				/>
			</div>
		</mModal>
	</div>
</template>

<script setup lang="ts">
import mModal from "@/components/common/mModal/index.vue";
import { DropdownOption } from "naive-ui";
import { reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { api } from "@/api/common";
import { t } from "@/locales";

const route = useRoute();
const router = useRouter();

const emit = defineEmits(["update-list"]);

const refModal = ref();
const data = reactive({
	title: "",
	curAddType: {}, // 由该页面导入 src/views/knowledge/details/dataset.vue
	txtFolderManual: "", // 文件夹/手动数据集 输入框
	txtContent: "", // 文本数据集内容输入框
	curTxtType: "local", // 当前文本类型
	inputPlaceholder: "请输入名称",
	manualDatasetDescription: "请输入描述信息",
});

// 修改当前标题
const getCurTitle = () => {
	switch (data.curAddType?.key) {
		// 文件夹
		case "folder":
			data.title = t("knowledge.createFolder");
			data.inputPlaceholder = t("knowledge.placeholderCreateFolder");
			data.manualDatasetDescription = t("knowledge.createFolderDesc");
			break;

		// 手动数据集
		case "datasetManual":
			data.title = t("knowledge.createDatasetManual");
			data.inputPlaceholder = t("knowledge.placeholderCreateDataset");
			data.manualDatasetDescription = t("knowledge.createDatasetManualDesc");
			break;

		// 文本数据集
		case "datasetTxt":
			data.title = t("knowledge.createDatasetTxt");
			data.inputPlaceholder = t("knowledge.placeholderCreateDataset");
			data.manualDatasetDescription = t("knowledge.createDatasetLink");
			break;

		// 网页链接
		case "datasetLink":
			data.title = t("knowledge.createDatasetLink");
			data.inputPlaceholder = t("knowledge.placeholderCreateLink");
			data.manualDatasetDescription = "";
			break;

		default:
			data.title = "";
			break;
	}
};

// 切换搜索模式
const changeTxtType = (item) => {
	data.curTxtType = item.value;
};

const onSelectType = (key: string, opt: DropdownOption) => {
	// 获取当前添加类型
	data.curAddType = opt;

	// 修改当前标题
	getCurTitle();
};

// 确认 按钮
const handleComfirm = async () => {
	switch (data.curAddType?.key) {
		case "folder":
			// todo 请求接口 添加文件夹
			console.log("添加文件夹");
			break;

		case "datasetManual":
			// todo 请求接口 添加手动数据集
			console.log("添加手动数据集");
			api
				.add_manual_container({
					name: data.txtFolderManual,
					knowledge_id: route.params?.id,
				})
				.then((res) => {
					// 刷新列表
					emit("update-list");
				})
				.catch((err) => {
					console.log(err);
				});
			changeModalShow();
			break;

		// 文本数据集
		case "datasetTxt":
			api
				.add_content({
					doc_name: data.txtFolderManual,
					knowledge_id: route.params?.id,
					doc_content: data.txtContent,
				})
				.then((res) => {
					// 刷新列表
					emit("update-list");
					router.push({
						name: "KnowledgeDetails_dataset_split",
						params: {
							id: route.params?.id,
							nodeId: res?.node_id,
						},
					});
				})
				.catch((err) => {
					console.log(err);
				});
			break;

		case "datasetLink":
			// todo 请求接口 添加网页链接数据集
			console.log("添加网页链接数据集");
			const res = await api.add_url_content({
				url: data.txtFolderManual,
				knowledge_id: route.params?.id,
			});
			emit("update-list");
			router.push({
				name: "KnowledgeDetails_dataset_split",
				params: {
					id: route.params?.id,
					nodeId: res?.node_id,
				},
			});
	}
};

// 重置表单
const resetForm = () => {
	data.txtFolderManual = "";
	data.curTxtType = "local";
};

// 模态框显示状态 变化时
const onShowChange = (isShow: boolean) => {
	// 关闭模态框时
	if (!isShow) return resetForm();
};

// 改变模态框显示 新建/导入
const changeModalShow = () => {
	refModal.value.toggleModal();
};

defineExpose({
	changeModalShow,
	onSelectType, // 新建/导入
});
</script>

<style lang="less" scoped></style>
