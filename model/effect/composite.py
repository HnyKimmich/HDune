# composite effect（占位）
class CompositeEffect:
    def __init__(self, effects):
        self.effects = effects
    def apply(self, target):
        for e in self.effects:
            e.apply(target)
