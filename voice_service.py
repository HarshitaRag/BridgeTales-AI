# voice_service.py
import os
import boto3

def generate_voice_with_polly(text: str, voice_id: str = "Joanna") -> str:
    """Synthesize 'text' to MP3 via Amazon Polly and return the local file path."""
    polly = boto3.client(
        "polly",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    # Basic safety: Polly max text length ~3000 chars; truncate if huge.
    safe_text = text[:2800]

    resp = polly.synthesize_speech(
        Text=safe_text,
        OutputFormat="mp3",
        VoiceId=voice_id  # good voices: Joanna, Matthew, Amy, Brian, Salli
    )

    out_path = "story_audio.mp3"
    with open(out_path, "wb") as f:
        audio_stream = resp.get("AudioStream")
        if audio_stream:
            f.write(audio_stream.read())
        else:
            raise RuntimeError("Polly returned no AudioStream.")
    return out_path