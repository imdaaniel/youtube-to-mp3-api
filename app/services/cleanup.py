import shutil
from pathlib import Path
from datetime import datetime
from app.config import settings

def cleanup_old_files() -> None:
    """Remove arquivos e pastas temporárias com mais de X minutos"""
    if not settings.TEMP_DIR.exists():
        return
    
    current_time = datetime.now().timestamp()
    deleted_count = 0
    
    # Deletar pastas antigas (cada pasta contém um vídeo)
    for folder in settings.TEMP_DIR.iterdir():
        if folder.is_dir():
            folder_age = current_time - folder.stat().st_mtime
            if folder_age > settings.FILE_TTL_SECONDS:
                try:
                    shutil.rmtree(folder)
                    deleted_count += 1
                    print(f"[CLEANUP] Pasta deletada: {folder.name}")
                except Exception as e:
                    print(f"[CLEANUP] Erro ao deletar pasta {folder.name}: {str(e)}")
    
    if deleted_count > 0:
        print(f"[CLEANUP] Total de pastas limpas: {deleted_count}")

def cleanup_all_temp_files() -> None:
    """Remove todos os arquivos temporários"""
    if settings.TEMP_DIR.exists():
        try:
            shutil.rmtree(settings.TEMP_DIR)
            settings.TEMP_DIR.mkdir(exist_ok=True)
            print("[CLEANUP] Todos os arquivos temporários foram removidos")
        except Exception as e:
            print(f"[CLEANUP] Erro ao limpar temp: {str(e)}")
