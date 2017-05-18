import observer


class Console(observer.Observer):
    def update(self, devices):
        for device in devices:
            print 'Name: {:10s}; Distance: {:f}; Awake: {}'.format(*device)
