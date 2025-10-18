import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # AWS Configuration
    AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    # OpenAI Configuration (optional backup)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # ElevenLabs Configuration
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    
    # Application Configuration
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        missing_configs = []
        warnings = []
        
        # AWS Bedrock is required
        if not cls.AWS_ACCESS_KEY_ID:
            missing_configs.append("AWS_ACCESS_KEY_ID")
        if not cls.AWS_SECRET_ACCESS_KEY:
            missing_configs.append("AWS_SECRET_ACCESS_KEY")
        
        # OpenAI is optional (backup only)
        if not cls.OPENAI_API_KEY:
            warnings.append("OPENAI_API_KEY (optional backup)")
        
        # ElevenLabs is required for voice generation
        if not cls.ELEVENLABS_API_KEY:
            missing_configs.append("ELEVENLABS_API_KEY")
        
        if missing_configs:
            print(f"❌ Missing required configuration: {', '.join(missing_configs)}")
            print("Please set these environment variables or create a .env file")
            return False
        
        if warnings:
            print(f"⚠️  Optional configuration missing: {', '.join(warnings)}")
            print("Bedrock will be used as primary, no OpenAI backup available")
        
        print(f"✅ AWS Bedrock configured for region: {cls.AWS_REGION}")
        return True
