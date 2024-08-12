import { VNode } from "vue"

declare namespace Knowledge {
    // type IMenuTree = {
    //     key?: string
    //     label: string
    //     children?: IMenuTree[]
    //     type?: string
    // }

    type IMenuTree = {
        icon?: string
        isfile: number
        key: number
        label: string
        parent_id?: number
        root_id?: number
        children?: IMenuTree[] | IFileMd[]
        type?: string
    }

    type IFileMd = {
        content: string
        id?: number
        name?: string
        status: string
        key?: number
        label?: string
    }

    interface IState {
        listMenu: IMenuTree[]
        curKnowledgeRange: string
    }
}