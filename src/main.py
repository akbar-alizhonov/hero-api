import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.config.logger import setup_logger
from src.hero.router import router

app = FastAPI()
add_pagination(app)
app.include_router(router)
setup_logger()

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        reload=True,
    )
