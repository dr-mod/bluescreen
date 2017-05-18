from observer import Observable
from transformer import Transformer
from aggregator import Aggregator
from config import Config
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

    config = Config()
    transformer = Transformer(config)
    aggregator = Aggregator(LOST_TIME)

    while True:
        messages = beacon_scanner.pop_messages()
        filtered_messages = [mes for mes in messages if transformer.tracked_message(mes)]
        dev_infos = list(map((lambda message: transformer.transform(message)), filtered_messages))
        cached_dev_infos = aggregator.update(dev_infos)
        observable.update_observers(cached_dev_infos)
        time.sleep(TICK_INTERVAL)

if __name__ == "__main__":
    main()
