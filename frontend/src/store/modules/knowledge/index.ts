import { defineStore } from 'pinia';
import { IKnowledge, getLocalSetting, setLocalSetting } from './helper';
import { api } from "@/api/common";
import { v4 as uuidv4 } from 'uuid';

export const useKnowledgeStore = defineStore('knowledge-store', {
  // 初始化状态，从本地存储中获取知识状态
  state: (): IKnowledge.KnowledgeState => getLocalSetting(),
  actions: {
    // 设置文档列表
    setDocs(docList: any[]) {
      this.$state.docList = docList;
    },

    // 检查并创建收藏夹
    async checkAndCreateFavorites() {
          try {
            // 假设收藏夹的类型为 'favorites'
            const favorites = this.$state.listKnowledge.find(item => item.cmetadata.type === 'favorites');
    
            if (!favorites) {
              // 创建一个新的收藏夹
              const newFavorites = {
                cmetadata: {
                  type: 'favorites'
                },
                name: '收藏夹', // 收藏夹名称
                uuid: uuidv4() // 替换为新的UUID
              };
    
              // 调用API添加收藏夹
              const res = await api.add_knowledge(newFavorites);
              if (res.status !== 'Success') throw res;
    
              // 更新本地状态
              this.$state.listKnowledge.push(res.data);
              this.recordState();
    
              console.log('Created new favorites', res.data);
            } else {
              console.log('Favorites already exists');
            }
          } catch (err) {
            console.error('Failed to check or create favorites', err);
          }
        },

    // 获取知识列表
    async getListKnowledge() {
      try {
        const res = await api.get_knowledges();
        if (res?.status !== 'Success') throw res;
        
        this.$state.listKnowledge = res.data;
        this.recordState();
      } catch (err) {
        console.error('Failed to fetch knowledge list', err);
      }
    },
    
    // 添加知识项
    async addKnowledge(knowledgeItem: any) {
      try {
        const res = await api.add_knowledge(knowledgeItem);
        if (res.status !== 'Success') throw res;

        if (!Array.isArray(this.$state.listKnowledge)) {
          this.$state.listKnowledge = [];
        }

        this.$state.listKnowledge.push(res.data);
        this.recordState();

        console.log('addKnowledge', res.data);
        return res.data.uuid;
      } catch (err) {
        console.error('Failed to add knowledge', err);
      }
    },

    // 设置知识列表
    setListKnowledge(list: IKnowledge.ListKnowledge[]) {
      this.$state.listKnowledge = [...this.$state.listKnowledge, ...list];
      this.recordState();
    },

    // 删除知识项
    async deleteKnowledge(params: { knowledge_id: string }) {
      try {
        const res = await api.delete_knowledge(params);
        if (res?.status !== 'Success') throw res;

        this.$state.listKnowledge = this.$state.listKnowledge.filter(
          item => item.uuid !== params.knowledge_id
        );
        this.recordState();
      } catch (err) {
        console.error('Failed to delete knowledge', err);
      }
    },

    // 设置搜索模式
    setSearchPattern(pattern: IKnowledge.OptSearchPattern) {
      this.$state.searchPattern = pattern;
    },

    // 设置搜索过滤
    setSearchFilter(filter: IKnowledge.OptSearchFilter) {
      this.$state.searchFilter = { ...this.$state.searchFilter, ...filter };
    },

    // 设置问题补全
    setQuestionComplement(curOpt: IKnowledge.OptQuestionComplement) {
      this.$state.questionComplement = { ...this.$state.questionComplement, ...curOpt };
    },

    // 设置搜索测试历史
    setSearchTestHistory(curHistoryID: string, oHistory: IKnowledge.SingleHistory) {
      if (!this.$state.listHistory[curHistoryID] || !this.$state.listHistory[curHistoryID].list) {
        this.$state.listHistory[curHistoryID] = {
          curHistory: curHistoryID,
          list: [],
        };
      }

      this.$state.listHistory[curHistoryID].curHistory = curHistoryID;
      this.$state.listHistory[curHistoryID].list.unshift(oHistory);
      this.recordState();
    },

    // 删除搜索测试单个历史
    deleteSearchTestSingleHistory(curHistoryID: string, oHistory: IKnowledge.SingleHistory) {
      this.$state.listHistory[curHistoryID].list = this.$state.listHistory[curHistoryID].list.filter(
        item => item !== oHistory
      );
      this.recordState();
    },

    // 记录状态到本地存储
    recordState() {
      setLocalSetting(this.$state);
    },
  },
});