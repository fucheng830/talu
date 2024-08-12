<template>
	<div ref="refEditor" class="h-full"></div>
</template>

<script setup lang="ts">
// 这是一个基于 Vue 3 和 TypeScript 的自定义代码编辑器组件。它使用了 Monaco Editor，这是一个强大的代码编辑器库，常用于构建类似于 Visual Studio Code 的编辑器。

// 组件功能概述：
// 模板部分 (<template>):

// 包含一个 div 元素，使用 ref 绑定来引用该元素，以便在脚本部分初始化 Monaco Editor。
// 脚本部分 (<script setup lang="ts">):

// 导入必要的库和模块，包括 monaco-editor 和 Vue 的 onMounted, reactive, ref。
// 定义了 emits 和 props，用于处理父组件传递的属性和事件。
// 使用 ref 和 reactive 创建响应式数据对象。
// 定义了 init 函数，用于初始化 Monaco Editor，并设置编辑器的语言、主题和初始值。
// 在组件挂载时（onMounted），调用 init 函数初始化编辑器。
// 样式部分 (<style lang="less" scoped>):

// 使用了 scoped 关键字，确保样式只作用于当前组件。
// 主要功能：
// 编辑器初始化：在 init 函数中，使用 monaco.editor.create 方法初始化编辑器，并设置编辑器的语言、主题和初始值。
// 内容变化监听：通过 oEditor.onDidChangeModelContent 监听编辑器内容的变化，并通过 emits 触发 update:value 事件，将编辑器的内容传递给父组件。
// 这个组件可以用于需要代码编辑功能的场景，比如在线代码编辑器、配置文件编辑等。
import * as monaco from "monaco-editor/esm/vs/editor/editor.api.js";
import { onMounted, reactive, ref } from "vue";
import { langHignlight } from "@/components/common/CodeEditor/langConfig.js";

const emits = defineEmits(["update:value"]);
const props = defineProps({
	value: String, // 编辑器的值
	theme: {
		type: String,
		default: "vs-dark", // 'vs' | 'vs-dark' | 'hc-black'
	},
	lang: {
		type: String,
		default: "javascript", // 'javascript' | 'json'
	},
});

// 当前编辑器对象，使用ref()绑定会导致触发onDidChangeModelContent时卡死页面
let oEditor: monaco.editor.IStandaloneCodeEditor;
const refEditor = ref();
const data = reactive({
	form: {
		txtInput: "",
	},
});

const init = () => {
	/**
	 * 官方文档
	 *  https://novaalone.github.io/monaco-editor-doc-zh/guide/create.html#%E5%B8%B8%E7%94%A8%E9%80%89%E9%A1%B9
	 *
	 * https://microsoft.github.io/monaco-editor/docs.html#modules/editor.html
	 */

	monaco.languages.register({
		id: "javascript",
	});

	monaco.languages.setMonarchTokensProvider(
		"javascript",
		langHignlight.javascript
	);

	// 初始化编辑器
	oEditor = monaco.editor.create(refEditor?.value, {
		value: props.value, // 编辑器的初始值
		theme: props.theme, // 'vs' | 'vs-dark' | 'hc-black'
		language: props.lang,
		minimap: {
			enabled: false,
		},
	});

	// console.log("oEditor loaded", oEditor);

	// 内容变化时
	oEditor.onDidChangeModelContent((val) => {
		// console.log("res", oEditor.getValue());
		emits("update:value", oEditor.getValue());
	});
};

onMounted(() => {
	init();
});
</script>

<style lang="less" scoped></style>
