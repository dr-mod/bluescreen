class Transformer:
    def __init__(self, config):
        self.__config = config

    def transform(self, message):
        uuid = self.__extract_uuid(message)
        name = self.__config.get_name(uuid.lower())
        rssi = message[1]
        distance = 10 ** ((-60 - rssi) / 20)
        awake = self.__awake(message[2])
        return name, distance, awake, uuid

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
        return {1: False,
                2: True}.get(payload[20], None)
