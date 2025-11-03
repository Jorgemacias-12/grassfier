from __future__ import annotations
from typing import Tuple, List
from pathlib import Path
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
from colorama import init, Fore, Style

init(autoreset=True)

CHECKPOINT_DIR: Path = Path("model/saved")
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)


def train(
    model: torch.nn.Module,
    train_loader,
    val_loader,
    device: torch.device,
    epochs: int = 10,
    lr: float = 1e-4
) -> Tuple[List[float], List[float]]:
    """
    Train the model and save the best checkpoint by validation accuracy.

    Args:
        model: PyTorch model.
        train_loader: DataLoader for training.
        val_loader: DataLoader for validation.
        device: device to train on.
        epochs: number of epochs.
        lr: learning rate.

    Returns:
        Tuple of lists: (train_losses_history, val_accuracies_history)
    """

    model = model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr)

    best_val_acc = 0.0

    train_losses: list[float] = []
    val_accuracies: list[float] = []

    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0

        # Barra de progreso de entrenamiento con color azul
        pbar = tqdm(
            train_loader,
            desc=Fore.BLUE + f"Epoch {epoch}/{epochs} - train",
            unit="batch",
            ncols=100,
            bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.BLUE, Fore.RESET)
        )

        for images, labels in pbar:
            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            pbar.set_postfix(loss=loss.item())

        epoch_loss = running_loss / (len(train_loader.dataset) or 1)
        train_losses.append(epoch_loss)

        model.eval()

        correct = 0
        total = 0

        with torch.no_grad():
            # Barra de progreso de validación con color magenta
            val_pbar = tqdm(
                val_loader,
                desc=Fore.MAGENTA + f"Epoch {epoch}/{epochs} - val",
                unit="batch",
                ncols=100,
                bar_format="{l_bar}%s{bar}%s{r_bar}" % (
                    Fore.MAGENTA, Fore.RESET)
            )

            for images, labels in val_pbar:
                images = images.to(device)
                labels = labels.to(device)
                outputs = model(images)
                _, preds = torch.max(outputs, 1)
                correct += (preds == labels).sum().item()
                total += labels.size(0)

            val_acc = correct / (total or 1)
            val_accuracies.append(val_acc)

            print(
                Fore.CYAN + f"\n📊 Epoch {epoch} summary: " +
                Fore.YELLOW + f"train_loss={epoch_loss:.4f} " +
                Fore.GREEN + f"val_acc={val_acc:.4f}"
            )

            if val_acc > best_val_acc:
                best_val_acc = val_acc
                ckpt_path = CHECKPOINT_DIR / "best_model.pth"
                torch.save({
                    "epoch": epoch,
                    "model_state": model.state_dict(),
                    "optimizer_state": optimizer.state_dict(),
                    "val_acc": val_acc
                }, ckpt_path)
                print(
                    Fore.GREEN + f"💾 Saved best model (val_acc={val_acc:.4f}) -> {ckpt_path}")

    print(Fore.GREEN + Style.BRIGHT +
          f"\n🎉 Training completed! Best validation accuracy: {best_val_acc:.4f}")
    return train_losses, val_accuracies
