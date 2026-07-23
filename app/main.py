from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
from PIL import Image
import io
import os

app = FastAPI(title="Bangladeshi Taka Note Detection API")

# Create a folder to save visualized results
RESULT_DIR = "static"
os.makedirs(RESULT_DIR, exist_ok=True)

# Serve the static folder so we can see images in the browser
app.mount("/static", StaticFiles(directory=RESULT_DIR), name="static")

# Load the fine-tuned model weights
MODEL_PATH = "model/best.pt"
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = "yolo11n.pt"

try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Could not load YOLO model: {e}")

@app.get("/")
async def root():
    return {"message": "Bangladeshi Taka Note Detection API is running"}

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
            # Save the visualized image to the static folder
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
