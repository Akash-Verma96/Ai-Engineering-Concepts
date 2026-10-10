import json
from dataclasses import dataclass
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()
from schemas.file_schema import create_file_schema, read_file_schema, update_file_schema, delete_file_schema, TOOLS
from schemas.terminal_schema import approve_command_to_launch_terminal
from client import select_provider, build_client





def ask_llm_with_tool_call(prompt: str,*,max_tokens:int = 400):

    provider = select_provider()
    client = build_client(provider)

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    while True:
        msg_result = client.chat.completions.create(
            model=provider.model,
            max_tokens=max_tokens,
            messages=messages,
            tools=[create_file_schema,read_file_schema,update_file_schema,delete_file_schema,approve_command_to_launch_terminal]
        )

        msg = msg_result.choices[0].message
       
        if not msg.tool_calls:
            return msg.content
        
        messages.append({
            "role": "assistant",
            "content": msg.content,
            "tool_calls": msg.tool_calls
        })

        for tool_call in msg.tool_calls:
            tool_call_name = tool_call.function.name
            tool_call_args = json.loads(tool_call.function.arguments) # {"ticker":"AAPL"}
            tool_call_id = tool_call.id

            if tool_call_name not in TOOLS:
                raise ValueError(f"Tool {tool_call_name} not found")

            tool = TOOLS[tool_call_name]

            result = tool(**tool_call_args)

            messages.append({
                "role":"tool",
                "tool_call_id": tool_call_id,
                "content": result
            })


while True:
    print("-"*70)
    print("Vexora is here to help you please type you query below 👇\n")
    user_query = input()

    if user_query.lower() in ["exit", "bye", "done"]:
        print("Vexora says Thank you!")
        break

    print(ask_llm_with_tool_call(user_query))
    print("-"*70)