from dotenv import load_dotenv
import os
import boto3
import json
import base64

# 👇 Add this line at the top of image_service.py
load_dotenv()

def generate_images(prompt: str):
    try:
        print("🎨 Generating image with Bedrock Stable Diffusion...")
        client = boto3.client(
            "bedrock-runtime",
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )

        body = json.dumps({
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 8,
            "steps": 40
        })

        # Try different Stable Diffusion models based on availability
        # Common model IDs: stability.stable-diffusion-xl-v1, amazon.titan-image-generator-v1
        response = client.invoke_model(
            modelId="stability.stable-diffusion-xl-v1:0",
            body=body
        )

        result = json.loads(response["body"].read())
        image_base64 = result["artifacts"][0]["base64"]

        output_path = "illustration.png"
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image_base64))

        print(f"✅ Image saved: {output_path}")
        return [output_path]

    except Exception as e:
        import traceback
        print("❌ Bedrock Image Generation failed:")
        traceback.print_exc()
        return ["https://placehold.co/600x400?text=Illustration+Unavailable"]