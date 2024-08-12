// import 'katex/dist/katex.min.css' // 该行被注释掉了，可能是因为不需要使用 KaTeX 的样式
import '@/styles/lib/tailwind.css' // 引入 Tailwind CSS 样式
import '@/styles/lib/highlight.less' // 引入代码高亮的样式
import '@/styles/lib/github-markdown.less' // 引入 GitHub Markdown 样式
import '@/styles/global.less' // 引入全局样式

/** Tailwind's Preflight Style Override */
function naiveStyleOverride() {
  // 创建一个 meta 标签，用于覆盖 naive-ui 的样式
  const meta = document.createElement('meta')
  meta.name = 'naive-ui-style'
  document.head.appendChild(meta) // 将 meta 标签添加到文档的 head 中
}

function setupAssets() {
  // 调用 naiveStyleOverride 函数，进行样式覆盖
  naiveStyleOverride()
}

// 导出 setupAssets 函数，供其他模块使用
export default setupAssets