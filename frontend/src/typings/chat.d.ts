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
}
