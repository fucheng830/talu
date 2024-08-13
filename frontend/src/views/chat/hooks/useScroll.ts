import type { Ref } from 'vue'
import { nextTick, ref } from 'vue'

// 定义滚动元素的类型为 HTMLDivElement 或 null
type ScrollElement = HTMLDivElement | null

// 定义一个接口，描述滚动相关的返回值
interface ScrollReturn {
  scrollRef: Ref<ScrollElement>  // 滚动元素的引用
  scrollToBottom: () => Promise<void>  // 滚动到底部的方法
  scrollToTop: () => Promise<void>  // 滚动到顶部的方法
  scrollToBottomIfAtBottom: () => Promise<void>  // 如果在底部则滚动到底部的方法
}

// 导出一个名为 useScroll 的函数，用于处理滚动相关的逻辑
export function useScroll(): ScrollReturn {
  const scrollRef = ref<ScrollElement>(null)  // 创建一个滚动元素的引用

  // 异步方法，用于滚动到底部
  const scrollToBottom = async () => {
    await nextTick()  // 等待下一个微任务
    if (scrollRef.value)  // 如果滚动元素存在
      scrollRef.value.scrollTop = scrollRef.value.scrollHeight  // 将滚动条位置设置为底部
  }

  // 异步方法，用于滚动到顶部
  const scrollToTop = async () => {
    await nextTick()  // 等待下一个微任务
    if (scrollRef.value)  // 如果滚动元素存在
      scrollRef.value.scrollTop = 0  // 将滚动条位置设置为顶部
  }

  // 异步方法，如果当前接近底部则滚动到底部
  const scrollToBottomIfAtBottom = async () => {
    await nextTick()  // 等待下一个微任务
    if (scrollRef.value) {  // 如果滚动元素存在
      const threshold = 100 // 定义一个阈值，表示滚动条到底部的距离阈值
      const distanceToBottom = scrollRef.value.scrollHeight - scrollRef.value.scrollTop - scrollRef.value.clientHeight  // 计算距离底部的距离
      if (distanceToBottom <= threshold)  // 如果距离底部小于等于阈值
        scrollRef.value.scrollTop = scrollRef.value.scrollHeight  // 将滚动条位置设置为底部
    }
  }

  return {
    scrollRef,
    scrollToBottom,
    scrollToTop,
    scrollToBottomIfAtBottom,
  }
}