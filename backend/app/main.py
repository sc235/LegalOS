from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.infrastructure.routers.ai import router as ai_router
from app.infrastructure.routers.archive import router as archive_router

app = FastAPI(
    title="LegalOS API",
    description="API REST de la plateforme LegalOS pour cabinets d'avocats en Afrique de l'Ouest",
    version="1.0.0"
)

# Configuration CORS pour autoriser l'accès du frontend Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des routes
app.include_router(ai_router, prefix="/api/v1")
app.include_router(archive_router, prefix="/api/v1")

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "service": "LegalOS API",
        "database": "configured"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
