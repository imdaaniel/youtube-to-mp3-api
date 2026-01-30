from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from app.config import settings
from app.routes.download import router as download_router
from app.services.cleanup import cleanup_old_files, cleanup_all_temp_files

def create_app() -> FastAPI:
    """Factory function para criar a aplicação FastAPI"""
    
    app = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
    )
    
    # Registrar rotas
    app.include_router(download_router)
    
    @app.get("/")
    def root():
        """Endpoint raiz - retorna informações da API"""
        return {
            "app": settings.APP_TITLE,
            "version": settings.APP_VERSION,
            "docs": "/docs"
        }
    
    @app.on_event("startup")
    async def startup():
        """Executado ao iniciar a aplicação"""
        print("🚀 API iniciada")
        cleanup_old_files()
        
        # Iniciar scheduler para limpeza periódica
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            cleanup_old_files,
            'interval',
            minutes=settings.CLEANUP_INTERVAL_MINUTES
        )
        scheduler.start()
        print(f"⏱️  Scheduler iniciado - limpeza a cada {settings.CLEANUP_INTERVAL_MINUTES} minutos")
    
    @app.on_event("shutdown")
    async def shutdown():
        """Executado ao desligar a aplicação"""
        print("🛑 API desligada")
        cleanup_all_temp_files()
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
