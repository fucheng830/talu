import { defineStore } from 'pinia'
import { IKnowledge, getLocalSetting, setLocalSetting } from './helper'
// import { store } from '@/store'
import { api } from "@/api/common";

export const useKnowledgeStore = defineStore('knowledge-store', {
  state: (): IKnowledge.KnowledgeState => getLocalSetting(),
  actions: {
    // 获取 知识库列表
    setDocs(docList: any[]) {
      this.$state.docList = docList

    },
    getListKnowledge() {
      return new Promise<void>((resolve, reject) => {
        api.get_knowledges().then((res) => {
          if (res?.status != 'Success') reject(res)

          this.$state.listKnowledge = res.data

          this.recordState();
          resolve(res)
        }).catch((err) => {
          reject(err)
        })
      })
    },

    addKnowledge(knowledgeItem: any) {
      return new Promise<void>((resolve, reject) => {
        // 发送请求到 'add_knowledge' 端点
        api.add_knowledge(knowledgeItem).then((res) => {
          if (res.status !== 'Success') {
            // 如果响应状态不是 'Success'，则拒绝 Promise
            reject(res);
          } else {
            // 如果添加成功，则将新的知识项添加到 listKnowledge
            // 确保 listKnowledge 是一个数组
            if (!Array.isArray(this.$state.listKnowledge)) {
              this.$state.listKnowledge = [];
            }

            this.$state.listKnowledge.push(res.data);
            // 记录新状态到本地存储
            this.recordState();
            // 解决 Promise
            console.log('addKnowledge', res.data)
            resolve(res.data.uuid);
          }
        }).catch((err) => {
          // 如果请求失败，则拒绝 Promise
          reject(err);
        });
      });
    },

    // 保存 知识库列表
    setListKnowledge(list: IKnowledge.ListKnowledge[]) {
      this.$state.listKnowledge = { ...this.$state.listKnowledge, ...list }
      this.recordState();
    },

    // 删除知识库
    deleteKnowledge(params: { knowledge_id: string }) {
      return new Promise<void>((resolve, reject) => {
        api.delete_knowledge(params).then((res: any) => {
          if (res?.status != 'Success') reject(res)

          this.$state.listKnowledge = this.$state.listKnowledge.filter(item => item.uuid != params.knowledge_id)

          this.recordState();
          resolve(res)
        }).catch(err => {
          reject(err)
        })
      })
    },

    setSearchPattern(pattern: IKnowledge.OptSearchPattern) {
      this.$state.searchPattern = pattern
      // 不记录，一次性数据
      // this.recordState();
    },

    setSearchFilter(filter: IKnowledge.OptSearchFilter) {
      this.$state.searchFilter = { ...this.$state.searchFilter, ...filter }
      // this.recordState();
    },

    setQuestionComplement(curOpt: IKnowledge.OptQuestionComplement) {
      this.$state.questionComplement = { ...this.$state.questionComplement, ...curOpt }
      // this.recordState();
    },

    // 设置当前搜索历史
    setSearchTestHistory(curHistoryID: string, oHistory: IKnowledge.SingleHistory) {
      // 未检索过，则初始化
      if (!this.$state.listHistory[curHistoryID] || !this.$state.listHistory[curHistoryID].list) {
        this.$state.listHistory[curHistoryID] = {
          curHistory: curHistoryID,
          list: [],
        }
      }

      this.$state.listHistory[curHistoryID].curHistory = curHistoryID
      this.$state.listHistory[curHistoryID].list.unshift(oHistory)
      this.recordState();
    },

    // 删除单个搜索历史
    deleteSearchTestSingleHistory(curHistoryID: string, oHistory: IKnowledge.SingleHistory) {
      this.$state.listHistory[curHistoryID].list = this.$state.listHistory[curHistoryID].list.filter(
        (item: any) => item != oHistory
      )
      this.recordState();
    },

    // 记录状态
    recordState() {
      setLocalSetting(this.$state)
    },
  },
})

// export function useKnowledgeStoreWithOut() {
//   return useKnowledgeStore(store)
// }
