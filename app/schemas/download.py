from typing import Optional, List
from pydantic import BaseModel, HttpUrl, computed_field
from app.utils.helpers import format_duration, format_filesize

class FormatInfo(BaseModel):
    """Informações de um formato específico"""
    format_id: str
    ext: str
    height: Optional[float] = None
    width: Optional[float] = None
    filesize: Optional[float] = None
    fps: Optional[float] = None
    
    @computed_field
    @property
    def quality_label(self) -> str:
        """Retorna um nome amigável para o formato (ex: '720p')"""
        if self.height:
            return f"{int(self.height)}p"
        return "Unknown"
    
    @computed_field
    @property
    def filesize_label(self) -> Optional[str]:
        """Retorna o tamanho formatado em unidade legível"""
        return format_filesize(self.filesize)


class VideoMetadata(BaseModel):
    """Metadados completos do vídeo"""
    title: str
    uploader: str
    duration: int
    
    @computed_field
    @property
    def duration_label(self) -> str:
        """Retorna a duração formatada no estilo YouTube (HH:MM:SS)"""
        return format_duration(self.duration)
    
    formats: List[FormatInfo]


class DownloadRequest(BaseModel):
    """Schema para requisição de download"""
    url: HttpUrl
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            }
        }


class DownloadRequestWithFormat(BaseModel):
    """Schema para requisição de download com seleção de formato"""
    url: HttpUrl
    format_id: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "format_id": "18"
            }
        }
