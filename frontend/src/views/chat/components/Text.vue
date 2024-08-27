<!-- 消息气泡模块 -->
<script lang="ts" setup>
// 引入Vue相关的函数
import { computed, ref } from "vue";
// 引入Markdown解析器
import MarkdownIt from "markdown-it";
// 引入Markdown的KaTeX插件，用于数学公式的渲染
import mdKatex from "@traptitech/markdown-it-katex";
// 引入Markdown的链接属性插件，用于自定义链接属性
import mila from "markdown-it-link-attributes";
// 引入代码高亮库
import hljs from "highlight.js";
// 引入自定义的Hook，用于获取基础布局信息
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { t } from "@/locales";

// 定义组件的Props类型
interface Props {
    inversion?: boolean;
    error?: boolean;
    text?: string;
    loading?: boolean;
    asRawText?: boolean;
}



const copyText = t('common.copy');

// 定义组件的Props
const props = defineProps<Props>();

// 从自定义Hook中获取是否为移动端的状态
const { isMobile } = useBasicLayout();

// 创建一个用于存储HTMLElement的引用
const textRef = ref<HTMLElement>();

// 初始化Markdown解析器实例，配置链接自动识别和代码高亮功能
const mdi = new MarkdownIt({
    linkify: true,
    highlight(code, language) {
        // 如果代码块的语言是HTML，则直接返回HTML代码
        // if (language === 'html') {
        //     return `<div class="html-block">${code}</div>`;
        // }
        // 其他语言的处理保持不变
        const validLang = !!(language && hljs.getLanguage(language));
        if (validLang) {
            const lang = language ?? "";
            return highlightBlock(
                hljs.highlight(code, { language: lang }).value,
                lang
            );
        }
        return highlightBlock(hljs.highlightAuto(code).value, "");
    },
});

// 使用链接属性插件，配置新标签页打开链接并添加安全属性
mdi.use(mila, { attrs: { target: "_blank", rel: "noopener" } });
// 使用KaTeX插件，配置数学公式的样式和错误颜色
mdi.use(mdKatex, {
    blockClass: "katexmath-block rounded-md p-[10px]",
    errorColor: " #cc0000",
});

// 计算包裹类名，根据不同状态应用不同的样式
const wrapClass = computed(() => {
    return [
        "text-wrap",
        "min-w-[10px]",
        "rounded-md",
        isMobile.value ? "p-2" : "px-3 py-1",
        props.inversion ? `bg-[#f4f6f8] text-[black]` : "text-[black]",
        props.inversion ? "dark:bg-[#a1dc95]" : "dark:bg-[#1e1e20]",
        props.inversion ? "message-request" : "message-reply",
        { "text-red-500": props.error },
    ];
});

// 计算文本内容，如果不是原始文本则使用Markdown解析器渲染
const text = computed(() => {
    const value = props.text ?? "";
    if (!props.asRawText) return mdi.render(value);
    return value;
});

// 定义代码高亮的函数
function highlightBlock(str: string, lang?: string) {
    
    return `<pre class="code-block-wrapper"><div class="code-block-header"><span class="code-block-header__lang">${lang}</span><span class="code-block-header__copy">${copyText}</span></div><code class="hljs code-block-body ${lang}">${str}</code></pre>`;
}

// 定义组件暴露的属性
defineExpose({ textRef });
</script>

<template>
    <!-- 根据计算得到的类名动态应用样式 -->
    <div :class="wrapClass">
        <!-- 如果处于加载状态，显示加载动画 -->
        <template v-if="loading">
            <span class="dark:text-white w-[4px] h-[20px] block animate-blink" />
        </template>
        <!-- 如果不是加载状态，显示文本内容 -->
        <template v-else>
            <div ref="textRef" class="leading-relaxed break-words">
                <!-- 如果不是反转模式，根据是否原始文本显示不同内容 -->
                <div v-if="!inversion">
                    <div v-if="!asRawText" class="markdown-body" v-html="text" />
                    <div v-else class="whitespace-pre-wrap" v-text="text" />
                </div>
                <!-- 如果是反转模式，显示原始文本 -->
                <div v-else class="whitespace-pre-wrap" v-text="text" />
            </div>
        </template>
    </div>
</template>

<style lang="less">
@import url(./style.less);
</style>