<template>
	<div>
		<mModal
			ref="refModal"
			title="新增问答数据"
			footerBtnSize="medium"
			footerComfirmBtnType="primary"
			:autoFocus="false"
			txtCancel="关闭"
			txtConfirm="完成"
			@onPositiveClick="handleComfirm"
			@onShowChange="handleModalShowChange"
			style="
				width: 80%;
				max-width: 550px;
				position: fixed;
				top: 10%;
				left: 50%;
				transform: translate(-50%, 0);
			"
		>
        <div class="flex flex-col gap-4 p-4">
        <!-- 问题输入 -->
        <div class="flex flex-col gap-1">
            <span>问题</span>
            <n-input
                v-model:value="data.questionAnswerInput.question"
                type="text"
                placeholder="请输入问题"
            />
        </div>
        <!-- 答案输入 -->
        <div class="flex flex-col gap-1">
            <span>答案</span>
            <n-input
                v-model:value="data.questionAnswerInput.answer"
                type="textarea"
                placeholder="请输入答案"
                :autosize="{
                    minRows: 3,
                    maxRows: 5,
                }"
            />
        </div>
        </div>
        <template v-slot:footer>
      <n-button @click="changeModalShow" size="medium">关闭</n-button>
      <n-button type="primary" size="medium" :loading="data.loading" @click="handleComfirm">完成</n-button>
    </template>
		</mModal>
	</div>
</template>

<script setup lang="ts">
import mModal from "@/components/common/mModal/index.vue";
import { reactive, ref } from "vue";
import { useMessage } from "naive-ui";
import { api } from '@/api/common';
import { defineEmits } from 'vue';


const msg = useMessage();
const refModal = ref();


// Define emits
const emit = defineEmits(['update-list']);

const props = defineProps({
  knowledgeId: String,
  nodeId: String,
})

const data = reactive({
	// 搜索模式
    questionAnswerInput: {
        question: '',  // 存储问题文本
        answer: ''  // 存储答案文本
    },

    loading: false, // 加载状态
});
// 确认
const handleComfirm = () => {
    data.loading=true; // If you have a loading state
    api.add_manual_document({
        node_id: props.nodeId, 
        question: data.questionAnswerInput.question, 
        answer: data.questionAnswerInput.answer,
        knowledge_id: props.knowledgeId
    })
    .then((res) => {
         // Turn off loading state
        if (res) {
            msg.success("保存成功");
            emit('update-list'); // Correctly emit the event
            changeModalShow(); // Hide modal based on ref
        }
    })
    .catch((err) => {
         // Turn off loading state
        msg.error("保存失败");
        changeModalShow(); // Hide modal based on ref
    }).finally(() => {
        data.loading=false; // Turn off loading state
    });
};

const handleModalShowChange = (show: boolean) => {
    if (!show) {
        // 清空输入框
        data.questionAnswerInput.question = '';
        data.questionAnswerInput.answer = '';
    }
};

// 改变模态框显示
const changeModalShow = () => {
	refModal.value.toggleModal();
};

defineExpose({
	changeModalShow,
});
</script>

<style lang="less" scoped></style>
