class Group:
    def __init__(self, host):
        self.me = host.credentials()
        self.others = set([self.me])

    def meet(self, other):
        self.others.add(other)

    def __iter__(self):
        return self.others.__iter__()
