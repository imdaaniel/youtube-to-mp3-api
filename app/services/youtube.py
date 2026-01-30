import asyncio
from pathlib import Path
from app.config import settings
from app.core.downloader import download_audio

async def download_youtube_audio(url: str, video_id: str) -> Path:
    """
    Baixa áudio do YouTube usando yt-dlp.
    
    Args:
        url: URL do vídeo do YouTube
        video_id: ID único para organizar os arquivos
    
    Returns:
        Path: Caminho do arquivo MP3 gerado
        
    Raises:
        Exception: Se o download ou processamento falhar
    """
    output_dir = settings.TEMP_DIR / video_id
    output_dir.mkdir(exist_ok=True)
    
    print(f"[{video_id}] Iniciando download: {url}")
    
    # Executar download em thread separada (não bloqueia event loop)
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None,
        download_audio,
        url,
        str(output_dir)
    )
    
    # Procurar o arquivo MP3 gerado
    mp3_files = list(output_dir.glob("*.mp3"))
    
    if not mp3_files:
        raise Exception("Arquivo MP3 não foi gerado após o download")
    
    mp3_file = mp3_files[0]
    print(f"[{video_id}] Download concluído: {mp3_file.name}")
    
    return mp3_file
