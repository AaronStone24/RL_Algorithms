import numpy as np
import random
import torch
from torch.utils.tensorboard import SummaryWriter

#The Environment
class ContextualBandit:
    def __init__(self, arms=10):
        self.arms = arms
        self.init_distribution(arms)
        self.update_state()
    
    def init_distribution(self, arms):
        self.bandit_matrix = np.random.rand(arms, arms)
    
    def reward(self, prob):
        reward = 0.0
        for i in range(self.arms):
            if random.random() < prob:
                reward += 1
        return reward
    
    def get_state(self):
        return self.state

    def update_state(self):
        self.state = np.random.randint(0, self.arms)
    
    def get_reward(self,arm):
        return self.reward(self.bandit_matrix[self.get_state()][arm])

    def choose_arm(self,arm):
        reward = self.get_reward(arm)
        self.update_state()
        return reward

#The Agent
writer = SummaryWriter()
arms = 10
N = 1          #Batch Size
D_in = arms    #Input Dimension
H = 100        #Hidden dimension
D_out = arms   #Output Dimension
model = torch.nn.Sequential(
    torch.nn.Linear(D_in, H),
    torch.nn.ReLU(),
    torch.nn.Linear(H, D_out),
    torch.nn.ReLU(),
)
loss_fn = torch.nn.MSELoss()

env = ContextualBandit(arms)
state = env.get_state()

def one_hot_encode(N, pos, val=1):
    one_hot_vec = np.zeros(N)
    one_hot_vec[pos] = val
    return one_hot_vec

def softmax(record,tau):
    sum = np.sum(np.exp(record/tau))
    probs = np.exp(record/tau)/sum
    return probs

def train(env, epochs=5000, learning_rate=1e-2):
    current_state = torch.Tensor(one_hot_encode(arms, env.get_state()))
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    rewards=[]
    for i in range(epochs):
        y_pred = model(current_state)
        av_softmax = softmax(y_pred.data.numpy(), tau=2.0)
        av_softmax /= av_softmax.sum()
        choice = np.random.choice(arms, p=av_softmax)
        current_reward = env.choose_arm(choice)
        one_hot_reward = y_pred.data.numpy().copy()
        one_hot_reward[choice] = current_reward
        reward = torch.Tensor(one_hot_reward)
        rewards.append(current_reward)
        loss = loss_fn(y_pred, reward)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        current_state = torch.Tensor(one_hot_encode(arms, env.get_state()))
        writer.add_scalar('Rewards', current_reward, i)
    return np.array(rewards)

def running_mean(x,N):
    c = x.shape[0] - N
    y = np.zeros(c)
    conv  = np.ones(N)
    for i in range(c):
        y[i] = (x[i:i+N] @ conv)/N
        writer.add_scalar('Mean Rewards', y[i], i)
    return y

rewards = train(env)
print("Training Complete!!")
running_mean(rewards, 500)