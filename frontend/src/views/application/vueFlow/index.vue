<template>
	<div ref="refFlowWrap" class="w-full h-full">
		<!-- 
      vue-flow 文档
      https://vueflow.dev/guide/vue-flow/state.html
     -->
		<VueFlow
			:nodes="data.flow.nodes"
			:edges="data.flow.edges"
			fit-view-on-init
			:default-viewport="{ zoom: 0.3 }"
			:nodes-draggable="data.opt.nodesDraggable"
			@connect="handleConnect"
			@keydown.stop="handleKeydown"
			@click="handleDeactive"
		>
			<Background />
			<MiniMap />
			<Controls />

			<!-- 自定义连接线 -->
			<template #edge-button="buttonEdgeProps">
				<EdgeCustom
					:id="buttonEdgeProps.id"
					:source-x="buttonEdgeProps.sourceX"
					:source-y="buttonEdgeProps.sourceY"
					:target-x="buttonEdgeProps.targetX"
					:target-y="buttonEdgeProps.targetY"
					:source-position="buttonEdgeProps.sourcePosition"
					:target-position="buttonEdgeProps.targetPosition"
					:marker-end="buttonEdgeProps.markerEnd"
					:style="buttonEdgeProps.style"
					@removeEdges="handleRemoveEdges"
				/>
			</template>

			<!-- 组件配置方法: #node-组件名="node" -->

			<template
				v-for="item in data.flow.nodes"
				:key="item.id"
				v-slot:[`node-${item.type}`]="node"
			>
				<!-- 组件框架 -->
				<CompLayout
					:node="node"
					@duplicate="handleDuplicate"
					@deleteNode="deleteNode"
				>
					<!-- 开始 -->
					<StartGuide
						v-if="item.type === 'startGuide'"
						:node="node"
						@saveForm="saveForm"
					/>
					<!-- 结束 -->
					<EndFlow
						v-if="item.type === 'endFlow'"
						:node="node"
						@saveForm="saveForm"
					/>
					<!-- LLM -->
					<LLM v-if="item.type === 'LLM'" :node="node" @saveForm="saveForm" />
					<!-- 代码 -->
					<Code v-if="item.type === 'code'" :node="node" @saveForm="saveForm" />
					<!-- 知识库 -->
					<Knowledge
						v-if="item.type === 'knowledge'"
						:node="node"
						@saveForm="saveForm"
					/>
					<!-- 条件 -->
					<Condition
						v-if="item.type === 'condition'"
						:node="node"
						@saveForm="saveForm"
					/>
					<!-- 变量 -->
					<Variable
						v-if="item.type === 'variable'"
						:node="node"
						@saveForm="saveForm"
					/>
					<!-- 数据库 -->
					<Database
						v-if="item.type === 'database'"
						:node="node"
						@saveForm="saveForm"
					/>
					<!-- 消息 -->
					<Message
						v-if="item.type === 'message'"
						:node="node"
						@saveForm="saveForm"
					/>
				</CompLayout>
			</template>

			<!-- 开始引导 -->
			<!-- <template #node-startGuide="node">
				<CompLayout :node="node">
					<StartGuide :node="node" />
				</CompLayout>
			</template> -->

			<!-- 结束 -->
			<!-- <template #node-endFlow="node">
				<CompLayout :node="node">
					<EndFlow :node="node" />
				</CompLayout>
			</template> -->

			<!-- LLM -->
			<!-- <template #node-LLM="node">
				<CompLayout :node="node" @duplicate="handleDuplicate">
					<LLM :node="node" />
				</CompLayout>
			</template> -->

			<!-- 代码 -->
			<!-- <template #node-code="node">
					<CompLayout :node="node" @duplicate="handleDuplicate">
						<Code :node="node" />
					</CompLayout>
				</template> -->

			<!-- 知识库 -->
			<!-- <template #node-knowledge="node">
				<CompLayout :node="node" @duplicate="handleDuplicate">
					<Knowledge :node="node" />
				</CompLayout>
			</template> -->

			<!-- 条件 -->
			<!-- <template #node-condition="node">
				<CompLayout :node="node" @duplicate="handleDuplicate">
					<Condition :node="node" />
				</CompLayout>
			</template> -->

			<!-- 变量 -->
			<!-- <template #node-variable="node">
				<CompLayout :node="node" @duplicate="handleDuplicate">
					<Variable :node="node" />
				</CompLayout>
			</template> -->

			<!-- 数据库 -->
			<!-- <template #node-database="node">
				<CompLayout :node="node" @duplicate="handleDuplicate">
					<Database :node="node" />
				</CompLayout>
			</template> -->

			<!-- 消息 -->
			<!-- <template #node-message="node">
				<CompLayout :node="node" @duplicate="handleDuplicate">
					<Message :node="node" />
				</CompLayout>
			</template> -->

			<!-- 对话入口 -->
			<!-- <template #node-chatEntrance="node">
				<CompLayout :node="node">
					<ChatEntrance :node="node" />
				</CompLayout>
			</template> -->

			<!-- AI 对话 -->
			<!-- <template #node-AIChat="node">
				<CompLayout :node="node">
					<AIChat :node="node" />
				</CompLayout>
			</template> -->

			<!-- 指定回复 -->
			<!-- <template #node-assignedReply="node">
				<CompLayout :node="node">
					<AssignedReply :node="node" />
				</CompLayout>
			</template> -->

			<!-- 知识库搜索 -->
			<!-- <template #node-knowledgeSearch="node">
				<CompLayout :node="node">
					<KnowledgeSearch :node="node" />
				</CompLayout>
			</template> -->

			<!-- 问题分类 -->
			<!-- <template #node-questionsClassify="node">
				<CompLayout :node="node">
					<QuestionsClassify :node="node" />
				</CompLayout>
			</template> -->

			<!-- 文本内容提取 -->
			<!-- <template #node-txtExtract="node">
				<CompLayout :node="node">
					<TxtExtract :node="node" />
				</CompLayout>
			</template> -->

			<!-- 知识库搜索引用合并 -->
			<!-- <template #node-knowledgeSearchMerge="node">
				<CompLayout :node="node">
					<KnowledgeSearchMerge :node="node" />
				</CompLayout>
			</template> -->

			<!-- 文本加工 -->
			<!-- <template #node-txtProgressing="node">
				<CompLayout :node="node">
					<TxtProgressing :node="node" />
				</CompLayout>
			</template> -->

			<!-- 判断器 -->
			<!-- <template #node-judger="node">
				<CompLayout :node="node">
					<Judger :node="node" />
				</CompLayout>
			</template> -->

			<!-- 应用调用 -->
			<!-- <template #node-appCall="node">
				<CompLayout :node="node">
					<AppCall :node="node" />
				</CompLayout>
			</template> -->

			<!-- HTTP 请求 -->
			<!-- <template #node-httpRequest="node">
				<CompLayout :node="node">
					<HttpRequest :node="node" />
				</CompLayout>
			</template> -->

			<!-- 问题优化 -->
			<!-- <template #node-questionOptimize="node">
				<CompLayout :node="node">
					<QuestionOptimize :node="node" />
				</CompLayout>
			</template> -->

			<!-- 自定义反馈 -->
			<!-- <template #node-customFeedback="node">
				<CompLayout :node="node">
					<CustomFeedback :node="node" />
				</CompLayout>
			</template> -->
		</VueFlow>
	</div>
</template>

<script setup lang="ts">
import {
	MarkerType,
	Position,
	useVueFlow,
	useZoomPanHelper,
	VueFlow,
	useVisibleNodes,
} from "@vue-flow/core";
import { Background } from "@vue-flow/background";
import { MiniMap } from "@vue-flow/minimap";
import { Controls } from "@vue-flow/controls";
import { computed, nextTick, reactive, ref } from "vue";
import { v4 as uuidv4 } from "uuid";
import EdgeCustom from "@/views/application/vueFlow/edges/EdgeCustom.vue";
import CompLayout from "@/views/application/vueFlow/components/CompLayout.vue";
import StartGuide from "@/views/application/vueFlow/components/pages/StartGuide.vue";
import LLM from "@/views/application/vueFlow/components/pages/LLM.vue";
import Code from "@/views/application/vueFlow/components/pages/Code.vue";
import Knowledge from "@/views/application/vueFlow/components/pages/Knowledge.vue";
import Condition from "@/views/application/vueFlow/components/pages/Condition.vue";
import Variable from "@/views/application/vueFlow/components/pages/Variable.vue";
import Database from "@/views/application/vueFlow/components/pages/Database.vue";
import Message from "@/views/application/vueFlow/components/pages/Message.vue";
import EndFlow from "@/views/application/vueFlow/components/pages/EndFlow.vue";
import { getFlowNodeType } from "@/views/application/vueFlow/flowConfig.ts";
import { useFlowStore } from "@/store";
import { useDialog } from "naive-ui";
import { getFlowNodesList } from "@/utils/flow";
// import ChatEntrance from "@/views/application/vueFlow/components/pages/ChatEntrance.vue";
// import AIChat from "@/views/application/vueFlow/components/pages/AIChat.vue";
// import AssignedReply from "@/views/application/vueFlow/components/pages/AssignedReply.vue";
// import KnowledgeSearch from "@/views/application/vueFlow/components/pages/KnowledgeSearch.vue";
// import QuestionsClassify from "@/views/application/vueFlow/components/pages/QuestionsClassify.vue";
// import TxtExtract from "@/views/application/vueFlow/components/pages/TxtExtract.vue";
// import KnowledgeSearchMerge from "@/views/application/vueFlow/components/pages/KnowledgeSearchMerge.vue";
// import TxtProgressing from "@/views/application/vueFlow/components/pages/TxtProgressing.vue";
// import Judger from "@/views/application/vueFlow/components/pages/Judger.vue";
// import AppCall from "@/views/application/vueFlow/components/pages/AppCall.vue";
// import HttpRequest from "@/views/application/vueFlow/components/pages/HttpRequest.vue";
// import QuestionOptimize from "@/views/application/vueFlow/components/pages/QuestionOptimize.vue";
// import CustomFeedback from "@/views/application/vueFlow/components/pages/CustomFeedback.vue";

const {
	onPaneReady,
	// onNodeDragStop,
	onConnect,
	addEdges,
	// api文档 https://vueflow.dev/typedocs/types/AddNodes.html
	addNodes,
	setViewport,
	toObject,
	getNodes,
	removeNodes,
} = useVueFlow();

const { getTransform } = useZoomPanHelper();
const dialog = useDialog();
const flowStore = useFlowStore();

const data = reactive({
	flow: {
		instanceFlow: undefined,
		// 节点
		// !attention 直接修改传入的数组会导致页面卡死一段时间，现采用视图、数据分开管理的方式
		nodes: [
			{
				id: "0",
				data: {},
				type: "startGuide",
				position: { x: 0, y: -500 },
			},
			{
				id: "1",
				data: {},
				type: "LLM",
				position: { x: -300, y: 0 },
			},
			{
				id: "2",
				data: {},
				label: "Node2",
				type: "code",
				position: { x: 500, y: 0 },
			},
			{
				id: "3",
				data: {},
				label: "Node3",
				type: "knowledge",
				position: { x: 1100, y: 0 },
			},
			{
				id: "4",
				data: {},
				label: "Node4",
				type: "condition",
				position: { x: 1700, y: 0 },
			},
			{
				id: "5",
				data: {},
				type: "variable",
				position: { x: 0, y: 1000 },
			},
			{
				id: "6",
				data: {},
				type: "database",
				position: { x: 600, y: 1000 },
			},
			{
				id: "7",
				data: {},
				type: "message",
				position: { x: 1200, y: 1000 },
			},
			{
				id: "8",
				data: {},
				type: "endFlow",
				position: { x: 1800, y: 1000 },
			},
		],
		/**
		 * !delete 已废除，实时读取操作很费时，会卡页面
		 * 只做读取操作，不进行修改，需要时读取
		 */
		// curNodes: computed(() => getFlowNodesList(getNodes.value)),
		// 连线
		edges: [],
		// { id: "e1-2", source: "1", target: "2", animated: true }
	},
	opt: {
		nodesDraggable: true, // 允许(节点?)拖动
	},
});

/**
 * 添加节点
 *
 * 如果对传入的节点数组进行修改，会导致页面卡死一段时间
 * 暂时没有好的解决方案，现不进行双向绑定，采用实时获取的方式获取当前节点数组
 */
const addFlowNode = (node: any) => {
	const { x, y, zoom } = getTransform();
	const position = {
		x: (node?.x - x) / zoom,
		// 58 为顶部导航栏高度
		// y: ((鼠标位置位于父元素位置 - 当前y坐标) / 缩放比例) - (顶部栏高度 / 缩放比例)
		y: (node?.y - y) / zoom + 58 / zoom,
	};

	addNodes({
		id: uuidv4(),
		data: {},
		label: node?.label || getFlowNodeType(node.type).label || "",
		type: node?.type,
		position: position,
		class: node?.class,
		style: node?.style,
	});
};

// 复制节点
const handleDuplicate = (node) => {
	const { position } = node;
	const newNode = reactive({
		// !attention 如果连原对象的events事件一起直接赋值，原组件的鼠标事件触发时会报错
		// 现只复制必要的参数
		// ...node,
		id: uuidv4(),
		data: node?.data || {},
		type: node.type,
		position: {
			...position,
			x: position.x + 60,
			y: position.y + 60,
		},
	});

	// 新增视图节点
	addNodes(newNode);
	// 同步新增数据节点
	// data.flow.nodes.push(newNode);

	// nextTick(() => {
	// 	data.flow.nodes = [...data.flow.nodes, newNode];
	// 	console.log(getNodes);
	// }, 0);
	// console.log(data.flow.curNodes);
	console.log(getFlowNodesList(getNodes.value));
};

// handle组件间被链接
const handleConnect = (e) => {
	const { source, target } = e;
	const curID = `${source}-${target}`;

	// 已有连接
	const isConnected = data.flow.edges.find((cur) => {
		return (
			// 已存在
			cur.id == curID
			// 已被链接
			// cur.source == source ||
			// cur.target == target
		);
	});

	if (isConnected) return;

	// 添加连接线
	data.flow.edges.push({
		id: curID,
		source,
		target,
		type: "button",
		// data: { id: curID },
		// markerEnd: MarkerType.ArrowClosed,
	});
};

// 视图上删除线后执行
const handleRemoveEdges = (id) => {
	const curIndex = data.flow.edges.findIndex((cur) => cur.id == id);
	data.flow.edges.splice(curIndex, 1);
};

// 删除节点
const deleteNode = (id = flowStore?.curActive) => {
	dialog.info({
		title: "删除当前节点",
		content: "一旦删除，将无法恢复。",
		positiveText: "删除",
		negativeText: "取消",
		onPositiveClick: () => {
			// data.flow.nodes = data.flow.nodes.filter((item) => {
			// 	return item.id != id;
			// });
			removeNodes(id);
		},
	});
};

// 处理键盘事件
const handleKeydown = (e: KeyboardEvent) => {
	// console.log(e.code);
	// 退格、删除键
	switch (e.code) {
		case "Backspace" || "Delete":
			if (!flowStore.curActive) return;
			deleteNode();
			break;
	}
};

// 取消节点激活，点击空白区时
const handleDeactive = () => {
	flowStore.setActiveComponent(undefined);
};

// 保存data数据
const saveForm = (id, form) => {
	// debounce(() => {
	// const curNode = data.flow.nodes.find((item) => item.id == id);
	// curNode.data = { ...curNode.data, form };
	// console.log("curNode", curNode);
	// }, 2000);
	// console.log(getNodes.value);

	console.log("curList", getFlowNodesList(getNodes.value));

	// todo 保存数据
};

onPaneReady((instance: any) => {
	instance.fitView();
	// 将对象缓存
	data.flow.instanceFlow = instance;
	// 设置缩放级别
	// data.instanceFlow.zoomTo(0.3);
	// data.instanceFlow.fitBounds(getRectOfNodes({ height: 100, width: 100 }));
});

defineExpose({
	addFlowNode,
});
</script>

<!-- 使用scoped会导致vue flow组件内部无法应用本文件导入或定义的样式 -->
<style lang="less">
/* these are necessary styles for vue flow */
@import "@vue-flow/core/dist/style.css";
/* this contains the default theme, these are optional styles */
@import "@vue-flow/core/dist/theme-default.css";
</style>
