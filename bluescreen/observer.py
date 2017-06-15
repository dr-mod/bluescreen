class Observer:
    def __init__(self, observable):
        observable.register(self)

    def update(self, devices):
        pass


class Observable:
    def __init__(self):
        self._observers = []

    def register(self, observer):
        self._observers.append(observer)

    def update_observers(self, devices):
        for observer in self._observers:
            observer.update(devices)
