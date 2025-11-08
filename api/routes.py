from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from slowapi.util import get_remote_address
from slowapi import Limiter
from PIL import Image
from io import BytesIO

router = APIRouter()

limiter = Limiter(key_func=get_remote_address)

MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}


@router.get('/')
async def root():
    return {
        "message": "Grassfier API running!"
    }


@router.post("/predict")
@limiter.limit("5/minute")
async def predict(request: Request, file: UploadFile = File(...)) -> dict:
    """
    Endpoint to receive an image file and perform prediction.
    """
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        # TODO: send json data
        raise HTTPException(status_code=400, detail="")

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        # TODO: send json data
        raise HTTPException(status_code=400, detail="")

    try:
        image = Image.open(BytesIO(contents)).convert("RGB")
    except Exception:
        # TODO: send json data
        raise HTTPException(status_code=500, detail="")

    return {}
