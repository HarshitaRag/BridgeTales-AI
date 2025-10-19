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
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("❌ GEMINI_API_KEY not found")
            return {
                "image_file": None,
                "description": "Gemini API key not configured",
                "status": "failed"
            }
            
        genai.configure(api_key=api_key)
        
        # Use the correct Gemini model - gemini-1.5-pro or gemini-1.0-pro
        try:
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
        except:
            # Fallback to older model
            model = genai.GenerativeModel('gemini-1.0-pro-latest')
        
        logger.info(f"🎨 Generating illustration description with Gemini...")
        
        # Generate a vivid visual description
        prompt = f"""You are a children's book illustrator. Based on this story segment about {theme}, 
create a detailed visual description for an illustration in 2-3 sentences:

Story: {story_text[:400]}

Describe: the setting, main character(s), their appearance, actions, mood, colors, and atmosphere.
Make it vivid, specific, and suitable for a whimsical children's storybook illustration."""
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            image_description = response.text.strip()
            logger.info(f"✅ Image description generated successfully")
            logger.info(f"📝 Description: {image_description[:100]}...")
            
            return {
                "image_file": None,  # Not generating actual images yet
                "description": image_description,
                "status": "description_generated"
            }
        else:
            logger.warning("⚠️ Empty response from Gemini")
            return {
                "image_file": None,
                "description": f"A beautiful storybook scene about {theme}",
                "status": "fallback"
            }
        
    except Exception as e:
        logger.error(f"❌ Image generation failed: {e}")
        # Return a fallback description
        return {
            "image_file": None,
            "description": f"A colorful, whimsical illustration depicting a scene about {theme} with warm, inviting colors and child-friendly characters.",
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
