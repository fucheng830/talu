import { defineStore } from 'pinia'
import type { SettingsState } from './helper'
import { defaultSetting, getLocalState, removeLocalState, setLocalState } from './helper'
import { api } from "@/api/common";

// 定义设置的 Pinia 存储
export const useSettingStore = defineStore('setting-store', {
  // 状态初始化，使用本地存储的设置
  state: (): SettingsState => getLocalState(),
  
  actions: {
    // 更新设置的方法，接收部分设置作为参数
    updateSetting(settings: Partial<SettingsState>) {
      // 合并当前状态和新的设置
      this.$state = { ...this.$state, ...settings }
      // 记录当前状态到本地存储
      this.recordState()
    },

    // 重置设置的方法
    resetSetting() {
      // 将状态重置为默认设置
      this.$state = defaultSetting()
      // 移除本地存储的设置
      removeLocalState()
    },

    // 记录当前状态的方法
    recordState() {
      // 将当前状态保存到本地存储
      setLocalState(this.$state)
    },
    
    // 新增异步方法，获取云端接口的 LLM 配置
    async fetchLLMConfig() {
      try {
        // 模拟请求云端接口，假设接口地址为 'https://api.example.com/llm-config'
        const response = api.llm();
        // 解析响应数据
        const llmConfig = await response;

        console.log(llmConfig)
        
        // 更新状态
        this.updateSetting({llmConfig: llmConfig});
      } catch (error) {
        console.error('获取 LLM 配置失败:', error);
      }
    },

    // 新增异步方法，获取云端tools配置
    async fetchToolsConfig() {
      try {
        // 模拟请求云端接口，假设接口地址为 'https://api.example.com/tools-config'
        const response = api.tools();
        // 解析响应数据
        const toolsConfig = await response;

        console.log(toolsConfig)
        
        // 更新状态
        this.updateSetting({toolsConfig: toolsConfig});
      } catch (error) {
        console.error('获取 tools 配置失败:', error);
      }
    },
  },
})
