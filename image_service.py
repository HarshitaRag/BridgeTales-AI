import os
import google.generativeai as genai
from PIL import Image
import io
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_image(story_text: str, theme: str, output_file: str = "story_image.png") -> str:
    """Generate an illustration for the story using Gemini"""
    try:
        # Configure Gemini
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Use Gemini Pro model for text generation
        model = genai.GenerativeModel('gemini-pro')
        
        # Create a concise prompt for image generation
        # Extract key visual elements from the story
        image_prompt = f"""Create a beautiful, storybook-style illustration for this scene:
        
Theme: {theme}
Scene: {story_text[:500]}

Style: Colorful, child-friendly, whimsical storybook illustration with warm colors and soft edges. 
Make it suitable for children aged 5-12. Focus on the main character and key scene elements."""

        logger.info(f"🎨 Generating illustration with Gemini...")
        
        # Generate image description first (Gemini doesn't directly generate images yet)
        # We'll create a placeholder or use a text-to-image API
        # For now, let's create a descriptive text that can be used with other services
        
        response = model.generate_content(f"""Based on this story segment, create a detailed visual description 
        for an illustration in 2-3 sentences that an artist could use:
        
        {story_text[:300]}
        
        Focus on: setting, character appearance, mood, and key visual elements.
        Make it vivid and specific for a children's storybook illustration.""")
        
        image_description = response.text
        logger.info(f"📝 Image description generated: {image_description[:100]}...")
        
        # For now, return the description
        # In production, you would use this with an actual image generation API
        # like DALL-E, Midjourney, or Stable Diffusion
        
        return {
            "image_file": output_file,
            "description": image_description,
            "status": "description_generated"
        }
        
    except Exception as e:
        logger.error(f"❌ Image generation failed: {e}")
        return {
            "image_file": None,
            "description": "Image generation unavailable",
            "status": "failed",
            "error": str(e)
        }


def generate_image_with_imagen(story_text: str, theme: str, output_file: str = "story_image.png") -> str:
    """
    Alternative: Generate image using Google's Imagen API
    Note: This requires access to Vertex AI and Imagen
    """
    try:
        from vertexai.preview.vision_models import ImageGenerationModel
        
        # Initialize Imagen model
        model = ImageGenerationModel.from_pretrained("imagegeneration@005")
        
        # Create prompt
        prompt = f"""A beautiful storybook illustration: {story_text[:200]}. 
        Style: colorful, child-friendly, whimsical, warm colors, soft edges"""
        
        # Generate image
        images = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio="1:1",
        )
        
        # Save the image
        images[0].save(output_file)
        logger.info(f"✅ Image saved to {output_file}")
        
        return output_file
        
    except Exception as e:
        logger.error(f"❌ Imagen generation failed: {e}")
        return None
