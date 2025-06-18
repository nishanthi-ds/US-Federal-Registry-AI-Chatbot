import openai
from agent.prompt import SYSTEM_MESSAGE
from agent.llm_model import *

client = openai.AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # dummy key required for OpenAI client
)

# Conversation memory
messages = [
    {"role": "system", "content": SYSTEM_MESSAGE}
]

# Continuous chat function
async def chat_with_agent():
    while True:
        user_input = input("User: ")
        
        if user_input.lower() in {"exit", "quit", "bye"}:
            print("Assistant: Goodbye!")
            break

        message = await llm_model_call(client, user_input, messages)

        # Step 2: If tool was called
        if message.tool_calls:
            
            await tool_call(message, messages)
            # Step 3: Final LLM call with tool result(s)
            final_message = await final_llmcall(client,messages)
            print("Assistant:", final_message.content)
            
        else:
            print("Assistant:", message.content)
