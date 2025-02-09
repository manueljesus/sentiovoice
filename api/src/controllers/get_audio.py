from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

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

    if not os.path.isfile(filename):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        return FileResponse(path=filename, media_type="audio/mpeg", filename=filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving file: {str(e)}")
