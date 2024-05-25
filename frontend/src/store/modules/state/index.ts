import { defineStore } from 'pinia'
import { api } from '@/api/common'


export const useStateStore = defineStore('user-state-store', {
  state: () => ({
    showvip: false,
    showlogin: false,
    showsigin: false,
    showAdTips: false,
    showGzhTips: false,
    showConversationSetting: false,
    myAgents: [],
  }),

  actions: {
    changeVip() {
      this.showvip = !this.showvip
    },
    changeLogin() {
      this.showlogin = !this.showlogin
    },
    changeSigin() {
      this.showsigin = !this.showsigin
    },
    changeLoginReg(isLogin = true) {
      this.showlogin = isLogin
    },
    changeAdTips() {
      this.showAdTips = !this.showAdTips
    },
    changeGzhTips() {
      this.showGzhTips = !this.showGzhTips
    },
    changeConversationSetting() {
      this.showConversationSetting = !this.showConversationSetting
    },
    async updateMyAgents() {
      const res = await api.my_agents()
      if (res) {
        this.$state.myAgents = res
        console.log('myAgents', this.$state.myAgents)
    }
    }
  },

})
