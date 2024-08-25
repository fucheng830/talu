import { post, get } from '@/utils/request'

const apiURL = [
  /**
   * 登录
   * {
   *  email: string
   *  password: string
   * }
   */
  '/login',

  /**
   * 检查邮箱是否已注册
   * {
   *  email: string
   * }
  */
  '/check_mail',
  /**
   * 注册
   * {
   *  userId: number
   *  email: string
   *  emailCode: string
   *  password: string
   *  referee: number
   * }
   */
  '/register',
  /**
   * 邮箱验证码
   * {
   *  userId: number
   *  email: string
   * }
   */
  '/send_code',

  /**
   * 获取智能体列表
   * {
   *  "id": "string"
   * }
   */
  '/agents',
  /**
 * 获取智能体信息单个
 * {
 *    "id": "string",
      "name": "string",
      "description": "string",
      "opening_text": "string",
      "opening_question": [
        "string"
      ],
      "system_prompt": "string",
      "knowledge": [
        "string"
      ],
      "tools": [
        "string"
      ],
      "voice": "string",
      "avatar": "string",
      "suggestion": {
        "is_enable": true,
        "custom_prompt": "string"
      },
      "permission": "string",
      "category": "string",
      "gid": "string"
 * }
 */
  '/agent',
  /**
   * 编辑智能体
   * {
   * }
   */
  '/agent_edit',
  /**
   * 获取对话标题
   * {
   * }
   */
  '/conversation/gen_title',
  /**
   * 创建知识库
   * {
   *  "name": "string",
      "type": "string"
   * }
   */
  '/add_knowledge',
  /**
   * 获取知识库列表
   * {
   * }
   * 
   */
  '/get_knowledges',
  /**
   * 删除知识库
   * {
   *  "knowledge_id": "string"
   * }
   */
  '/delete_knowledge',
  /**
   * 分割文档
    documents: list
    splitter_name: str
    splitter_params: dict
   */
  '/split_document',
  '/add_manual_container',
  '/extract_document',
  '/upload_data',
  '/list_knowledge_data',
  '/delete_node',
  '/preview_segment_data',
  '/add_manual_document',
  '/add_content',
  '/scan_qr',
  '/check_wechat_login',
  '/get_node_data',
  '/add_url_content',

  /**
   * 知识库 搜索测试
   * {
   *   "query": "string",
   *   "knowledge_id": "string",
   *   "search_config": {
   *      embedding_ratio: 1  // 语义检索
   *      bm25_ratio: 1 // 全文
   *  }
   * }
   */
  '/search_node',
  '/my_agents',
  '/wechat_pay',
  '/check_order',
  '/delete_agent',
  '/wechat_login',
  '/search_agent',
  '/llm',
]

function generateApiFunctions(list: string[]) {
  const result: { [key: string]: <T = any>(data?: T) => Promise<T> } = {};

  for (const path of list) {
    // 将路径转换为驼峰形式的函数名
    const functionName = path.split('/')
      .filter(segment => segment)
      .map((segment, index) => index === 0 ? segment : segment[0].toUpperCase() + segment.slice(1))
      .join('');

    result[functionName] = function <T = any>(data?: T) {
      return post<T>({ url: path, data });
    };
  }

  return result;
}

export const api = generateApiFunctions(apiURL);