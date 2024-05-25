<template>
  <div class="flex h-full w-full relative bg-white">
    <div
      class="relative flex-col flex w-full create-bot-module"
      :class="[isMobile ? 'flex-1' : 'max-w-[640px]']"
    >
      <!-- 顶部栏 -->
      <header
        class="text-[18px] flex items-center border-b justify-between relative h-[64px] mx-[16px]"
      >
        <!-- pc端 -->
        <div v-if="!isMobile" class="flex items-center font-bold">
          <!-- 返回按钮 -->
          <div
            @click="goBack"
            class="font-normal w-[24px] h-[24px] bg-[rgba(0,0,0,0.03)] rounded-full mr-[16px] flex justify-center items-center cursor-pointer"
          >
            <Icon icon="iconamoon:arrow-left-2-light" width="22" />
          </div>
          <span>创建对话型角色</span>
        </div>
        <!-- 移动端 -->
        <template v-else>
          <!-- 弹出侧边栏按钮 -->
          <Icon
            v-if="isMobile"
            icon="oi:collapse-left"
            width="18"
            class="rotate-180"
            @click="changeNavCollapsed"
          />
          <span class="font-bold">创建对话型角色</span>
          <Icon
            v-if="isMobile"
            icon="tabler:eye-cog"
            width="24"
            @click="changeCollapsedRight"
          />
        </template>
      </header>

      <!-- 参数配置区 -->
      <div class="wrapper overflow-y-scroll pb-[80px] flex-1">
        <div
          class="relative bg-[#F9F9FA] rounded-lg mb-[24px] mx-[16px] mt-[16px] p-[20px]"
        >
          <h3 class="font-bold text-[16px] flex items-center relative">
            <i class="w-[6px] h-[18px] rounded-[3px] mr-[12px]" :class="[`bg-[${globalColors.btnActive}]`]">
            </i>
            <span> 角色设定 </span>
          </h3>

          <!-- 头像、名称栏 -->
          <div class="py-[20px] flex items-center">
            <div
              class="relative cursor-pointer flex-center mr-[20px] w-[48px] h-[48px] bg-[rgba(0,0,0,0.15)] text-white rounded-full flex-shrink-0"
            >
              <n-avatar
                round
                :size="48"
                src="https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg"
              />
              <!-- 编辑按钮 -->
              <div
                class="absolute w-[20px] h-[20px] rounded-full bg-white right-[-2px] bottom-[-2px] flex justify-center items-center"
              >
                <Icon icon="clarity:edit-line" width="12" color="black" />
              </div>
            </div>
            <n-input
              v-model:value="data.roleName"
              placeholder="如翻译助理、健身教练等"
              show-count
              :maxlength="12"
            />
          </div>

          <!-- 角色设定Prompt -->
          <div class="flex justify-between items-center mb-[10px]">
            <h5 class="text-[14px] font-bold">角色设定Prompt：</h5>
            <!-- AI一键生成 -->
            <round-button @emit="handleGeneratePrompt" />
          </div>

          <n-input
            v-model:value="data.prompt"
            type="textarea"
            :autosize="{
              minRows: 7,
              maxRows: 10,
            }"
            show-count
            :maxlength="2000"
            :placeholder="`请输入角色设定的Prompt，参考格式如下：
角色：小红书文案助手
能力：能根据我提供的产品信息撰写小红书风格的种草文案
说话风格：幽默、可爱、亲和，喜欢用emoji表情，与用户产生共鸣
回答身份：始终以小红书文案助手的身份回答我的任何问题。`"
            class="outline-none border-0"
          />
        </div>

        <!-- 详细设置(模型设置，表单设置，知识库) -->
        <div class="bg-[#F9F9FA] rounded-[8px] overflow-hidden mx-[16px]">
          <div class="text-xs py-2 px-[20px] text-[grey]">
            专业版功能，
            <span class="text-[blue] underline cursor-pointer"> 开通会员 </span>
          </div>
          <!-- tabs -->
          <n-tabs
            type="line"
            :tabs-padding="20"
            pane-class="bg-[#f9f9fa]"
            class="bg-[#f1f1f4]"
          >
            <!-- 面板 模型设置 -->
            <n-tab-pane name="modelSetting" tab="模型设置">
              <div class="text-[14px] pb-[20px] px-[20px]">
                <div class="flex items-center pb-[8px] font-bold mt-[10px]">
                  <span>联想能力： </span>
                  <!-- 问号 提示 tip -->
                  <icon-tip />
                </div>

                <!-- 滑动条 -->
                <div class="mx-2">
                  <n-slider
                    v-model:value="data.associativeAbility"
                    :marks="data.option.associativeAbility"
                    step="mark"
                  />
                </div>

                <!-- 对话模式 -->
                <div class="pt-[18px] pb-[8px] font-bold">对话模式：</div>
                <div
                  class="w-[244px] relative font-bold flex rounded-[20px] bg-[#F1F1F4] h-[32px] overflow-hidden cursor-pointer"
                >
                  <template
                    v-for="item in data.option.chatPattern"
                    :key="item.value"
                  >
                    <div
                      @click="handleChatPatternChange(item)"
                      class="flex-1 flex justify-center items-center"
                      :class="[
                        data.chatPattern === item.value
                          ? 'text-black bg-white font-bold'
                          : 'text-[#84818F] font-normal',
                      ]"
                    >
                      {{ item.label }}
                    </div>
                  </template>
                </div>
              </div>
            </n-tab-pane>

            <!-- 面板 表单设置 -->
            <n-tab-pane name="formSetting" tab="表单设置">
              <div class="text-[14px] pb-[20px] px-[20px]">
                <div class="flex flex-col">
                  <div class="flex items-center pb-[8px] font-bold">
                    <span> 用户消息上下文编辑： </span>
                    <icon-tip msg="自动拼接到用户消息的上方与下方一同发送。" />
                  </div>
                  <div
                    class="rounded-[16px] bg-[#F1F1F4] p-[12px] flex flex-col"
                  >
                    <!-- 用户消息上文 -->
                    <n-input
                      v-model:value="data.userChatBefore"
                      type="textarea"
                      :autosize="{
                        minRows: 3,
                        maxRows: 5,
                      }"
                      placeholder="请输入用户消息上文"
                      show-count
                      :maxlength="150"
                    />

                    <!-- 用户消息 展示 -->
                    <span
                      class="my-[12px] text-[14px] leading-[20px] text-theme"
                    >
                      <span
                        :style="{
                          color: globalColors.btnActive,
                        }"
                      >
                        {{ data.userChat }}
                      </span>
                    </span>

                    <!-- 用户消息下文 -->
                    <n-input
                      v-model:value="data.userChatAfter"
                      type="textarea"
                      :autosize="{
                        minRows: 3,
                        maxRows: 5,
                      }"
                      placeholder="请输入用户消息下文"
                      show-count
                      :maxlength="150"
                    />
                  </div>
                </div>
              </div>
            </n-tab-pane>

            <!-- 面板 知识库 -->
            <n-tab-pane name="knowledge" tab="知识库">
              <div class="pb-[20px] pt-[16px] px-[20px]">
                <div class="mb-3 collection-bind-prompt">
                  <div class="mb-2 text-xs">
                    <span
                      class="text-primary font-bold text-[14px] leading-[17px]"
                    >
                      知识库使用指引Prompt：
                    </span>
                  </div>
                  <!-- 用户消息下文 -->
                  <n-input
                    v-model:value="data.userChatAfter"
                    type="textarea"
                    :autosize="{
                      minRows: 3,
                      maxRows: 5,
                    }"
                    placeholder="如果为空将使用默认的知识库使用指引Prompt"
                    show-count
                    :maxlength="1000"
                  />

                  <div class="w-full overflow-hidden mt-[24px]">
                    <div
                      class="flex flex-col collection-cover justify-center hover:shadow-md rounded"
                    >
                      <div class="flex font-bold gap-[24px]">
                        <n-button
                          color="#FFF"
                          size="large"
                          tag="div"
                          class="flex-1"
                          @click="changeUploadShow"
                        >
                          <span
                            class="flex items-center gap-1 text-[14px] font-normal text-[black]"
                            :class="[`hover:text-[${globalColors.btnActive}]`]"
                          >
                            <Icon icon="pepicons-pencil:cloud-up" width="24" />
                            从本地上传
                          </span>
                        </n-button>

                        <n-button
                          color="#FFF"
                          size="large"
                          tag="div"
                          class="flex-1"
                        >
                          <span
                            class="flex items-center gap-1 text-[14px] font-normal text-[black]"
                            :class="[`hover:text-[${globalColors.btnActive}]`]"
                          >
                            <Icon icon="ion:folder-outline" width="24" />
                            选择已有知识库
                          </span>
                        </n-button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </n-tab-pane>
          </n-tabs>
        </div>

        <!-- 角色资料 -->
        <div class="bg-[#F9F9FA] rounded-lg p-[20px] my-[24px] mx-[16px]">
          <h3
            class="font-bold text-[16px] flex items-center relative mb-[18px]"
          >
            <i class="w-[6px] h-[18px] rounded-[3px] mr-[12px]" :class="[`bg-[${globalColors.btnActive}]`]">
            </i>
            角色资料
          </h3>

          <!-- 角色简介 -->
          <div class="flex justify-between items-center mb-[6px]">
            <h5 class="text-[14px] font-bold">角色简介：</h5>
            <!-- AI一键生成 -->
            <round-button @emit="handleGenerateRoleDesc" />
          </div>
          <n-input
            placeholder="一句话介绍下你的角色"
            show-count
            :maxlength="18"
          />

          <!-- 对话开场白 -->
          <div class="mt-[24px] flex justify-between items-center mb-[6px]">
            <h5 class="text-[14px] font-bold">对话开场白：</h5>
            <!-- AI一键生成 -->
            <round-button @emit="handleGeneratePrologue" />
          </div>
          <n-input
            v-model:value="data.chatPrologue"
            type="textarea"
            :autosize="{
              minRows: 5,
              maxRows: 7,
            }"
            placeholder="这里输入对话开始时你的角色会说出的开场白。如需要给用户提供提问示例，请使用双#号包含，如：#提问示例#"
            show-count
            :maxlength="2048"
          />

          <!-- 表单底部 开关 -->
          <div
            class="mt-[24px] flex text-[14px] font-bold flex-row-reverse gap-x-8"
          >
            <div class="flex items-center gap-x-2">
              <span> 设置为公开角色 </span>
              <n-switch v-model:value="data.openRole" />
            </div>
            <div v-show="data.openRole" class="flex items-center gap-x-2">
              <span> 角色设定Prompt公开可见 </span>
              <n-switch v-model:value="data.openPrompt" />
            </div>
          </div>
        </div>
      </div>

      <footer
        class="absolute left-0 bottom-0 h-[64px] w-full py-[13px] flex items-center px-[12px] bg-white border-t z-30 justify-end"
      >
        <div class="flex overflow-hidden rounded-lg">
          <n-button size="large" tertiary color="grey" @click="handelCrate">
            <span class="w-[140px] text-[grey] text-[14px]"> 完成创建 </span>
          </n-button>
        </div>
      </footer>
    </div>

    <!-- 右侧预览 -->
    <preview
      ref="refPreview"
      :isCollapsedRight="data.isCollapsedRight"
      :roleName="data.roleName"
      :chatPrologue="data.chatPrologue"
    />

    <!-- 上传模态框 -->
    <upload ref="refModalUpload" />
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from "vue";
import { Icon } from "@iconify/vue";
import { useRouter } from "vue-router";
import { globalColors } from "@/hooks/useTheme";
import RoundButton from "@/components/common/RoundButton/index.vue";
import IconTip from "@/components/common/IconTip/index.vue";
import Preview from "@/views/createai/components/Preview.vue";
import Upload from "@/views/knowledge/components/Upload.vue";
import { useBasicLayout } from "@/hooks/useBasicLayout";
import { useNavStore } from "@/store";

const { isMobile } = useBasicLayout();
const router = useRouter();
const navStore = useNavStore();

const refPreview = ref(); // 预览页
const refModalUpload = ref(); // 上传模态框
const data = reactive({
  roleName: "", // 角色名
  prompt: "", // 角色设定Prompt
  //   表单设置
  associativeAbility: 50, // 联想能力
  chatPattern: "auto", // 对话模式
  //   表单设置
  userChatBefore: "", // 用户消息上文
  userChat: "{{用户消息}}", // 用户消息
  userChatAfter: "", // 用户消息下文
  //   角色资料
  roleDesc: "", // 角色简介
  chatPrologue: "", // 对话开场白
  openRole: false, // 设置为公开角色
  openPrompt: false, // 角色设定Prompt公开可见

  isCollapsedRight: false, // 是否隐藏右侧预览
  option: {
    // 联想能力
    associativeAbility: {
      0: "最精确",
      25: "较精确",
      50: "平衡",
      75: "强创造力",
      100: "天马行空",
    },
    // 对话模式
    chatPattern: [
      {
        label: "连续对话",
        value: "auto",
      },
      {
        label: "单次回合",
        value: "single",
      },
    ],
  },
});

// 改变左侧导航栏折叠
const changeNavCollapsed = () => {
  navStore.changeNavCollapsed();
};

const goBack = () => {
  router.go(-1);
};

// 生成 角色设定Prompt
const handleGeneratePrompt = () => {
  data.prompt = "自动生成";
};

// 改变对话模式
const handleChatPatternChange = (cur) => {
  data.chatPattern = cur.value;
};

// 生成 角色简介
const handleGenerateRoleDesc = () => {
  data.roleDesc = "自动生成";
};

// 生成 对话开场白
const handleGeneratePrologue = () => {
  data.chatPrologue = "自动生成";
};

// 切换 上传模态框 显示
const changeUploadShow = () => {
  refModalUpload.value.changeModalShow();
};

// 切换右侧预览页折叠状态
const changeCollapsedRight = () => {
  refPreview.value.changeCollapsedRight();
};

// 完成创建
const handelCrate = () => {};
</script>

<style></style>
