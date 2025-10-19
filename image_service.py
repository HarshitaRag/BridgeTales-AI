# image_service.py
import boto3
import json
import base64
import os

def generate_images(prompt: str):
    """Generate a storybook illustration using AWS Bedrock's Stable Diffusion XL"""
    try:
        client = boto3.client(
            "bedrock-runtime",
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

        body = json.dumps({
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,     # how closely it follows the prompt
            "steps": 30         # rendering quality (more = smoother)
        })

        response = client.invoke_model(
            modelId="stability.stable-diffusion-xl-v1",
            body=body
        )

        result = json.loads(response["body"].read())
        image_base64 = result["artifacts"][0]["base64"]

        # Save locally
        output_file = "illustration.png"
        with open(output_file, "wb") as f:
            f.write(base64.b64decode(image_base64))

        print(f"✅ Image saved as {output_file}")
        return [output_file]

    except Exception as e:
        print(f"❌ AWS Image Generation failed: {e}")
        # Fallback placeholder
        return ["https://placehold.co/600x400?text=Illustration+Unavailable"]