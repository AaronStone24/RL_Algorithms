from GridWorld import GridWorld
import numpy as np
import torch
import random
import os
from torch.utils.tensorboard import SummaryWriter

l1, l2, l3, l4 = 64, 150, 100, 4

model = torch.nn.Sequential(
    torch.nn.Linear(l1,l2),
    torch.nn.ReLU(),
    torch.nn.Linear(l2,l3),
    torch.nn.ReLU(),
    torch.nn.Linear(l3,l4)
)
loss_fn = torch.nn.MSELoss()
learning_rate = 1e-3
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
writer = SummaryWriter()


gamma = 0.9
epsilon = 1.0

action_set = {
    0: 'u',
    1: 'd',
    2: 'l',
    3: 'r'
}

epochs = 2000
losses = []
for i in range(epochs):
    game = GridWorld(size=4, mode='rand')
    state_ = game.board.render_np().reshape(1,64) + np.random.rand(1,64)/10.0
    state1 = torch.from_numpy(state_).float()
    status = 1
    while(status == 1):
        qval = model(state1)
        qval_ = qval.data.numpy()
        if random.random() < epsilon:
            action_ = np.random.randint(0,4)
        else:
            action_ = np.argmax(qval_)
        
        action = action_set[action_]
        game.makeMove(action)
        state2_ = game.board.render_np().reshape(1,64) + np.random.rand(1,64)/10.0
        state2 = torch.from_numpy(state2_).float()
        reward = game.reward()
        with torch.no_grad():
            newQ = model(state2.reshape(1,64))
        maxQ = torch.max(newQ)
        if reward == -1:
            Y = reward + (gamma * maxQ)
        else:
            Y = reward
        Y = torch.Tensor([Y]).detach()
        X = qval.squeeze()[action_].unsqueeze(0)
        #print(qval.squeeze().shape)
        loss = loss_fn(X, Y)
        optimizer.zero_grad()
        loss.backward()
        losses.append(loss.item())
        writer.add_scalar('Loss', loss.item(), len(losses)-1)
        optimizer.step()
        state1 = state2
        if reward != -1:
            status = 0
        
    if epsilon > 0.1:
        epsilon -= (1/epochs)

print("Training Complete!")
path = os.getcwd() + "\DRL_in_Action\GridWorldModel.pth"
print(path)
torch.save(model, path)