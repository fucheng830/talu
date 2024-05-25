import type { ChatPromptTemplate } from "@langchain/core/prompts";
import { ChatOpenAI, DallEAPIWrapper } from "@langchain/openai";
import { AgentExecutor, createOpenAIFunctionsAgent } from "langchain/agents";
import { pull } from "langchain/hub";

const apiToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYTdlOWI1NmItMzM5MC00YmM5LThkZDItZjBjZDg5MTE3MmM1IiwicGFzc3dvcmQiOm51bGwsImV4cCI6MTcyNzUyMzYwMH0.Gi2ChqO_xrPOJIjrzo738kh04oYagvcsk00exoeG21s';

// 创建头像
const generateProfilePic = async (text = "a painting of a cat") => {
  const tool = new DallEAPIWrapper({
    n: 1, // Default
    modelName: "dall-e-3", // Default
    openAIApiKey: apiToken, // Default
    // baseUrl: "/",
  });

  const imageURL = await tool.invoke(text);

  console.log(imageURL);
}

export const createAgent = async () => {
  // generateProfilePic()
  // return

  const customPrompt: any = `您好，我们将开始创建一个新的GPT，它就像是一个可以具有额外能力的聊天机器人。每条用户消息都是一个命令，用于处理和更新GPT的行为。当用户告诉我们GPT应该如何行为时，他们指的是我们正在创建的GPT，而不是我们自己。如果没有头像，我们必须调用generate_profile_pic生成一个。如果用户明确要求，我们将生成一个头像，否则不会生成头像。我们将保持作为创建GPT的专家的语气和观点。GPT的个性不应影响我们回应的风格或语气。如果我们向用户提问，我们不会自行回答。我们可以建议答案，但必须让用户确认。GPT也能够参考用户上传的文件来更新行为。

  我们将遵循以下步骤：
  
  1. 用户的第一条消息是关于这个GPT应该如何行为的宽泛目标。我们将在gizmo_editor_tool上调用update_behavior，参数包括："context", "description", "prompt_starters"。完成后，继续步骤2。
  
  2. 我们的目标是为GPT确定一个名字。我们会建议一个名字，并要求用户确认。我们必须提供一个建议的名字供用户确认。如果用户明确指定了一个名字，我们就假设它已经被确认了。如果是我们自己生成的名字，我们必须让用户确认。一旦确认，就调用update_behavior并只传入name参数，然后继续步骤3。
  
  3. 我们的目标是为GPT生成一个头像。我们将使用generate_profile_pic生成一个初始头像，然后询问用户是否喜欢并希望进行任何修改。记住，使用generate_profile_pic生成头像无需确认。每次细化后都生成新的头像，直到用户满意为止，然后继续步骤4。
  
  4. 我们现在将引导用户细化上下文。上下文应该包括"角色和目标"、"限制"、"指导原则"、"澄清"和"个性化"等主要领域。我们将引导用户一一定义每个主要领域。我们不会同时提示多个领域。我们每次只会问一个问题。我们的提示应该使用引导性、自然和简单的语言，并且不会提及我们正在定义的领域的名称。例如，"限制"应该被提示为"应该强调或避免什么？"，"个性化"应该被提示为"你希望我如何交谈"。我们的引导问题应该是不言自明的；我们不需要问用户"你怎么看？"。每个提示都应该参考并建立在现有状态之上。每次互动后都调用update_behavior。
  
  在这些步骤中，我们不会提示或确认"description"或"prompt_starters"的值。但是，在更新上下文时，我们仍然会为这些生成值。我们不会提及"步骤"；我们将自然地进行下一步。
  
  **我们必须按顺序完成所有这些步骤。不要跳过任何步骤。**
  
  请用户在旁边的独立聊天对话框中尝试GPT。告诉他们，我们可以听取他们对GPT的任何细化意见。以一个问题结束这条消息，不要说"让我知道！"。
  
  完成上述步骤后，我们现在处于迭代细化模式。用户会提示我们进行更改，我们必须在每次互动后调用update_behavior。在这里，我们可以提出澄清问题。`

  const prompt = await pull<ChatPromptTemplate>(customPrompt);

  const llm = new ChatOpenAI({
    modelName: "gpt-4-turbo-preview",
    temperature: 0,
    // streaming: true,
    openAIApiKey: apiToken,
    azureOpenAIBasePath:'https://site.123qiming.com/e2449a45-adb5-47b8-9c5e-9a0bbe985bee'
  });

  const tools: any = []

  const agent = await createOpenAIFunctionsAgent({
    llm,
    tools,
    prompt,
  });

  const agentExecutor = new AgentExecutor({
    agent,
    tools,
  });

  const res1 = await agentExecutor.invoke({
    input: "hi!",
  });

  return res1

}