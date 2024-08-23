<template>
  <div class="bg-gray-200 text-gray-700 text-xs px-2 py-1 rounded-md">
    <n-dropdown
      trigger="click"
      :options="formattedOptions"
      :render-option="renderOption"
      @select="handleSelect"
      class="w-64"
    >
      <span class="select-none">{{ selectedOption ? selectedOption.label : 'Select an Option' }}</span>
    </n-dropdown>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, h} from 'vue';
import { NDropdown } from 'naive-ui';
import OpenAI from '/public/OpenAI.svg';
import { useChatStore } from "@/store";

const chatStore = useChatStore();

const currentAgent = computed(() => chatStore.currentAgent())

interface Option {
  label: string;
  key: string;
  maxToken: string;
  icon: string;
  group: string;
}

const options = ref<Option[]>([
  { label: 'GPT-4o Mini', key: 'gpt-4o-mini', maxToken: '128K', icon: OpenAI, group: 'OpenAI' },
  { label: 'GPT-4o', key: 'gpt-4o', maxToken: '256K', icon: OpenAI, group: 'OpenAI' },
  { label: 'GPT-4 Turbo', key: 'gpt-4-turbo', maxToken: '512K', icon: OpenAI, group: 'OpenAI' },
  { label: 'Claude 3.5 Sonnet', key: 'claude-3-5-sonnet', maxToken: '200K', icon: OpenAI, group: 'Claude' },
  { label: 'Claude 3 Opus', key: 'claude-3-opus', maxToken: '200K', icon: OpenAI, group: 'Claude' },
  { label: 'Claude 3 Haiku', key: 'claude-3-haiku', maxToken: '200K', icon: OpenAI, group: 'Claude' },
  { label: 'Gemini 1.5 Pro', key: 'gemini-1-5-pro', maxToken: '2M', icon: OpenAI, group: 'Gemini' },
  { label: 'Gemini 1.5 Flash', key: 'gemini-1-5-flash', maxToken: '1M', icon: OpenAI, group: 'Gemini' },
  { label: 'DeepSeek V2', key: 'deepseek-v2', maxToken: '128K', icon: OpenAI, group: 'DeepSeek' },
  { label: 'DeepSeek Coder V2', key: 'deepseek-coder-v2', maxToken: '128K', icon: OpenAI, group: 'DeepSeek' }
]);

const selectedOption = ref<Option | null>(options.value.find(option => option.key === currentAgent.value?.llm.model) || options.value[0]);


const formattedOptions = computed(() => {
  const formatted: any[] = [];
  let lastGroup = '';

  options.value.forEach((option) => {
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

  return formatted;
});

const renderOption = (props: { node: any, option: any }) => {
  if (props.option.type === 'group') {
    return h('div', { class: 'px-4 py-2 text-sm text-gray-500 font-semibold' }, props.option.label || '');
  }
  return h('div', {
    class: 'flex justify-between items-center px-4 py-2 cursor-pointer hover:bg-gray-300',
    onClick: () => handleSelect(props.option.key)
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
  selectedOption.value = options.value.find(option => option.key === key) || null;
  currentAgent.value.llm.model = key;
  chatStore.uploadLocalAgentSetting(currentAgent.value);
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

.hover:bg-gray-300:hover {
  background-color: #e5e7eb;
}
</style>