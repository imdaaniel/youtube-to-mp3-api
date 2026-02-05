import pytest
import re
from app.utils.helpers import (
    sanitize_filename,
    format_duration,
    format_filesize,
    generate_video_id
)


class TestSanitizeFilename:
    """Testes para sanitização de nomes de arquivo"""
    
    def test_removes_special_characters(self):
        """Deve remover caracteres especiais"""
        filename = "Video @#$% com símbolos!"
        result = sanitize_filename(filename)
        assert "@" not in result
        assert "#" not in result
        assert "%" not in result
        assert "!" not in result
    
    def test_replaces_spaces_with_underscores(self):
        """Deve substituir espaços por underscores"""
        filename = "Video com espaços"
        result = sanitize_filename(filename)
        assert " " not in result
        assert "_" in result
    
    def test_preserves_alphanumeric(self):
        """Deve preservar caracteres alfanuméricos"""
        filename = "Video123ABC"
        result = sanitize_filename(filename)
        assert "Video123ABC" in result
    
    def test_preserves_hyphens_and_dots(self):
        """Deve preservar hífens e pontos"""
        filename = "video-file.mp3"
        result = sanitize_filename(filename)
        assert "-" in result
        assert "." in result
    
    def test_removes_multiple_underscores(self):
        """Deve remover underscores múltiplos"""
        filename = "video    com    muitos    espacos"
        result = sanitize_filename(filename)
        # Não deve ter múltiplos underscores consecutivos
        assert "__" not in result
    
    def test_strips_leading_trailing_dots_underscores(self):
        """Deve remover pontos e underscores no início e fim"""
        filename = "___video.mp3___"
        result = sanitize_filename(filename)
        assert not result.startswith("_")
        assert not result.endswith("_")
    
    def test_empty_string(self):
        """Deve lidar com string vazia"""
        filename = ""
        result = sanitize_filename(filename)
        assert result == ""
    
    def test_only_special_characters(self):
        """Deve lidar com apenas caracteres especiais"""
        filename = "@#$%&*()"
        result = sanitize_filename(filename)
        # Deve retornar string vazia ou muito pequena
        assert len(result) == 0


class TestFormatDuration:
    """Testes para formatação de duração"""
    
    def test_zero_seconds(self):
        """Deve formatar 0 segundos corretamente"""
        result = format_duration(0)
        assert result == "0:00"
    
    def test_seconds_only(self):
        """Deve formatar apenas segundos"""
        result = format_duration(45)
        assert result == "0:45"
    
    def test_minutes_and_seconds(self):
        """Deve formatar minutos e segundos"""
        result = format_duration(125)  # 2:05
        assert result == "2:05"
    
    def test_hours_minutes_seconds(self):
        """Deve formatar horas, minutos e segundos"""
        result = format_duration(3665)  # 1:01:05
        assert result == "1:01:05"
    
    def test_exact_minute(self):
        """Deve formatar minuto exato"""
        result = format_duration(120)  # 2:00
        assert result == "2:00"
    
    def test_exact_hour(self):
        """Deve formatar hora exata"""
        result = format_duration(3600)  # 1:00:00
        assert result == "1:00:00"
    
    def test_padding_zero(self):
        """Deve adicionar zero à esquerda quando necessário"""
        result = format_duration(65)  # 1:05
        assert result == "1:05"
        
        result = format_duration(3605)  # 1:00:05
        assert result == "1:00:05"


class TestFormatFilesize:
    """Testes para formatação de tamanho de arquivo"""
    
    def test_none_value(self):
        """Deve retornar None para valor None"""
        result = format_filesize(None)
        assert result is None
    
    def test_zero_bytes(self):
        """Deve retornar None para 0 bytes"""
        result = format_filesize(0)
        assert result is None
    
    def test_bytes(self):
        """Deve formatar bytes sem decimal"""
        result = format_filesize(500)
        assert result == "500B"
    
    def test_kilobytes(self):
        """Deve formatar kilobytes com 1 casa decimal"""
        result = format_filesize(1536)  # 1.5 KB
        assert result == "1.5KB"
    
    def test_megabytes(self):
        """Deve formatar megabytes"""
        result = format_filesize(1048576)  # 1 MB
        assert result == "1.0MB"
        
        result = format_filesize(5242880)  # 5 MB
        assert result == "5.0MB"
    
    def test_gigabytes(self):
        """Deve formatar gigabytes"""
        result = format_filesize(1073741824)  # 1 GB
        assert result == "1.0GB"
    
    def test_exact_1024(self):
        """Deve formatar exatamente 1024 bytes como KB"""
        result = format_filesize(1024)
        assert result == "1.0KB"
    
    def test_float_input(self):
        """Deve aceitar entrada float"""
        result = format_filesize(1536.5)
        assert "KB" in result


class TestGenerateVideoId:
    """Testes para geração de IDs únicos"""
    
    def test_generates_valid_format(self):
        """Deve gerar ID com formato timestamp_hash"""
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
        
        # Os hashes devem ser diferentes
        hash1 = id1.split('_')[1]
        hash2 = id2.split('_')[1]
        assert hash1 != hash2
    
    def test_hash_consistent_for_same_url(self):
        """Hash deve ser consistente para a mesma URL"""
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
        assert len(hash_part) == 8
    
    def test_timestamp_increases(self):
        """Timestamp deve aumentar entre chamadas"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
        id1 = generate_video_id(url)
        id2 = generate_video_id(url)
        
        timestamp1 = int(id1.split('_')[0])
        timestamp2 = int(id2.split('_')[0])
        
        assert timestamp2 >= timestamp1
    
    def test_empty_string_url(self):
        """Deve lidar com URL vazia"""
        url = ""
        video_id = generate_video_id(url)
        
        assert video_id is not None
        assert '_' in video_id
        pattern = r"^\d+_[a-f0-9]{8}$"
        assert re.match(pattern, video_id)
    
    def test_special_characters_in_url(self):
        """Deve lidar com caracteres especiais na URL"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=10s&list=ABC_123"
        video_id = generate_video_id(url)
        
        assert video_id is not None
        pattern = r"^\d+_[a-f0-9]{8}$"
        assert re.match(pattern, video_id)
