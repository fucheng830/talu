<template>
	<n-scrollbar style="flex: 1 0 0">
		<div :class="!isMobile && 'py-6'">
			<!-- 顶部栏 -->
			<div
				class="flex gap-2 px-4 text-[16px] font-bold"
				:class="[isMobile ? 'flex-col' : 'items-center']"
			>
				<span class="flex-1">
					{{ $t("knowledge.files") }} ({{ data.table.data.length }})
				</span>
				<div class="flex items-center gap-4">
					<n-input
						v-model:value="data.txtSearch"
						type="text"
						:placeholder="$t('common.search')"
						:style="{ 'border-radius': globalConfig.btnRadius }"
					>
						<template #prefix>
							<Icon icon="iconamoon:search" width="18" />
						</template>
					</n-input>

					<n-dropdown :options="data.opt.menuAdd" @select="handleAdd">
						<n-button
							:color="theme.primaryColor"
							:style="{ 'border-radius': '8px' }"
						>
							<Icon icon="lucide:import" width="18" />
							<span class="ml-2">
								{{ $t("common.create") }}/{{ $t("common.import") }}
							</span>
						</n-button>
					</n-dropdown>
				</div>
			</div>

			<!-- 表格 -->
			<div class="px-4 pt-4">
				<n-data-table
					:columns="data.table.columns"
					:data="data.table.data"
					:pagination="data.table.pagination"
					:bordered="false"
					:paginate-single-page="false"
					:row-props="
						(row) => ({
							style: 'cursor: pointer;',
							onClick: () => handleRowClick(row),
						})
					"
				/>
			</div>

			<!-- 模态框 新建/导入 -->
			<ModalDatasetAdd
				ref="refModalDatasetAdd"
				@update-list="fetchDatasetList"
			/>
		</div>
	</n-scrollbar>
</template>

<script setup lang="ts">
import { h, reactive, ref } from "vue";
import { Icon } from "@iconify/vue";
import { globalConfig } from "@/hooks/useTheme";
import { renderIcon } from "@/utils/functions";
import { DropdownOption, NDropdown } from "naive-ui";
import ModalDatasetAdd from "@/views/knowledge/details/components/ModalDatasetAdd.vue";
import { useRoute, useRouter } from "vue-router";
import { onMounted } from "vue";
import { api } from "@/api/common";
import { datasetTypeIcon } from "@/views/knowledge/knowledgeConfig.ts";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { t } from "@/locales";
import { useThemeVars } from "naive-ui";

const theme = useThemeVars();
const route = useRoute();
const router = useRouter();
const { isMobile } = useBasicLayout();

const handleSelect = (row, option) => {
	// 这里填写重命名函数的逻辑
	console.log("Rename dataset:", row, option);
	if (option.key === "rename") {
		// 重命名
		console.log("重命名");
	} else if (option.key === "delete") {
		// 删除
		console.log("删除");
		api
			.delete_node({ node_id: row.node_id })
			.then((res) => {
				console.log("删除成功", res);
				data.table.data = data.table.data.filter(
					(item) => item.node_id !== row.node_id
				);
			})
			.catch((err) => {
				console.log("删除失败", err);
			});
	}
};

const refModalDatasetAdd = ref();
const data = reactive({
	txtSearch: "",
	opt: {
		menuAdd: [
			// {
			// 	label: "文件夹",
			// 	key: "folder",
			// 	icon: () =>
			// 		renderIcon({
			// 			icon: "material-symbols-light:folder",
			// 			color: "#FDB022",
			// 		}),
			// },
			{
				label: t("knowledge.datasetManual"),
				key: "datasetManual",
				icon: () =>
					renderIcon({ icon: datasetTypeIcon.datasetManual, width: 18 }),
			},
			{
				label: t("knowledge.datasetFile"),
				key: "datasetFile",
				icon: () =>
					renderIcon({ icon: datasetTypeIcon.datasetFile, width: 18 }),
			},
			{
				label: t("knowledge.datasetTxt"),
				key: "datasetTxt",
				icon: () => renderIcon({ icon: datasetTypeIcon.datasetTxt, width: 18 }),
			},
			{
				label: t("knowledge.datasetLink"),
				key: "datasetLink",
				icon: () =>
					renderIcon({ icon: datasetTypeIcon.datasetLink, width: 18 }),
			},
			// {
			// 	label: "表格数据集",
			// 	key: "datasetTable",
			// 	icon: () => renderIcon({ icon: "teenyicons:csv-outline", width: 18 }),
			// },
		],
		menuTable: [
			{
				label: t("common.rename"),
				key: "rename",
				icon: () => renderIcon({ icon: "radix-icons:input", width: 18 }),
			},
			{
				label: t("common.delete"),
				key: "delete",
				icon: () => renderIcon({ icon: "radix-icons:input", width: 18 }),
			},
		],
	},
	table: {
		data: [],
		pagination: {
			pageSize: 10,
		},
		columns: [
			{
				title: t("common.name"),
				key: "name",
				render(row) {
					const iconNode = renderIcon({
						icon: row.icon, // 使用为每个数据集对象添加的图标属性
						width: 18,
					});

					return h(
						"div",
						{
							style: { display: "flex", alignItems: "center" },
						},
						[
							h(
								"span",
								{
									style: { marginRight: "6px" }, // 设置图标的外边距
								},
								[iconNode]
							),
							row.name, // 数据集名称
						]
					);
				},
			},
			// {
			// 	title: "数据总量",
			// 	key: "totalData",
			// 	align: "center",
			// 	render(row: any) {
			// 		return h("span", null, {
			// 			default: () => (row.totalData > 0 ? row.totalData : "-"),
			// 		});
			// 	},
			// },
			{
				title: "",
				key: "action",
				render(row) {
					return h(
						NDropdown,
						{
							options: data.opt.menuTable,
							onSelect: (key, opt) => handleSelect(row, opt),
						},
						{
							default: () =>
								renderIcon({ icon: "material-symbols:more-horiz" }),
						}
					);
				},
			},
		],
	},
});

// 新建/导入
const handleAdd = (key: string, opt: DropdownOption) => {
	refModalDatasetAdd.value?.onSelectType(key, opt);

	// 多个条件分支
	switch (key) {
		case "datasetFile":
			// 打开弹窗，创建文件数据集
			console.log("创建文件数据集");
			router.push({
				name: "KnowledgeDetails_dataset_upload",
				params: {
					id: route.params?.id,
					type: "datasetFolder",
				},
			});
			break;

		default:
			// 打开弹窗，创建文件夹/手动数据集
			changeModalDatasetAddShow();
			break;
	}
};

// 点击表行
const handleRowClick = (row) => {
	console.log("Row clicked:", row);
	router.push({
		name: "KnowledgeDetails_dataset_details",
		params: {
			id: route.params?.id,
			fileID: row.node_id,
			fileName: row.name,
			nodeType: row.node_type,
		},
	});
};

// 切换模态框显示 新建/导入
const changeModalDatasetAddShow = () => {
	refModalDatasetAdd.value?.changeModalShow();
};

const fetchDatasetList = async () => {
	try {
		// 调用API函数获取数据，并赋值给表格data属性
		const fetchedData = await api.list_knowledge_data({
			knowledge_id: route.params?.id,
		});

		// 根据文件类型为每一行数据添加图标属性
		const dataWithIcons = fetchedData.map((item) => {
			let iconType = "";
			// 根据文件类型或其他标准确定图标类型的逻辑
			// 这里是一个示例逻辑，请根据您实际的逻辑来替换
			switch (
				item.node_type // 用实际表示文件类型的属性名替换 'type'
			) {
				case "folder":
					iconType = "material-symbols-light:folder";
					break;
				case "datasetManual":
					iconType = "radix-icons:input";
					break;
				case "datasetFile":
					iconType = "radix-icons:file-text";
					break;
				case "datasetTxt":
					iconType = "fluent-mdl2:text-document-edit";
					break;
				case "datasetLink":
					iconType = "solar:link-broken";
					break;
				case "datasetTable":
					iconType = "teenyicons:csv-outline";
					break;
				default:
					iconType = "heroicons-outline:document-text";
			}
			return {
				...item,
				icon: iconType,
			};
		});

		data.table.data = dataWithIcons;
	} catch (error) {
		// 出错处理，可以是显示错误信息，记录日志等
		console.error("获取数据出错:", error);
	}
};

onMounted(async () => {
	await fetchDatasetList();
});
</script>

<style lang="less" scoped></style>
