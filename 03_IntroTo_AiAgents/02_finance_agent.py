import yfinance as yf
import json
from dataclasses import dataclass
from openai import OpenAI
import os
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
    Provider("Groq","GROQ_API_KEY",True,"https://api.groq.com/openai/v1","qwen/qwen3.8-27b"),
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

def stock_price_checker(ticker_symbol: str) -> str:
    try:
        stock = yf.Ticker(ticker_symbol.upper())
        price = stock.fast_info["last_price"]
        currency = stock.fast_info["currency"]
        # print(f"Price of stock {ticker_symbol} is {price} and currency is {currency}")
        return json.dumps({
            "ticker": ticker_symbol,
            "Price": price,
            "Currency": currency
        })
    except Exception as e:
        # print(f"Error fetching stock for {ticker_symbol}")
        return json.dumps({
            "error": str(e)
        })


stock_price_checker_schema = {
    "type": "function",
    "function": {
        "name": "stock_price_checker",
        "description": "This is a stock price checker for a ticker symbol",
        "parameters":{
            "type":"object",
            "properties": {
                "ticker_symbol": {"type": "string", "description": "The ticker to look up the finance for."}
            },
            "required": ["ticker_symbol"]
        }
    }
}

TOOLS = {
    "stock_price_checker": stock_price_checker
}


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
            tools=[stock_price_checker_schema]
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
    print("Hello Finance customer service is here to help you please type you query below 👇\n")
    user_query = input()

    if user_query.lower() in ["exit", "bye", "done"]:
        print("Finance customer service says Thank you!")
        break

    print(ask_llm_with_tool_call(user_query))
    print("-"*70)