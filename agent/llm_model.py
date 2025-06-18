from agent.tool_definition import TOOLS
import json
from database.connect_mysql import get_connection
from agent.tool_function import TOOL_MAP


async def llm_model_call(client, user_input, messages):
    messages.append({"role": "user", "content": user_input})

    # Step 1: First model call
    response = await client.chat.completions.create(
        model="llama3.1",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto"
    )

    message = response.choices[0].message
    messages.append(message)
    return message

async def tool_call(message, messages):
    for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                print(f"[DEBUG] Tool called: {function_name} with args: {args}")

                if function_name in TOOL_MAP:
                    # Run tool
                    conn = get_connection()
                    cursor = conn.cursor()
                    result = TOOL_MAP[function_name](cursor=cursor, **args)
                    cursor.close()
                    conn.close()
                else:
                    result = {"error": f"Unknown tool {function_name}"}

                # Send tool response back to LLM
                tool_result_msg = {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, default=str)
                }
                messages.append(tool_result_msg)

async def final_llmcall(client, messages):
    final_response = await client.chat.completions.create(
                    model="llama3.1",
                    messages=messages
                )
    final_message = final_response.choices[0].message
    messages.append(final_message)

    return final_message