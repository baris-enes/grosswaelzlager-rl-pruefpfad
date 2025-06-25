import numpy as np
import random

class QLearningAgentV1:
    def __init__(self, state_space_shape, action_space, alpha=0.1, gamma=0.9, epsilon=1.0):
        self.state_space_shape = state_space_shape
        self.action_space = action_space
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.05

        self.q_table = np.zeros(state_space_shape + (len(action_space),))  #  gefixt

    def discretize_state(self, state):
        temperaturgradient, wärmebehandlungsgrad = state
        tg_idx = min(int(temperaturgradient * self.state_space_shape[0]), self.state_space_shape[0] - 1)
        wh_idx = min(int(wärmebehandlungsgrad * self.state_space_shape[1]), self.state_space_shape[1] - 1)
        return (tg_idx, wh_idx)

    def choose_action(self, state):
        s = self.discretize_state(state)
        if random.random() < self.epsilon:
            action = random.choice(self.action_space)  #  gefixt
        else:
            action = np.argmax(self.q_table[s])
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        return action

    def update(self, state, action, reward, next_state):
        s = self.discretize_state(state)
        s_ = self.discretize_state(next_state)
        best_next_action = np.argmax(self.q_table[s_])
        td_target = reward + self.gamma * self.q_table[s_][best_next_action]
        td_error = td_target - self.q_table[s][action]
        self.q_table[s][action] += self.alpha * td_error
