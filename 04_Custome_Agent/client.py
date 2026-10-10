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