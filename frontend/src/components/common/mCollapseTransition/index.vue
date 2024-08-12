<template>
    <!-- 折叠组件 -->
    <div class="w-full">
        <div class="grid grid-cols-[1fr_2rem]">
            <!-- 插槽，用于自定义头部内容，传递 changeCollapsed 函数 -->
            <slot name="header" :changeCollapsed="changeCollapsed"></slot>

            <!-- 右侧展开按钮 -->
            <div class="flex justify-center items-center" @click="() => changeCollapsed()">
                <!-- Icon 组件，设置图标和旋转动画 -->
                <Icon
                    icon="mingcute:right-fill"
                    width="44"
                    :style="{
                        transition: 'all .3s',
                        transform: `rotate(${data.isCollapsed ? 90 : 0}deg)`,
                    }"
                />
            </div>
        </div>

        <!-- 折叠过渡组件，控制显示和隐藏 -->
        <n-collapse-transition :show="data.isCollapsed">
            <!-- 默认插槽，用于显示内容 -->
            <slot>
                <div>暂无数据</div>
            </slot>
        </n-collapse-transition>
    </div>
</template>

<script setup lang="ts">
import { isBoolean } from "@/utils/is";
import { onMounted, reactive } from "vue";
import { Icon } from "@iconify/vue";

// 定义组件的 props
const props = defineProps({
    defaultCollapsed: {
        type: Boolean,
        default: true,
    },
});

// 定义响应式数据
const data = reactive({
    isCollapsed: true,
});

// 组件挂载时设置初始折叠状态
onMounted(() => {
    data.isCollapsed = props.defaultCollapsed;
});

// 改变折叠状态的函数
const changeCollapsed = (show: boolean | undefined = undefined) => {
    // 如果传入了布尔值，则设置折叠状态为该值
    if (isBoolean(show)) return (data.isCollapsed = show);
    // 否则，切换折叠状态
    data.isCollapsed = !data.isCollapsed;
};
</script>

<style lang="less" scoped></style>