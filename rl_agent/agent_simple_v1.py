class SimpleAgentV1:
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, state):
        temperaturgradient, wärmebehandlungsgrad = state

        # 1. Spielt auf Nummer sicher → UT zu früh
        if temperaturgradient > 0.6:
            return 1  # UT – obwohl manchmal Brinell reichen würde

        # 2. Versucht Brinell – aber zu vorsichtig
        elif temperaturgradient < 0.4 and wärmebehandlungsgrad > 0.5:
            return 2  # Brinell

        # 3. Wärmebehandlung, auch wenn schon fast okay
        elif wärmebehandlungsgrad < 0.4:
            return 5  # WBH – evtl. unnötig

        # 4. Heizen bei mittlerem TG, auch wenn kein Plan
        elif 0.4 <= temperaturgradient <= 0.6:
            return 3  # Heizen zu oft

        # 5. Rest: Überspringen – manchmal zu risikofreudig
        else:
            return 0  # Skip
