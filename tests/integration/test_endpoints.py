import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestRootEndpoint:
    """Testes para o endpoint raiz"""
    
    def test_root_returns_200(self):
        """Deve retornar status 200"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_returns_json(self):
        """Deve retornar JSON válido"""
        response = client.get("/")
        data = response.json()
        
        assert isinstance(data, dict)
        assert "app" in data
        assert "version" in data
        assert "docs" in data
    
    def test_root_has_correct_fields(self):
        """Deve retornar campos corretos"""
        response = client.get("/")
        data = response.json()
        
        assert data["app"] == "YT to MP3 API"
        assert data["docs"] == "/docs"

class TestDownloadEndpoint:
    """Testes para o endpoint de download"""
    
    def test_download_with_invalid_url(self):
        """Deve retornar erro 400 para URL inválida"""
        response = client.post(
            "/api/download",
            json={"url": "https://google.com"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
    
    def test_download_with_malformed_json(self):
        """Deve retornar erro para JSON malformado"""
        response = client.post(
            "/api/download",
            json={"url": "not-a-url"}
        )
        
        # Pode ser 400 ou 422 dependendo da validação
        assert response.status_code in [400, 422]
    
    def test_download_without_url_field(self):
        """Deve retornar erro quando falta campo url"""
        response = client.post(
            "/api/download",
            json={}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_download_with_valid_youtube_url_fails_download(self):
        """Deve tentar fazer download com URL válida (simulado)"""
        with patch('app.routes.download.download_youtube_audio') as mock_download:
            # Simular erro no download
            mock_download.side_effect = Exception("Vídeo não encontrado")
            
            response = client.post(
                "/api/download",
                json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
            )
            
            # Deve retornar erro 500
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data
    
    def test_download_accepts_youtube_urls(self):
        """Deve aceitar URLs válidas do YouTube"""
        # Mock do download para não fazer requisição real
        with patch('app.routes.download.download_youtube_audio') as mock_download:
            mock_download.return_value = None
            
            # Esta requisição pode falhar por outros motivos, mas não por URL inválida
            response = client.post(
                "/api/download",
                json={"url": "https://www.youtube.com/watch?v=test123"}
            )
            
            # Se passou validação de URL, pode falhar em outro ponto
            assert response.status_code in [200, 500]

class TestDownloadEndpointWithVariousUrls:
    """Testes parametrizados para diferentes tipos de URL"""
    
    @pytest.mark.parametrize("invalid_url", [
        "https://google.com",
        "https://vimeo.com/123456",
        "not-a-url",
        "",
    ])
    def test_rejects_invalid_urls(self, invalid_url):
        """Deve rejeitar URLs inválidas"""
        response = client.post(
            "/api/download",
            json={"url": invalid_url}
        )
        
        assert response.status_code in [400, 422]
    
    @pytest.mark.parametrize("valid_youtube_url", [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://youtube.com/watch?v=dQw4w9WgXcQ",
    ])
    def test_accepts_valid_youtube_urls(self, valid_youtube_url):
        """Deve aceitar URLs válidas do YouTube"""
        with patch('app.routes.download.download_youtube_audio') as mock_download:
            mock_download.return_value = None
            
            response = client.post(
                "/api/download",
                json={"url": valid_youtube_url}
            )
            
            # Status pode variar, mas não deve ser 400 por URL inválida
            assert response.status_code != 400

class TestAPIDocumentation:
    """Testes para documentação automática da API"""
    
    def test_docs_endpoint_exists(self):
        """Deve ter endpoint de docs Swagger"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_openapi_schema_exists(self):
        """Deve gerar schema OpenAPI válido"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        data = response.json()
        assert "openapi" in data
        assert "paths" in data
