import yt_dlp
import os
import time

def download_audio(video_url: str, output_path: str = 'downloads') -> None:
    """
    Baixa o áudio de um vídeo do YouTube em formato MP3.
    
    Args:
        video_url: URL do vídeo do YouTube
        output_path: Caminho onde salvar o arquivo (padrão: 'downloads')
    """
    # Criar diretório se não existir
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Configurar opções do yt-dlp com strategies diferentes
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android'],  # Tentar clientes mobile
            }
        },
    }
    
    try:
        print(f"Baixando áudio de: {video_url}")
        time.sleep(1)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            print(f"Áudio baixado com sucesso: {info['title']}.mp3")
    except Exception as e:
        print(f"Erro ao baixar: {str(e)}")
        import traceback
        traceback.print_exc()
