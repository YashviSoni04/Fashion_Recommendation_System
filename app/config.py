import os
from dotenv import load_dotenv

# Explicitly provide path to .env file relative to this file's location
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
print(f"Loading .env from: {dotenv_path}")
load_dotenv(dotenv_path)

print("DEBUG: GEMINI_API_KEY =", os.getenv("GEMINI_API_KEY"))

class Settings:
    # API Configuration
    API_TITLE: str = os.getenv("API_TITLE", "Fashion Recommendation API")
    API_DESCRIPTION: str = os.getenv("API_DESCRIPTION", "AI-powered fashion styling recommendations")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")
    
    # Gemini Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-1.5-flash"
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", 8000))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    def validate_settings(self):
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        return True

settings = Settings()