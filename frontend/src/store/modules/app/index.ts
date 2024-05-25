import { defineStore } from 'pinia'
import type { AppState, Language, Theme } from './helper'
import { getLocalSetting, setLocalSetting } from './helper'
import { store } from '@/store'
import { isBoolean } from '@/utils/is'

export const useAppStore = defineStore('app-store', {
  state: (): AppState => getLocalSetting(),
  actions: {
    setSiderCollapsed(collapsed: boolean) {
      this.siderCollapsed = collapsed
      this.recordState()
    },

    setTheme(theme: Theme) {
      this.theme = theme
      this.recordState()
    },

    setLanguage(language: Language) {
      if (this.language !== language) {
        this.language = language
        this.recordState()
      }
    },

    // 修改 设置弹窗 显示状态
    changeShowSettingModal(show: boolean | undefined = undefined) {
      if (isBoolean(show))
        return (this.showSettingModal = show)

      this.showSettingModal = !this.showSettingModal
    },

    // 修改 登录弹窗 显示状态
    changeShowLoginModal(show: boolean | undefined = undefined) {
      if (isBoolean(show))
        return (this.showLoginModal = show)

      this.showLoginModal = !this.showLoginModal
    },

    recordState() {
      // 强制 将 设置弹窗关闭
      setLocalSetting({ ...this.$state, showSettingModal: false })
    },
  },
})

export function useAppStoreWithOut() {
  return useAppStore(store)
}
