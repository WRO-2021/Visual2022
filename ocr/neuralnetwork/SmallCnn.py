from torch import nn


class NeuralNetwork(nn.Module):
    def __init__(self, numLabel, not_color):
        super(NeuralNetwork, self).__init__()
        self.linear_relu_stack = nn.Sequential(
            # image downsampled by 4
            nn.AvgPool2d(kernel_size=4, stride=4),
            nn.Conv2d(in_channels=1 if not_color else 3, out_channels=10, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=10, out_channels=32, kernel_size=5),
        )

        self.flatten = nn.Flatten(start_dim=1)

        self.linear_layers = nn.Sequential(
            # https://madebyollin.github.io/convnet-calculator/
            nn.Linear(32, numLabel),
            nn.LogSoftmax(dim=1)
        )
    def forward(self, x):
        logits = self.linear_relu_stack(x)
        logits = self.flatten(logits)
        logits = self.linear_layers(logits)
        return logits
