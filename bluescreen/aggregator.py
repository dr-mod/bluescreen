import time


class Aggregator:
    def __init__(self, lost_time):
        self._cache = {}
        self.new_uuids = []
        self.lost_uuids = []
        self._lost_time = lost_time

    def process(self, dev_infos):
        self.new_uuids = []
        self.lost_uuids = []
        for info in dev_infos:
            uuid = info[3]
            if uuid not in self._cache:
                self.new_uuids.append(uuid)
                self._cache[uuid] = _Element(info)
            else:
                element = self._cache[uuid]
                element.update_last_seen()
                if element.dev_info != info:
                    self._dev_info_updated(uuid, info)

        self._remove_lost_devices()
        return list(map((lambda e: e.dev_info), self._cache.values()))

    def _remove_lost_devices(self):
        self.lost_uuids = [uuid for uuid, element in self._cache.items() if
                           time.time() - element.last_seen > self._lost_time]
        for uuid in self.lost_uuids:
            del self._cache[uuid]

    def _dev_info_updated(self, uuid, dev_info):
        # TODO: implement merging
        self._cache[uuid].dev_info = dev_info


class _Element:
    def __init__(self, dev_info):
        self.dev_info = dev_info
        self.last_seen = time.time()

    def update_last_seen(self):
        self.last_seen = time.time()
