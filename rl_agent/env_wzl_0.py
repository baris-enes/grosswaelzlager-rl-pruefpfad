import numpy as np

class WzlPruefEnv2D:
    def __init__(self):
        self.action_space = [0, 1, 2, 3, 4, 5]
        self.reset()

    def reset(self):
        self.state = np.array([
            np.random.uniform(0.0, 1.0),
            np.random.uniform(0.0, 1.0)
        ], dtype=np.float32)
        self.last_action = -1
        self.step_count = 0
        return self.state

    def step(self, action):
        temperaturgradient, wärmbehandlungsgrad = self.state
        reward = 0
        done = False

        # Strafe für doppelte Aktion
        if action == self.last_action:
            reward -= 1.0

        if action == 0:  # überspringen
            done = True
            if temperaturgradient > 0.7 or wärmbehandlungsgrad < 0.3:
                reward += -5
            else:
                reward += 0

        elif action == 1:  # UT
            done = True
            if temperaturgradient > 0.7:
                reward += 3
            else:
                reward += -1.5

        elif action == 2:  # Brinell
            done = True
            if wärmbehandlungsgrad >= 0.3:
                reward += 2
            else:
                reward += -1

        elif action == 3:  # Heizen
            temperaturgradient = min(1.0, temperaturgradient + 0.1)
            reward -= 0.1

        elif action == 4:  # Kühlen
            temperaturgradient = max(0.0, temperaturgradient - 0.1)
            wärmbehandlungsgrad = max(0.0, wärmbehandlungsgrad - 0.1)
            reward -= 0.1

        elif action == 5:  # Wärmebehandlung
            wärmbehandlungsgrad = min(1.0, wärmbehandlungsgrad + 0.2)
            reward -= 0.1

        # Rauschen
        temperaturgradient += np.random.uniform(-0.02, 0.02)
        wärmbehandlungsgrad += np.random.uniform(-0.02, 0.02)

        temperaturgradient = np.clip(temperaturgradient, 0.0, 1.0)
        wärmbehandlungsgrad = np.clip(wärmbehandlungsgrad, 0.0, 1.0)

        self.state = np.array([temperaturgradient, wärmbehandlungsgrad], dtype=np.float32)
        self.last_action = action
        self.step_count += 1

        if self.step_count >= 2:
            done = True

        return self.state, reward, done, {}
