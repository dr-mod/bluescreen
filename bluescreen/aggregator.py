import time


class Aggregator:
    def __init__(self, lost_time):
        self.__cache = {}
        self.new_uuids = []
        self.lost_uuids = []
        self.__lost_time = lost_time

    def update(self, dev_infos):
        self.new_uuids = []
        self.lost_uuids = []
        for info in dev_infos:
            uuid = info[0]
            if uuid not in self.__cache:
                self.new_uuids.append(uuid)
                self.__cache[uuid] = _Element(info)
            else:
                element = self.__cache[uuid]
                element.update_last_seen()
                if element.dev_info != info:
                    self.__dev_info_updated(uuid, info)

        self.__remove_lost_devices()
        return list(map((lambda e: e.dev_info), self.__cache.values()))

    def __remove_lost_devices(self):
        self.lost_uuids = [uuid for uuid, element in self.__cache.items() if
                           time.time() - element.last_seen > self.__lost_time]
        for uuid in self.lost_uuids:
            del self.__cache[uuid]

    def __dev_info_updated(self, uuid, dev_info):
        # TODO: implement merging
        self.__cache[uuid].dev_info = dev_info


class _Element:
    def __init__(self, dev_info):
        self.dev_info = dev_info
        self.last_seen = time.time()

    def update_last_seen(self):
        self.last_seen = time.time()
