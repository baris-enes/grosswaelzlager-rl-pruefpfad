import numpy as np

class WzlPruefEnv4D:
    def __init__(self):
        self.action_space = [0, 1, 2, 3, 4, 5]
        self.reset()

    def reset(self):
        self.prev_action = -1
        self.last_action = -1
        self.step_count = 0
        temperaturgradient = np.random.uniform(0.0, 1.0)
        wärmebehandlungsgrad = np.random.uniform(0.0, 1.0)
        self.state = np.array([temperaturgradient, wärmebehandlungsgrad], dtype=np.float32)
        return np.array([temperaturgradient, wärmebehandlungsgrad, self.last_action, self.prev_action], dtype=np.float32)

    def step(self, action):
        temperaturgradient, wärmebehandlungsgrad = self.state
        reward = 0
        done = False

        # Strafe für doppelte Aktion
        if action == self.last_action:
            reward -= 1.0

        # Prüfaktionen
        if action == 0:  # Skip
            done = True
            if temperaturgradient > 0.7 or wärmebehandlungsgrad < 0.3:
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
            if wärmebehandlungsgrad >= 0.3:
                reward += 2
            else:
                reward += -1

        elif action == 3:  # Heizen
            temperaturgradient = min(1.0, temperaturgradient + 0.1)
            reward -= 0.1

        elif action == 4:  # Kühlen
            temperaturgradient = max(0.0, temperaturgradient - 0.1)
            wärmebehandlungsgrad = max(0.0, wärmebehandlungsgrad - 0.1)
            reward -= 0.1

        elif action == 5:  # Wärmebehandlung
            wärmebehandlungsgrad = min(1.0, wärmebehandlungsgrad + 0.2)
            reward -= 0.1

        # Rauschen
        temperaturgradient += np.random.uniform(-0.02, 0.02)
        wärmebehandlungsgrad += np.random.uniform(-0.02, 0.02)

        temperaturgradient = np.clip(temperaturgradient, 0.0, 1.0)
        wärmebehandlungsgrad = np.clip(wärmebehandlungsgrad, 0.0, 1.0)

        self.prev_action = self.last_action
        self.last_action = action
        self.step_count += 1
        self.state = np.array([temperaturgradient, wärmebehandlungsgrad], dtype=np.float32)

        if self.step_count >= 2:
            done = True

        return np.array([temperaturgradient, wärmebehandlungsgrad, self.last_action, self.prev_action], dtype=np.float32), reward, done, {}
