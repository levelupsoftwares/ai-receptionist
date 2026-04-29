from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import silero
from agent.pipeline.stt import get_stt
from agent.pipeline.llm import get_llm
from agent.pipeline.tts import get_tts


class Receptionist(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful receptionist. Be brief and natural."
        )

async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()
    
    session = AgentSession(
        stt=get_stt(),
        llm=get_llm(),
        tts=get_tts(),
        vad = silero.VAD.load()
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