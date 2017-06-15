class Transformer:
    def __init__(self, config):
        self._config = config

    def transform(self, message):
        uuid = self._extract_uuid(message)
        name = self._config.get_name(uuid.lower())
        rssi = message[1]
        distance = 10 ** ((-60 - rssi) / 20)
        awake = self._awake(message[2])
        return name, distance, awake, uuid

    def tracked_message(self, message):
        uuid = self._extract_uuid(message)
        return uuid in self._config.devices

    @staticmethod
    def _extract_uuid(message):
        return message[0]

    @staticmethod
    def _awake(payload):
        if len(payload) >= 21:
            return {1: False,
                    2: True}.get(payload[20], None)
