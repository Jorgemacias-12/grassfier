from pathlib import Path
import tensorflow as tf
import keras

DATASET_DIR = Path("data/processed")

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32


def load_datasets():
    train_dataset = keras.utils.image_dataset_from_directory(
        DATASET_DIR / "train",
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=True
    )

    validation_dataset = keras.utils.image_dataset_from_directory(
        DATASET_DIR / "val",
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    test_dataset = keras.utils.image_dataset_from_directory(
        DATASET_DIR / "test",
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    normalization_layer = keras.layers.Rescaling(1.0 / 255)

    # Modify the images using the normalization layer
    train_dataset = train_dataset.map(lambda x, y: (normalization_layer(x), y))
    validation_dataset = validation_dataset.map(
        lambda x, y: (normalization_layer(x), y))
    test_dataset = test_dataset.map(lambda x, y: (normalization_layer(x), y))

    # prefetch all the datasets to improve CPU/GPU usage
    AUTOTUNE = tf.data.AUTOTUNE

    train_dataset = train_dataset.cache().shuffle(
        1000).prefetch(buffer_size=AUTOTUNE)
    validation_dataset = validation_dataset.cache().prefetch(buffer_size=AUTOTUNE)
    test_dataset = test_dataset.cache().prefetch(buffer_size=AUTOTUNE)

    print("Datasets cargados correctamente.")
    print(f"Clases detectadas: {train_dataset.class_names}")

    return train_dataset, validation_dataset, test_dataset, train_dataset.class_names
