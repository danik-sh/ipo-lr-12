class Client:
    def __init__(self, name: str, cargo_weight: float, is_vip: bool = False):
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip