import type { GlobalThemeOverrides } from 'naive-ui'
import { computed, watch } from 'vue'
import { darkTheme, useOsTheme } from 'naive-ui'
import { useAppStore } from '@/store'

export const globalColors = {
  btnActive: '#0653FF',
  btnDeactive: '#4D79AB',
  bgMain: '#f5f7fa',
  bgChatActive: '#ebeaed',
  txtDeep: '#333639',
  txtMainColor: '#111824',

  agentBg: '#F7F7F8', // 智能体背景
}

export const globalConfig = {
  btnRadius: '8px',  // 圆角按钮
}

export function useTheme() {
  const appStore = useAppStore()

  const OsTheme = useOsTheme()

  const isDark = computed(() => {
    if (appStore.theme === 'auto')
      return OsTheme.value === 'dark'
    else
      return appStore.theme === 'dark'
  })

  const theme = computed(() => {
    return isDark.value ? darkTheme : undefined
  })

  const globalThemeConfig = {
    primaryColor: globalColors.btnActive,
    primaryColorHover: globalColors.btnActive,
    // hoverColor: globalColors.btnActive,
    borderRadius: '8px',
  }

  const themeOverrides = computed<GlobalThemeOverrides>(() => {
    if (isDark.value) {
      return {
        common: {
          ...globalThemeConfig,
        },
      }
    }

    return {
      common: {
        ...globalThemeConfig,
      },
    }
  })

  watch(
    () => isDark.value,
    (dark) => {
      if (dark)
        document.documentElement.classList.add('dark')
      else
        document.documentElement.classList.remove('dark')
    },
    { immediate: true },
  )

  return { isDark, theme, themeOverrides }
}
