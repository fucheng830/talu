/** @type {import('tailwindcss').Config} */
module.exports = {
  // 暗模式配置，使用 class 模式
  darkMode: 'class',
  // 内容配置，指定哪些文件需要应用 Tailwind CSS
  content: [
    './index.html', // 主 HTML 文件
    './src/**/*.{vue,js,ts,jsx,tsx}', // 所有在 src 目录下的 Vue、JavaScript、TypeScript、JSX、TSX 文件
  ],
  // 主题配置
  theme: {
    // 扩展默认主题
    extend: {
      // 动画配置
      animation: {
        blink: 'blink 1.2s infinite steps(1, start)', // 定义一个名为 blink 的动画，1.2秒无限循环，步进模式
      },
      // 关键帧配置
      keyframes: {
        blink: {
          '0%, 100%': { 'background-color': 'currentColor' }, // 0% 和 100% 时背景颜色为当前颜色
          '50%': { 'background-color': 'transparent' }, // 50% 时背景颜色为透明
        },
      },
    },
  },
  // 插件配置
  plugins: [],
}