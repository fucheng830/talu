import { ss } from '@/utils/storage'

const LOCAL_NAME = 'knowledgeStorage'

export declare namespace IKnowledge {
  interface KnowledgeState {
    listKnowledge: ListKnowledge[]
    searchPattern: OptSearchPattern  // 搜索测试 配置项
    searchFilter: OptSearchFilter  // 搜索过滤 配置项
    questionComplement: OptQuestionComplement // 问题补全 配置项
    listHistory: any
    docList: any[]
  }

  interface ListKnowledge {
    cmetadata: {
      type: string
    },
    name: string
    user_id: string
    uuid: string
  }

  // 搜索模式
  interface OptSearchPattern {
    curSearchType: string
    resultResort: boolean
  }

  // 搜索过滤
  interface OptSearchFilter {
    referenceLimit: number | string
    minRelevancy: number | string
  }

  interface OptQuestionComplement {
    useQuestionComplement: boolean
    curAIModel: string
    desc: string
    opt: {
      AIList: AIList[]
    }
  }

  type AIList = {
    label: string
    value: string
  }

  // 搜索历史
  type ListHistory = {
    curHistory: string
    list: singleHistory[]
  }

  // 单个历史
  type SingleHistory = {
    id: string
    content: string
    type: 'summary' | 'qa' | 'content'
  }

}

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

export function getLocalSetting(): IKnowledge.KnowledgeState {
  const localSetting: IKnowledge.ListKnowledge | undefined = ss.get(LOCAL_NAME)
  return { ...defaultSetting(), ...localSetting }
}

export function setLocalSetting(state: IKnowledge.KnowledgeState): void {
  ss.set(LOCAL_NAME, state)
}
