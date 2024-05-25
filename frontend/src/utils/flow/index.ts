export let isDraggable = true

export const setDraggable = (draggable?: boolean) => {
  if (draggable)
    return isDraggable = draggable

  isDraggable = !isDraggable
}

// 阻止flow节点可拖动
export const stopDraggable = (e: MouseEvent) => {
  // 不可拖动时阻止拖动
  if (!isDraggable) e.stopPropagation()
}

/**
 * 获取当前flow中的节点数组
 * @param nodeList getNodes返回的节点数组 (需要使用flow组件的页面传入，否则获取为空)
 * @returns 处理后的节点数组
 * 
 * !attention 如果对传入的节点数组进行修改，会导致页面卡死一段时间
 * 暂时没有好的解决方案，现采用视图、数据分开管理的方式，实时获取当前所有节点
 */
export const getFlowNodesList = (nodeList: any) => {
  return nodeList?.map((cur: any) => ({
    id: cur?.id,
    data: cur?.data,
    label: cur?.label,
    type: cur?.type,
    position: cur?.position,
  }))
}
