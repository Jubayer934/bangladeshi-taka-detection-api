# Bangladeshi Taka Note Detection API

This project provides a REST API for detecting Bangladeshi Taka notes using a fine-tuned **YOLOv11** model.

## Folder Structure
```
taka-detection-api/
├── model/
│   └── best.pt          # Fine-tuned YOLOv11 weights (Phase-1)
├── app/
│   └── main.py          # FastAPI application
├── test_images/         # 5+ images for testing
├── Dockerfile           # Docker configuration
├── .dockerignore        # Files to exclude from Docker build
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # Optional Compose configuration
└── README.md            # Project documentation
```

## Setup & Installation

### Local Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the API:
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker Setup
1. Build the Docker image:
   ```bash
   docker build -t taka-detection-api .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 taka-detection-api
   ```
   *Alternatively, use Docker Compose:* `docker-compose up`

## API Usage
- **Endpoint:** `/predict`
- **Method:** `POST`
- **Input:** Image file (multipart/form-data)
- **Response:** JSON

### Example with `curl`
```bash
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_image.jpg;type=image/jpeg'
```

## Prediction Accuracy Discussion
The model's accuracy depends on several factors:
1. **Dataset Quality**: The variety of lighting conditions, angles, and backgrounds in the training data for Taka notes.
2. **Model Choice**: YOLOv11n (Nano) is optimized for speed, while YOLOv11m or YOLOv11l would provide higher accuracy at the cost of inference time.
3. **Confidence Threshold**: A threshold of 0.25 was used in this API. Increasing this reduces false positives but might miss some notes in poor lighting.
4. **Resolution**: The API processes images at their native resolution or resizes them to the model's expected input (usually 640x640), which is generally sufficient for note detection.

## Deployment Steps (Cloud)
1. **Containerize:** Ensure the Docker image is working locally.
2. **Push to Registry:** Push the image to Docker Hub or AWS ECR.
3. **Deploy:** 
   - On **Render/Railway**: Connect GitHub repo, select Dockerfile, and deploy.
   - On **AWS App Runner**: Connect to ECR and deploy the container.
   - On **GCP Cloud Run**: Use `gcloud run deploy`.
