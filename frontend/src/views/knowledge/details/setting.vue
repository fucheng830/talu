<template>
	<div class="w-full h-full p-8">
		<n-form
			ref="refForm"
			:model="data.form"
			label-placement="left"
			label-width="10rem"
			label-align="left"
		>
			<n-form-item label="知识库 ID">
				<span>{{ data.opt.knowledgeInfo.id }}</span>
			</n-form-item>

			<n-form-item label="知识库头像">
				<n-avatar round size="large" :src="data.form.avatar" />
			</n-form-item>

			<n-form-item label="知识库名称">
				<div class="max-width w-[90%]">
					<n-input v-model:value="data.form.name" type="text" placeholder="" />
				</div>
			</n-form-item>

			<n-form-item label="索引模型">
				<span>{{ data.opt.knowledgeInfo.indexModel }}</span>
			</n-form-item>

			<n-form-item label="单条数据上限">
				<span>{{ data.opt.knowledgeInfo.singleDataLimit }}</span>
			</n-form-item>

			<n-form-item label="文件处理模型">
				<div class="max-width w-[90%]">
					<n-select
						v-model:value="data.form.AIModel"
						:options="data.opt.AIList"
					/>
				</div>
			</n-form-item>

			<n-form-item label="介绍">
				<div class="max-width w-[90%]">
					<n-input
						v-model:value="data.form.desc"
						type="textarea"
						placeholder="介绍"
						:autosize="{
							minRows: 3,
							maxRows: 7,
						}"
					/>
				</div>
			</n-form-item>

			<n-form-item label="使用权限">
				<div class="w-[90%] max-w-[27rem] grid grid-cols-2 gap-4">
					<template v-for="(item, index) in data.opt.permission" :key="index">
						<!-- 单选 -->
						<n-radio-group
							v-model:value="data.form.permission"
							name="permission"
						>
							<!-- 单个选项 -->
							<div
								@click="changePermission(item)"
								class="search-type flex justify-between items-center gap-4 border py-2 px-4 rounded-lg cursor-pointer select-none hover:border-[#0653FF]"
								:style="{
									'background-color':
										data.form.permission == item.value ? '#F0F4FF' : '',
									'border-color':
										data.form.permission == item.value
											? globalColors.btnActive
											: '',
								}"
							>
								<div class="flex-1 flex items-center gap-4">
									<!-- 图标 类型 -->
									<Icon :icon="item.icon" width="18" />
									<div class="flex flex-col">
										<span>{{ item.label }}</span>
										<span class="text-[#667085] text-xs">{{ item.desc }}</span>
									</div>
								</div>
								<n-radio :value="item.value"></n-radio>
							</div>
						</n-radio-group>
					</template>
				</div>
			</n-form-item>
			<n-form-item label=" ">
				<div class="flex items-center gap-4">
					<!-- 保存 -->
					<n-button :color="globalColors.btnActive" @click="handleSubmit">
						<span class="px-4"> 保存 </span>
					</n-button>

					<!-- 删除 -->
					<n-button @click="changeModalDeleteShow">
						<template #icon>
							<Icon icon="material-symbols:delete-sharp" />
						</template>
					</n-button>
				</div>
			</n-form-item>
		</n-form>

		<!-- 模态框 删除 -->
		<n-modal
			v-model:show="data.showModalDelete"
			preset="dialog"
			title="删除警告"
			content="确认删除该知识库？删除后数据无法恢复，请确认！"
			positive-text="确认"
			negative-text="算了"
			:positive-button-props="{
				type: 'error',
			}"
			@positive-click="handleDelete"
		>
			<template #icon>
				<Icon icon="mingcute:alert-fill" color="#FB6547" />
			</template>
		</n-modal>
	</div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { globalColors } from "@/hooks/useTheme";
import { Icon } from "@iconify/vue";

const refForm = ref();
const data = reactive({
	form: {
		avatar: "", // 知识库头像
		name: "", // 知识库名称
		AIModel: "", // 文件处理模型
		desc: "", // 介绍
		permission: "", // 使用权限
	},
	showModalDelete: false, // 删除模态框 显示状态
	opt: {
		knowledgeInfo: {
			id: "65d5eadb757a6e1c31c914ea", //知识库 ID
			avatar: "https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg", // 知识库头像
			name: "knowledgeName", // 知识库名称
			indexModel: "Embedding-2", // 索引模型
			singleDataLimit: "3000", // 单条数据上限
			AIModel: "AIModel", // 文件处理模型
			desc: "", // 介绍
			permission: "private", // 使用权限
		},
		AIList: [
			{
				label: "FastAI-4k",
				value: "FastAI-4k",
			},
			{
				label: "FastAI-16k",
				value: "FastAI-16k",
			},
		],
		permission: [
			{
				label: "私有",
				value: "private",
				desc: "仅自己可用",
				icon: "mdi:account-lock-outline",
			},
			{
				label: "团队",
				value: "team",
				desc: "团队所有成员可使用",
				icon: "fluent:people-team-16-regular",
			},
		],
	},
});

// 切换 使用权限
const changePermission = (item) => {
	data.form.permission = item.value;
};

// 保存
const handleSubmit = () => {
	console.log("save");
	// todo 请求接口 修改配置
};

// 切换删除模态框显示
const changeModalDeleteShow = () => {
	data.showModalDelete = !data.showModalDelete;
};

// 删除
const handleDelete = () => {
	console.log("delete");
	// todo 请求接口 删除知识库
};

const init = () => {
	// 初始化表单
	const { avatar, name, AIModel, desc, permission } = data.opt.knowledgeInfo;
	data.form = { ...data.form, avatar, name, AIModel, desc, permission };
};

onMounted(() => {
	init();
});
</script>

<style lang="less" scoped>
.max-width {
	max-width: 20rem;
}
</style>
