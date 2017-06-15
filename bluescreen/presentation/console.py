from bluescreen.observer import Observer


class Console(Observer):
    def update(self, devices):
        for device in devices:
            print 'Name: {:10s}; Distance: {:f}; Awake: {}'.format(*device)
