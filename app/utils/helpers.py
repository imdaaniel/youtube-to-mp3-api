from typing import Optional

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