class Transformer:
    def __init__(self, config):
        self.__config = config

    def transform(self, message):
        uuid = self.__extract_uuid(message)
        name = self.__config.devices.get(uuid.lower())
        rssi = message[1]
        distance = 10 ** ((-60 - rssi) / 20)
        awake = self.__awake(message[2])
        return name, distance, awake

    def tracked_message(self, message):
        uuid = self.__extract_uuid(message)
        return uuid in self.__config.devices

    @staticmethod
    def __extract_uuid(message):
        return message[0]

    @staticmethod
    def __awake(payload):
        if len(payload) < 21:
            return None
        return payload[20] == 2
