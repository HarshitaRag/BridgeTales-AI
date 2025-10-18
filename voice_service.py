import os
from elevenlabs import ElevenLabs, save

def generate_voice(story_text: str, voice_id="21m00Tcm4TlvDq8ikWAM"):
    """Generate narration audio using ElevenLabs API
    
    Default voice_id is Rachel (21m00Tcm4TlvDq8ikWAM) - a pre-made voice
    Other popular pre-made voices:
    - Rachel: 21m00Tcm4TlvDq8ikWAM
    - Drew: 29vD33N1CtxCmqQRPOHJ
    - Clyde: 2EiwWnXFnvU5JabPnv8n
    - Paul: 5Q0t7uMcjvnagumLfvZi
    """
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    response = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id="eleven_turbo_v2",
        text=story_text
    )

    # Save MP3 locally
    output_file = "story_audio.mp3"
    with open(output_file, "wb") as f:
        for chunk in response:
            f.write(chunk)
    
    print(f"✅ Voice narration saved to {output_file}")
    return output_file