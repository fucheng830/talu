<template>
  <div class="bg-gray-200 text-gray-700 text-xs px-2 py-1 rounded-md">
    <n-dropdown
      trigger="click"
      :options="formattedOptions"
      :render-option="renderOption"
      @select="handleSelect"
      v-model:show="dropdownVisible"
      class="w-64"
      :style="{ maxHeight: '500px', overflowY: 'auto' }" 
    >
      <span class="select-none">{{ selectedOption ? selectedOption.label : 'Select an Option' }}</span>
    </n-dropdown>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, h } from 'vue';
import { NDropdown } from 'naive-ui';
import { useChatStore, useSettingStore } from "@/store";

const chatStore = useChatStore();
const settingStore = useSettingStore();

const currentAgent = computed(() => chatStore.currentAgent());
const llmConfig = computed(() => settingStore.llmConfig);

interface Option {
  label: string;
  key: string;
  maxToken: string;
  icon: string;
  group: string;
}

const selectedOption = ref<Option | null>(null);
const dropdownVisible = ref(false); // Add a reactive variable to control dropdown visibility

const formatMaxToken = (maxToken: number): string => {
  if (maxToken >= 1000) {
    return `${(maxToken / 1000).toFixed(0)}k`; // 转换为千
  }
  return maxToken.toString(); // 小于1000的直接返回
};

const formattedOptions = computed(() => {
  const formatted: any[] = [];
  let lastGroup = '';

  llmConfig.value.forEach((config) => {
    const option: Option = {
      label: config.model_name,
      key: config.model_name,
      maxToken: formatMaxToken(config.max_token),
      icon: config.icon_url || '/ChatGPT.jpg',
      group: config.model_provider
    };

    if (option.group !== lastGroup) {
      formatted.push({
        type: 'group',
        label: option.group,
        key: `${option.group}-group`
      });
      lastGroup = option.group;
    }

    formatted.push({
      label: option.label,
      key: option.key,
      icon: option.icon,
      maxToken: option.maxToken
    });
  });

  // 设置默认选项
  if (!selectedOption.value && formatted.length > 0) {
    selectedOption.value = formatted.find(option => option.key === currentAgent.value?.llm.model) || formatted[0];
  }

  return formatted;
});

const renderOption = (props: { node: any, option: any }) => {
  if (props.option.type === 'group') {
    return h('div', { class: 'px-4 py-2 text-sm text-gray-500 font-semibold' }, props.option.label || '');
  }
  return h('div', {
    class: 'flex justify-between items-center px-4 py-2 cursor-pointer hover:bg-gray-300',
    onClick: () => handleSelect(props.option.key) // Ensure this calls handleSelect
  }, [
    h('div', { class: 'flex items-center' }, [
      h('img', { src: props.option.icon, class: 'w-4 h-4 mr-2' }),
      h('span', props.option.label)
    ]),
    h('span', { class: 'text-gray-400' }, props.option.maxToken)
  ]);
};

const handleSelect = (key: string) => {
  console.log('Selected:', key);
  selectedOption.value = formattedOptions.value.find(option => option.key === key) || null;
  currentAgent.value.llm.model = key;
  chatStore.uploadLocalAgentSetting(currentAgent.value);

  dropdownVisible.value = false; // Close the dropdown after selecting an option
};
</script>

<style scoped>
.select-none {
  user-select: none;
}

.w-64 {
  width: 16rem;
}

.cursor-pointer {
  cursor: pointer;
}

.hover\:bg-gray-300:hover {
  background-color: #e5e7eb;
}

/* 限制下拉框的最大高度并添加滚动条 */
.n-dropdown {
  max-height: 200px; /* 根据需要调整高度 */
  overflow-y: auto; /* 允许垂直滚动 */
}
</style>
