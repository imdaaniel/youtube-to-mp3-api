import pytest
from app.utils.validators import validate_youtube_url

class TestValidateYoutubeUrl:
    """Testes para validação de URLs do YouTube"""
    
    def test_valid_youtube_watch_url(self):
        """Deve validar URL padrão do YouTube watch"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        assert validate_youtube_url(url) is True
    
    def test_valid_youtube_short_url(self):
        """Deve validar URL encurtada youtu.be"""
        url = "https://youtu.be/dQw4w9WgXcQ"
        assert validate_youtube_url(url) is True
    
    def test_valid_youtube_shorts_url(self):
        """Deve validar URL do YouTube Shorts"""
        url = "https://www.youtube.com/shorts/ABC123def456"
        assert validate_youtube_url(url) is True
    
    def test_valid_youtube_no_www(self):
        """Deve validar YouTube sem www"""
        url = "https://youtube.com/watch?v=dQw4w9WgXcQ"
        assert validate_youtube_url(url) is True
    
    def test_invalid_google_url(self):
        """Deve rejeitar URL do Google"""
        url = "https://google.com/search?q=test"
        assert validate_youtube_url(url) is False
    
    def test_invalid_vimeo_url(self):
        """Deve rejeitar URL do Vimeo"""
        url = "https://vimeo.com/123456789"
        assert validate_youtube_url(url) is False
    
    def test_invalid_malformed_url(self):
        """Deve rejeitar URL malformada"""
        url = "not-a-url"
        assert validate_youtube_url(url) is False
    
    def test_empty_string(self):
        """Deve rejeitar string vazia"""
        url = ""
        assert validate_youtube_url(url) is False
    
    def test_youtube_with_parameters(self):
        """Deve validar YouTube com parâmetros adicionais"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=10s&list=ABC"
        assert validate_youtube_url(url) is True
    
    def test_http_protocol(self):
        """Deve validar com protocolo HTTP"""
        url = "http://www.youtube.com/watch?v=dQw4w9WgXcQ"
        assert validate_youtube_url(url) is True
