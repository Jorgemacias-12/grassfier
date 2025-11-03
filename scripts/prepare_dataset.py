from pathlib import Path
from typing import List, Dict
import shutil
import random
from tqdm import tqdm
from colorama import init, Fore, Back, Style

init(autoreset=True)

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

VALID_EXTENSIONS = {".png", ".jpg", ".jpeg",
                    ".bmp", ".gif", ".webp", ".tiff", ".jfif"}

SPLITS = ["train", "val", "test"]
SPLIT_RATIOS = [0.7, 0.2, 0.1]

def split_images(images: List[Path]) -> Dict[str, List[Path]]:
    """
    Split a list of image paths into train, validation, and test sets.

    Args:
        images (List[Path]): List of image file paths.

    Returns:
        Dict[str, List[Path]]: Dictionary containing train, val, and test image lists.
    """

    random.shuffle(images)

    total_items = len(images)
    train_items = int(total_items * SPLIT_RATIOS[0])
    validation_items = int(total_items * SPLIT_RATIOS[1])

    return {
        "train": images[:train_items],
        "val": images[train_items:train_items + validation_items],
        "test": images[train_items + validation_items:]
    }

def prepare_dataset() -> None:
    """
     Organize raw dataset into train/val/test folders for PyTorch ImageFolder usage.
    """

    for split in SPLITS:
        (PROCESSED_DIR / split).mkdir(parents=True, exist_ok=True)

    class_dirs = [d for d in RAW_DIR.iterdir() if d.is_dir()]

    if not class_dirs:
        print(Fore.RED + "❌ No class directories found in 'data/raw'.")
        return

    for class_dir in class_dirs:
        images = [img for img in class_dir.iterdir(
        ) if img.suffix.lower() in VALID_EXTENSIONS]

        if not images:
            print(Fore.YELLOW + f"⚠️ No valid images found in '{class_dir.name}'")
            continue

        print(Fore.CYAN + f"\n📂 Processing class: {class_dir.name} ({len(images)} images)")
        split_data = split_images(images)

        for split, split_imgs in split_data.items():
            split_class_dir = PROCESSED_DIR / split / class_dir.name
            split_class_dir.mkdir(parents=True, exist_ok=True)

            # Color diferente para cada split
            split_color = {
                "train": Fore.GREEN,
                "val": Fore.BLUE,
                "test": Fore.MAGENTA
            }.get(split, Fore.WHITE)

            for img in tqdm(split_imgs, desc=split_color + f"  → {split}", unit="img", ncols=80):
                shutil.copy(img, split_class_dir / img.name)

        print(Fore.GREEN + f"✅ Class '{class_dir.name}' processed successfully.")

    print(Fore.GREEN + Style.BRIGHT + "\n🎉 Dataset prepared successfully in 'data/processed'.")


if __name__ == "__main__":
    prepare_dataset()