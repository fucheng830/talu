import type { App } from 'vue'
import type { RouteRecordRaw } from 'vue-router'
import { createRouter, createWebHashHistory } from 'vue-router'

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        name: 'Root',
        component: () => import('@/views/layout/index.vue'),
        redirect: '/square',
        children: [

            {
                path: '/chat/:id?',
                name: 'Chat',
                component: () => import('@/views/chat/index.vue'),
            },
            {
                path: '/agent',
                name: 'Agent',
                component: () => import('@/views/agent/index.vue'),
            },
            {
                path: '/data',
                name: 'Data',
                component: () => import('@/views/data/index.vue'),
            },
            {
                path: '/community',
                name: 'Community',
                component: () => import('@/views/community/index.vue'),
            },
            {
                path: '/square',
                name: 'Square',
                component: () => import('@/views/square/index.vue'),
            },
            {
                path: '/createai',
                name: 'Createai',
                component: () => import('@/views/createai/index.vue'),
            },
            {
                path: '/createai/createrole/:id?',
                name: 'CreateRole',
                component: () => import('@/views/createai/createRole.vue'),
            },
            {
                path: '/createai/application',
                name: 'Application',
                component: () => import('@/views/application/index.vue'),
            },
            {
                path: '/createai/application/details/:id?',
                name: 'ApplicationDetails',
                component: () => import('@/views/application/details/index.vue'),
                children: [
                    {
                        path: '/application/simpleConfig/:id?',
                        name: 'ApplicationDetails_simpleConfig',
                        component: () => import('@/views/application/details/simpleConfig.vue'),
                    },
                    {
                        path: '/application/publishApp/:id?',
                        name: 'ApplicationDetails_publishApp',
                        component: () => import('@/views/application/details/publishApp.vue'),
                    },
                    {
                        path: '/application/chatHistory/:id?',
                        name: 'ApplicationDetails_chatHistory',
                        component: () => import('@/views/application/details/chatHistory.vue'),
                    },
                ]
            },
            {
                path: '/createai/application/advancedFlow/:id?',
                name: 'ApplicationDetails_advancedFlow',
                component: () => import('@/views/application/details/advancedFlow.vue'),
            },
            {
                path: '/knowledge',
                name: 'Knowledge',
                component: () => import('@/views/knowledge/index.vue'),
            },
            {
                path: '/knowledgeDetails?',
                name: 'KnowledgeDetails',
                component: () => import('@/views/knowledge/details/index.vue'),
                children: [
                    {
                        path: '/knowledgeDetails/dataset/:id?',
                        name: 'KnowledgeDetails_dataset',
                        component: () => import('@/views/knowledge/details/dataset.vue'),
                        // 数据集列表页
                    },
                    {
                        path: '/knowledgeDetails/dataset/details/:id?/:fileID?/:nodeType/:fileName?',
                        name: 'KnowledgeDetails_dataset_details',
                        component: () => import('@/views/knowledge/details/datasetDetails.vue'),
                        // 数据集详情页
                    },
                    {
                        path: '/knowledgeDetails/datasetUpload/:id?/:type?',
                        name: 'KnowledgeDetails_dataset_upload',
                        component: () => import('@/views/knowledge/details/datasetUpload.vue'),
                        // 数据集上传页
                    },
                    {
                        path: '/knowledgeDetails/datasetSplit/:id?/:nodeId?',
                        name: 'KnowledgeDetails_dataset_split',
                        component: () => import('@/views/knowledge/details/datasetSplit.vue'),
                        // 数据集拆分页
                    },
                    {
                        path: '/knowledgeDetails/searchTest/:id?',
                        name: 'KnowledgeDetails_searchTest',
                        component: () => import('@/views/knowledge/details/searchTest.vue'),
                    },
                    {
                        path: '/knowledgeDetails/setting/:id?',
                        name: 'KnowledgeDetails_setting',
                        component: () => import('@/views/knowledge/details/setting.vue'),
                    },
                ]
            },
            {
                path: '/vippay',
                name: 'VipPay',
                component: () => import('@/views/vipPay/index.vue'),
            },
            {
                path: '/dashboard/uploadImage',
                name: 'uploadImage',
                component: () => import('@/views/dashboard/uploadImage/index.vue'),
            },
        ],
    },
    {
        path: '/login/:referee?',
        name: 'Login',
        component: () => import('@/views/login/index.vue'),
    },
    {
        path: '/wechatCheck',
        name: 'wechatCheck',
        component: () => import('@/views/login/wechatCheck.vue'),
    },
    {
        path: '/500',
        name: '500',
        component: () => import('@/views/exception/500/index.vue'),
    },
    {
        path: '/404',
        name: '404',
        component: () => import('@/views/exception/404/index.vue'),
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'notFound',
        redirect: '/404',
    },
]

export const router = createRouter({
    history: createWebHashHistory(),
    routes,
    scrollBehavior: () => ({ left: 0, top: 0 }),
})

// setupPageGuard(router)

export async function setupRouter(app: App) {
    app.use(router)
    await router.isReady()
}
