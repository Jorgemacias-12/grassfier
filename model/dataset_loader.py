from __future__ import annotations
from pathlib import Path
from typing import Tuple, List
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import torch

DATASET_DIR: Path = Path("data/processed")
IMAGE_SIZE: Tuple[int, int] = (224, 224)
BATCH_SIZE: int = 32
NUM_OF_WORKERS: int = 4 if torch.cuda.is_available() else 0


def load_datasets(
    batch_size: int = BATCH_SIZE,
    image_size: Tuple[int, int] = IMAGE_SIZE,
    num_of_workers: int = NUM_OF_WORKERS
) -> Tuple[DataLoader, DataLoader, DataLoader, List[str]]:
    """
    Load train/val/test datasets from `data/processed` using torchvision ImageFolder.

    Args:
        batch_size (int): batch size for the DataLoaders.
        image_size (Tuple[int,int]): target size (H, W) to resize images.
        num_workers (int): DataLoader workers (0 on Windows without CUDA).

    Returns:
        Tuple[DataLoader, DataLoader, DataLoader, List[str]]:
            train_loader, val_loader, test_loader, class_names
    """

    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])

    train_transform = transforms.Compose([
        transforms.Resize(image_size),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1),
        transforms.ToTensor(),
        normalize
    ])

    eval_transform = transforms.Compose([
        transforms.Resize(image_size),
        transforms.CenterCrop(image_size),
        transforms.ToTensor(),
        normalize
    ])

    train_dataset = datasets.ImageFolder(
        DATASET_DIR / "train", transform=train_transform)
    val_dataset = datasets.ImageFolder(
        DATASET_DIR / "val", transform=eval_transform)
    test_dataset = datasets.ImageFolder(
        DATASET_DIR / "test", transform=eval_transform)

    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_of_workers)
    val_loader = DataLoader(
        val_dataset, batch_size=batch_size, shuffle=False, num_workers=num_of_workers)
    test_loader = DataLoader(
        test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_of_workers)

    class_names = train_dataset.classes

    print(
        f"✅ Datasets loaded: {len(class_names)} classes, train={len(train_dataset)} val={len(val_dataset)} test={len(test_dataset)}")

    return train_loader, val_loader, test_loader, class_names
