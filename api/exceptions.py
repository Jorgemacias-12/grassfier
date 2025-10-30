from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from main import app


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = {
        "detail": exc.errors(),
        "body": exc.body
    }

    return JSONResponse(
        status_code=422,
        content=errors
    )
