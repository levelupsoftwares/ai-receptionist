from pydantic_settings import BaseSettings
from pathlib import Path
import os


class Settings(BaseSettings):
  # voice pipeline
    LIVEKIT_URL:str
    LIVEKIT_API_KEY:str
    LIVEKIT_API_SECRET:str

 # keys
    GROQ_API_KEY:str
    RESEMBLE_API_KEY:str
    ELEVEN_API_KEY:str
    OPENAI_API_KEY:str

 #  LLM   
    LLM_MODEL:str = 'meta-llama/llama-4-scout-17b-16e-instruct'
    temprature:float = 0.3
    MAX_TOKENS:int = 150

 # STT
    STT_MODEL:str = 'whisper-large-v3-turbo'
 # TTS
    TTS_MODEL:str = 'eleven_flash_v2_5'
    # TTS_MODEL2:RESEMBLE_API_KEY

 # Embeddinging model
    EMBEDDING_MODEL:str = 'openai/text-embedding-3-small'

 # rag
    CHUNK_SIZE:int = 500
    CHUNK_OVERLAP:int = 100
    CHROMA_PATH:str = 'data/chroma_storage'
    TOP_K:int = 2

 # paths
    BASE_DIR:Path = Path(__file__).resolve().parents[1]
    CHROMA_DB_DIR:Path = BASE_DIR / "data" / "chroma_storage"
    
 # system prompt path
    SYSTEM_PROMPTS_PATH:str = "agent/prompts/system.txt"
    class Config:
        env_file = '.env.local'
        extra = 'ignore'


settings = Settings()

os.environ["LIVEKIT_URL"] = settings.LIVEKIT_URL
os.environ["LIVEKIT_API_KEY"] = settings.LIVEKIT_API_KEY
os.environ["LIVEKIT_API_SECRET"] = settings.LIVEKIT_API_SECRET