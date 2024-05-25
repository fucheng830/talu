import { computed, reactive, ref } from "vue";
import { useChatStore, useNavStore, useUserStore } from "@/store";
import { fetchChatAPI } from "@/api";

const chatStore = useChatStore();
const navStore = useNavStore();
const userStore = useUserStore();

const decoder = new TextDecoder("utf-8");

// 当前页面数据
const data = reactive({
	txtInput: "",
	isInputing: false,
	loading: false,
	messages: [],
	curChatInfo: {
		agent: computed(() => chatStore.currentAgent()),
		agentHistory: computed(() => chatStore.currentAgentHistory()),
	},
	opt: {
		collapseLeft: false,
		userInfo: computed(() => userStore.$state.userInfo),
	},
});


// 发送
const handleSend = () => {
	if (!data.txtInput) return;
	if (data.loading) return;
	  // 消息内容
	const message = {
			dateTime: new Date().toLocaleString(),
			content: data.txtInput,
			role: "user",
			error: false,
			loading: false,
			avatar: data.opt.userInfo?.avatar,
		};
	// 添加到消息列表
	data.messages.push(message);
	// 显示加载中
	data.loading = true;
	// 清空输入框
	data.txtInput = "";
	const index = data.messages.length

	data.messages[index] = {
				dateTime: new Date().toLocaleString(),
				content: "思考中...",
				role: "Assistant",
				error: false,
				loading: true,
				avatar: data.curChatInfo.agent?.avatar,
	};
	generate(index);
	
};

// 对话处理
async function generate(index: number) {
  // 添加可中断控制
  let controller = new AbortController();
	// 滚动到到底部
	// scrollToBottom();
	// 获取数据
	// Add the object to the dataSources array
  try {
    const { body, status } = await fetchChatAPI(
		{messages: data.messages.slice(0, index), stream: true}, 
		data.curChatInfo.agent.id,
		userStore.$state.userInfo.token,
      	controller.signal
    );


  if (body) {
      const reader = body.getReader();
      await readStream(reader, status, index);
    }
  } catch (error: any) {
    console.log(error);
  } finally {
    data.messages[index].loading = false;
    controller.abort();
    data.loading = false;
  }
}

const readStream = async (
  reader: ReadableStreamDefaultReader<Uint8Array>,
  status: number,
  index: number
) => {
  let partialLine = "";
  

  while (true) {
    // eslint-disable-next-line no-await-in-loop
    const { value, done } = await reader.read();
    if (done) break;

    const decodedText = decoder.decode(value, { stream: true });
    if (status !== 200) {
      const json = JSON.parse(decodedText);
      const content = json.error?.message ?? decodedText;

      requestAnimationFrame(() => {
		// 
      });
      // 弹出付费框
      if (status === 401) {
        // 弹出付费框
      }
      return;
    }

    const chunk = partialLine + decodedText;
    const newLines = chunk.split(/\r?\n/);

    partialLine = newLines.pop() ?? "";

    for (const line of newLines) {
      if (line.length === 0) continue; // ignore empty message
      if (line.startsWith(":")) continue; // ignore sse comment message
      if (line === "data: [DONE]") return; //
      const json = JSON.parse(line.substring(6)); // start with "data: "

      // 有内容返回后，取消输入中状态，否则不会渲染内容
      if (json.choices[0].delta.content.length > 0)
        if (data.messages[index].loading == true) {
			data.messages[index].loading = false;
			data.messages[index].content = "";
		}
	 
		

      const content =
        status === 200
          ? (json.choices &&
              json.choices[0] &&
              json.choices[0].delta &&
              json.choices[0].delta.content) ||
            ""
          : json.error.message;
      appendLastMessageContent(content, index);
    }
  }
};

const appendLastMessageContent = (content: string, index: number) => {
  	data.messages[index].content += content;
  // 在这里执行依赖于 DOM 更新的操作，比如滚动
//   scrollToBottom();
};




