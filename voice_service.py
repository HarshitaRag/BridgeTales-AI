import os
from elevenlabs import ElevenLabs, save

def generate_voice(story_text: str, voice_name="Rachel"):
    """Generate narration audio using ElevenLabs API"""
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    
    audio = client.generate(
        text=story_text,
        voice=voice_name,
        model="eleven_turbo_v2"
    )

    output_file = "story_audio.mp3"
    save(audio, output_file)
    return output_file