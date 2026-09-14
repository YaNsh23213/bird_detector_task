import shutil
from pathlib import Path
from ultralytics import YOLO

def main():
    model = YOLO("yolo26n.pt")

    results = model.train(
        data="dataset/data.yaml",
        epochs=50,
        imgsz=640,
        batch=16,
        patience=15,
        name="bird_detector",
        project="runs/train",
        pretrained=True,
        seed=42,
    )

    trained_best = Path(results.save_dir) / "weights" / "best.pt"

    final_weights = Path("weights/best.pt")
    final_weights.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(trained_best, final_weights)
    
    print(f"Training completed.")
    print(f"Original weights (with logs/plots): {trained_best}")
    print(f"Copied to: {final_weights}")

if __name__ == "__main__":
    main()