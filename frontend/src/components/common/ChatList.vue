<template>
    <div class="flex flex-col items-center justify-center h-screen bg-gray-100">
      <div class="w-full max-w-md p-4 bg-white rounded-lg shadow">
        <div class="mb-4">
          <div class="flex items-center bg-gray-200 rounded-full">
            <input
              class="flex-grow p-2 rounded-l-full bg-transparent focus:outline-none"
              placeholder="搜索"
              type="text"
            />
            <button class="p-2">
              <i class="fas fa-plus"></i>
            </button>
          </div>
        </div>
        <div class="flex items-center p-3 rounded-lg bg-gray-50">
          <img
            alt="Colorful circle resembling a chat logo"
            class="mr-2 rounded-full"
            height="50"
            src="https://dalleprodsec.blob.core.windows.net/private/images/b63630d4-0c75-492d-9887-9d5d497e5d10/generated_00.png?se=2024-08-10T13%3A35%3A05Z&amp;sig=jZcziuQqJFByCzMzsdj0DMIlO3cjy8O4Yn3wtCntdeQ%3D&amp;ske=2024-08-15T16%3A37%3A58Z&amp;skoid=e52d5ed7-0657-4f62-bc12-7e5dbb260a96&amp;sks=b&amp;skt=2024-08-08T16%3A37%3A58Z&amp;sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&amp;skv=2020-10-02&amp;sp=r&amp;spr=https&amp;sr=b&amp;sv=2020-10-02"
            width="50"
          />
          <div>
            <h2 class="text-md font-semibold">QuChat</h2>
            <p class="text-gray-500">您的AI助手</p>
          </div>
        </div>
        <div class="flex items-center mt-4 p-3 rounded-lg bg-gray-50">
          <img
            alt="Circular icon with command prompt symbol"
            class="mr-2 rounded-full"
            height="50"
            src="https://dalleproduse.blob.core.windows.net/private/images/7ea02f36-a90f-4b21-b497-d4316cc174d6/generated_00.png?se=2024-08-10T13%3A35%3A02Z&amp;sig=uGwNapZ7ETCfvOtmexpxVrRxlf89MzO8QC1X4cDYfos%3D&amp;ske=2024-08-16T12%3A18%3A05Z&amp;skoid=09ba021e-c417-441c-b203-c81e5dcd7b7f&amp;sks=b&amp;skt=2024-08-09T12%3A18%3A05Z&amp;sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&amp;skv=2020-10-02&amp;sp=r&amp;spr=https&amp;sr=b&amp;sv=2020-10-02"
            width="50"
          />
          <div>
            <p class="text-gray-500">
              上次交互，稍后再和您确认收到的数据
            </p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  </script>
  
  <style scoped>
  body {
    font-family: 'Roboto', sans-serif;
  }
  </style>
  