from dotenv import load_dotenv
import os
import boto3
import json
import base64

# 👇 Add this line at the top of image_service.py
load_dotenv()

def generate_images(prompt: str, page_number: int = 0):
    """Generate images using Amazon Titan Image Generator
    
    Args:
        prompt: Text description for the image
        page_number: Unique identifier for this story page
    """
    try:
        print(f"🎨 Generating image for page {page_number} with Amazon Titan...")
        client = boto3.client(
            "bedrock-runtime",
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )

        # Titan Image Generator request format
        body = json.dumps({
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": prompt
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "quality": "standard",
                "cfgScale": 8.0,
                "height": 512,
                "width": 512,
                "seed": page_number  # Use page number as seed for unique images
            }
        })

        # Use Amazon Titan Image Generator
        response = client.invoke_model(
            modelId="amazon.titan-image-generator-v1",
            body=body
        )

        result = json.loads(response["body"].read())
        
        # Titan returns images in base64
        image_base64 = result["images"][0]

        # Use unique filename for each page
        output_path = f"illustration_page_{page_number}.png"
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image_base64))

        print(f"✅ Image saved: {output_path}")
        return [output_path]

    except Exception as e:
        import traceback
        print("❌ Bedrock Image Generation failed:")
        traceback.print_exc()
        return []