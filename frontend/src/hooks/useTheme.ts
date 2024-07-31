import { computed, watch } from 'vue'
import { darkTheme, useOsTheme } from 'naive-ui'
import { useAppStore } from '@/store'

// 可以修改的全局主题配置
// {
//   "name": "common", // 通用主题名称
//   "fontFamily": "v-sans, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif, \"Apple Color Emoji\", \"Segoe UI Emoji\", \"Segoe UI Symbol\"", // 通用字体系列
//   "fontFamilyMono": "v-mono, SFMono-Regular, Menlo, Consolas, Courier, monospace", // 等宽字体系列
//   "fontWeight": "400", // 常规字体粗细
//   "fontWeightStrong": "500", // 强调字体粗细
//   "cubicBezierEaseInOut": "cubic-bezier(.4, 0, .2, 1)", // 缓入缓出动画贝塞尔曲线
//   "cubicBezierEaseOut": "cubic-bezier(0, 0, .2, 1)", // 缓出动画贝塞尔曲线
//   "cubicBezierEaseIn": "cubic-bezier(.4, 0, 1, 1)", // 缓入动画贝塞尔曲线
//   "borderRadius": "3px", // 通用边框圆角
//   "borderRadiusSmall": "2px", // 小尺寸边框圆角
//   "fontSize": "14px", // 常规字体大小
//   "fontSizeMini": "12px", // 迷你字体大小
//   "fontSizeTiny": "12px", // 极小字体大小
//   "fontSizeSmall": "14px", // 小字体大小
//   "fontSizeMedium": "14px", // 中等字体大小
//   "fontSizeLarge": "15px", // 大字体大小
//   "fontSizeHuge": "16px", // 特大字体大小
//   "lineHeight": "1.6", // 行高
//   "heightMini": "16px", // 迷你高度
//   "heightTiny": "22px", // 极小高度
//   "heightSmall": "28px", // 小高度
//   "heightMedium": "34px", // 中等高度
//   "heightLarge": "40px", // 大高度
//   "heightHuge": "46px", // 特大高度
//   "baseColor": "#FFF", // 基础颜色
//   "primaryColor": "#18a058", // 主要颜色
//   "primaryColorHover": "#36ad6a", // 主要颜色悬停时的颜色
//   "primaryColorPressed": "#0c7a43", // 主要颜色按压时的颜色
//   "primaryColorSuppl": "#36ad6a", // 主要颜色补充
//   "infoColor": "#2080f0", // 信息颜色
//   "infoColorHover": "#4098fc", // 信息颜色悬停时的颜色
//   "infoColorPressed": "#1060c9", // 信息颜色按压时的颜色
//   "infoColorSuppl": "#4098fc", // 信息颜色补充
//   "successColor": "#18a058", // 成功颜色
//   "successColorHover": "#36ad6a", // 成功颜色悬停时的颜色
//   "successColorPressed": "#0c7a43", // 成功颜色按压时的颜色
//   "successColorSuppl": "#36ad6a", // 成功颜色补充
//   "warningColor": "#f0a020", // 警告颜色
//   "warningColorHover": "#fcb040", // 警告颜色悬停时的颜色
//   "warningColorPressed": "#c97c10", // 警告颜色按压时的颜色
//   "warningColorSuppl": "#fcb040", // 警告颜色补充
//   "errorColor": "#d03050", // 错误颜色
//   "errorColorHover": "#de576d", // 错误颜色悬停时的颜色
//   "errorColorPressed": "#ab1f3f", // 错误颜色按压时的颜色
//   "errorColorSuppl": "#de576d", // 错误颜色补充
//   "textColorBase": "#000", // 基础文本颜色
//   "textColor1": "rgb(31, 34, 37)", // 一级文本颜色
//   "textColor2": "rgb(51, 54, 57)", // 二级文本颜色
//   "textColor3": "rgb(118, 124, 130)", // 三级文本颜色
//   "textColorDisabled": "rgba(194, 194, 194, 1)", // 禁用文本颜色
//   "placeholderColor": "rgba(194, 194, 194, 1)", // 占位符文本颜色
//   "placeholderColorDisabled": "rgba(209, 209, 209, 1)", // 禁用占位符文本颜色
//   "iconColor": "rgba(194, 194, 194, 1)", // 图标颜色
//   "iconColorHover": "rgba(146, 146, 146, 1)", // 图标悬停时的颜色
//   "iconColorPressed": "rgba(175, 175, 175, 1)", // 图标按压时的颜色
//   "iconColorDisabled": "rgba(209, 209, 209, 1)", // 禁用图标颜色
//   "opacity1": "0.82", // 不透明度1
//   "opacity2": "0.72", // 不透明度2
//   "opacity3": "0.38", // 不透明度3
//   "opacity4": "0.24", // 不透明度4
//   "opacity5": "0.18", // 不透明度5
//   "dividerColor": "rgb(239, 239, 245)", // 分割线颜色
//   "borderColor": "rgb(224, 224, 230)", // 边框颜色
//   "closeIconColor": "rgba(102, 102, 102, 1)", // 关闭图标颜色
//   "closeIconColorHover": "rgba(102, 102, 102, 1)", // 关闭图标悬停时的颜色
//   "closeIconColorPressed": "rgba(102, 102, 102, 1)", // 关闭图标按压时的颜色
//   "closeColorHover": "rgba(0, 0, 0, .09)", // 关闭颜色悬停时的颜色
//   "closeColorPressed": "rgba(0, 0, 0, .13)", // 关闭颜色按压时的颜色
//   "clearColor": "rgba(194, 194, 194, 1)", // 清除颜色
//   "clearColorHover": "rgba(146, 146, 146, 1)", // 清除颜色悬停时的颜色
//   "clearColorPressed": "rgba(175, 175, 175, 1)", // 清除颜色按压时的颜色
//   "scrollbarColor": "rgba(0, 0, 0, 0.25)", // 滚动条颜色
//   "scrollbarColorHover": "rgba(0, 0, 0, 0.4)", // 滚动条悬停时的颜色
//   "scrollbarWidth": "5px", // 滚动条宽度
//   "scrollbarHeight": "5px", // 滚动条高度
//   "scrollbarBorderRadius": "5px", // 滚动条边角半径
//   "progressRailColor": "rgba(235, 235, 235, 1)", // 进度条轨道颜色
//   "railColor": "rgb(219, 219, 223)", // 轨道颜色
//   "popoverColor": "#fff", // 弹出层颜色
//   "tableColor": "#fff", // 表格背景颜色
//   "cardColor": "#fff", // 卡片背景颜色
//   "modalColor": "#fff", // 模态框背景颜色
//   "bodyColor": "#fff", // 主体背景颜色
//   "tagColor": "#eee", // 标签颜色
//   "avatarColor": "rgba(204, 204, 204, 1)", // 头像背景颜色
//   "invertedColor": "rgb(0, 20, 40)", // 反转背景颜色
//   "inputColor": "rgba(255, 255, 255, 1)", // 输入框背景颜色
//   "codeColor": "rgb(244, 244, 248)", // 代码块背景颜色
//   "tabColor": "rgb(247, 247, 250)", // 选项卡背景颜色
//   "actionColor": "rgb(250, 250, 252)", // 操作颜色
//   "tableHeaderColor": "rgb(250, 250, 252)", // 表头颜色
//   "hoverColor": "rgb(243, 243, 245)", // 悬停背景颜色
//   "tableColorHover": "rgba(0, 0, 100, 0.03)", // 表格悬停行颜色
//   "tableColorStriped": "rgba(0, 0, 100, 0.02)", // 表格条纹行颜色
//   "pressedColor": "rgb(237, 237, 239)", // 按压背景颜色
//   "opacityDisabled": "0.5", // 禁用透明度
//   "inputColorDisabled": "rgb(250, 250, 252)", // 禁用输入框背景颜色
//   "buttonColor2": "rgba(46, 51, 56, .05)", // 按钮颜色2
//   "buttonColor2Hover": "rgba(46, 51, 56, .09)", // 按钮悬停颜色2
//   "buttonColor2Pressed": "rgba(46, 51, 56, .13)", // 按钮按压颜色2
//   "boxShadow1": "0 1px 2px -2px rgba(0, 0, 0, .08), 0 3px 6px 0 rgba(0, 0, 0, .06), 0 5px 12px 4px rgba(0, 0, 0, .04)", // 阴影效果1
//   "boxShadow2": "0 3px 6px -4px rgba(0, 0, 0, .12), 0 6px 16px 0 rgba(0, 0, 0, .08), 0 9px 28px 8px rgba(0, 0, 0, .05)", // 阴影效果2
//   "boxShadow3": "0 6px 16px -9px rgba(0, 0, 0, .08), 0 9px 28px 0 rgba(0, 0, 0, .05), 0 12px 48px 16px rgba(0, 0, 0, .03)" // 阴影效果3
// }


export const globalColors = {
  btnActive: '#0653FF',
  btnDeactive: '#4D79AB',
  bgMain: '#f5f7fa',
  bgChatActive: '#ebeaed',
  txtDeep: '#333639',
  txtMainColor: '#111824',
  agentBg: '#F7F7F8',
  borderColor: '#4b9e5f',
  bgNeutral: '#f5f5f5',
  textColor: '#4b9e5f',
  darkBg: '#24272e',
};


// 定义全局颜色常量
export const lightThemeColors = {
  btnActive: '#0653FF', // 激活按钮颜色
  btnDeactive: '#4D79AB', // 未激活按钮颜色
  bgMain: '#f5f7fa', // 主背景颜色
  bgChatActive: '#F4F4F4', // 活跃聊天背景颜色
  txtDeep: '#333639', // 深色文字颜色
  txtMainColor: '#111824', // 主文字颜色
  agentBg: '#F7F7F8', // 智能体背景颜色
}

export const darkThemeColors = {
  btnActive: '#0653FF', // 激活按钮颜色
  btnDeactive: '#4D79AB', // 未激活按钮颜色
  bgMain: '#1A202C', // 主背景颜色
  bgChatActive: '#F7F7F8', // 活跃聊天背景颜色
  txtDeep: '#E2E8F0', // 深色文字颜色
  txtMainColor: '#E2E8F0', // 主文字颜色
  agentBg: '#2D3748', // 智能体背景颜色
}

// 定义全局配置常量
export const globalConfig = {
  btnRadius: '8px',  // 按钮圆角半径
}

// 自定义主题钩子函数
export function useTheme() {
  const appStore = useAppStore()
  // 系统主题
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


  const themeOverrides = computed(() => {
    if (isDark.value) {
      return {
        common: {
          ...darkThemeColors,
        },
      }
    }

    return {
      common: {
        ...lightThemeColors,
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


