from __future__ import annotations
from pathlib import Path
import torch
from model.dataset_loader import load_datasets
from model.model_builder import build_resnet, CNN
from model.trainer import train
from model.device_manager import get_device
from typing import List


def main() -> None:
    """
    High-level training entry point.
    Loads data, builds a model (ResNet18 by default), and runs training.
    """
    device = get_device()

    train_loader, val_loader, classes = load_datasets()
    num_classes: int = len(classes)

    model_choice: str = "simple"

    if model_choice == "resnet":
        model = build_resnet(num_classes=num_classes, pretrained=True)
    else:
        model = CNN(num_classes=num_classes)

    train_losses, val_accuracies = train(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        device=device,
        epochs=10,
        lr=1e-4
    )

    print("✅ Training completed.")

    model_dir = Path("model/saved")
    model_dir.mkdir(parents=True, exist_ok=True)

    model_path = model_dir / "model.pth"
    torch.save(model.state_dict(), model_path)

    print(f"💾 Model saved successfully at: {model_path.resolve()}")


if __name__ == "__main__":
    main()
