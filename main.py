from fastapi import FastAPI
from dotenv import load_dotenv
import os

from app.api.v1 import (
    users,
    stations,
    records,
)

application = FastAPI()

application.include_router(users.router)
application.include_router(stations.router)
application.include_router(records.router)


if __name__ == "__main__":
    import uvicorn
    load_dotenv()
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(application, host=host, port=port)
