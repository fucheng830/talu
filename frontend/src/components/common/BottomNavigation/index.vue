<script setup lang="ts">
import { reactive, computed } from 'vue';
import { Icon } from '@iconify/vue';
import { useRouter } from 'vue-router';
import { useTheme } from '@/hooks/useTheme';
import { lineThemeColorDark, lineThemeColorLight } from '@/styles/env/theme';

// 这个组件可以作为应用程序的底部导航栏，提供导航和主题切换功能。

// 获取路由实例
const router = useRouter();

// 子传父
const emitUpdateSettingShow = defineEmits(['changeShowSetting'])

const navigationData = reactive({
    data: [
        { iconURL: "basil:chat-outline", msg: "AI聊天", url: '/chat' },
        { iconURL: "mdi-light:book", msg: "知识库", url: '/knowledge' },
        { iconURL: "icon-park-outline:setting-two", msg: "设置" },
    ]
})

// 获取当前是否暗色系
const isDark = computed(() => useTheme().isDark.value)
console.log(isDark)

function navigate(option?: string | undefined) {
    option ? goUrl(option) : emitUpdateSettingShow('changeShowSetting')
}

function goUrl(url: any) {
    router.push(url)
}

</script>

<!-- 底部导航栏 -->
<template>
    <div class="bottom-0 fixed w-full py-2 flex border-t-2 shadow-inner"
        :style="[`border-color:${useTheme().isDark.value ? lineThemeColorDark : lineThemeColorLight}`]">
        <!-- 导航标签 -->
        <div v-for="(e, i) in navigationData.data" :key="`icon${i}`" class="flex flex-col flex-1 items-center">
            <a @click="navigate(e?.url)" class="flex flex-col items-center dark:text-[grey]">
                <Icon :icon="e.iconURL" width="26" />
                <span>{{ e.msg }} </span>
            </a>
        </div>
    </div>
</template>