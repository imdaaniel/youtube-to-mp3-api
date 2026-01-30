from pathlib import Path
from typing import Optional

class Settings:
    """Configurações da aplicação"""
    
    # App
    APP_TITLE: str = "YT to MP3 API"
    APP_DESCRIPTION: str = "API para converter vídeos do YouTube em MP3"
    APP_VERSION: str = "1.0.0"
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    TEMP_DIR: Path = BASE_DIR / "temp"
    
    # Cleanup
    CLEANUP_INTERVAL_MINUTES: int = 2
    FILE_TTL_SECONDS: int = 300  # 5 minutos
    
    # Download
    SOCKET_TIMEOUT: int = 60
    RETRIES: int = 5
    FRAGMENT_RETRIES: int = 5
    
    def __init__(self):
        """Inicializar e criar diretórios necessários"""
        self.TEMP_DIR.mkdir(exist_ok=True)

settings = Settings()
