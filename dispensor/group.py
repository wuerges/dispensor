class Group:
    def __init__(self, me):
        self.me = me
        self.others = []

    def meet(self, other):
        self.others.append(other)
