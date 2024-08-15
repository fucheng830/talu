import { defineStore } from "pinia";
import { Router } from "vue-router";
import { api } from "@/api/common";
import { ss } from "@/utils/storage"


const LOCAL_NAME = 'chatStorage'

export declare namespace IChat {
    interface message {
        dateTime: string
        content: string
        role: string
        error: boolean
        loading: boolean
        avatar: string
    }

    interface conversation { 
        id: string
        name: string
        messages: message[]
    }

    interface ChatState {
        curActive: string | null
        agentChatHistory: any
        agentList: any
    }
}


const defaultAgent = {
    "id":"1",
    "name": "ChatBot",
    "type": "chat",
    "description": "Chatting casually",
    "opening_question": [],
    "tools": [],
    "avatar": "https://site.123qiming.com/image/3f40de780cb29eb51519a0ce4c7f5d08.png",
    "system_prompt": "",
    "knowledge": [],
    "voice": null,
    "suggestion": {
            "is_enable": true,
            "custom_prompt": ""
            },
    "llm": {
        "model": "gpt-4o-mini",
        "temperature": 0.8,
    },
    "opening_text": null
}

export function defaultChatSetting(): IChat.ChatState {
    return {
        // 当前默认的agent
        curActive: '1',
        // 当前的agents列表
        agentList: [defaultAgent],
        // 当前的聊天记录
        agentChatHistory: []
    }
}

export function getLocalSetting(): IChat.ChatState {
    const localSetting: IChat.ChatState | undefined = ss.get(LOCAL_NAME)
    return { ...defaultChatSetting(), ...localSetting }
}

export function setLocalSetting(setting: IChat.ChatState): void {
    ss.set(LOCAL_NAME, setting)
}


export const useChatStore = defineStore('chat-store', {
    state: (): IChat.ChatState => getLocalSetting(),

    actions: {
        async setCurrentAgent(agentId: string) {
            if (agentId === null) {
                return
            }
            if (this.$state.curActive === agentId) {
                return
            }

            this.$state.curActive = agentId
            this.$state.agentChatHistory = []
            const exists = this.isAgentInList(agentId)
            if (!exists) {
                // 请求Agent信息
                const res = await api.agent({id: agentId})
                console.log('res', res)
                if (res) {
                    this.$state.agentList.push(res);
                }
            }

            setLocalSetting(this.$state)
        },

        getMessages() {
            return this.$state.agentChatHistory
        },

        addAgent(agent: any) {
            console.log('this.$state.add', this.$state.curActive)
            const exists = this.isAgentInList(agent.id)
            // 如果 agent 不存在，则添加到 agentList
            if (!exists) {
                // 请求Agent信息
                // agent = await 
                this.$state.agentList.push(agent);
                setLocalSetting(this.$state)
            }

        },

        getAgentList() {
            const agentList = this.$state.agentList
            if (agentList.length == 0) {
                // 请求Agent列表
                this.$state.agentList = [

                    ]
                setLocalSetting(this.$state)
            }
            return this.$state.agentList
        },

        deleteAgent(agentId: string) {
            // 从 agentList 中删除指定的 agent
            this.$state.agentList = this.$state.agentList.filter(agent => agent.id !== agentId)
            // 如果删除的是当前激活的 agent，则将 curActive 设置为 第一个 agent 的 id
            if (this.$state.curActive === agentId) {
                this.$state.curActive = this.$state.agentList.length > 0 ? this.$state.agentList[0].id : null
            }
            setLocalSetting(this.$state)
        },

        isAgentInList(agentId: string) {
            // 假设 agentList 是存储在状态中的代理列表
            // 并且每个 agent 对象都有一个唯一的 'id' 属性
            let exists = false;

            // 遍历 agentList 检查 agent 是否已存在
            for (const existingAgent of this.$state.agentList) {
                if (existingAgent.id === agentId) {
                exists = true;
                break; // 如果找到匹配的 agent，终止循环
                }
            }
            return exists
        },

        currentAgent() {
            const agent = this.$state.agentList.find(agent => agent.id == this.$state.curActive)
            return agent
        },


        gotoChat(router: Router) {
            if (this.curActive === null) {
                router.push(`/chat`)
            } else {
                router.push(`/chat/${this.curActive}`)
            }

        },
        // 置顶会话
        pinChat(curChat: { id: string; isPin: boolean }) {
            // 拿到当前会话的下标
            console.log('执行pinChat', curChat)
            const curIndex = this.$state.agentList.findIndex(item => item.id === curChat.id);
        
            if (curIndex === -1) {
                console.error('Chat not found');
                return;
            }
        
            // 已置顶则取消置顶
            if (curChat.isPin) {
                this.$state.agentList[curIndex].isPin = false;
                this.$state.agentList.sort((a, b) => {
                    // 将要取消置顶的会话移到其他已置顶的下面
                    if (a.isPin && !b.isPin) return -1;
                    if (!a.isPin && b.isPin) return 1;
                    return 0;
                });
            } else {
                // 拿到当前会话，并删除原会话列表中的当前会话
                const curTar = this.$state.agentList.splice(curIndex, 1)[0];
        
                // 改变置顶标记
                curTar.isPin = true;
        
                // 将当前会话放到列表最前面
                this.$state.agentList.unshift(curTar);
            }
        
            // 保存状态
            setLocalSetting(this.$state);
        },
        

        saveState() {
            setLocalSetting(this.$state)
        }
    }




})