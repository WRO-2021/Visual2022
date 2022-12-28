from torch import nn

# Define model
class NeuralNetwork(nn.Module):
    def __init__(self, numLabel):
        super(NeuralNetwork, self).__init__()
        #self.flatten = nn.Flatten()
        # take in input resistance, age, heater_r and heater_V
        self.linear_relu_stack = nn.Sequential(
            # Defining a 2D convolution layer
            nn.Conv2d(in_channels=1, out_channels=20, kernel_size=(5,5)),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(2,2), stride=(2,2)),
            # second 2D convolution layer
            nn.Conv2d(in_channels=20, out_channels=50, kernel_size=(5,5)),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(2,2), stride=(2,2)),
        )

        self.linear_layers = nn.Sequential(
            nn.Flatten(),
            # https://madebyollin.github.io/convnet-calculator/
            nn.Linear(50, numLabel),
            nn.LogSoftmax(dim=1)
        )


    def forward(self, x):
        #x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        logits = self.linear_layers(logits)
        return logits