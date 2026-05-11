from livekit.plugins import resemble ,elevenlabs
from agent.config import settings

def get_tts():
    # return elevenlabs.TTS(
    #             model="eleven_flash_v2", 
    #             language="en",
    #             api_key=settings.ELEVEN_API_KEY,
    #             voice_id='21m00Tcm4TlvDq8ikWAM'
    #     )
    return resemble.TTS(
                
                # language="en",
                api_key=settings.RESEMBLE_API_KEY,
                # voice_id='21m00Tcm4TlvDq8ikWAM'
                voice_uuid="e8d6d3c8"
        )


