import observer
import transformer
import view
import time


def main():
    transf = transformer.Transformer()
    observable = observer.Observable()
    view.Console(observable)

    i = 0
    while True:
        device_info = transf.transform(("FF:FF:FF:FF:FF:FF", i))
        observable.update_observers(device_info)
        i += 1
        time.sleep(2)

if __name__ == "__main__":
    main()
