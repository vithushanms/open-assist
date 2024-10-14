import asyncio
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero

load_dotenv()


async def entrypoint(ctx: JobContext):
    initial_context = llm.ChatContext().append(
        role="system",
        text="You're an voice enabled AI assistant. you should give short and precise response to user's questions",
    )

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        chat_ctx=initial_context,
    )
    assistant.start(ctx.room)

    await asyncio.sleep(1)
    await assistant.say("Hello, I'm an voice enabled AI assistant. How can I help you today?", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
