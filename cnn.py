# -*- coding: utf-8 -*-
"""Untitled8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GbtFHkQqyVBtSOIEbKmnmXqT_AeSebhv
"""

import matplotlib.pyplot as plt
import numpy as np

import torch
import torchvision
import torchvision.transforms as transforms

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

transform = transforms.Compose(
    [transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))])

# datasets
trainset = torchvision.datasets.USPS('./data',
    download=True,
    train=True,
    transform=transform)
testset = torchvision.datasets.USPS('./data',
    download=True,
    train=False,
    transform=transform)

trainloader = torch.utils.data.DataLoader(trainset, shuffle=True)
testloader = torch.utils.data.DataLoader(testset,shuffle=False)

# Experiment 2 - Start

#class CNN(nn.Module):
#    def __init__(self):
#        super(CNN, self).__init__()
#        self.conv1 = nn.Conv2d(1, 8, kernel_size=3)
#        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
#        self.conv2 = nn.Conv2d(8, 16, kernel_size=3)
#        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
#        self.fc1 = nn.Linear(4 * 4 * 4, 32)
#        self.fc2 = nn.Linear(32, 10)
#
#    def forward(self, x):
#        x = self.pool(torch.nn.functional.relu(self.conv1(x)))
#        x = self.pool(torch.nn.functional.relu(self.conv2(x)))
#        x = x.view(-1, 4 * 4 * 4)
#        x = torch.nn.functional.relu(self.fc1(x))
#        x = self.fc2(x)
#        return x
#
#net = CNN()

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 8, kernel_size=2)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(8, 16, kernel_size=2)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv3 = nn.Conv2d(16, 64, kernel_size=2)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(4 * 4 * 4, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 10)

    def forward(self, x):
        x = self.pool(torch.nn.functional.relu(self.conv1(x)))
        x = self.pool(torch.nn.functional.relu(self.conv2(x)))
        x = self.pool(torch.nn.functional.relu(self.conv3(x)))
        x = x.view(-1, 4 * 4 * 4)
        x = torch.nn.functional.relu(self.fc1(x))
        x = self.fc2(x)
        x = self.fc3(x)
        return x

net = CNN()

# Experiment 2 - End

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
net.to(device)

criterion = nn.CrossEntropyLoss()
# Experiment 1 - Start
# optimizer = optim.SGD(net.parameters(), lr=0.001)
optimizer = optim.Adam(net.parameters(), lr=0.001)
# Experiment 1 - Complete
current_loss = 0.0

for i in range(5):
  current_loss = 0.0

  for data in trainloader:
    inputs, labels = data

    inputs, labels = inputs.to(device), labels.to(device)

    optimizer.zero_grad()

    outputs = net(inputs)
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()

    current_loss += loss.item()
  print(f'Training Complete for Epoch {i + 1}, loss - {current_loss}')