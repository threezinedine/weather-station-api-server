from fastapi import FastAPI
from dotenv import load_dotenv
import os

from app.api.v1 import (
    users,
    stations,
)

app = FastAPI()
print(stations.router, users.router)

app.include_router(users.router)
app.include_router(stations.router)


if __name__ == "__main__":
    import uvicorn
    load_dotenv()
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host=host, port=port)
