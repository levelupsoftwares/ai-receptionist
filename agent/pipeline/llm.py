from livekit.plugins import groq
from agent.config import settings

def get_llm():
    return groq.LLM(
        model=settings.LLM_MODEL,
        max_completion_tokens=settings.MAX_TOKENS,
        api_key=settings.GROQ_API_KEY
    )

