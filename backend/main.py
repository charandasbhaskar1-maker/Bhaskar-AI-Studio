import re
from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Bhaskar AI Studio API",
    description="Backend for Bhaskar AI Studio",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://charandasbhaskar1-maker.github.io"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class StoryRequest(BaseModel):
    story: str = Field(min_length=20, max_length=12000)
    language: Literal[
        "Hindi",
        "Chhattisgarhi",
        "English"
    ] = "Hindi"
    style: str = Field(
        default="Photorealistic Cinematic",
        max_length=80
    )
    scenes: int = Field(default=6, ge=1, le=10)


@app.get("/")
def home():
    return {
        "app": "Bhaskar AI Studio",
        "status": "ready",
        "version": "0.1.0"
    }


@app.get("/health")
def health():
    return {
        "ok": True,
        "service": "bhaskar-ai-studio-api"
    }


@app.post("/api/storyboard")
def create_storyboard(payload: StoryRequest):

    parts = re.split(
        r"(?<=[.!?।])\s+|\n+",
        payload.story.strip()
    )

    parts = [part.strip() for part in parts if part.strip()]

    if not parts:
        parts = [payload.story.strip()]

    scenes = []

    for index, beat in enumerate(parts[:payload.scenes]):

        scenes.append({
            "scene": index + 1,
            "story_beat": beat,
            "visual_prompt": (
                f"{payload.style}, realistic cinematic scene, "
                f"consistent character identity. "
                f"Scene action: {beat}"
            )
        })

    return {
        "status": "storyboard_ready",
        "ai_generation_enabled": False,
        "message": (
            "Storyboard planning API is working. "
            "AI generation provider will be connected later."
        ),
        "language": payload.language,
        "style": payload.style,
        "scenes": scenes
    }