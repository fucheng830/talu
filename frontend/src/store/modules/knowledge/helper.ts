import { ss } from '@/utils/storage'

const LOCAL_NAME = 'knowledgeStorage'

export declare namespace IKnowledge {
  // 知识状态接口
  interface KnowledgeState {
    listKnowledge: ListKnowledge[]
    searchPattern: OptSearchPattern  // 搜索测试 配置项
    searchFilter: OptSearchFilter  // 搜索过滤 配置项
    questionComplement: OptQuestionComplement // 问题补全 配置项
    listHistory: any
    docList: any[]
  }

  // 知识列表项接口
  interface ListKnowledge {
    cmetadata: {
      type: string
    },
    name: string
    user_id: string
    uuid: string
  }

  // 搜索模式接口
  interface OptSearchPattern {
    curSearchType: string
    resultResort: boolean
  }

  // 搜索过滤接口
  interface OptSearchFilter {
    referenceLimit: number | string
    minRelevancy: number | string
  }

  // 问题补全接口
  interface OptQuestionComplement {
    useQuestionComplement: boolean
    curAIModel: string
    desc: string
    opt: {
      AIList: AIList[]
    }
  }

  // AI模型列表项类型
  type AIList = {
    label: string
    value: string
  }

  // 单个历史记录类型
  type SingleHistory = {
    id: string
    content: string
    type: 'summary' | 'qa' | 'content'
  }

  // 搜索历史记录类型
  type ListHistory = {
    curHistory: string
    list: SingleHistory[]
  }
}

// 默认设置函数
export function defaultSetting(): IKnowledge.KnowledgeState {
  return {
    listKnowledge: [],
    searchPattern: {
      curSearchType: 'semantic',  // 当前搜索类型
      resultResort: false,  // 结果重排
    },
    searchFilter: {
      referenceLimit: 5000, // 引用上限
      minRelevancy: 0, // 最低相关度
    },
    questionComplement: {
      curAIModel: 'FastAI-4k',  // 当前AI模型
      useQuestionComplement: false, // 使用问题补全
      desc: '',
      opt: {
        AIList: [ // AI模型列表
          {
            label: "FastAI-4k",
            value: "FastAI-4k",
          },
          {
            label: "FastAI-16k",
            value: "FastAI-16k",
          },
        ]
      }
    },
    listHistory: {},
    docList: [],
  }
}

// 获取本地设置函数
export function getLocalSetting(): IKnowledge.KnowledgeState {
  const localSetting: IKnowledge.ListKnowledge | undefined = ss.get(LOCAL_NAME)
  return { ...defaultSetting(), ...localSetting }
}

// 设置本地设置函数
export function setLocalSetting(state: IKnowledge.KnowledgeState): void {
  ss.set(LOCAL_NAME, state)
}