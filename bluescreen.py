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
        transformed_devices_info = []
        for message in beacon_scanner.pop_messages():
            device_info = transformer.transform(message)
            if device_info is not None:
                transformed_devices_info.append(device_info)
        observable.update_observers(transformed_devices_info)
        time.sleep(TICK_INTERVAL)

if __name__ == "__main__":
    main()
