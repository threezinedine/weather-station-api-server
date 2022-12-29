from fastapi import FastAPI
from dotenv import load_dotenv
import os


app = FastAPI()


if __name__ == "__main__":
    import uvicorn
    load_dotenv()
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host=host, port=port)
