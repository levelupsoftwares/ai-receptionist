from livekit.plugins import groq
from agent.config import settings

def get_stt():
    return groq.STT(
        model=settings.STT_MODEL,
        api_key=settings.GROQ_API_KEY,
        language='en',
    )