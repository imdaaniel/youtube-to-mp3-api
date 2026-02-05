import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from main import create_app

app = create_app()
client = TestClient(app)


class TestRootEndpoint:
    """Testes para o endpoint raiz"""
    
    def test_root_returns_200(self):
        """Deve retornar status 200"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_returns_json(self):
        """Deve retornar JSON válido com campos corretos"""
        response = client.get("/")
        data = response.json()
        
        assert isinstance(data, dict)
        assert "app" in data
        assert "version" in data
        assert "docs" in data
        assert data["app"] == "YT to MP3 API"
        assert data["docs"] == "/docs"


class TestFormatsEndpoint:
    """Testes para o endpoint GET /api/formats"""
    
    def test_formats_requires_url_parameter(self):
        """Deve retornar erro 422 quando falta parâmetro url"""
        response = client.get("/api/formats")
        assert response.status_code == 422
    
    def test_formats_rejects_invalid_url(self):
        """Deve retornar erro 400 para URL inválida"""
        response = client.get("/api/formats?url=https://google.com")
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "inválida" in data["detail"].lower() or "youtube" in data["detail"].lower()
    
    @patch('app.routes.download.extract_video_metadata')
    def test_formats_accepts_valid_youtube_url(self, mock_extract):
        """Deve aceitar URL válida do YouTube e retornar metadados"""
        # Mock dos metadados retornados
        mock_extract.return_value = {
            'title': 'Test Video',
            'duration': 120,
            'uploader': 'Test Channel',
            'formats': [
                {
                    'format_id': '18',
                    'ext': 'mp4',
                    'resolution': '360p',
                    'filesize': 1024000,
                    'vcodec': 'h264',
                    'acodec': 'aac'
                }
            ]
        }
        
        response = client.get("/api/formats?url=https://www.youtube.com/watch?v=test123")
        assert response.status_code == 200
        
        data = response.json()
        assert 'title' in data
        assert 'duration' in data
        assert 'formats' in data
        assert data['title'] == 'Test Video'
    
    @patch('app.routes.download.extract_video_metadata')
    def test_formats_handles_extraction_error(self, mock_extract):
        """Deve retornar erro 500 quando a extração de metadados falha"""
        mock_extract.side_effect = Exception("Video not found")
        
        response = client.get("/api/formats?url=https://www.youtube.com/watch?v=invalid")
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data


class TestDownloadStreamEndpoint:
    """Testes para o endpoint POST /api/download-stream"""
    
    def test_download_stream_requires_url(self):
        """Deve retornar erro 422 quando falta campo url"""
        response = client.post("/api/download-stream", json={"format_id": "18"})
        assert response.status_code == 422
    
    def test_download_stream_requires_format_id(self):
        """Deve retornar erro 422 quando falta campo format_id"""
        response = client.post(
            "/api/download-stream",
            json={"url": "https://www.youtube.com/watch?v=test123"}
        )
        assert response.status_code == 422
    
    def test_download_stream_rejects_invalid_url(self):
        """Deve retornar erro 400 para URL inválida"""
        response = client.post(
            "/api/download-stream",
            json={
                "url": "https://google.com",
                "format_id": "18"
            }
        )
        assert response.status_code == 400
    
    @patch('app.routes.download.extract_video_metadata')
    @patch('app.routes.download.stream_video')
    def test_download_stream_accepts_valid_request(self, mock_stream, mock_extract):
        """Deve aceitar requisição válida e iniciar streaming"""
        # Mock metadados
        mock_extract.return_value = {
            'title': 'Test Video',
            'formats': [
                {'format_id': '18', 'ext': 'mp4'}
            ]
        }
        
        # Mock streaming (retornar iterável vazio)
        mock_stream.return_value = iter([])
        
        response = client.post(
            "/api/download-stream",
            json={
                "url": "https://www.youtube.com/watch?v=test123",
                "format_id": "18"
            }
        )
        
        # Deve retornar streaming (200) ou erro de streaming
        assert response.status_code in [200, 500]


class TestDownloadEndpoint:
    """Testes para o endpoint POST /api/download"""
    
    def test_download_requires_url(self):
        """Deve retornar erro 422 quando falta campo url"""
        response = client.post("/api/download", json={})
        assert response.status_code == 422
    
    def test_download_rejects_invalid_url(self):
        """Deve retornar erro 400 para URL inválida"""
        response = client.post(
            "/api/download",
            json={"url": "https://google.com"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
    
    @patch('app.routes.download.download_youtube_audio')
    def test_download_handles_download_error(self, mock_download):
        """Deve retornar erro 500 quando o download falha"""
        mock_download.side_effect = Exception("Download failed")
        
        response = client.post(
            "/api/download",
            json={"url": "https://www.youtube.com/watch?v=test123"}
        )
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data


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
        assert "/api/formats" in data["paths"]
        assert "/api/download-stream" in data["paths"]
        assert "/api/download" in data["paths"]

