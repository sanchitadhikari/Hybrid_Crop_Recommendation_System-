from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from . import config
from .model_service import model_service
from .schemas import (
    PredictRequest,
    PredictResponse,
    ShapGlobalResponse,
    ShapLocalResponse,
)


app = FastAPI(title="Hybrid Crop Recommendation API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    model_service.load()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest) -> PredictResponse:
    result = model_service.predict(payload.model_dump())
    return PredictResponse(**result)


@app.get("/shap/global", response_model=ShapGlobalResponse)
def shap_global() -> ShapGlobalResponse:
    return ShapGlobalResponse(items=model_service.get_shap_global())


@app.post("/shap/local", response_model=ShapLocalResponse)
def shap_local(payload: PredictRequest) -> ShapLocalResponse:
    return ShapLocalResponse(**model_service.get_shap_local(payload.model_dump()))


@app.get("/insights/shap-image")
def shap_image() -> FileResponse:
    if not config.SHAP_GLOBAL_IMAGE_PATH.exists():
        raise FileNotFoundError(
            f"Insight image not found: {config.SHAP_GLOBAL_IMAGE_PATH}. Run image generation step."
        )
    return FileResponse(config.SHAP_GLOBAL_IMAGE_PATH, media_type="image/png")


@app.get("/insights/correlation-heatmap-image")
def correlation_heatmap_image() -> FileResponse:
    if not config.CORRELATION_HEATMAP_IMAGE_PATH.exists():
        raise FileNotFoundError(
            f"Insight image not found: {config.CORRELATION_HEATMAP_IMAGE_PATH}. Run image generation step."
        )
    return FileResponse(config.CORRELATION_HEATMAP_IMAGE_PATH, media_type="image/png")


@app.get("/insights/crop-distribution-image")
def crop_distribution_image() -> FileResponse:
    if not config.CROP_DISTRIBUTION_IMAGE_PATH.exists():
        raise FileNotFoundError(
            f"Insight image not found: {config.CROP_DISTRIBUTION_IMAGE_PATH}. Run image generation step."
        )
    return FileResponse(config.CROP_DISTRIBUTION_IMAGE_PATH, media_type="image/png")


@app.exception_handler(FileNotFoundError)
async def missing_artifacts_handler(_, exc: FileNotFoundError):
    return JSONResponse(status_code=500, content={"error": str(exc)})
