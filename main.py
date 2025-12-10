from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from aqkanji2koe import aqkanji2koe
from aquestalk import aquestalk1, aquestalk2, aquestalk10

app = FastAPI()
converter = aqkanji2koe()

class SynthRequest(BaseModel):
    text: str
    engine: Optional[str] = None
    voice: Optional[str] = None
    speed: Optional[int] = 100
    pitch: Optional[int] = 100
    accent: Optional[int] = 100
    lmd: Optional[int] = 100

@app.post(
    "/synthesis",
    response_class=Response,
    responses={
        200: {
            "description": "WAV audio data",
            "content": {"audio/wav": {"schema": {"type": "string", "format": "binary"}}},
        }
    },
)
def synthesis(req: SynthRequest):
    """音声を合成し、WAV オーディオを返します。

    レスポンスは `audio/wav` (WAV バイナリ) です。
    """
    if not req.text:
        raise HTTPException(status_code=400, detail="パラメータ `text` は必須です。")

    try:
        converted = converter.convert(req.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"音声記述への変換に失敗しました: {e}")

    try:
        match req.engine:
            case 'aquestalk1':
                voice = req.voice
                if not voice:
                    raise HTTPException(status_code=400, detail="AquesTalk1 では `voice` パラメータが必要です。")
                engine = aquestalk1(converted, voice, int(req.speed or 100))

            case 'aquestalk2':
                voice = req.voice
                if not voice:
                    raise HTTPException(status_code=400, detail="AquesTalk2 では `voice` パラメータが必要です。")
                engine = aquestalk2(converted, voice, int(req.speed or 100))

            case 'aquestalk10':
                voice = req.voice
                if not voice:
                    raise HTTPException(status_code=400, detail="AquesTalk10 では `voice` パラメータが必要です。")
                engine = aquestalk10(converted, voice, int(req.speed or 100), int(req.pitch or 100), int(req.accent or 100), int(req.lmd or 100))

            case _:
                raise HTTPException(status_code=400, detail=f"指定されたエンジンが不明です: {req.engine}")

        wav = engine.get_audio()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"音声合成に失敗しました: {e}")

    return Response(content=wav, media_type="audio/wav")
