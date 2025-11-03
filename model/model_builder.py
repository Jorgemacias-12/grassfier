from __future__ import annotations
from typing import Tuple
import torch
import torch.nn as nn
import torchvision.models as models


class CNN(nn.Module):
    """
        Simple CNN for image classification (lightweight).
    """

    def __init__(self, num_classes: int) -> None:
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            # assumes input 224x224 -> 28x28 after 3 pools
            nn.Linear(128 * 28 * 28, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.features(x))


def build_resnet(num_classes: int, pretained: bool = True) -> nn.Module:
    """
    Build a ResNet18 model adapted to `num_classes`.
    Prefer this for better accuracy and transfer learning.
    """

    model = models.resnet18(pretained=pretained)
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)

    return model
