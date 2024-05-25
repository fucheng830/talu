<script setup lang="ts">
// 引入Naive UI的配置提供器
import { NConfigProvider } from "naive-ui";
// 引入自定义的Naive提供器
import { NaiveProvider } from "@/components/common";
// 引入全局主题颜色和配置
import { globalColors, globalConfig } from "@/hooks/useTheme";
// 使用主题
import { useTheme } from "@/hooks/useTheme.ts";
import { useLanguage } from "@/hooks/useLanguage";

// 从定义的主题变量中获取主题覆盖
const { themeOverrides } = useTheme();
const { language } = useLanguage(); // 使用useLanguage钩子函数获取语言选项
</script>

<template>
	<!-- 主题提供器，全屏显示，并使用主题覆盖 -->
	<NConfigProvider
		class="w-full h-full"
		:theme-overrides="themeOverrides"
		:locale="language"
	>
		<!-- Naive提供器用于包裹内部组件，以便可以使用Naive UI的组件和功能 -->
		<NaiveProvider>
			<!-- 路由视图，显示由路由决定的组件 -->
			<RouterView />
		</NaiveProvider>
	</NConfigProvider>
</template>

<style lang="less">
/* 设置元素盒模型为border-box模式，这样元素的内边距和边框不影响设定的宽高 */
* {
	box-sizing: border-box;
}

/* 创建一个flex居中的类，将元素居中显示 */
.flex-center {
	display: flex;
	justify-content: center;
	align-items: center;
}

/* 隐藏滚动条 */
.no-scrollbar {
	scrollbar-width: none; /* Firefox */
	-ms-overflow-style: none; /* IE 10+ */
	&::-webkit-scrollbar {
		display: none; /* Chrome Safari */
	}
}
</style>
