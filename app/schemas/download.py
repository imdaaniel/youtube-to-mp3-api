from pydantic import BaseModel, HttpUrl

class DownloadRequest(BaseModel):
    """Schema para requisição de download"""
    url: HttpUrl
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            }
        }
