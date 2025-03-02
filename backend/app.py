from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
import uvicorn

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
