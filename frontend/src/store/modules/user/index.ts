import { defineStore } from 'pinia';
import { ss } from '@/utils/storage';

const LOCAL_NAME = 'userStorage';

export interface UserInfo {
  union_id: string | null; // 微信用户的union_id
  openid: string; // 微信用户的openid
  avatar: string | null; // 用户头像URL
  subscribe_scene: string | null; // 用户关注的场景信息
  phone_num: string | null; // 用户手机号码
  vip_end_time: string | null; // VIP结束时间
  register_time: string; // 用户注册时间
  email: string | null; // 用户邮箱地址
  ip: string | null; // 用户IP地址
  name: string; // 用户名
  user_id: string; // 用户唯一标识符
  session_key: string | null; // 微信会话密钥
  status: number; // 用户状态
  user_info: { // 用户的其他信息
    usable_token: number; // 用户可用的令牌数量
  };
  referee: string | null; // 推荐人信息
  access_token: string; // 用于API请求的访问令牌
}

export interface UserState {
  userInfo: UserInfo | null;
  currentAgentId: string | null;
  currentConvsationId: string | null;
  invitecode: string | null;
}

export function getLocalState(): UserState {
  return ss.get(LOCAL_NAME) || { userInfo: null };
}

export function setLocalState(setting: UserState): void {
  ss.set(LOCAL_NAME, setting);
}

export const useUserStore = defineStore('user-store', {
  state: getLocalState,
  actions: {
    getUserInfo() {
      return this.$state.userInfo;
    },

    isvip() {
      const vipEndTime = this.$state.userInfo?.vip_end_time;
      if (!vipEndTime) {
        return false; // 如果 `vip_end_time` 是空值，则用户不是 VIP
      }
      
      // 获取当前时间
      const currentTime = new Date();
      const vipEndDate = new Date(vipEndTime);
    
      // 判断当前时间是否在 VIP 结束时间之前
      return currentTime < vipEndDate;
    },

    getUsableToken() {
      return this.$state.userInfo?.user_info?.usable_token || 0;
    },

    updateUserInfo(userInfo: Partial<UserInfo>) {
      if (this.$state.userInfo) {
        Object.assign(this.$state.userInfo, userInfo);
        this.recordState();
      } else {
        this.$state.userInfo = userInfo as UserInfo;
        this.recordState();
      }
    },

    resetUserInfo() {
      this.$state.userInfo = null;
      this.recordState();
    },

    recordState() {
      setLocalState(this.$state);
    },

    removeToken() {
      if (this.$state.userInfo) {
        this.$state.userInfo.access_token = '';
        this.recordState();
      }
    },
  },
});