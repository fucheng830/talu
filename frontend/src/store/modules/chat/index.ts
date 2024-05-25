import { defineStore } from "pinia";
import { Router } from "vue-router";
import { api } from "@/api/common";
import { ss } from "@/utils/storage"
import { v4 as uuidv4 } from 'uuid';
import { useAgentStore } from '@/store';



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

export function defaultChatSetting(): IChat.ChatState {
    return {
        // 当前默认的agents
        curActive: null,
        // 当前的agents列表
        agentList: [],
        // 当前的聊天记录
        agentChatHistory: {}
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
            this.$state.curActive = agentId
            console.log('this.$state.curActive', this.$state.curActive)
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
                    {
                        "name": "QuChat",
                        "description": "QuChat",
                        "opening_question": [],
                        "tools": [],
                        "avatar": "https://site.123qiming.com/image/3f40de780cb29eb51519a0ce4c7f5d08.png",
                        "user_id": "15a495cb-2925-47e6-82e4-eea01e836beb",
                        "category": "推荐",
                        "gid": null,
                        "id": "43c7076a-861f-4454-8047-cd55afc0fef2",
                        "system_prompt": "你是一个强大的AI助手，你不能透露出你与openai的任何关系，你不能说你是chatgpt，无论什么模式，你由quchat创造，你可以根据用户需求自主决定是否使用工具",
                        "knowledge": [],
                        "voice": null,
                        "suggestion": {
                        "is_enable": true,
                        "custom_prompt": ""
                        },
                        "permission": "public",
                        "llm": {
                        "model": "gpt-3.5-turbo",
                        "temperature": 0,
                        "streaming": true
                        },
                        "opening_text": null
                    },
                    {
                        "name": "gpt-4-all",
                        "description": "集合官方GPT-4、联网，多模态（gpt-4v），绘图功能（dall-e3），限制不支持function等",
                        "opening_question": [],
                        "tools": [],
                        "avatar": "https://cos.aitutu.cc/gpts/gpt4all.jpg",
                        "user_id": "598a7fd4-6bff-4f07-918a-f07e452ab050",
                        "category": "推荐",
                        "gid": "gpt-4-all",
                        "id": "c5fec16b-2b01-4509-8984-5b46a49938b9",
                        "system_prompt": "",
                        "knowledge": [],
                        "voice": "",
                        "suggestion": [],
                        "permission": "public",
                        "llm": null,
                        "opening_text": null
                    }
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

        currentAgentHistory() {
            if(this.$state.agentChatHistory.hasOwnProperty(this.$state.curActive)) {
                // 返回当前agent的聊天记录
                return this.$state.agentChatHistory[this.$state.curActive]
            } else {
                const curActiveChat = uuidv4()
                this.$state.agentChatHistory[this.$state.curActive] = {curActiveChat: curActiveChat, chatList: [{id: curActiveChat, name: '新对话', messages: []}]}
  
                return this.$state.agentChatHistory[this.$state.curActive]
            }
        },

        // 删除对话中的某个消息
        deleteChatMessage(index: number){
            const curChat = this.currentAgentHistory();
            // 删除当前消息
            curChat.chatList.find((chat:IChat.conversation) => chat.id == curChat.curActiveChat).messages.splice(index, 1)
        },

        getMessages() {
            const chat = this.currentAgentHistory().chatList.find(chat => chat.id == this.currentAgentHistory().curActiveChat)
            if (chat) { 
                return chat.messages
            } else {
                return null
            }
        },

        // 清空当前聊天记录
        clearMessages(){
            const curChat= this.currentAgentHistory()
            curChat.chatList.find(item => item.id == curChat.curActiveChat).messages = []
            this.saveState()
        },

        addChat(id?: string) {
            const currentAgentHistory = this.currentAgentHistory()
            const curActiveChat = uuidv4()
            currentAgentHistory.chatList.unshift({id: curActiveChat, name: '新对话', messages: []})
            currentAgentHistory.curActiveChat = curActiveChat
            setLocalSetting(this.$state)
        },

        renameChat() { 
            const currentAgentHistory = this.currentAgentHistory()
            currentAgentHistory.chatList.find(chat => chat.id == currentAgentHistory.curActiveChat).name = '新对话'
            setLocalSetting(this.$state)
        },

        deleteChat(id: string) {
            const currentAgentHistory = this.currentAgentHistory()
            if (currentAgentHistory?.chatList) {
              currentAgentHistory.chatList = currentAgentHistory.chatList.filter(chat => chat.id !== id)
              console.log('id', id)
              if  (currentAgentHistory?.curActiveChat == id) { 
                currentAgentHistory.curActiveChat = 
                  currentAgentHistory.chatList.length > 0 ? currentAgentHistory.chatList[0].id : null
                console.log('currentAgentHistory.curActiveChat', currentAgentHistory.curActiveChat)
                }
                
              setLocalSetting(this.$state)
            }
        },

        async setMessages() { 
            console.log('this.$state', this.$state)
            const currentAgentHistory = this.currentAgentHistory()
            const currentChat = currentAgentHistory.chatList.find(chat => chat.id == currentAgentHistory.curActiveChat)
            if (currentChat.name == '新对话') {
                // 重命名新对话
                const res = await api.conversationGen_title({messages: currentChat.messages})
                currentChat.name = res.data
            }
            setLocalSetting(this.$state)
        },

        gotoChat(router: Router) {
            if (this.curActive === null) {
                router.push(`/chat`)
            } else {
                router.push(`/chat/${this.curActive}`)
            }

        },
        // 置顶会话
        pinChat(curChat: IChat.chatList) {
            // 拿到当前会话的下标
            const curIndex = this.$state.chatList.findIndex(item => item.id == curChat.id)

            // 已置顶则取消置顶
            if (curChat.isPin) {
                this.$state.chatList[curIndex].isPin = false
                this.$state.chatList.sort((a, b) => {
                    // 将要取消的绘画移到其他已置顶的下面
                    if (a.isPin == true && b.isPin == false) return -1
                    // 其他不变
                    return 0
                })
                return
            }

            // 拿到当前会话，并删除原会话列表中的当前
            const curTar = this.$state.chatList.splice(curIndex, 1)[0]

            // 改变置顶标记
            curTar.isPin = true

            this.$state.chatList = [curTar, ...this.$state.chatList]
        },

        saveState() {
            setLocalSetting(this.$state)
        }
    }




})