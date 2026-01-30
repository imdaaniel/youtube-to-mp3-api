import pytest
from pathlib import Path
from fastapi.testclient import TestClient
import shutil
import sys

# Adicionar app ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app
from app.config import settings

@pytest.fixture
def client():
    """Cliente de teste para a API"""
    return TestClient(app)

@pytest.fixture
def temp_dir_test(tmp_path):
    """Diretório temporário para testes"""
    test_temp = tmp_path / "temp_test"
    test_temp.mkdir()
    
    # Backup do temp original
    original_temp = settings.TEMP_DIR
    settings.TEMP_DIR = test_temp
    
    yield test_temp
    
    # Restaurar e limpar
    settings.TEMP_DIR = original_temp
    if test_temp.exists():
        shutil.rmtree(test_temp)

@pytest.fixture
def sample_urls():
    """URLs de amostra para testes"""
    return {
        "valid_regular": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "valid_short": "https://youtu.be/dQw4w9WgXcQ",
        "valid_youtube_short": "https://www.youtube.com/shorts/ABC123",
        "invalid_youtube": "https://youtube.com/invalid",
        "invalid_url": "https://google.com/search?q=test",
        "malformed_url": "not-a-url",
    }
