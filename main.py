from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import tenvad
from livekit.plugins.turn_detector.english import EnglishModel

# STT / LLM / TTS
from agent.pipeline.stt import get_stt
from agent.pipeline.llm import get_llm
from agent.pipeline.tts import get_tts

# RAG Retriever
from agent.rag.retriever import retriever_context

# setting/ configuration
from agent.config import settings

# intent classifier
from agent.pipeline.intent import detect_intent
import asyncio
import aiofiles


# =====================================
# Global System prompt cache
# -------------------------------------
# Loaded once during session and reused for all sessions.
# Avoids repeated file read from memory during relatime conversation
_system_prompt:str|None = None

# Path of system prompt
system_prompt_path = settings.BASE_DIR/'agent'/'prompts'/'system.txt'

# =====================================
# Load system prompt
# -------------------------------------
# Async file(aiofile) prevent blocking the event loop.
# prompt is cached globaly after first load
# ======================================
async def load_system_prompt()-> str:
    global _system_prompt
    if _system_prompt is None:
        async with aiofiles.open(system_prompt_path,'r',encoding='utf-8') as f:
            _system_prompt = await f.read()
    return _system_prompt

# =======================================
# AI Receptionist Agent

class Receptionist(Agent):
    def __init__(self):
        super().__init__(
            # Base system instruction shared accross all turns
            instructions=_system_prompt
        )

# ========================================
# Triggered whenever the user finishes speaking
# ----------------------------------------
# Responsibilities:
# 1.Detect conversational intent
# 2.Decide weather rag is needed
# 3.Inject orchestration instructions
# =========================================
    async def on_user_turn_completed(self, turn_ctx, new_message):
        
        user_query = new_message.text_content.strip()

        # intent classification
        intent = detect_intent(user_query)

        # Dynamic orchestration variables 
        context = "" 
        orchestration_prompt = ""

# =========================================
# Acknowledgement / Listening / Farewell
 # Skip unnecessary RAG + LLM reasoning to reduce:
        # - latency
        # - token usage
        # - interruption noise
# ===========================================
        if intent in ["acknowledgement","listening"]: 
            return 
        
        # Farewell
        elif intent == 'farewell':
           # "llm only -no rag"
            orchestration_prompt = """
            user is ending the conversation. Respond briefly and politely
            """
        
# ================================================
    # BOOKING INTENT
# ------------------------------------------------
        # Tool-oriented workflow.
        # Avoid unnecessary RAG retrieval.
        #
        # Goal:
        # - gather structured booking information
        # - later trigger booking tool/function
# =================================================
        
        elif intent == 'booking':
            

            orchestration_prompt = """
                user want to book a plumbing service.
                collect: name,address,plumbing issue(if not discussed yet),preffered data/time
                once collected. keep response short.Once all detailed collected call the booking tool. 
            """
# =================================================
        # EMERGENCY INTENT
# -------------------------------------------------
        # Emergency scenarios require:
        # - reassurance
        # - urgency
        # - fast assistance
        #
        # RAG retrieval runs inside asyncio.to_thread()
        # so blocking vector search does NOT freeze:
        # - audio streaming
        # - STT
        # - TTS
        # - VAD
        # - turn detection
# =================================================
        elif intent == "emergency":

            
            context  = await asyncio.to_thread(retriever_context,user_query) 

            orchestration_prompt = f"""
                    User has plumbing emergency.
                    Prioritize: urgency,reassurance,fast assistance
                    Relevant company context:
                    {context}
"""
# =================================================
        # GENERAL QUERY
        # -------------------------------------------------
        # Standard informational workflow using RAG.
# =================================================
        else: 

            context = await asyncio.to_thread(retriever_context,user_query)

            orchestration_prompt = f"""
             Relevant company context:
             {context}
            """

        # Final system system prompt
# =================================================
        # Dynamic System Injection
        # -------------------------------------------------
        # Inject lightweight orchestration guidance
        # into the current conversational turn.
        #
        # NOTE:
        # Base instructions already exist in Agent()
        # so we inject ONLY dynamic runtime context.
# =================================================
        final_prompt  = f"""
            Current_intent :{intent}
            {orchestration_prompt}
                                    """
        
        turn_ctx.add_message(
            role="system",
            content=final_prompt
        )

        # prompt = f"""
        # {_system_prompt}

        # Relevant company context:
        # {context}
        # """
        # turn_ctx.add_message(
        #     role="system",
        #     content=prompt
        # )
        
# =========================================================
# LiveKit Entrypoint
# ---------------------------------------------------------
async def entrypoint(ctx: agents.JobContext):
    # connect worker to livekit room
    await ctx.connect()
    
    #load the prompt before creating the agent
    await load_system_prompt()

    # preload chroma before any call comes in 
    await asyncio.to_thread(retriever_context,"plumbing services") #warm up
# =============================================
# Agent Session Configuration
# =============================================
    session = AgentSession(
        stt=get_stt(),
        llm=get_llm(),
        tts=get_tts(),
        vad = tenvad.VAD.load(),
        turn_detection=EnglishModel()
    )

# Start realtime voice session
    await session.start(
        room=ctx.room,
        agent=Receptionist(),
        room_input_options=RoomInputOptions(),
    )

# =========================================================
# Application Entry
# =========================================================
if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(entrypoint_fnc=entrypoint)
    )