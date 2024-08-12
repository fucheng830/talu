<script setup lang='ts'>
// 导入必要的模块和组件
import { computed } from 'vue'
import type { PopoverPlacement } from 'naive-ui'
import { NTooltip } from 'naive-ui'
import Button from './Button.vue'

// 定义组件的 Props 接口
interface Props {
  tooltip?: string
  placement?: PopoverPlacement
}

// 定义组件的 Emit 接口
interface Emit {
  (e: 'click'): void
}

// 定义 props 的默认值
const props = withDefaults(defineProps<Props>(), {
  tooltip: '',
  placement: 'bottom',
})

// 定义 emit 函数用于触发事件
const emit = defineEmits<Emit>()

// 计算属性，用于判断是否显示 tooltip
const showTooltip = computed(() => Boolean(props.tooltip))

// 处理按钮点击事件的函数，并触发 'click' 事件
function handleClick() {
  emit('click')
}
</script>

<template>
  <!-- 根据 showTooltip 条件渲染 -->
  <div v-if="showTooltip">
    <!-- Tooltip 组件，设置位置和触发方式 -->
    <NTooltip :placement="placement" trigger="hover">
      <!-- Tooltip 触发器中的按钮插槽 -->
      <template #trigger>
        <Button @click="handleClick">
          <slot />
        </Button>
      </template>
      <!-- Tooltip 内容 -->
      {{ tooltip }}
    </NTooltip>
  </div>
  <div v-else>
    <!-- 没有 tooltip 的按钮 -->
    <Button @click="handleClick">
      <slot />
    </Button>
  </div>
</template>