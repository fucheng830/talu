import { VNode } from "vue";

declare namespace Knowledge {
    type IMenuTree = {
        icon?: string;
        isfile: number;
        key: number;
        label: string;
        parent_id?: number;
        root_id?: number;
        children?: IMenuTree[] | IFileMd[];
        type?: string;
    };

    type IFileMd = {
        content: string;
        id?: number;
        name?: string;
        status: string;
        key?: number;
        label?: string;
    };

    interface IState {
        listMenu: IMenuTree[];
        curKnowledgeRange: string;
    }

    interface KnowledgeState {
        listKnowledge: ListKnowledge[];
        searchPattern: OptSearchPattern; // 搜索测试 配置项
        searchFilter: OptSearchFilter; // 搜索过滤 配置项
        questionComplement: OptQuestionComplement; // 问题补全 配置项
        listHistory: any;
        docList: any[];
    }

    interface ListKnowledge {
        cmetadata: {
            type: string;
        };
        name: string;
        user_id: string;
        uuid: string;
    }

    interface OptSearchPattern {
        curSearchType: string;
        resultResort: boolean;
    }

    interface OptSearchFilter {
        referenceLimit: number | string;
        minRelevancy: number | string;
    }

    interface OptQuestionComplement {
        useQuestionComplement: boolean;
        curAIModel: string;
        desc: string;
        opt: {
            AIList: AIList[];
        };
    }

    type AIList = {
        label: string;
        value: string;
    };

    type ListHistory = {
        curHistory: string;
        list: SingleHistory[];
    };

    type SingleHistory = {
        id: string;
        content: string;
        type: 'summary' | 'qa' | 'content';
    };
}