import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # AWS Configuration
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
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
        
        if not cls.AWS_ACCESS_KEY_ID:
            missing_configs.append("AWS_ACCESS_KEY_ID")
        if not cls.AWS_SECRET_ACCESS_KEY:
            missing_configs.append("AWS_SECRET_ACCESS_KEY")
        if not cls.OPENAI_API_KEY:
            missing_configs.append("OPENAI_API_KEY")
        
        if missing_configs:
            print(f"Warning: Missing configuration for: {', '.join(missing_configs)}")
            print("Please set these environment variables or create a .env file")
        
        return len(missing_configs) == 0
