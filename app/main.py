from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from ultralytics import YOLO
from PIL import Image
import io
import os

app = FastAPI(title="Bangladeshi Taka Note Detection API")

# Define base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # /app/app
ROOT_DIR = os.path.dirname(BASE_DIR)                 # /app

# Ensure static directory exists in the root
RESULT_DIR = os.path.join(ROOT_DIR, "static")
os.makedirs(RESULT_DIR, exist_ok=True)

# Serve the static folder
app.mount("/static", StaticFiles(directory=RESULT_DIR), name="static")

# Load model from /app/model/best.pt
MODEL_PATH = os.path.join(ROOT_DIR, "model", "best.pt")
if not os.path.exists(MODEL_PATH):
    print(f"Warning: {MODEL_PATH} not found, using base yolo11n.pt")
    MODEL_PATH = "yolo11n.pt"

try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Could not load YOLO model: {e}")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Find index.html in the same folder as main.py
    html_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>API is running, but index.html was not found.</h1>"

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image format.")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # Run inference
        results = model.predict(source=image, conf=0.25)
        
        predictions = []
        for result in results:
            # Save visualized image to /app/static/latest_result.jpg
            save_path = os.path.join(RESULT_DIR, "latest_result.jpg")
            result.save(filename=save_path)
            
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
