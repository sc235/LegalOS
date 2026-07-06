from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.config import settings

# Création de l'moteur asynchrone SQLAlchemy
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Activer les logs SQL en développement
    future=True
)

# Fabrique de sessions asynchrones
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base déclarative pour les modèles ORM
Base = declarative_base()

# Dépendance FastAPI pour obtenir la session DB par requête
async def get_db_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
