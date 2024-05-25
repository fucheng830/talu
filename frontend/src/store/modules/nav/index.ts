import { defineStore } from "pinia";
import { INav, getLocalSetting } from "./helper";

export const useNavStore = defineStore('nav-store', {
    state: (): INav.NavState => getLocalSetting(),
    actions: {
        // 修改导航栏当前激活按钮
        setNavActive(navActive: number) {
            this.curActive = navActive
        },
        // 改变左侧导航栏折叠
        changeNavCollapsed() {
            this.isNavcollapsed = !this.isNavcollapsed
        }
    }
})