from livekit.plugins import resemble ,elevenlabs
from agent.config import settings

def get_tts():
    return elevenlabs.TTS(
                model="eleven_flash_v2_5", 
                language="en",
                api_key=settings.ELEVEN_API_KEY
        )


