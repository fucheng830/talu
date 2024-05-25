import { Icon } from "@iconify/vue"
import { h } from "vue"

export function getCurrentDate() {
  const date = new Date()
  const day = date.getDate()
  const month = date.getMonth() + 1
  const year = date.getFullYear()
  return `${year}-${month}-${day}`
}

// 渲染图标
// 可能需要另外 手动在vue中导入
// import { Icon } from "@iconify/vue";
export const renderIcon = ({ icon, color = "inherit", width = 22 }: {
  icon: string,
  color?: string,
  width?: number | string
}) => {
  return h(Icon, { icon, color, width });
};