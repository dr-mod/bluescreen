import json


class JsonConfig:
    def __init__(self, file_name="conf/devices.json"):
        self.devices = self.__load_devices(file_name)

    @staticmethod
    def __load_devices(file_name):
        js = open(file_name)
        result = {}
        for mac, alias in json.load(js).iteritems():
            result[mac.lower()] = alias
        return result
