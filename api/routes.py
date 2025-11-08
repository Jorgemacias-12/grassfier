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
    error_response = {
        "success": False,
        "errors": []
    }

    has_error = False

    try:
        if file.content_type not in ALLOWED_CONTENT_TYPES:
            error_response["errors"].append(
                f"Tipo de archivo no permitido. Tipos permitidos: {', '.join(ALLOWED_CONTENT_TYPES)}")

            has_error = True

        contents = await file.read()

        if len(contents) > MAX_FILE_SIZE:
            error_response["errors"].append(
                f"Archivo demasiado grande. Tamaño máximo: {MAX_FILE_SIZE} bytes"
            )

            has_error = True

        if has_error:
            return error_response

        image = Image.open(BytesIO(contents)).convert("RGB")

        image_info = {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_size": len(contents),
            "image_format": image.format,
            "image_size": f"{image.width}x{image.height}",
            "image_mode": image.mode
        }

        return {
            "success": True,
            "data": {
                "message": "Imagen procesada exitosamente",
                "image_info": image_info,
                "prediction": "pending"
            }
        }
    except Exception as e:
        error_response["errors"].append(
            f"Error al procesar la imagen: {str(e)}")

        return error_response
