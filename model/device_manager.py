from __future__ import annotations
import torch
from colorama import init, Fore, Style

init(autoreset=True)


def get_device() -> torch.device:
    """
    Return the best available device (CUDA if available, otherwise CPU).

    Returns:
        torch.device: device to be used for model and tensor operations.
    """
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(Fore.GREEN + f"✅ Using GPU: {torch.cuda.get_device_name(0)}")
    else:
        device = torch.device("cpu")
        print(Fore.YELLOW + "⚠️ GPU not available — using CPU.")
    return device
