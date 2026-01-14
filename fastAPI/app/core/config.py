"""DICT Procurement Management System - Configuration Settings"""

from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    # Application
    APP_NAME: str = "DICT Procurement Management System"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 3306
    DATABASE_NAME: str = "dict_procurement"
    DATABASE_USER: str = "root"
    DATABASE_PASSWORD: str = ""
    DATABASE_CHARSET: str = "utf8mb4"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 3600
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct async MySQL database URL"""
        return (
            f"mysql+aiomysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
            f"?charset={self.DATABASE_CHARSET}"
        )
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    
    @property
    def REDIS_URL(self) -> str:
        """Construct Redis URL"""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # JWT Authentication
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Password Policy
    PASSWORD_MIN_LENGTH: int = 12
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_NUMBERS: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = True
    PASSWORD_BCRYPT_COST: int = 12
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    LOGIN_RATE_LIMIT: int = 5
    LOGIN_LOCKOUT_MINUTES: int = 15
    
    # Session Timeout
    SESSION_TIMEOUT_MINUTES: int = 120
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: str = "pdf,doc,docx,xls,xlsx,png,jpg,jpeg"
    QUOTATION_MAX_FILE_SIZE_MB: int = 5
    
    @property
    def ALLOWED_FILE_EXTENSIONS(self) -> List[str]:
        """Parse allowed file types into list"""
        return [ext.strip() for ext in self.ALLOWED_FILE_TYPES.split(",")]
    
    # Email Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "noreply@dict.gov.ph"
    SMTP_USE_TLS: bool = True
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:3000"
    
    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        """Parse CORS origins into list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # Celery Configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    CELERY_TASK_ALWAYS_EAGER: bool = False
    
    # PDF Generation
    PDF_TEMP_DIR: str = "temp/pdfs"
    PDF_LOGO_PATH: str = "assets/dict-logo.png"
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Government Procurement Constants
    PR_NUMBER_PREFIX: str = "PR"
    RFQ_NUMBER_PREFIX: str = "RFQ"
    CANVASS_NUMBER_PREFIX: str = "CANVASS"
    BAC_DOCUMENT_NUMBER_PREFIX: str = "BAC"
    PO_NUMBER_PREFIX: str = "PO"
    
    # Audit Logging
    AUDIT_LOG_RETENTION_DAYS: int = 365
    
    # Feature Flags
    ENABLE_EMAIL_NOTIFICATIONS: bool = True
    ENABLE_TWO_FACTOR_AUTH: bool = True
    ENABLE_TWO_FACTOR_ROLES: str = "ADMIN,PROCUREMENT_OFFICER"
    
    @property
    def TWO_FACTOR_ROLES_LIST(self) -> List[str]:
        """Parse 2FA roles into list"""
        return [role.strip() for role in self.ENABLE_TWO_FACTOR_ROLES.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Export settings instance
settings = get_settings()
