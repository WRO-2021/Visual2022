from torch import nn


class NeuralNetwork(nn.Module):
    def __init__(self, numLabel, not_color):
        super(NeuralNetwork, self).__init__()
        self.linear_relu_stack = nn.Sequential(
            # Defining a 2D convolution layer
            nn.Conv2d(in_channels=1 if not_color else 3, out_channels=20, kernel_size=5),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            # second 2D convolution layer
            nn.Conv2d(in_channels=20, out_channels=50, kernel_size=5),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.linear_layers = nn.Sequential(
            # https://madebyollin.github.io/convnet-calculator/
            nn.Linear(800, numLabel),
            nn.LogSoftmax(dim=1)
        )
        self.flatten = nn.Flatten(start_dim=1)

    def forward(self, x):
        logits = self.linear_relu_stack(x)
        logits = self.flatten(logits)
        logits = self.linear_layers(logits)
        return logits
