from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from ultralytics import YOLO
from PIL import Image
import io
import os

app = FastAPI(title="Bangladeshi Taka Note Detection API")

# Setup folder paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULT_DIR = "static"
os.makedirs(RESULT_DIR, exist_ok=True)

# Serve the static folder
app.mount("/static", StaticFiles(directory=RESULT_DIR), name="static")

# Load model
MODEL_PATH = os.path.join(os.path.dirname(BASE_DIR), "model", "best.pt")
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = "yolo11n.pt"

try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Could not load YOLO model: {e}")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Return the HTML UI
    html_path = os.path.join(BASE_DIR, "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image format.")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        results = model.predict(source=image, conf=0.25)
        
        predictions = []
        for result in results:
            # Save visualized image
            result.save(filename=os.path.join(RESULT_DIR, "latest_result.jpg"))
            
            for box in result.boxes:
                predictions.append({
                    "denomination": model.names[int(box.cls[0])],
                    "confidence": round(float(box.conf[0]), 4),
                    "bounding_box": box.xyxy[0].tolist()
                })

        return {
            "status": "success",
            "count": len(predictions),
            "predictions": predictions,
            "image_url": "/static/latest_result.jpg"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
