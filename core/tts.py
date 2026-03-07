import os
import asyncio
import edge_tts
from config import TEMP_DIR

# Using ChristopherNeural for a deep, authoritative, and slightly tensed voice
VOICE = "en-US-ChristopherNeural"

async def _generate_audio(text: str, output_path: str, srt_path: str):
    """
    Internal async function for Ashley MindShift.
    Slower, more dramatic pacing to increase tension and dopamine.
    """
    # Rate: -5% to slow it down and make it more deliberate
    # Pitch: -10Hz for a deeper, darker tone
    # Volume: +5% to make it feel closer and more personal (human)
    communicate = edge_tts.Communicate(
        text, 
        VOICE, 
        rate="-5%", 
        pitch="-10Hz", 
        volume="+10%",
        boundary="WordBoundary"
    )
    submaker = edge_tts.SubMaker()
    
    with open(output_path, "wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
                
    with open(srt_path, "w", encoding="utf-8") as sub_file:
        sub_file.write(submaker.get_srt())

def generate_voiceover(text: str, filename="voiceover.mp3"):
    """
    Generates a dark, human-like voiceover and SRT.
    """
    output_path = os.path.join(TEMP_DIR, filename)
    srt_filename = filename.rsplit('.', 1)[0] + ".srt"
    srt_path = os.path.join(TEMP_DIR, srt_filename)
    
    print(f"Generating dark voiceover ({VOICE}): {output_path}")
    
    # Run the async edge-tts command
    asyncio.run(_generate_audio(text, output_path, srt_path))
    
    return output_path, srt_path
