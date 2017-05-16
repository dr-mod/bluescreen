from observer import Observable
from transformer import Transformer
from view import Console
from scanner import BleScanner
from oled import OledDisplay
import time

TICK_INTERVAL = 2


def main():
    transformer = Transformer()
    observable = Observable()
    Console(observable)
    OledDisplay(observable)

    beacon_scanner = BleScanner()
    beacon_scanner.start()

    while True:
        for message in beacon_scanner.pop_messages():
            device_info = transformer.transform(message)
            if device_info is not None:
                observable.update_observers(device_info)
        time.sleep(TICK_INTERVAL)

if __name__ == "__main__":
    main()
