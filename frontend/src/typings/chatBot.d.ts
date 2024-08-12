declare namespace ChatBot {

	interface ChatBot {
		name: string
		description: string
		avatar: string
		llm: boolean
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
}
