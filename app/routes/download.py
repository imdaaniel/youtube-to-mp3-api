from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.schemas.download import DownloadRequest
from app.utils.validators import validate_youtube_url
from app.utils.id_generator import generate_video_id
from app.services.youtube import download_youtube_audio

router = APIRouter(prefix="/api", tags=["download"])

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
