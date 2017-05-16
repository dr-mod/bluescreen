import observer


class Console(observer.Observer):
    def update(self, device):
        print 'Name: {:10s}; Awake: {}; Distance: {:f}'.format(*device)
