import { ss } from '@/utils/storage'

// 定义本地存储的名称
const LOCAL_NAME = 'settingsStorage'

// 定义设置状态的接口
export interface SettingsState {
  systemMessage: string // 系统消息
  llmConfig?: any // LLM 配置
}

// 默认设置函数
export function defaultSetting(): SettingsState {
  // 获取当前日期，格式为 YYYY-MM-DD
  const currentDate = new Date().toISOString().split('T')[0]
  return {
    // 返回默认的系统消息，包含知识截止日期和当前日期
    systemMessage: `You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.\nKnowledge cutoff: 2021-09-01\nCurrent date: ${currentDate}`,
  }
}

// 获取本地状态的函数
export function getLocalState(): SettingsState {
  // 从本地存储中获取设置
  const localSetting: SettingsState | undefined = ss.get(LOCAL_NAME)
  // 合并默认设置和本地存储的设置
  return { ...defaultSetting(), ...localSetting }
}

// 设置本地状态的函数
export function setLocalState(setting: SettingsState): void {
  // 将设置保存到本地存储
  ss.set(LOCAL_NAME, setting)
}

// 移除本地状态的函数
export function removeLocalState() {
  // 从本地存储中移除设置
  ss.remove(LOCAL_NAME)
}
