#!/usr/bin/env python3
""" Neural networks tutorials from pytorch.org
"""

import argparse


import  torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear (16 * 5 * 5, 120)
        self.fc2 = nn.Linear (120, 84)
        self.fc3 = nn.Linear (84, 10)
    
    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        return x
    
    def num_flat_features(self, x):
        _size = x.size()[1:]
        num_features = 1
        for s in _size:
            num_features *= s
        return num_features


def main():
    net = Net()
    print(net)
    params = list(net.parameters())
    #print(params[0][0])
    _input = torch.randn(1, 1, 32, 32)
    out = net(_input)
    net.zero_grad()
    out.backward(torch.randn(1, 10))
    #print(params[0][0])
    output = net(_input)
    target = torch.randn(10)
    print(target)
    target = target.view(1, -1)
    criterion = nn.MSELoss()

    loss = criterion(output, target)
    print(loss)
    print(loss.grad_fn)
    print(loss.grad_fn.next_functions[0][0])
    #print(loss.grad_fn.next_functions[0][0].next_functions[0][0].next_functions[0][0])
    net.zero_grad()

    print('conv1.bias.grad before backward')
    print(net.conv1.bias.grad)

    loss.backward()
    print('conv1.bias.grad AFTER backward')
    print(net.conv1.bias.grad)

    ## THIS
    #learning_rate = 0.01
    #for f in net.parameters():
        #f.data.sub_(f.grad.data * learning_rate)

    ## OR THIS
    import torch.optim as optim

    # create your optimizer
    optimizer = optim.SGD(net.parameters(), lr=0.01)

    # in your training loop:
    optimizer.zero_grad()   # zero the gradient buffers
    output = net(_input)
    loss = criterion(output, target)
    loss.backward()
    optimizer.step()  
if __name__ == "__main__":
    main()
