import uvicorn
from models import EnvEnum
from core.config import settings

if __name__ == "__main__":
    if settings.ENV == EnvEnum.DEV.value:
        uvicorn.run('app:app', host=settings.API_HOST,
                    port=settings.API_PORT, reload=True)
    else:
        uvicorn.run('app:app', host=settings.API_HOST,
                    port=settings.API_PORT, reload=False, workers=4)
