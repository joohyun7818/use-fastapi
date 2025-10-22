# config.py
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """애플리케이션 설정 (pydantic-settings v2 최신 패턴)"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # .env 파일의 정의되지 않은 변수 무시
    )

    # 애플리케이션 메타정보
    app_name: str = Field(
        default="Kaira Server",
        description="애플리케이션 이름",
    )
    app_version: str = Field(
        default="0.1.0",
        description="애플리케이션 버전",
    )

    # 실행 환경 설정
    environment: str = Field(
        default="development",
        description="실행 환경 (development, staging, production)",
    )
    debug: bool = Field(
        default=True,
        description="디버그 모드 활성화 여부",
    )

    # 정적 파일 경로
    static_files_path: str = Field(
        default="kaira-1.0.0",
        description="프론트엔드 정적 파일 폴더 경로 (src/kaira_fastapi_poetry/ 기준)",
    )


# 싱글톤 인스턴스 생성 (애플리케이션 전역에서 사용)
settings = Settings()
