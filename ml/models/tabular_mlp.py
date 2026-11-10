"""ml/models/tabular_mlp.py



PyTorch implementation of a simple feed‑forward network for tabular data.



The model expects **pre‑scaled** numeric features and integer‑encoded

categorical columns (as provided by the preprocessing step).



Exported symbols:

- `TabularMLP` – the torch `nn.Module`.

- `build_model(input_dim: int) -> TabularMLP` – convenience factory.

"""



import torch

import torch.nn as nn





class TabularMLP(nn.Module):

    """Simple multi‑layer perceptron for binary classification.



    Architecture (default):

        Input -> Linear(64) -> ReLU -> Dropout(0.2)

        -> Linear(32) -> ReLU -> Linear(1)

    The final layer outputs **logits** (no sigmoid) – use

    ``torch.nn.BCEWithLogitsLoss`` during training.

    """



    def __init__(self, input_dim: int, hidden_dims: list[int] | None = None):

        super().__init__()

        if hidden_dims is None:

            hidden_dims = [64, 32]

        layers = []

        prev_dim = input_dim

        for dim in hidden_dims:

            layers.append(nn.Linear(prev_dim, dim))

            layers.append(nn.ReLU())

            layers.append(nn.Dropout(p=0.2))

            prev_dim = dim

        # Output layer – single logit for binary classification

        layers.append(nn.Linear(prev_dim, 1))

        self.network = nn.Sequential(*layers)



    def forward(self, x):

        # x: [batch, features]

        return self.network(x).squeeze(1)  # shape -> [batch]





def build_model(input_dim: int) -> TabularMLP:

    """Factory that creates a ``TabularMLP`` with the default architecture.

    """

    return TabularMLP(input_dim)
