// src/utils/readStream.ts
import { fetchChatAPI } from "@/api";
import { useUserStore } from "@/store";
import { t } from "@/locales";

const decoder = new TextDecoder("utf-8");
const userStore = useUserStore();


export async function generate(index: number, data: any) {
  if (data.loading) return;

  data.messages[index] = {
    dateTime: new Date().toLocaleString(),
    content: `${t("chat.thinking")}...`,
    role: "assistant",
    error: false,
    loading: true,
    avatar: data.agent?.avatar,
    isShowRaw: true,
    showTools: false,
  };

  data.loading = true;
  const controller = new AbortController();

  try {
    const access_token = userStore.$state.userInfo?.access_token;
    if (!access_token) {
      data.messages[index].content = t("common.unlogin");
      data.messages[index].loading = false;
      data.loading = false;
      return;
    }

    const { body, status } = await fetchChatAPI(
      { messages: data.messages.slice(0, index), stream: true },
      data.agent.id,
      access_token,
      controller.signal
    );

    if (status === 200) {
      const reader = body?.getReader();
      await readStream(reader, status, index, data);
    } else {
      const json = await body?.json();
      const content = json.error?.message ?? "";
      data.messages[index].content = content;
    }
  } catch (error: any) {
    console.log(error);
  } finally {
    data.messages[index].loading = false;
    controller.abort();
    data.loading = false;
  }
}

async function readStream(
  reader: ReadableStreamDefaultReader<Uint8Array>,
  status: number,
  index: number,
  data: any
) {
  let partialLine = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    const decodedText = decoder.decode(value, { stream: true });

    if (status !== 200) {
      const json = JSON.parse(decodedText);
      const content = json.error?.message ?? decodedText;
      console.log(content);

      requestAnimationFrame(() => {
        //
      });
      data.messages[index].content = content;

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
      appendLastMessageContent(content, index, data);
    }
  }
}

function appendLastMessageContent(content: string, index: number, data: any) {
  data.messages[index].content += content;
}