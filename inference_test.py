import os
import glob
from ultralytics import YOLO

# 1. Set paths
MODEL_PATH = 'model/best.pt'
SOURCE_DIR = 'test_images'
OUTPUT_DIR = 'inference_results'

def run_batch_inference():
    # Ensure the model weights exist
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model file not found at {MODEL_PATH}")
        return

    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

    # 2. Load the fine-tuned YOLOv11 model
    print(f"Loading model from {MODEL_PATH}...")
    model = YOLO(MODEL_PATH)

    # 3. Get all images from the test_images folder
    # Supports common image formats
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.webp']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(SOURCE_DIR, ext)))
        # Also check for uppercase extensions
        image_files.extend(glob.glob(os.path.join(SOURCE_DIR, ext.upper())))

    if not image_files:
        print(f"No images found in {SOURCE_DIR}. Please add some images.")
        return

    print(f"Found {len(image_files)} images. Starting inference...")

    # 4. Loop through each image
    for img_path in image_files:
        img_name = os.path.basename(img_path)
        print(f"\nProcessing: {img_name}")
        
        # Run inference
        # Using conf=0.25; adjust if needed.
        results = model.predict(source=img_path, conf=0.25)

        for result in results:
            # Print detection summary to console
            boxes = result.boxes
            print(f"   - Detected {len(boxes)} notes.")

            # 5. Save visualized result to the output folder
            output_path = os.path.join(OUTPUT_DIR, f"result_{img_name}")
            result.save(filename=output_path)
            print(f"   - Saved result to: {output_path}")

    print(f"\nBatch processing complete! All results are in the '{OUTPUT_DIR}' folder.")

if __name__ == "__main__":
    run_batch_inference()
