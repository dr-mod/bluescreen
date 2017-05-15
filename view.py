import observer


class Console(observer.Observer):
    def update(self, device):
        print('Name', device[0], 'distance', device[1])
