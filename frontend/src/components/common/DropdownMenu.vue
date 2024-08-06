<template>
    <div class="bg-gray-200 text-gray-700 text-xs px-2 py-1 rounded-[5px]">
      <n-dropdown trigger="click" :options="formattedOptions" @select="handleSelect">
        <span class="no-copy">{{ selectedOption ? selectedOption.label : 'Select an Option' }}</span>
      </n-dropdown>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, computed, h } from 'vue'
  import { NDropdown, NButton } from 'naive-ui'
  import { Baichuan } from '@lobehub/icons';
  
  interface Option {
    label: string;
    key: string;
    value: string;
    icon: any;
  }
  
  const options = ref<Option[]>([
    { label: 'GPT-40 mini', key: 'gpt-40-mini', value: '128K', icon: Baichuan.Avatar },
    { label: 'GPT-40', key: 'gpt-40', value: '128K', icon: '/vite.svg' },
    { label: 'GPT-4 Turbo', key: 'gpt-4-turbo', value: '128K', icon: '/vite.svg' },
    { label: 'Claude 3.5 Sonnet', key: 'claude-3-5-sonnet', value: '200K', icon: '/vite.svg' },
    { label: 'Claude 3 Opus', key: 'claude-3-opus', value: '200K', icon: '/vite.svg' },
    { label: 'Claude 3 Haiku', key: 'claude-3-haiku', value: '200K', icon: '/vite.svg' },
    { label: 'Gemini 1.5 Pro', key: 'gemini-1-5-pro', value: '2M', icon: '/vite.svg' },
    { label: 'Gemini 1.5 Flash', key: 'gemini-1-5-flash', value: '1M', icon: '/vite.svg' },
    { label: 'DeepSeek-V2', key: 'deepseek-v2', value: '128K', icon: '/vite.svg' },
    { label: 'DeepSeek-Coder-V2', key: 'deepseek-coder-v2', value: '128K', icon: '/vite.svg' }
  ])
  
  const selectedOption = ref<Option | null>(options.value[0])
  
  const formattedOptions = computed(() =>
    options.value.map(option => ({
      label: () => h('div', { class: 'dropdown-option' }, [
        h('div', { class: 'flex items-center' }, [
          h('img', { src: option.icon, class: 'dropdown-option-icon' }),
          option.label
        ]),
        h('div', { class: 'dropdown-option-value' }, option.value)
      ]),
      key: option.key
    }))
  )
  
  const handleSelect = (key: string) => {
    selectedOption.value = options.value.find(option => option.key === key) || null
  }
  </script>
  
  <style scoped>
  .dropdown-option {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
  }
  
  .dropdown-option-icon {
    margin-right: 8px;
  }
  
  .dropdown-option-value {
    color: gray;
  }

  .no-copy {
  user-select: none; /* Disable text selection */
}
  </style>
  