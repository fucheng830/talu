import type { GenericAbortSignal } from 'axios'

// 定义 fetchChatAPI 函数，使用泛型 T 来定义返回数据的类型
export async function fetchChatAPI<T = any>(
  data: any,
  agentId: string,
  token: string,
  signal?: GenericAbortSignal,
  defaultPath: string = '/v1/chat/completions',
): Promise<T> {
  // 使用环境变量获取 API 的基本 URL
  const baseURL: string = import.meta.env.VITE_GLOB_API_URL;

  // 正确地构建 URL 来避免双斜杠问题
  const url = new URL(`${agentId}${defaultPath}`, baseURL).toString();
  // 发起 POST 请求
  const result = await fetch(url, {
    method: "post",
    signal: signal as AbortSignal, // Cast signal to AbortSignal
    headers: {
      "Content-Type": "application/json",
      Authorization: token ? `Bearer ${token}` : '',
    },
    body: JSON.stringify(data),
  });

  return result as T;
}
















