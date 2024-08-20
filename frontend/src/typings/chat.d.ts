declare namespace Chat {

	interface Chat {
		dateTime: string
		text: string
		inversion?: boolean
		error?: boolean
		loading?: boolean
		conversationOptions?: ConversationRequest | null
		requestOptions: { prompt: string; options?: ConversationRequest | null }
	}

	interface History {
		title: string
		isEdit: boolean
		uuid: number
		rid: number
		icon: string
	}

	interface ChatState {
		active: number | null
		usingContext: boolean
		history: History[]
		chat: { uuid: number; modelVersion: string; data: Chat[] }[]
	}

	interface ConversationRequest {
		conversationId?: string
		parentMessageId?: string
		rid?: number
	}

	interface ConversationResponse {
		conversationId: string
		detail: {
			choices: { finish_reason: string; index: number; logprobs: any; text: string }[]
			created: number
			id: string
			model: string
			object: string
			usage: { completion_tokens: number; prompt_tokens: number; total_tokens: number }
		}
		id: string
		parentMessageId: string
		role: string
		text: string
	}

	interface FileData {
		url: string | null; // 文件预览 URL
		type: string; // 文件类型
		progress: number; // 上传进度
		file_id?: string; // 服务器返回的文件 ID
	}
	
	interface Message {
		dateTime: string = new Date().toLocaleString();
		content: string;
		role: string;
		error: boolean;
		loading: boolean;
		avatar: string;
		showTools: boolean = false; // 这里设置了默认值为 false
		fileData: FileData | null;
	  }

	  interface ChatModel {
		icon: string;
		name: string;
		maxToken: number;
		supportsVision: boolean;
		supportsFunctionCall: boolean;
	}

	 interface Tool {
		id: string; // UUID represented as a string
		name: string; // Variable character string
		description: string; // Variable character string
		func: string; // Variable character string
		user_id: string; // Variable character string
		code: string; // Text
		permission: string; // Variable character string
		avatar: string; // Variable character string
	 }

	 interface Agent {
		id: string; // 主键，不能为空
		name?: string; // 可选字段
		description?: string; // 可选字段
		system_prompt?: string; // 可选字段
		opening_question?: any; // JSON 类型字段，使用 any
		knowledge?: any; // JSON 类型字段，使用 any
		tools?: any; // JSON 类型字段，使用 any
		voice?: string; // 可选字段
		avatar?: string; // 可选字段
		suggestion?: any; // JSON 类型字段，使用 any
		user_id?: string; // 可选字段
		permission?: string; // 可选字段
		category?: string; // 可选字段
		llm?: any; // JSON 类型字段，使用 any
		gid?: string; // 可选字段
		opening_text?: string; // 可选字段
		isplus?: boolean; // 布尔类型字段
	}



}
