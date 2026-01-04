from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):    
    # App
    app_name: str = "VisionHub"
    debug: bool = True
    
    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    jwt_secret_key: str = "dev-jwt-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 1440  # 24 hours
    
    # Database
    database_url: str = "postgresql://visionhub:visionhub123@localhost:5432/visionhub"
    
    # S3/MinIO
    s3_endpoint: str = "http://minio:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket: str = "visionhub"
    s3_public_url: str = "" 
    
    @property
    def s3_url_for_images(self) -> str:
        """URL to use in image_url field (public-accessible)"""
        if self.s3_public_url:
            return self.s3_public_url
        return self.s3_endpoint
            
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()