import time

from bluescreen.aggregator import Aggregator
from bluescreen.jsonconfig import JsonConfig
from bluescreen.observer import Observable
from bluescreen.presentation.console import Console
from bluescreen.presentation.oled import OledDisplay
from bluescreen.scanner import BleScanner
from bluescreen.transformer import Transformer
from bluescreen.taskhandler import TaskHandler

TICK_INTERVAL = 2
LOST_TIME = 15


def main():
    beacon_scanner = BleScanner()
    beacon_scanner.setDaemon(True)
    beacon_scanner.start()

    observable = Observable()
    Console(observable)
    OledDisplay(observable)

    config = JsonConfig()
    transformer = Transformer(config)
    aggregator = Aggregator(LOST_TIME)

    task_handler = TaskHandler(config)

    while True:
        messages = beacon_scanner.pop_messages()
        dev_infos = [transformer.transform(mes) for mes in messages if transformer.tracked_message(mes)]
        cached_dev_infos = aggregator.process(dev_infos)
        task_handler.appeared_uuids(aggregator.new_uuids)
        task_handler.lost_uuids(aggregator.lost_uuids)
        observable.update_observers(cached_dev_infos)
        time.sleep(TICK_INTERVAL)

if __name__ == "__main__":
    main()
