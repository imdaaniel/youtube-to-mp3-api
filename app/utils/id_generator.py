import hashlib
from datetime import datetime

def generate_video_id(url: str) -> str:
    """Gera ID único usando timestamp + hash da URL"""
    timestamp = int(datetime.now().timestamp() * 1000)
    url_hash = hashlib.md5(str(url).encode()).hexdigest()[:8]
    return f"{timestamp}_{url_hash}"
