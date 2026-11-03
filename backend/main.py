
import re
from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Bhaskar AI Studio API",
    description="Backend for Bhaskar AI Studio",
    version="0.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://charandasbhaskar1-maker.github.io"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class StoryRequest(BaseModel):
    story: str = Field(min_length=20, max_length=12000)
    language: Literal["Hindi", "Chhattisgarhi", "English"] = "Hindi"
    style: str = Field(default="Photorealistic Cinematic", max_length=80)
    scenes: int = Field(default=6, ge=1, le=10)
    character_name: str = Field(default="", max_length=80)
    character_look: str = Field(default="", max_length=500)
    starting_costume: str = Field(default="", max_length=250)


def split_story(text: str, scene_count: int) -> list[str]:
    sentences = [
        item.strip()
        for item in re.split(r"(?<=[.!?।])\s+|\n+", text.strip())
        if item.strip()
    ]

    if not sentences:
        sentences = [text.strip()]

    while len(sentences) < scene_count:
        candidate_index = max(
            range(len(sentences)),
            key=lambda i: len(sentences[i])
        )
        candidate = sentences[candidate_index]

        pieces = [
            p.strip()
            for p in re.split(r"[,;:—]\s*", candidate)
            if p.strip()
        ]

        if len(pieces) > 1:
            sentences[candidate_index:candidate_index + 1] = pieces

        elif len(candidate) > 100:
            midpoint = len(candidate) // 2
            split_at = candidate.rfind(" ", 0, midpoint + 25)

            if split_at < 20:
                split_at = candidate.find(" ", midpoint)

            if split_at > 0:
                sentences[candidate_index:candidate_index + 1] = [
                    candidate[:split_at].strip(),
                    candidate[split_at:].strip()
                ]
            else:
                break
        else:
            break

    if len(sentences) <= scene_count:
        return sentences + [
            "इस दृश्य में पिछले घटनाक्रम का स्वाभाविक अगला भाग दिखाएँ।"
        ] * (scene_count - len(sentences))

    groups = []

    for i in range(scene_count):
        start = round(i * len(sentences) / scene_count)
        end = round((i + 1) * len(sentences) / scene_count)
        groups.append(" ".join(sentences[start:end]))

    return groups


SHOT_PLANS = [
    ("Wide establishing shot", "धीरे आगे बढ़ता camera", "स्थान और समय स्थापित करें"),
    ("Medium character shot", "हल्का tracking movement", "किरदार की प्रतिक्रिया दिखाएँ"),
    ("Close-up on face and eyes", "slow push-in", "भावनात्मक बदलाव पर ध्यान दें"),
    ("Over-the-shoulder shot", "स्थिर camera", "संवाद और प्रतिक्रिया स्पष्ट रखें"),
    ("Dynamic action shot", "controlled tracking movement", "गतिविधि स्वाभाविक रखें"),
    ("Cinematic final wide shot", "धीमा pull-back", "दृश्य का प्रभावशाली समापन करें"),
]


@app.get("/")
def home():
    return {
        "app": "Bhaskar AI Studio API",
        "status": "ready",
        "version": "0.2.0"
    }


@app.get("/health")
def health():
    return {
        "ok": True,
        "service": "bhaskar-ai-studio-api",
        "version": "0.2.0"
    }


@app.post("/api/storyboard")
def create_storyboard(payload: StoryRequest):
    beats = split_story(payload.story, payload.scenes)

    name = payload.character_name.strip()
    look = payload.character_look.strip()
    costume = payload.starting_costume.strip()

    identity = (
        "हर दृश्य में वही चेहरा, उम्र, hairstyle, "
        "शरीर की बनावट और पहचान बनाए रखें।"
    )

    if name:
        identity = (
            f"{name} का चेहरा और पहचान सभी दृश्यों में "
            "एक जैसी रखें। " + identity
        )

    if look:
        identity += f" स्थायी रूप-रंग: {look}."

    if costume:
        wardrobe = (
            f"शुरुआती पोशाक: {costume}. कहानी में समय, स्थान "
            "या परिस्थिति बदलने पर ही कपड़े बदलें; कपड़े "
            "बदलने पर भी चेहरा और पहचान न बदलें।"
        )
    else:
        wardrobe = (
            "कहानी के समय, स्थान, मौसम और परिस्थिति के अनुसार "
            "पोशाक रखें; बिना कारण कपड़े न बदलें।"
        )

    scenes = []

    for index, beat in enumerate(beats):
        shot, movement, purpose = SHOT_PLANS[
            index % len(SHOT_PLANS)
        ]

        prompt = (
            f"{payload.style}, {identity} "
            f"Scene action: {beat} "
            "Natural human anatomy, realistic lighting, "
            "detailed environment, cinematic composition, "
            "no face change, no duplicate people."
        )

        scenes.append({
            "scene": index + 1,
            "story_beat": beat,
            "scene_purpose": purpose,
            "shot_type": shot,
            "camera_movement": movement,
            "lighting_mood": (
                "कहानी के भाव और स्थान के अनुसार "
                "natural cinematic lighting"
            ),
            "acting_direction": (
                "आँखों, चेहरे के भाव, हाथों और body language "
                "को कहानी के अनुरूप स्वाभाविक रखें।"
            ),
            "dialogue_plan": (
                f"{payload.language} में इस दृश्य के लिए छोटा, "
                "स्पष्ट संवाद या narration लिखें।"
            ),
            "music_sfx_plan": (
                "दृश्य के mood के अनुसार background score "
                "और वातावरण के sound effects रखें।"
            ),
            "identity_lock": identity,
            "wardrobe_director": wardrobe,
            "image_prompt": prompt,
            "video_prompt": (
                prompt + f" Camera: {shot}; movement: {movement}. "
                "Natural motion, consistent character identity."
            ),
            "visual_prompt": prompt
        })

    return {
        "status": "storyboard_ready",
        "ai_generation_enabled": False,
        "planner_type": "structured_rule_based_story_director",
        "message": (
            "Structured storyboard plan तैयार है। "
            "वास्तविक AI media generation provider "
            "अभी connected नहीं है।"
        ),
        "language": payload.language,
        "style": payload.style,
        "requested_scenes": payload.scenes,
        "scenes": scenes
    }
