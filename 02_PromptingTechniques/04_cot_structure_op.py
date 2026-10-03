from dataclasses import dataclass
from openai import OpenAI
import os
from typing import Literal
from pydantic import BaseModel
import json
from dotenv import load_dotenv
load_dotenv()

@dataclass(frozen=True)
class Provider:
    """One provider to reliably route requests accross all inference providers """

    name: str
    env_var: str
    is_true: bool
    base_url: str | None
    model: str


PROVIDERS = [
    Provider("Groq","GROQ_API_KEY",True,"https://api.groq.com/openai/v1","openai/gpt-oss-120b"),
    Provider("OpenRouter","OPENROUTER_API_KEY",True,"https://openrouter.ai/api/v1","stealth/space-bunny-alpha")
]

def select_provider() -> Provider:
    for provider in PROVIDERS:
        if os.getenv(provider.env_var):
            return provider

    expected = ", ".join(p.env_var for p in PROVIDERS)
    raise RuntimeError(f"No provider key set, add one of {expected} to your environment variables")


def build_client(provider: Provider) -> OpenAI:

    api_key = os.getenv(provider.env_var)


    return OpenAI(
        api_key=api_key,
        base_url=provider.base_url
    )

def have_any_key() -> bool:
    return any(os.getenv(p.env_var) for p in PROVIDERS)

print("Found a provider key." if have_any_key() else "No provider key found.")







SYSTEM_PROMPT = """
You are an expert assistant that solves user queries using chain of thought.
You work in different phases -> THINKING (you think about the next step to be executed for the solving the user query) and FINAL_OUTPUT (you output the final answer to the user query).

Rules:
- Reply with ONLY a JSON object -  no other text or comments - in exactly the following shape:

JSON_SCHEMA = 
{
    "content": "your thinking or final output",
    "step_type": "THINKING" | "FINAL_OUTPUT"
}

- Emit one small thinking/plan step at a time until you have the final answer ready.
- When done with your chain of thought for the reasoning, emit the FINAL_OUTPUT step with the final answer.

Example:
Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can contains 3 tennis balls. How many tennis balls does Roger have now?

{"step_type": "THINKING", "content": "User wants a total count of tennis balls. In the start Roger has 5 tennis balls. current_count = 5."}
{"step_type": "THINKING", "content": "Roger buys 2 more cans of tennis balls. Each can contains 3 tennis balls. total_cans = 2. total_can_balls = 2 * 3 = 6"}
{"step_type": "THINKING", "content": "Total tennis balls = current_count + total_can_balls"}
{"step_Type": "THINKING", "content": "Total tennis balls = 5 + 6 = 11"}
{"step_type": "FINAL_OUTPUT", "content": "Roger has 11 tennis balls now."}

Please think step by step and emit the steps one by one. For each reply only emit the next step to be executed.
"""


class cot_step(BaseModel):
    """A step in the CoT process."""
    
    content: str
    step_type: Literal["THINKING","FINAL_OUTPUT"]

def parse_cot_step(raw_response: str) -> cot_step | str:
    """Parse a raw reply into a CotStep."""
    try:
        parsed = json.loads(raw_response)
        return cot_step(**parsed)
    except json.JSONDecodeError as e:
            print(e)
            return f"Invalid JSON: {raw_response}"

def llm_json_reply(message: list[dict]) -> str:

    provider = select_provider()
    client = build_client(provider)

    kwargs: dict = {
        "model":provider.model,
        "max_tokens":400,
        "messages":message
    }


    llm_res = client.chat.completions.create(**kwargs)

    return llm_res.choices[0].message.content


question="""
Weng earns $12 an hour for babysitting. Yesterday, she babysat for 5 hours. She spent $15 on lunch and $6 on a movie ticket. How much money does she have left from what she earned yesterday?
"""


class cot_assistent:
    """An assistant that solves user queries using chain of thought."""

    def __init__(self):
        self.message_prompt = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        self.MAX_STEPS = 15

    def run(self,user_query: str) ->str:
        self.message_prompt.append({"role":"user","content":user_query})

        for _ in range(self.MAX_STEPS):
            raw_reply = llm_json_reply(self.message_prompt)

            self.message_prompt.append({"role":"assistant","content":raw_reply})

            parsed_output = parse_cot_step(raw_reply)

            if isinstance(parsed_output, cot_step): # check if the parsed_output is a valid CotStep object
                
                if parsed_output.step_type == "THINKING":
                    print(f"💡 {parsed_output.content}\n")
                    continue
                if parsed_output.step_type == "FINAL_OUTPUT":
                    print(f"🎯 {parsed_output.content}\n")
                    return parsed_output.content
            else:
                print(f"❌ {parsed_output}\n")
                return parsed_output

        return f"Failed to derive the answer in {self.MAX_STEPS} steps."

assistent = cot_assistent()

while True :
    user_query = input("👉🏻 Enter your question: ")

    if user_query.lower() in ["exit","bys","quit"]:
        break

    answer = assistent.run(user_query)
    # print(f"🎯 {answer}\n")
    print("--------------------------------")
