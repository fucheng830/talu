import { t } from "@/locales"
import { ss } from "@/utils/storage"

const LOCAL_NAME = 'navStorage'

export declare namespace INav {
    interface navList {
        label: string       // 按钮名称
        icon: string        // 按钮图标
        iconActive: string  // 按钮图标 激活状态
        path: string        // 路由
    }

    interface NavState {
        curActive: number   // 默认激活下标
        isNavcollapsed: boolean // 是否折叠左侧导航栏
        navList: navList[]  // 导航列表
    }
}

export function defaultNavSetting(): INav.NavState {
    return {
        curActive: 1,
        isNavcollapsed: true,
        navList: [
            {
                label: 'chat',
                icon: "mingcute:chat-1-line",
                iconActive: "mingcute:chat-1-fill",
                path: '/chat'
            },
            {
                label: 'square',
                icon: "ph:squares-four",
                iconActive: "ph:squares-four-fill",
                path: '/square'
            },
            {
                label: 'create',
                icon: "material-symbols:person-add-outline",
                iconActive: "material-symbols:person-add",
                path: '/createai'
            },
            {
                label: 'knowledge',
                icon: "mdi:folder-open-outline",
                iconActive: "mdi:folder-open",
                path: '/knowledge'
            },
            // {
            //     label: "应用",
            //     icon: "mage:robot-happy",
            //     iconActive: "mage:robot-happy-fill",
            //     path: '/application'
            // }
            // {
            //     label: "社区",
            //     icon: "f7:person-2",
            //     iconActive: "f7:person-2-fill",
            //     path: '/community'
            // },
            // {
            //     label: "广场",
            //     icon: "ph:squares-four",
            //     iconActive: "ph:squares-four-fill",
            //     path: '/square'
            // },

            // {
            //     label: "知识库",
            //     icon: "solar:notebook-broken",
            //     iconActive: "solar:notebook-bold",
            //     path: '/knowledge'
            // },
        ]
    }
}

export function getLocalSetting(): INav.NavState {
    const localSetting: INav.NavState | undefined = ss.get(LOCAL_NAME)
    return { ...defaultNavSetting(), ...localSetting }
}

export function setLocalSetting(setting: INav.NavState): void {
    ss.set(LOCAL_NAME, setting)
}