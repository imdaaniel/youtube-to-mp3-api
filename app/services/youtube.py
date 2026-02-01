import asyncio
from pathlib import Path
from typing import Dict, Any, List
from app.config import settings
from app.core.downloader import download_audio
from app.schemas.download import FormatInfo, VideoMetadata
import yt_dlp


async def extract_video_metadata(url: str) -> Dict[str, Any]:
    """
    Extrai metadados de um vídeo do YouTube sem fazer download.
    
    Args:
        url: URL do vídeo do YouTube
    
    Returns:
        Dict com estrutura compatível com VideoMetadata:
        {
            'title': str,
            'duration': int (segundos),
            'uploader': str,
            'formats': list[FormatInfo]
        }
        
    Raises:
        Exception: Se a extração de metadados falhar
    """
    
    print(f"[extract] Extraindo metadados de {url}")
    
    def _extract():
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'socket_timeout': 30,
            'retries': 3,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            
            # Extrair formatos disponíveis
            # Estratégia: combinar video-only + audio-only para máximas opções
            formats_list: List[Dict[str, Any]] = []
            
            # Pré-processar: agrupar formatos
            video_only_by_height: Dict[int, Dict[str, Any]] = {}  # height -> melhor video-only
            audio_only_formats: List[Dict[str, Any]] = []  # todos os audios
            
            if 'formats' in info and info['formats']:
                for fmt in info['formats']:
                    format_id = fmt.get('format_id', '')
                    vcodec = fmt.get('vcodec', 'none')
                    acodec = fmt.get('acodec', 'none')
                    height = fmt.get('height')
                    
                    # Ignorar formatos sem identificador
                    if not format_id:
                        continue
                    
                    # Formato video-only
                    if vcodec != 'none' and acodec == 'none':
                        if height and height > 0:
                            if height not in video_only_by_height:
                                video_only_by_height[height] = fmt
                            else:
                                # Preferir maior bitrate/filesize
                                current_size = fmt.get('filesize') or 0
                                best_size = video_only_by_height[height].get('filesize') or 0
                                if current_size > best_size:
                                    video_only_by_height[height] = fmt
                    
                    # Formato audio-only
                    elif vcodec == 'none' and acodec != 'none':
                        audio_only_formats.append(fmt)
            
            # Selecionar melhor áudio (maior bitrate)
            best_audio = None
            if audio_only_formats:
                best_audio = max(
                    audio_only_formats,
                    key=lambda f: f.get('abr') or 0
                )
            
            # Combinar video-only com audio-only, por altura
            for height in sorted(video_only_by_height.keys()):
                video_fmt = video_only_by_height[height]
                
                # Se temos áudio, criar combinação
                if best_audio:
                    combined_id = f"{video_fmt.get('format_id')}+{best_audio.get('format_id')}"
                    
                    # Estimar tamanho combinado
                    video_size = video_fmt.get('filesize') or 0
                    audio_size = best_audio.get('filesize') or 0
                    combined_size = video_size + audio_size if video_size and audio_size else None
                    
                    format_info = {
                        'format_id': combined_id,
                        'ext': video_fmt.get('ext', ''),
                        'height': height,
                        'width': video_fmt.get('width'),
                        'filesize': combined_size,
                        'fps': video_fmt.get('fps'),
                        'vcodec': video_fmt.get('vcodec'),
                        'acodec': best_audio.get('acodec'),
                        'abr': best_audio.get('abr'),
                        'vbr': video_fmt.get('vbr'),
                    }
                    formats_list.append(format_info)
                else:
                    # Sem áudio disponível, adicionar video-only mesmo assim
                    format_info = {
                        'format_id': video_fmt.get('format_id', ''),
                        'ext': video_fmt.get('ext', ''),
                        'height': height,
                        'width': video_fmt.get('width'),
                        'filesize': video_fmt.get('filesize'),
                        'fps': video_fmt.get('fps'),
                        'vcodec': video_fmt.get('vcodec'),
                        'acodec': 'none',
                        'abr': None,
                        'vbr': video_fmt.get('vbr'),
                    }
                    formats_list.append(format_info)
            
            # Ordenar por altura crescente
            formats_list.sort(key=lambda f: f.get('height') or 0)
            
            metadata = {
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Unknown'),
                'formats': formats_list,
            }
            
            print(f"[extract] Metadados extraídos com sucesso. Formatos disponíveis: {len(formats_list)}")
            return metadata
            
        except Exception as e:
            raise Exception(f"Erro ao extrair metadados do YouTube: {str(e)}")
    
    # Executar extração em thread separada (não bloqueia event loop)
    loop = asyncio.get_event_loop()
    metadata = await loop.run_in_executor(None, _extract)
    
    return metadata


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
