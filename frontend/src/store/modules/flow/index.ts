import { defineStore } from 'pinia'
import { IFlow, getLocalSetting, setLocalSetting } from './helper'

export const useFlowStore = defineStore('flow-store', {
  state: (): IFlow.FlowState => getLocalSetting(),
  actions: {
    setCurActive(id: string) {
      this.$state.curActive = id
    },

    // 保存 flow列表
    setFlowList(list: IFlow.FlowList[]) {
      // this.$state.flowList = { ...this.$state.flowList, ...list }
      this.$state.flowList = list
      this.recordState();
    },

    // 获取当前flow
    // getCurFlow(id: string) {
    //   return this.$state.flowList.find((item) => item.id === id)
    // },

    setActiveComponent(id: string | undefined) {
      this.$state.curActive = id
    },

    // 记录状态
    recordState() {
      setLocalSetting(this.$state)
    },
  },
})

// export function useKnowledgeStoreWithOut() {
//   return useKnowledgeStore(store)
// }
