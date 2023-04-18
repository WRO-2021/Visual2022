from torch import nn


class NeuralNetwork(nn.Module):
    def __init__(self, numLabel, not_color):
        super(NeuralNetwork, self).__init__()
        self.linear_relu_stack = nn.Sequential(
            # Defining a 2D convolution layer
            nn.AvgPool2d(kernel_size=4, stride=4),
            nn.Conv2d(in_channels=1 if not_color else 3, out_channels=10, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        self.flatten = nn.Flatten(start_dim=1)

        self.linear_layers = nn.Sequential(
            # https://madebyollin.github.io/convnet-calculator/
            nn.Linear(9, numLabel),
            nn.LogSoftmax(dim=1)
        )
    def forward(self, x):
        logits = self.linear_relu_stack(x)
        logits = self.flatten(logits)
        logits = self.linear_layers(logits)
        return logits
