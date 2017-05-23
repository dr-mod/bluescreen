import os


class TaskHandler:
    def __init__(self, config):
        self.__config = config

    def appeared_uuids(self, macs):
        self.__handle(macs, (lambda mac: self.__config.get_appear_action(mac)))

    def lost_uuids(self, macs):
        self.__handle(macs, (lambda mac: self.__config.get_lost_action(mac)))

    def __handle(self, macs, get_command):
        for mac in macs:
            command = get_command(mac)
            if command is not None:
                os.system(command)
