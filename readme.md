# 🇧🇩 Bangladeshi Taka Note Detection API

A full-stack AI application that detects Bangladeshi Taka denominations using a fine-tuned **YOLOv11** model. The project features a **FastAPI** backend, a modern **Web UI**, and is fully **Dockerized** for easy deployment.

## 🚀 Features
- **YOLOv11 Inference:** Fast and accurate detection of Taka notes.
- **REST API:** POST endpoint for image analysis with JSON responses.
- **Web UI:** User-friendly interface for uploading and visualizing detections.
- **Dockerized:** One-command setup using Docker and Docker Compose.
- **Cloud Ready:** Optimized for deployment on Render.

---

## 📂 Project Structure
```text
taka-detection-api/
├── app/
│   ├── main.py              # FastAPI Backend
│   └── index.html           # Web Frontend (HTML/CSS/JS)
├── model/
│   └── best.pt              # Trained YOLOv11 weights
├── test_images/             # Sample images for testing
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Multi-container orchestration
├── requirements.txt         # Python dependencies
├── .dockerignore            # Exclude files from Docker build
├── .gitignore               # Exclude files from GitHub
└── README.md                # Project documentation
```

---

## 🛠️ Installation & Setup

### 1. Local Setup (Without Docker)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Open `http://localhost:8000` in your browser.

### 2. Docker Setup (Recommended)
1. Build and run the container:
   ```bash
   docker compose up --build
   ```
2. Access the Web UI at `http://localhost:8000`.

---

## 🔌 API Documentation
- **Endpoint:** `/predict`
- **Method:** `POST`
- **Payload:** `file` (Image)
- **Response:**
  ```json
  {
    "status": "success",
    "count": 1,
    "predictions": [
      {
        "denomination": "100 Taka",
        "confidence": 0.98,
        "bounding_box": [x1, y1, x2, y2]
      }
    ],
    "image_url": "/static/latest_result.jpg"
  }
  ```

---

## ☁️ Cloud Deployment (Render)
1. Push this project to GitHub.
2. Create a new **Web Service** on Render.
3. Connect your repository and select **Docker** as the runtime.
4. Render will automatically use the `Dockerfile` to deploy your API.

---

## 📈 Prediction Accuracy Discussion
The model utilizes the YOLOv11 nano architecture, fine-tuned on a custom dataset of Bangladeshi Taka notes.
- **Strengths:** High speed and accurate detection in varied lighting.
- **Limitations:** May struggle with extremely folded or partially visible notes.
- **Optimization:** Using `opencv-python-headless` ensures stability in server environments without graphics drivers.

---

URL of the project : [Taka-Detection-URL](https://taka-detection-api-1y0h.onrender.com/)
