from pydantic import BaseModel
import time
from typing import Optional

class Message(BaseModel):
    content: str
    role: str

class Choice(BaseModel):
    index: int
    delta: Message
    finish_reason: Optional[str] = None
    logprobs: None = None  # 这个字段在示例中为null

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    def __init__(self, prompt_tokens: int, completion_tokens: int, **data):
        super().__init__(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, 
                         total_tokens=prompt_tokens + completion_tokens, **data)

class ChatCompletionResponse(BaseModel):
    model: str
    choices: list[Choice]
    created: int
    id: str
    object: str
    usage: Usage

    def __init__(self, model: str, choices: list[Choice], prompt_tokens: int, completion_tokens: int, **data):
        super().__init__(model=model, choices=choices, created=int(time.time()),
                         id="chatcmpl-" + self._generate_id(), object="chat.completion",
                         usage=Usage(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens), **data)

    def _generate_id(self):
        # 这里是一个简化的ID生成方法，实际上可能需要更复杂的逻辑
        return "7QyqpwdfhqwajicIEznoc6Q47XAyW"

def sse_json(content, finish_reason=None, model="gpt-3.5-turbo-0613") -> str:
    # 构造数据
    message = Message(content=content, role="assistant")
    choice = Choice(index=0, delta=message, finish_reason=finish_reason)
    chunk = ChatCompletionResponse(model="gpt-3.5-turbo-0613", choices=[choice], prompt_tokens=57, completion_tokens=17)
    return chunk.dict()

