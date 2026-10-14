"""Backend chat untuk Gemini. Kunci API hanya dibaca di sisi server."""

import os
import re
from urllib.parse import quote

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


DEFAULT_MODEL = "gemini-2.5-flash"
SYSTEM_PROMPT = (
    "Namamu Neko, asisten belajar yang ramah. Jawab dalam bahasa Indonesia "
    "dengan jelas dan ringkas. Jika tidak tahu, katakan terus terang."
)

app = FastAPI(title="Neko Chat API", docs_url=None, redoc_url=None)
allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS", "https://zenkaizura.github.io,http://127.0.0.1:8765"
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


async def generate_reply(message: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="Kunci Gemini belum diatur di server.")

    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", model):
        raise HTTPException(status_code=503, detail="Nama model Gemini tidak valid.")

    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{quote(model)}:generateContent"
    )
    payload = {
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": message}]}],
        "generationConfig": {"maxOutputTokens": 256},
    }
    try:
        async with httpx.AsyncClient(timeout=25.0) as client:
            response = await client.post(
                endpoint,
                headers={"x-goog-api-key": api_key},
                json=payload,
            )
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="Layanan AI belum bisa dihubungi.") from exc

    if response.status_code == 429:
        raise HTTPException(status_code=429, detail="Kuota AI tercapai. Coba lagi nanti.")
    if response.is_error:
        raise HTTPException(status_code=502, detail="Layanan AI menolak permintaan.")

    try:
        parts = response.json()["candidates"][0]["content"]["parts"]
        reply = "".join(part.get("text", "") for part in parts).strip()
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        raise HTTPException(status_code=502, detail="Jawaban AI tidak dapat dibaca.") from exc
    if not reply:
        raise HTTPException(status_code=502, detail="AI tidak memberikan jawaban teks.")
    return reply


@app.post("/api/chat")
async def chat(request: ChatRequest) -> dict[str, str]:
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=422, detail="Pesan tidak boleh kosong.")
    return {"reply": await generate_reply(message)}
