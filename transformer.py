import json


class Transformer:
    def __init__(self, file_name="devices.json"):
        self.__devices = self.__load_devices(file_name)

    def transform(self, device):
        uuid = device[0]
        name = self.__devices.get(uuid.lower())
        if name is None:
            return None
        rssi = device[1]
        distance = 10 ** ((-60 - rssi) / 20)
        return name, distance

    @staticmethod
    def __load_devices(file_name):
        js = open(file_name)
        result = {}
        for mac, alias in json.load(js).iteritems():
            result[mac.lower()] = alias
        return result
