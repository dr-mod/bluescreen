from observer import Observable
from transformer import Transformer
from aggregator import Aggregator
from view import Console
from scanner import BleScanner
from oled import OledDisplay
import time

TICK_INTERVAL = 2
LOST_TIME = 10


def main():
    beacon_scanner = BleScanner()
    beacon_scanner.start()

    observable = Observable()
    Console(observable)
    OledDisplay(observable)

    transformer = Transformer()
    aggregator = Aggregator(LOST_TIME)

    while True:
        messages = beacon_scanner.pop_messages()
        dev_infos = list(map((lambda message: transformer.transform(message)), messages))
        dev_infos = [dev_info for dev_info in dev_infos if dev_info is not None]
        cached_dev_infos = aggregator.update(dev_infos)
        observable.update_observers(cached_dev_infos)
        time.sleep(TICK_INTERVAL)

if __name__ == "__main__":
    main()
