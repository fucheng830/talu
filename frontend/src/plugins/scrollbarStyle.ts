import { darkTheme, lightTheme } from 'naive-ui'

const setupScrollbarStyle = () => {
  // 创建一个 style 标签
  const style = document.createElement('style')
  // 定义样式内容
  const styleContent = `
    ::-webkit-scrollbar {
      background-color: transparent;
      width: ${lightTheme.Scrollbar.common?.scrollbarWidth};
    }
    ::-webkit-scrollbar-thumb {
      background-color: ${lightTheme.Scrollbar.common?.scrollbarColor};
      border-radius: ${lightTheme.Scrollbar.common?.scrollbarBorderRadius};
    }
    html.dark ::-webkit-scrollbar {
      background-color: transparent;
      width: ${darkTheme.Scrollbar.common?.scrollbarWidth};
    }
    html.dark ::-webkit-scrollbar-thumb {
      background-color: ${darkTheme.Scrollbar.common?.scrollbarColor};
      border-radius: ${darkTheme.Scrollbar.common?.scrollbarBorderRadius};
    }
  `

  // 将样式内容添加到 style 标签中
  style.innerHTML = styleContent
  // 将 style 标签添加到文档的 head 中
  document.head.appendChild(style)
}

// 导出 setupScrollbarStyle 函数，供其他模块使用
export default setupScrollbarStyle