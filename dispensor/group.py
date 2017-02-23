class Group:
    def __init__(self, me):
        self.me = me
        self.others = set()

    def meet(self, other):
        self.others.add(other)

    def __iter__(self):
        return self.others.__iter__()
