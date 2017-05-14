class Observer:
    def __init__(self, observable):
        observable.register(self)

    def update(self, device):
        pass


class Observable:
    def __init__(self):
        self.__observers = []

    def register(self, observer):
        self.__observers.append(observer)

    def update_observers(self, device):
        for observer in self.__observers:
            observer.update(device)
