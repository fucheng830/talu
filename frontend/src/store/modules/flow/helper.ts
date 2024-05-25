import { ss } from '@/utils/storage'

const LOCAL_NAME = 'flowStorage'

export declare namespace IFlow {
  interface FlowState {
    flowList: FlowList[], // flow列表
    curActive: String | undefined // 当前选中的节点
  }

  // flow列表
  interface FlowList {
    id: string
    label: string
    desc?: string
    icon?: string
    // data: Flow
  }

  interface Flow {
    nodes: any[],
    edges: any[],
  }
}

export function defaultSetting(): IFlow.FlowState {
  return {
    flowList: [
      {
        id: 'qwejkl',
        label: 'tmp',
        // data: {
        //   nodes: [
        //     {
        //       id: "0",
        //       type: "startGuide",
        //       position: { x: 0, y: -500 },
        //     },
        //     {
        //       id: "1",
        //       type: "LLM",
        //       position: { x: -300, y: 0 },
        //     },
        //     {
        //       id: "2",
        //       label: "Node2",
        //       type: "code",
        //       position: { x: 500, y: 0 },
        //     },
        //     {
        //       id: "3",
        //       label: "Node3",
        //       type: "knowledge",
        //       position: { x: 1100, y: 0 },
        //     },
        //     {
        //       id: "4",
        //       label: "Node4",
        //       type: "condition",
        //       position: { x: 1700, y: 0 },
        //     },
        //     {
        //       id: "5",
        //       type: "variable",
        //       position: { x: 0, y: 1000 },
        //     },
        //     {
        //       id: "6",
        //       type: "database",
        //       position: { x: 600, y: 1000 },
        //     },
        //     {
        //       id: "7",
        //       type: "message",
        //       position: { x: 1200, y: 1000 },
        //     },
        //     {
        //       id: "8",
        //       type: "endFlow",
        //       position: { x: 1800, y: 1000 },
        //     },
        //   ],
        //   edges: [],
        // }

      }
    ],
    curActive: '',
  }
}

export function getLocalSetting(): IFlow.FlowState {
  const localSetting: IFlow.FlowList | undefined = ss.get(LOCAL_NAME)
  return { ...defaultSetting(), ...localSetting }
}

export function setLocalSetting(state: IFlow.FlowState): void {
  ss.set(LOCAL_NAME, state)
}
