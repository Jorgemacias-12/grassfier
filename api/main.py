from fastapi import FastAPI, File, UploadFile

app = FastAPI(title="Grassfier API")


@app.get("/")
async def root():
    return {
        "status": "Grassfier service running"
    }
