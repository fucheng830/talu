<template>
  <div class="w-full h-full flex flex-col overflow-y-auto">
    <div class="px-7 py-10 flex-grow">
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-xl font-semibold">
          {{ data.fileName }}
        </h1>
        <!-- Conditionally render the insert button if nodeType is 'datasetManual' -->
        <button 
          v-if="data.nodeType === 'datasetManual'"
          class="text-white bg-blue-500 hover:bg-blue-700 font-medium py-2 px-4 rounded"
          type="button"
          @click="handelShowInsertModal"
          >
          插入
        </button>


      </div>
      <div class="flex justify-between items-center mb-4">
        <div class="flex justify-between items-center">
          <div class="mr-2 text-gray-700 font-semibold">分段展示</div>
          <n-button 
            v-if="data.nodeType != 'datasetManual'"
            type="default"
            size="small"
            @click="handleRedoSegmentation"
          >
          重新切分
        </n-button>
        </div>


        <div class="relative">
          <n-input
            v-model:value="data.txtSearch"
            type="text"
            placeholder="搜索"
            :style="{ 'border-radius': globalConfig.btnRadius }"
          >
            <template #prefix>
              <Icon icon="iconamoon:search" width="18" style="color: #9ca3af;"/>
            </template>
          </n-input>
        </div>
      </div>
      <div class="grid grid-cols-2 gap-4">

          <!-- 为卡片设置固定高度并允许内部内容滚动 -->
          <div class="bg-white border border-gray-300 p-6 rounded flex flex-col" v-for="(item, index) in data.segmentData" :key="index">
          <!-- 内容区域 -->
          <div class="overflow-y-hidden flex-grow">
            <h2 class="text-lg font-semibold mb-4">
              # {{ index + 1 }}
            </h2>
            <p class="text-gray-700 mb-4" v-if="data.nodeType==='datasetManual'">
              <p>问题：{{ item.document }}</p>
              <p>答案: {{ item.cmetadata['answer'] }}</p>  
            </p>
            <p class="text-gray-700 mb-4" v-else>
              {{ item.document }}
            </p>
          </div>
          <!-- 固定在底部的字符计数 -->
          <div class="text-gray-500 mt-auto">
            <span>
              {{ item.document.length }} 字符
            </span>
          </div>
        </div>

      </div>
    </div>
  </div>
  <!-- 插入模态框 -->
<ModalDatasetAdd ref="refModalDatasetAdd" @update-list="fetchDatasetList" :knowledgeId=data.knowledgeId :nodeId=data.node_id />
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';
import { api } from '@/api/common';
import { Icon } from "@iconify/vue";
import { globalConfig } from "@/hooks/useTheme";
import ModalDatasetAdd from "./components/ModalInsertQa.vue";
import { useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const refModalDatasetAdd = ref();
const data = reactive({
  txtSearch: '',
  node_id: route.params.fileID,
  fileName: route.params.fileName,
  nodeType: route.params.nodeType,
  knowledgeId: route.params.id,
  segmentData: [],
  // ...其他响应式数据...
});

const fetchDatasetList = () => {
  api.preview_segment_data({ node_id: data.node_id }).then((res) => {
    data.segmentData = res;
  });
}

const handelShowInsertModal = () => {
  refModalDatasetAdd.value.changeModalShow();
}

const handleRedoSegmentation = () => {
  // 进入分段页面
  router.push({ name: 'KnowledgeDetails_dataset_split', params: { nodeId: data.node_id, id: data.knowledgeId } });
};

onMounted(() => {
  fetchDatasetList();
});
</script>

<style lang="less" scoped>
/* 如果需要添加或修改样式，可以在这里写入 */
</style>