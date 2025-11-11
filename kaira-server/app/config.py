# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    """애플리케이션 설정"""
  
    # 앱 설정
    app_name: str = "Kaira Static Server"
    debug: bool = False
    environment: str = "development"
  
    # 서버 설정
    host: str = "0.0.0.0"
    port: int = 8000
  
    # 정적 파일 경로
    static_dir: str = "../../kaira-1.0.0"
  
    # 로그 설정
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
  
    # 데이터베이스 (향후 사용)
    database_url: str = "sqlite:///./app.db"
  
    model_config = SettingsConfigDict(
        env_file=".env",  # 현재 디렉토리에서 .env 파일 찾기
        env_file_encoding="utf-8",
        case_sensitive=False
    )
  
    @property
    def static_path(self) -> Path:
        """정적 파일 절대 경로"""
        return Path(__file__).parent.parent.parent / self.static_dir

# 전역 설정 인스턴스
settings = Settings()