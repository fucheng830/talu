import { defineStore } from 'pinia';
// 用于获取云端数据的逻辑
import { api } from "@/api/common";

export interface Agents {
  categories: string[]
  agents: any[]
}


export const useAgentStore = defineStore('agents-store', {
  state: () => ({
    categories: [],
    agents: []
  }),

  actions: {
    async updateAgents() {
      const res = await api.agents()
      if (res) {
        this.$state.categories = res.data.categories
        this.$state.agents = res.data.agents
      }
    }
  },
});


