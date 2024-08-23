<template>
  <m-modal
    ref="refModal"
    title="创建一个新的知识库"
    style="width: 700px; border-radius: 30px"
  >
    <div class="flex flex-col px-[16px] py-[32px]">
      <n-upload
        multiple
        directory-dnd
        action="https://www.mocky.io/v2/5e4bafc63100007100d8b70f"
        :max="5"
      >
        <n-upload-dragger style="border-radius: 20px">
          <!-- 图标 -->
          <div class="w-full flex justify-center">
            <Icon icon="pepicons-pencil:cloud-up" width="24" color="#666666" />
          </div>
          <!-- 中段 字样 -->
          <n-text class="flex justify-center">
            <span
              class="mt-[4px] text-sm text-[#666666] font-bold text-[14px] leading-[17px]"
            >
              拖拽文件至此 /
            </span>
            <span class="font-bold" :style="{ color: theme.primaryColor }">
              点击上传文件
            </span>
          </n-text>
          <!-- 底部字样 -->
          <n-p depth="3" style="margin-top: 0">
            <span
              class="text-placeholder text-center mt-[4px] text-[14px] leading-[17px] text-[#A9A9AA]"
            >
              支持pdf、docx、markdown、txt、html格式的文本，最大20MB
            </span>
          </n-p>
        </n-upload-dragger>
      </n-upload>

      <div class="flex flex-col mt-[24px]">
        <div class="flex width-full gap-[12px]">
          <!-- 分段方式 单选 -->
          <template v-for="item in data.arrSegmentType" :key="item.key">
            <div
              @click="changeSegmentType(item.key)"
              class="flex flex-col rounded-[8px] bg border hover:cursor-pointer h-[80px] hover:bg-white flex-1"
              :class="[
                `hover:border-[blue]`,
                data.segmentType === item.key
                  ? 'border-[blue] bg-white'
                  : 'bg-[#F5F5F5]',
              ]"
            >
              <div class="h-full flex items-center pl-[16px] pr-[16px]">
                <div class="rounded flex items-center mr-[16px]">
                  <!-- 图标 -->
                  <Icon :icon="item.icon" width="36" />
                </div>

                <!-- 分割线 -->
                <div class="w-0 h-[40px] border-r mr-[16px]"></div>

                <!-- 右侧字样 -->
                <div class="flex flex-col flex-1">
                  <div class="flex-col justify-center">
                    <!-- 标题 -->
                    <span
                      class="text text-primary w-full flex justify-between font-bold text-[14px] leading-[20px]"
                    >
                      {{ item.title }}

                      <!-- radio 单选 -->
                      <n-radio
                        :checked="data.segmentType === item.key"
                        :value="item.key"
                        name="segmentType"
                      />
                    </span>

                    <!-- 描述 -->
                    <span
                      class="text-[12px] leading-[17px] mt-[4px] text-[#999999]"
                    >
                      {{ item.desc }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </div>
      </div>

      <!-- 自定义分段 选项 -->
      <template v-if="data.segmentType === 'manual'">
        <n-form>
          <div
            class="flex border-base mt-[12px] border rounded-[8px] bg-white pt-[20px] px-[24px]"
            :style="{ border: `1px solid ${theme.primaryColor}` }"
          >
            <n-grid x-gap="12" :cols="2">
              <n-gi>
                <n-form-item label="分段标识符">
                  <!-- :validation-status="inputValidationStatus" -->
                  <n-input
                    v-model:value="data.form.segmentIdentifier"
                    type="text"
                    placeholder="请输入分段标识符"
                  />
                </n-form-item>
              </n-gi>

              <n-gi>
                <n-form-item label="分段最大长度（50-6000)">
                  <n-input
                    v-model:value="data.form.segmentMaxLength"
                    type="text"
                    placeholder="请输入分段最大长度"
                  />
                </n-form-item>
              </n-gi>

              <n-gi>
                <n-form-item label="文本预处理规则">
                  <n-checkbox v-model:checked="data.form.prehandle">
                    替换掉连续的空格、换行符、制表符
                  </n-checkbox>
                </n-form-item>
              </n-gi>

              <n-gi>
                <n-form-item label="">
                  <n-checkbox v-model:checked="data.form.deleteAll">
                    删除所有URL和电子邮件地址
                  </n-checkbox>
                </n-form-item>
              </n-gi>
            </n-grid>
          </div>
        </n-form>
      </template>
    </div>
  </m-modal>
</template>

<script setup lang="ts">
import mModal from "@/components/common/mModal/index.vue";
import { reactive, ref } from "vue";
import { Icon } from "@iconify/vue";

const refModal = ref();

const data = reactive({
  // 当前 分段方式
  segmentType: "auto",
  form: {
    segmentIdentifier: "\\n", // 分段标识符
    segmentMaxLength: "500", // 分段最大长度
    prehandle: true, // 文本预处理规则
    deleteAll: false, // 删除所有URL和电子邮件地址
  },
  // 分段方式
  arrSegmentType: [
    {
      key: "auto",
      title: "系统自动分段",
      desc: "分段规则将使用系统默认的分段规则",
      icon: "mdi:refresh-auto",
    },
    {
      key: "manual",
      title: "自定义分段",
      desc: "自定义文件的分段和清洗规则",
      icon: "tabler:circle-letter-m",
    },
  ],
});


// 改变分段选项
const changeSegmentType = (key) => {
  data.segmentType = key;
};

defineExpose({
  changeModalShow: () => refModal.value?.toggleModal(),
});
</script>

<style lang="less" scoped>
// 自定义分段(选项表单) > 标题行
:deep(.n-form-item-label__text) {
  font-weight: bold;
}
</style>
