from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get('/')
async def root():
    return {
        "message": "Grassfier API running!"
    }


@router.post("predict")
async def predict(file: UploadFile = File(...)):
    filename = file.filename

    content = {
        "message": f"Imagen {filename} aun no procesada"
    }

    return JSONResponse(content)
