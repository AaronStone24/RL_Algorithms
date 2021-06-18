import numpy as np
from scipy import stats
import random
import matplotlib.pyplot as plt

n = 10
mean_rewards = np.random.randn(n)
epsilon = 0.1

def get_reward(prob, n=10):
    reward = 0
    for i in range(n):
        if random.random() < prob:
            reward += 1
    return reward

record = np.zeros((n,2))

def get_action_value(action, record = record):
    return record[action,1]

def argmax(arr):
    indices = np.where(arr == np.amax(arr, axis=0))[0]
    return random.choice(indices)

def get_best_arm(record):
    arm_index = argmax(record[:,1])
    return arm_index

def update_record(record,reward,action):
    record[action,0] += 1
    record[action,1] = record[action,1] + (reward - record[action,1])/record[action,0]
    return record

def softmax(record,tau=1.12):
    sum = np.sum(np.exp(record[:,1]/tau))
    probs = np.exp(record[:,1]/tau)/sum
    return probs

fig,ax = plt.subplots()
ax.set_xlabel("Plays")
ax.set_ylabel("Average Reward")
fig.set_size_inches(9,5)
rewards = [0]

for i in range(500):
    if random.random() > epsilon:
        choice = get_best_arm(record)
    else:
        probs = softmax(record)
        choice = np.random.choice(np.arange(10), p=probs)
    reward = get_reward(mean_rewards[choice])
    record = update_record(record, reward, choice)
    rewards.append(rewards[-1] + (reward - rewards[-1])/(i+2))
ax.scatter(np.arange(len(rewards)), rewards, alpha=0.75)
#show the plot
plt.show()