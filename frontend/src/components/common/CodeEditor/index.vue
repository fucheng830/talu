<template>
	<div ref="refEditor" class="h-full"></div>
</template>

<script setup lang="ts">
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
