from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str
    supabase_url: str
    supabase_key: str
    image_generation_url: str = "https://image.pollinations.ai/prompt"

    class Config:
        env_file = ".env"

settings = Settings()