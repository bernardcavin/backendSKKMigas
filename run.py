import uvicorn
from app.core.config import settings

if __name__ == '__main__':
    uvicorn.run('app.core.main:app', host=settings.DOMAIN, port=8000, reload=True)