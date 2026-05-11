from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import silero
from livekit.plugins.turn_detector.english import EnglishModel
from agent.pipeline.stt import get_stt
from agent.pipeline.llm import get_llm
from agent.pipeline.tts import get_tts
from agent.rag.retriever import retriever_context
from agent.config import settings

_system_prompt = None

system_prompt_path = settings.BASE_DIR/'agent'/'prompts'/'system.txt'

if _system_prompt is None:
    with open(system_prompt_path,'r') as f:
        _system_prompt = f.read()


class Receptionist(Agent):
    def __init__(self):
        super().__init__(
            instructions=_system_prompt
        )

        
    async def on_user_turn_completed(self, turn_ctx, new_message):
        

        user_query = new_message.text_content

        # retrieve RAG context
        context = retriever_context(user_query)

        # dynamically inject context
        prompt = f"""
        {_system_prompt}

        Relevant company context:
        {context}
        """
        turn_ctx.add_message(
            role="system",
            content=prompt
        )
        

async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()
    
    session = AgentSession(
        stt=get_stt(),
        llm=get_llm(),
        tts=get_tts(),
        vad = silero.VAD.load(),
        turn_detection=EnglishModel()
    )

    await session.start(
        room=ctx.room,
        agent=Receptionist(),
        room_input_options=RoomInputOptions(),
    )
if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(entrypoint_fnc=entrypoint)
    )