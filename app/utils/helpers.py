from typing import Optional
import re
import hashlib
from datetime import datetime

def sanitize_filename(filename: str) -> str:
    """
    Normaliza nome de arquivo removendo caracteres especiais.
    Segue a mesma lógica do restrictfilenames do yt-dlp.
    
    Args:
        filename: Nome do arquivo a ser normalizado
    
    Returns:
        str: Nome do arquivo normalizado (apenas A-Z, a-z, 0-9, ponto, hífen, underscore)
    """
    # Remove ou substitui caracteres não-ASCII e especiais
    # Permite apenas: A-Z, a-z, 0-9, ponto, hífen, underscore
    filename = re.sub(r'[^\w\s\-\.]', '', filename)
    # Substitui espaços por underscore
    filename = re.sub(r'\s+', '_', filename)
    # Remove underscores múltiplos
    filename = re.sub(r'_+', '_', filename)
    # Remove pontos e underscores no início/fim
    filename = filename.strip('._')
    
    return filename


def format_duration(seconds: int) -> str:
    """Formata duração em segundos para formato HH:MM:SS (estilo YouTube)"""
    if not seconds:
        return "0:00"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"


def format_filesize(bytes_size: Optional[float]) -> Optional[str]:
    """Formata tamanho em bytes para unidade legível (KB, MB, GB, etc) com 1 casa decimal"""
    if bytes_size is None or bytes_size == 0:
        return None
    
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = float(bytes_size)
    
    for unit in units:
        if size < 1024:
            if unit == 'B':
                return f"{int(size)}{unit}"
            return f"{size:.1f}{unit}"
        size /= 1024
    
    return f"{size:.1f}PB"

def generate_video_id(url: str) -> str:
    """Gera ID único usando timestamp + hash da URL"""
    timestamp = int(datetime.now().timestamp() * 1000)
    url_hash = hashlib.md5(str(url).encode()).hexdigest()[:8]
    return f"{timestamp}_{url_hash}"