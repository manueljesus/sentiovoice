from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

from src import api_settings

router = APIRouter(prefix="/audio", tags=["audio"])


@router.get(
    "/{filename}",
    summary="Download feedback audio file",
    description="Downloads the specified feedback MP3 file.",
    response_description="The requested audio file.",
)
async def download_audio(filename: str):
    if not filename.endswith(".mp3"):
        raise HTTPException(status_code=400, detail="Invalid filename")

    path = os.path.join(api_settings.azure_ai_services.audio_path, filename)

    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        return FileResponse(
            path=path,
            media_type="audio/mpeg",
            filename=filename,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving file: {str(e)}")
