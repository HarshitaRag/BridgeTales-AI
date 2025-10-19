# voice_service.py
import os
import boto3

def generate_voice_with_polly(text: str, voice_id: str = "Ivy", output_file: str = "story_audio.mp3") -> str:
    """Synthesize 'text' to MP3 via Amazon Polly and return the local file path.
    
    Child-friendly voices:
    - Ivy: Young female child voice (US English) - DEFAULT
    - Kevin: Young male child voice (US English)
    - Joanna: Adult female (US English)
    - Matthew: Adult male (US English)
    """
    try:
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
            VoiceId=voice_id,
            Engine="neural"  # Neural engine for more natural voice
        )

        out_path = output_file
        with open(out_path, "wb") as f:
            audio_stream = resp.get("AudioStream")
            if audio_stream:
                f.write(audio_stream.read())
            else:
                raise RuntimeError("Polly returned no AudioStream.")
        
        print(f"✅ Voice narration saved with {voice_id} voice")
        return out_path
    except Exception as e:
        print(f"⚠️ Polly voice generation failed: {e}")
        print(f"ℹ️  Story will continue without audio")
        return None