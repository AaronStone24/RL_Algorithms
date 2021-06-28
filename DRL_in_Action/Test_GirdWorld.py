from GridWorld import GridWorld
import numpy as np
import torch
import os

action_set = {
    0: 'u',
    1: 'd',
    2: 'l',
    3: 'r'
}

path = os.getcwd() + "\DRL_in_Action\GridWorldModel.pth"
model = torch.load(path)

def test_model(model, mode='static', display=True):
    i = 0
    test_game = GridWorld(mode=mode)
    state_ = test_game.board.render_np().reshape(1,64) + np.random.rand(1,64)/10.0
    state = torch.from_numpy(state_).float()
    if display:
        print("Initial State:")
        print(test_game.display())
    status = 1
    while(status == 1):
        qval = model(state)
        qval_ = qval.data.numpy()
        action_ = np.argmax(qval_)
        action = action_set[action_]
        if display:
            print('Move No: {}; Taking action: {}'.format(i,action))
        test_game.makeMove(action)
        state_ = test_game.board.render_np().reshape(1,64) + np.random.rand(1,64)/10.0
        state = torch.from_numpy(state_).float()
        if display:
            print(test_game.display())
        reward = test_game.reward()
        if reward != -1:
            if reward > 0:
                status = 2
                if display:
                    print("Game won! Reward: %s" % (reward,))
            else:
                status = 0
                if display:
                    print("Game LOST. Reward: %s" % (reward,))
        i += 1
        if i>10:
            if display:
                print("Game LOST. Too many moves")
            break
    win = True if status == 2 else False
    return win

test_model(model, 'rand')