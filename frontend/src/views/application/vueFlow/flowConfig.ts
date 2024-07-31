import { globalColors } from "@/hooks/useTheme"

declare namespace IConfig {
  interface IGroup {
    title: string      // 分组名称
    children: INode[]  // 组件列表
  }

  interface INode {
    label: string   // 组件名称
    key: string     // 组件key
    desc: string    // 描述
    icon: string    // 图标
    iconColor: string     // 图标颜色
    undeletable?: boolean // 不可删除
    width?: string  // 组件宽度
  }
}

export const flowConfig = {
  width: '400px',
  borderRadius: '8px',
}

export const flowNodeType: IConfig.INode[] = [
  {
    label: "LLM",
    key: "LLM",
    desc: "调用大型语言模型使用变量和提示词生成回答。",
    icon: "mdi:robot",
    iconColor: globalColors.btnActive,
    width: '700px',
  },
  {
    label: "代码",
    key: "code",
    desc: "编写代码以处理输入变量并生成返回值。",
    icon: "ph:code-duotone",
    iconColor: globalColors.btnActive,
    width: '500px',
  },
  {
    label: "知识库",
    key: "knowledge",
    desc: "在所选知识中，匹配信息并基于输入变量重新收集信息，最后作为数组返回。",
    icon: "icon-park-outline:tree",
    iconColor: globalColors.btnActive,
    width: '500px',
  },
  {
    label: "条件",
    key: "condition",
    desc: "连接两个下游分支。如果满足设置的条件，则仅运行“if”分支；否则，只运行'else'分支。",
    icon: "icon-park-outline:branch",
    iconColor: globalColors.btnActive,
    width: '1000px',
  },
  {
    label: "变量",
    key: "variable",
    desc: "用于在您的机器人中读取和写入变量，变量名称必须与机器人中的变量名称匹配。",
    icon: "mdi:variable-box",
    iconColor: globalColors.btnActive,
    width: '500px',
  },
  {
    label: "数据库",
    key: "database",
    desc: "用户可以在开发人员控制的数据库中读取和写入数据。必须事先将表添加到Bot的数据库中。",
    icon: "healthicons:database",
    iconColor: globalColors.btnActive,
    width: '500px',
  },
  {
    label: "消息",
    key: "message",
    desc: "支持中间进程中的消息输出以及流式和非流式方法",
    icon: "icon-park-outline:message-one",
    iconColor: globalColors.btnActive,
    width: '500px',
  },
  // {
  //   title: "系统输入",
  //   children: [
  //     {
  //       label: "对话入口",
  //       key: "chatEntrance",
  //       desc: "当用户发送一个内容后，流程将会从这个模块开始执行。",
  //       icon: "iconoir:input-field",
  //       iconColor: globalColors.btnActive,
  //     },
  //   ],
  // },
  // {
  //   title: "文本输出",
  //   children: [
  //     {
  //       label: "AI 对话",
  //       key: "AIChat",
  //       desc: "AI 大模型对话",
  //       icon: "uil:robot",
  //       iconColor: "#363C42",
  //     },
  //     {
  //       label: "指定回复",
  //       key: "assignedReply",
  //       desc: "该模块可以直接回复一段指定的内容。常用于引导、提示。非字符串内容传入时，会转成字符串进行输出。",
  //       icon: "carbon:chat",
  //       iconColor: "#898E92",
  //     },
  //   ],
  // },
  // {
  //   title: "功能调用",
  //   children: [
  //     {
  //       label: "知识库搜索",
  //       key: "knowledgeSearch",
  //       desc: "调用知识库搜索能力，查找有可能与问题相关的内容",
  //       icon: "solar:cloud-storage-bold-duotone",
  //       iconColor: globalColors.btnActive,
  //     },
  //     {
  //       label: "问题分类",
  //       key: "questionsClassify",
  //       desc: "根据用户的历史记录和当前问题判断该次提问的类型。可以添加多组问题类型，下面是一个模板例子：类型1: 打招呼；类型2: 关于商品“使用”问题；类型3: 关于商“购买”问题；类型4: 其他问题",
  //       icon: "flat-color-icons:idea",
  //       iconColor: "",
  //     },
  //     {
  //       label: "文本内容提取",
  //       key: "txtExtract",
  //       desc: "可从文本中提取指定的数据，例如：sql语句、搜索关键词、代码等",
  //       icon: "icon-park-outline:tree",
  //       iconColor: globalColors.btnActive,
  //     },
  //   ],
  // },
  // {
  //   title: "工具",
  //   children: [
  //     {
  //       label: "知识库搜索引用合并",
  //       key: "knowledgeSearchMerge",
  //       desc: "可以将多个知识库搜索结果进行合并输出。使用 RRF 的合并方式进行最终排序输出。",
  //       icon: "carbon:direction-merge-filled",
  //       iconColor: "#1296DB",
  //     },
  //     {
  //       label: "文本加工",
  //       key: "txtProgressing",
  //       desc: "可对固定或传入的文本进行加工后输出，非字符串类型数据最终会转成字符串类型。",
  //       icon: "icon-park-outline:edit-one",
  //       iconColor: "#FCAA3E",
  //     },
  //     {
  //       label: "判断器",
  //       key: "judger",
  //       desc: "根据传入的内容进行 True False 输出。默认情况下，当传入的内容为 false, undefined, null, 0, none 时，会输出 false。你也可以增加一些自定义的字符串来补充输出 false 的内容。非字符、非数字、非布尔类型，直接输出 True。",
  //       icon: "material-symbols:calculate-outline",
  //       iconColor: "#48C9B0",
  //     },
  //   ],
  // },
  // {
  //   title: "外部调用",
  //   children: [
  //     {
  //       label: "应用调用",
  //       key: "appCall",
  //       desc: "可以选择一个其他应用进行调用",
  //       icon: "icon-park-twotone:more-app",
  //       iconColor: "#5689F5",
  //     },
  //     {
  //       label: "HTTP 请求",
  //       key: "httpRequest",
  //       desc: "可以发出一个 HTTP 请求，实现更为复杂的操作（联网搜索、数据库查询等）",
  //       icon: "fluent:document-one-page-link-24-regular",
  //       iconColor: globalColors.btnActive,
  //     },
  //   ],
  // },
  // {
  //   title: "其他",
  //   children: [
  //     {
  //       label: "问题优化",
  //       key: "questionOptimize",
  //       desc: "使用问题优化功能，可以提高知识库连续对话时搜索的精度。使用该功能后，会先利用 AI 根据上下文构建一个或多个新的检索词，这些检索词更利于进行知识库搜索。该模块已内置在知识库搜索模块中，如果您仅进行一次知识库搜索，可直接使用知识库内置的补全功能。",
  //       icon: "oi:timer",
  //       iconColor: globalColors.btnActive,
  //     },
  //     {
  //       label: "自定义反馈",
  //       key: "customFeedback",
  //       desc: "该模块被触发时，会给当前的对话记录增加一条反馈。可用于自动记录对话效果等。",
  //       icon: "ant-design:node-index-outlined",
  //       iconColor: "#1DCCA1",
  //     },
  //   ],
  // },
]

// 默认配置 不展示在左侧添加栏的组件配置项
const defaultConfig: IConfig.INode[] = [
  {
    label: "开始",
    key: "startGuide",
    desc: "工作流的起始节点，用于设置启动工作流所需的信息。",
    icon: "mdi:ray-start",
    iconColor: globalColors.btnActive,
    width: '700px',
    undeletable: true,  // 不可删除，隐藏右上角按钮
  },
  {
    label: "结束",
    key: "endFlow",
    desc: "工作流的最后一个节点，用于在工作流运行后返回结果信息。",
    icon: "material-symbols:line-end",
    iconColor: globalColors.btnActive,
    width: '500px',
    undeletable: true,
  },
]

/**
 * 根据key获取对应的组件类型配置项
 * @param key 组件key
 * @returns 返回对应的组件
 */
export const getFlowNodeType = (key: string) => {
  let res: undefined | IConfig.INode = undefined;
  // 每个分组
  // flowNodeType.find((curGroup: IConfig.IGroup) => {
  //   // 每个组件类型
  //   curGroup?.children?.find((node: IConfig.INode) => {
  //     if (node.key == key)
  //       return res = node
  //   })
  // })

  // 寻找当前配置项
  flowNodeType.find((curGroup: IConfig.INode) => {
    if (curGroup.key == key)
      return res = curGroup
  })

  // 不在普通配置中
  if (res) return res;

  // 从默认配置查找
  defaultConfig.find((node) => {
    if (node.key == key)
      // 默认节点不可删除，或改为单独配置
      return res = { ...node, undeletable: true }
  })
  return res;
}