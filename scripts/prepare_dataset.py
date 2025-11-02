import os
import shutil
import random
from pathlib import Path
from tqdm import tqdm

RAW_DIR = Path("data/raw/PlantVillage")
PROCESSED_DIR = Path("data/processed")

TRAIN_SPLIT = 0.7
VAL_SPLIT = 0.2
TEST_SPLIT = 0.1

folders_to_create = ["train", "val", "test"]


def prepare_dataset():
    for split in folders_to_create:
        (PROCESSED_DIR / split).mkdir(parents=True, exist_ok=True)

    classes = [d for d in RAW_DIR.iterdir() if d.is_dir()]

    progress = tqdm(classes, desc="Procesando clases")

    for class_dir in progress:
        images = list()

        random.shuffle(images)

        n_total = len(images)
        n_train = int(n_total * TRAIN_SPLIT)
        n_val = int(n_total * VAL_SPLIT)

        subsets = {
            "train": images[:n_train],
            "val": images[n_train:n_train + n_val],
            "train": images[n_train + n_val]
        }

        for split, files in subsets.items():
            target_dir = PROCESSED_DIR / split / class_dir.name
            target_dir.mkdir(parents=True, exist_ok=True)

            for img_path in files:
                shutil.copy(img_path, target_dir / img_path.name)

        print("Dataset preparado correctamente en 'data/processed/'")


if __name__ == "__main__":
    prepare_dataset()
