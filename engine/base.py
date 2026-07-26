class Base:
    def __init__(self, size=44):
        self.size = size
        self.matrix = [[None] * size for _ in range(size)]
        self.buildings = []