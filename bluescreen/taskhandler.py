import os


class TaskHandler:
    def __init__(self, config):
        self._config = config

    def appeared_uuids(self, macs):
        self._handle(macs, (lambda mac: self._config.get_appear_action(mac)))

    def lost_uuids(self, macs):
        self._handle(macs, (lambda mac: self._config.get_lost_action(mac)))

    def _handle(self, macs, get_command):
        for mac in macs:
            command = get_command(mac)
            if command is not None:
                os.system(command)
