from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import upload, query, webhook

app = FastAPI(title="Meeting Intelligence Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api")
app.include_router(query.router, prefix="/api")
app.include_router(webhook.router, prefix="/api")

@app.get("/")
def health():
    return {"status": "running", "message": "Meeting Agent is live"}