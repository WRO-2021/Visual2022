from torch import nn


class NeuralNetwork(nn.Module):
    def __init__(self, numLabel, not_color):
        super(NeuralNetwork, self).__init__()
        self.linear_relu_stack = nn.Sequential(
            # image downsampled to a 3x3 grid
            nn.AvgPool2d(kernel_size=8, stride=8),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=1 if not_color else 3, out_channels=20, kernel_size=3),
            nn.Flatten(start_dim=1),
            nn.Linear(20, 16),
            nn.ReLU(inplace=True),
            nn.Linear(16, numLabel),
            nn.LogSoftmax(dim=1)
        )

    def forward(self, x):
        logits = self.linear_relu_stack(x)
        return logits
