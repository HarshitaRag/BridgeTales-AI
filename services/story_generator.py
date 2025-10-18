import os
import json
import asyncio
from typing import Dict, Optional, List, Any
import boto3
import openai
from botocore.exceptions import ClientError, NoCredentialsError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StoryGenerator:
    def __init__(self):
        self.aws_region = os.getenv("AWS_REGION", "us-east-2")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize AWS Bedrock client (primary)
        try:
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                region_name=self.aws_region
            )
            logger.info(f"✅ AWS Bedrock client initialized for region: {self.aws_region}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize AWS Bedrock client: {e}")
            self.bedrock_client = None
        
        # Initialize OpenAI client (optional backup)
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
            logger.info("✅ OpenAI client initialized successfully")
        else:
            logger.info("ℹ️  OpenAI API key not found - using Bedrock only")
    
    async def check_bedrock_connection(self) -> bool:
        """Check if AWS Bedrock connection is available"""
        try:
            if not self.bedrock_client:
                return False
            
            # List available models to test connection
            bedrock_client_list = boto3.client('bedrock', region_name=self.aws_region)
            response = bedrock_client_list.list_foundation_models()
            return True
        except Exception as e:
            logger.error(f"Bedrock connection check failed: {e}")
            return False
    
    async def check_openai_connection(self) -> bool:
        """Check if OpenAI connection is available"""
        try:
            if not self.openai_api_key:
                return False
            
            # Test with a simple completion
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.error(f"OpenAI connection check failed: {e}")
            return False
    
    def _build_bedrock_prompt(self, prompt: str, genre: Optional[str] = None, 
                            characters: Optional[List[str]] = None, 
                            setting: Optional[str] = None) -> str:
        """Build a comprehensive prompt for Bedrock"""
        system_prompt = """You are a creative storyteller. Write engaging, well-structured stories based on the given prompts. 
        Focus on character development, vivid descriptions, and compelling narratives."""
        
        user_prompt = f"Write a story based on this prompt: {prompt}"
        
        if genre:
            user_prompt += f"\nGenre: {genre}"
        if characters:
            user_prompt += f"\nCharacters: {', '.join(characters)}"
        if setting:
            user_prompt += f"\nSetting: {setting}"
        
        user_prompt += "\n\nMake the story engaging and well-written."
        
        return f"{system_prompt}\n\n{user_prompt}"
    
    def _build_openai_prompt(self, prompt: str, genre: Optional[str] = None, 
                           characters: Optional[List[str]] = None, 
                           setting: Optional[str] = None) -> List[Dict[str, str]]:
        """Build a prompt for OpenAI Chat API"""
        messages = [
            {
                "role": "system", 
                "content": "You are a creative storyteller. Write engaging, well-structured stories based on the given prompts. Focus on character development, vivid descriptions, and compelling narratives."
            }
        ]
        
        user_content = f"Write a story based on this prompt: {prompt}"
        
        if genre:
            user_content += f"\nGenre: {genre}"
        if characters:
            user_content += f"\nCharacters: {', '.join(characters)}"
        if setting:
            user_content += f"\nSetting: {setting}"
        
        messages.append({"role": "user", "content": user_content})
        return messages
    
    async def _generate_with_bedrock(self, prompt: str, max_length: int, 
                                   temperature: float, genre: Optional[str] = None,
                                   characters: Optional[List[str]] = None,
                                   setting: Optional[str] = None) -> Dict[str, Any]:
        """Generate story using AWS Bedrock"""
        try:
            # Use Claude model (adjust model ID as needed)
            model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
            
            full_prompt = self._build_bedrock_prompt(prompt, genre, characters, setting)
            
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_length,
                "temperature": temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ]
            }
            
            response = self.bedrock_client.invoke_model(
                modelId=model_id,
                body=json.dumps(body),
                contentType='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            story = response_body['content'][0]['text']
            
            return {
                "story": story,
                "model_used": f"Bedrock-{model_id}"
            }
            
        except Exception as e:
            logger.error(f"Bedrock generation failed: {e}")
            raise Exception(f"Bedrock story generation failed: {str(e)}")
    
    async def _generate_with_openai(self, prompt: str, max_length: int, 
                                  temperature: float, genre: Optional[str] = None,
                                  characters: Optional[List[str]] = None,
                                  setting: Optional[str] = None) -> Dict[str, Any]:
        """Generate story using OpenAI as backup"""
        try:
            messages = self._build_openai_prompt(prompt, genre, characters, setting)
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=max_length,
                temperature=temperature
            )
            
            story = response.choices[0].message.content
            
            return {
                "story": story,
                "model_used": "OpenAI-GPT-3.5-Turbo"
            }
            
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise Exception(f"OpenAI story generation failed: {str(e)}")
    
    async def generate_story(self, prompt: str, max_length: int = 500, 
                           temperature: float = 0.7, genre: Optional[str] = None,
                           characters: Optional[List[str]] = None,
                           setting: Optional[str] = None) -> Dict[str, Any]:
        """Generate a story using the best available service"""
        
        # Try Bedrock first (primary)
        if self.bedrock_client and await self.check_bedrock_connection():
            try:
                logger.info("🚀 Generating story with AWS Bedrock")
                return await self._generate_with_bedrock(
                    prompt, max_length, temperature, genre, characters, setting
                )
            except Exception as e:
                logger.warning(f"⚠️  Bedrock failed: {e}")
                
                # Try OpenAI backup if available
                if self.openai_api_key and await self.check_openai_connection():
                    try:
                        logger.info("🔄 Falling back to OpenAI")
                        return await self._generate_with_openai(
                            prompt, max_length, temperature, genre, characters, setting
                        )
                    except Exception as openai_error:
                        logger.error(f"❌ OpenAI backup also failed: {openai_error}")
                else:
                    logger.error("❌ No OpenAI backup available")
        else:
            logger.error("❌ AWS Bedrock is not available")
            
            # Try OpenAI as last resort if available
            if self.openai_api_key and await self.check_openai_connection():
                try:
                    logger.info("🔄 Using OpenAI as primary (Bedrock unavailable)")
                    return await self._generate_with_openai(
                        prompt, max_length, temperature, genre, characters, setting
                    )
                except Exception as e:
                    logger.error(f"❌ OpenAI also failed: {e}")
        
        raise Exception("❌ All AI services are unavailable. Please check your AWS Bedrock configuration.")
