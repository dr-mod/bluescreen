import observer


class Console(observer.Observer):
    def update(self, device):
        print 'Name: {:10s}; Distance: {:f}; Awake: {}'.format(*device)
