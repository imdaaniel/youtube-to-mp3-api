import pytest
from pathlib import Path
from datetime import datetime
import time
from app.services.cleanup import cleanup_old_files, cleanup_all_temp_files
from app.config import settings

class TestCleanupOldFiles:
    """Testes para limpeza de arquivos antigos"""
    
    def test_removes_files_older_than_ttl(self, tmp_path):
        """Deve remover pastas mais antigas que TTL"""
        # Criar pasta de teste
        old_folder = tmp_path / "old_video_folder"
        old_folder.mkdir()
        
        # Criar arquivo dentro
        old_file = old_folder / "audio.mp3"
        old_file.write_text("dummy audio")
        
        # Simular que é antigo (mudar mtime)
        old_time = datetime.now().timestamp() - (settings.FILE_TTL_SECONDS + 100)
        import os
        os.utime(old_folder, (old_time, old_time))
        
        # Backup do temp original
        original_temp = settings.TEMP_DIR
        settings.TEMP_DIR = tmp_path
        
        try:
            cleanup_old_files()
            
            # Pasta deveria ter sido deletada
            assert not old_folder.exists(), "Pasta antiga deveria ter sido deletada"
        finally:
            settings.TEMP_DIR = original_temp
    
    def test_does_not_remove_recent_files(self, tmp_path):
        """Não deve remover pastas recentes"""
        # Criar pasta de teste
        new_folder = tmp_path / "new_video_folder"
        new_folder.mkdir()
        
        # Criar arquivo dentro
        new_file = new_folder / "audio.mp3"
        new_file.write_text("dummy audio")
        
        # Backup do temp original
        original_temp = settings.TEMP_DIR
        settings.TEMP_DIR = tmp_path
        
        try:
            cleanup_old_files()
            
            # Pasta deveria continuar existindo
            assert new_folder.exists(), "Pasta recente não deveria ser deletada"
        finally:
            settings.TEMP_DIR = original_temp
    
    def test_handles_empty_temp_dir(self, tmp_path):
        """Deve lidar corretamente com diretório vazio"""
        original_temp = settings.TEMP_DIR
        settings.TEMP_DIR = tmp_path
        
        try:
            # Não deve lançar erro
            cleanup_old_files()
            assert True
        finally:
            settings.TEMP_DIR = original_temp
    
    def test_handles_nonexistent_temp_dir(self):
        """Deve lidar corretamente com diretório que não existe"""
        original_temp = settings.TEMP_DIR
        settings.TEMP_DIR = Path("/nonexistent/path")
        
        try:
            # Não deve lançar erro
            cleanup_old_files()
            assert True
        finally:
            settings.TEMP_DIR = original_temp

class TestCleanupAllTempFiles:
    """Testes para limpeza total de arquivos temporários"""
    
    def test_removes_all_temp_files(self, tmp_path):
        """Deve remover todos os arquivos temporários"""
        # Criar múltiplas pastas
        folder1 = tmp_path / "video1"
        folder2 = tmp_path / "video2"
        folder1.mkdir()
        folder2.mkdir()
        
        (folder1 / "audio.mp3").write_text("dummy")
        (folder2 / "audio.mp3").write_text("dummy")
        
        original_temp = settings.TEMP_DIR
        settings.TEMP_DIR = tmp_path
        
        try:
            cleanup_all_temp_files()
            
            # Diretório temp deveria ter sido deletado e recriado vazio
            assert settings.TEMP_DIR.exists(), "Diretório temp deveria ser recriado"
            assert len(list(settings.TEMP_DIR.iterdir())) == 0, "Temp deveria estar vazio"
        finally:
            settings.TEMP_DIR = original_temp
    
    def test_recreates_temp_directory(self, tmp_path):
        """Deve recriar o diretório temp após deletar"""
        original_temp = settings.TEMP_DIR
        settings.TEMP_DIR = tmp_path
        
        try:
            cleanup_all_temp_files()
            
            # Diretório deveria ser recriado
            assert settings.TEMP_DIR.exists(), "Diretório temp deveria ser recriado"
            assert settings.TEMP_DIR.is_dir(), "Temp deveria ser um diretório"
        finally:
            settings.TEMP_DIR = original_temp
