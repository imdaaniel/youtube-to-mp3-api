import pytest
import re
from app.utils.id_generator import generate_video_id

class TestGenerateVideoId:
    """Testes para geração de IDs únicos"""
    
    def test_generates_valid_format(self):
        """Deve gerar ID com formato correto timestamp_hash"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        video_id = generate_video_id(url)
        
        # Padrão: timestamp_8caracteres
        pattern = r"^\d+_[a-f0-9]{8}$"
        assert re.match(pattern, video_id), f"ID não segue formato: {video_id}"
    
    def test_generates_different_ids_for_different_urls(self):
        """Deve gerar IDs diferentes para URLs diferentes"""
        url1 = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        url2 = "https://www.youtube.com/watch?v=abc123def456"
        
        id1 = generate_video_id(url1)
        id2 = generate_video_id(url2)
        
        assert id1 != id2, "IDs deveriam ser diferentes para URLs diferentes"
    
    def test_hash_consistent_for_same_url(self):
        """A parte de hash deve ser consistente para a mesma URL"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
        # Gerar múltiplas vezes (timestamp vai variar, hash não)
        ids = [generate_video_id(url) for _ in range(3)]
        
        # Extrair hashes (última parte após _)
        hashes = [vid.split('_')[1] for vid in ids]
        
        # Todos os hashes devem ser iguais
        assert len(set(hashes)) == 1, "Hash deveria ser consistente para mesma URL"
    
    def test_hash_length_is_8(self):
        """Hash deve ter exatamente 8 caracteres"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        video_id = generate_video_id(url)
        
        hash_part = video_id.split('_')[1]
        assert len(hash_part) == 8, f"Hash deveria ter 8 caracteres, tem {len(hash_part)}"
    
    def test_timestamp_increases(self):
        """Timestamp deve aumentar entre chamadas"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
        id1 = generate_video_id(url)
        id2 = generate_video_id(url)
        
        timestamp1 = int(id1.split('_')[0])
        timestamp2 = int(id2.split('_')[0])
        
        assert timestamp2 >= timestamp1, "Timestamp deveria aumentar ou manter"
    
    def test_empty_string_url(self):
        """Deve lidar com URL vazia"""
        url = ""
        video_id = generate_video_id(url)
        
        # Não deve lançar erro, apenas gerar um ID
        assert video_id is not None
        assert '_' in video_id
    
    def test_special_characters_in_url(self):
        """Deve lidar com caracteres especiais na URL"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=10s&list=ABC_123"
        video_id = generate_video_id(url)
        
        # Não deve lançar erro
        assert video_id is not None
        assert re.match(r"^\d+_[a-f0-9]{8}$", video_id)
