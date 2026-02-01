from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, StreamingResponse

from app.schemas.download import DownloadRequest, DownloadRequestWithFormat, VideoMetadata
from app.utils.validators import validate_youtube_url
from app.utils.id_generator import generate_video_id
from app.services.youtube import download_youtube_audio, extract_video_metadata
from app.core.downloader import stream_video

router = APIRouter(prefix="/api", tags=["download"])


@router.get("/formats", response_model=VideoMetadata)
async def get_formats(url: str):
    """
    Extrai metadados e formatos disponíveis de um vídeo do YouTube.
    
    **Query Parameters:**
    - url: URL do vídeo do YouTube (obrigatório)
    
    **Response:**
    - title: Título do vídeo
    - duration: Duração em segundos
    - uploader: Nome do uploader
    - formats: Lista de formatos disponíveis com informações técnicas
    """
    
    # Validar URL
    if not validate_youtube_url(url):
        raise HTTPException(
            status_code=400,
            detail="URL inválida ou não é um vídeo do YouTube"
        )
    
    try:
        print(f"[formats] Extraindo metadados de {url}")
        metadata = await extract_video_metadata(url)
        return metadata
        
    except Exception as e:
        print(f"[formats] Erro ao extrair metadados: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao extrair metadados: {str(e)}"
        )


@router.post("/download-stream")
async def download_stream(request: DownloadRequestWithFormat):
    """
    Faz streaming direto de vídeo/áudio do YouTube sem armazenar em disco.
    
    **Request:**
    - url: URL do vídeo do YouTube
    - format_id: ID do formato desejado (obtido via GET /api/formats)
    
    **Response:**
    - Streaming de vídeo/áudio com chunks de 64KB
    """
    
    url = str(request.url)
    format_id = request.format_id
    
    # Validar URL
    if not validate_youtube_url(url):
        raise HTTPException(
            status_code=400,
            detail="URL inválida ou não é um vídeo do YouTube"
        )
    
    # Gerar ID único
    video_id = generate_video_id(url)
    
    try:
        print(f"[{video_id}] Iniciando streaming de {url} com formato {format_id}")
        
        # Buscar metadados para obter extensão do formato
        metadata = await extract_video_metadata(url)
        ext = "mp4"  # Padrão
        video_title = "video"
        
        # Procurar o formato selecionado para obter a extensão
        for fmt in metadata.get('formats', []):
            if fmt.get('format_id') == format_id:
                ext = fmt.get('ext', 'mp4')
                break
        
        # Usar título do vídeo como nome (com sanitização)
        if metadata.get('title'):
            video_title = metadata['title'][:50].replace(' ', '_')  # Primeiros 50 caracteres
        
        filename = f"{video_title}.{ext}"
        
        # Retornar stream
        return StreamingResponse(
            stream_video(url, format_id, video_id),
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Accept-Ranges": "bytes"
            }
        )
        
    except Exception as e:
        print(f"[{video_id}] Erro ao fazer streaming: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao fazer streaming: {str(e)}"
        )


@router.post("/download", response_class=FileResponse)
async def download(request: DownloadRequest):
    """
    Baixa áudio de um vídeo do YouTube e retorna como MP3.
    
    **Request:**
    - url: URL do vídeo do YouTube
    
    **Response:**
    - Audio stream em formato MP3
    """
    
    url = str(request.url)
    
    # Validar URL
    if not validate_youtube_url(url):
        raise HTTPException(
            status_code=400,
            detail="URL inválida ou não é um vídeo do YouTube"
        )
    
    # Gerar ID único
    video_id = generate_video_id(url)
    
    try:
        # Fazer download
        mp3_file = await download_youtube_audio(url, video_id)
        
        # Retornar arquivo com stream
        # Nota: O arquivo será deletado automaticamente pelo scheduler
        return FileResponse(
            path=mp3_file,
            filename=mp3_file.name,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"attachment; filename={mp3_file.name}"
            }
        )
        
    except Exception as e:
        print(f"[{video_id}] Erro ao baixar: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao baixar vídeo: {str(e)}"
        )
