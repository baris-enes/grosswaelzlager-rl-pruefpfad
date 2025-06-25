import numpy as np
import random

class QLearningAgentV2:
    def __init__(self, state_space_shape, action_space, alpha=0.1, gamma=0.9, epsilon=1.0):
        self.state_space_shape = state_space_shape  # z. B. (10, 10, 6)
        self.action_space = action_space
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.05

        self.q_table = np.zeros(state_space_shape + (len(action_space),))  # Kein .n, da list

    def discretize_state(self, state):
        """3D State: [temperaturgradient, wärmebehandlungsgrad, last_action]"""
        tg, wbh, last = state
        tg_idx = min(int(tg * self.state_space_shape[0]), self.state_space_shape[0] - 1)
        wbh_idx = min(int(wbh * self.state_space_shape[1]), self.state_space_shape[1] - 1)
        last_idx = int(last)
        return (tg_idx, wbh_idx, last_idx)

    def choose_action(self, state):
        s = self.discretize_state(state)
        if random.random() < self.epsilon:
            action = random.choice(self.action_space)
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
