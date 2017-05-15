import os
import sys
import struct
import bluetooth._bluetooth as bluez
import threading

LE_META_EVENT = 0x3e
OGF_LE_CTL = 0x08
OCF_LE_SET_SCAN_ENABLE = 0x000C
EVT_LE_CONN_COMPLETE = 0x01
EVT_LE_ADVERTISING_REPORT = 0x02


class BleScanner(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__lock = threading.Lock()
        self.__messages = []
        self.__sock = self.init_bluetooth()

    def run(self):
        self.__sock.getsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, 14)
        cmd_pkt = struct.pack("<BB", 0x01, 0x00)
        bluez.hci_send_cmd(self.__sock, OGF_LE_CTL, OCF_LE_SET_SCAN_ENABLE, cmd_pkt)

        while True:
            old_filter = self.__sock.getsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, 14)
            flt = bluez.hci_filter_new()
            bluez.hci_filter_all_events(flt)
            bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
            self.__sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, flt)

            pkt = self.__sock.recv(255)
            ptype, event, plen = struct.unpack("BBB", pkt[:3])

            if event == LE_META_EVENT:
                sub_event, = struct.unpack("B", pkt[3])
                pkt = pkt[4:]
                if sub_event == EVT_LE_CONN_COMPLETE:
                    le_handle_connection_complete(pkt)
                elif sub_event == EVT_LE_ADVERTISING_REPORT:
                    mac = self.packed_bdaddr_to_string(pkt[3:9])
                    rssi = struct.unpack("b", pkt[-1])[0]
                    self.__lock.acquire()
                    self.__messages.append((mac, rssi))
                    self.__lock.release()

            self.__sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, old_filter)

    def pop_messages(self):
        self.__lock.acquire()
        result = self.__messages
        self.__messages = []
        self.__lock.release()
        return result

    @staticmethod
    def init_bluetooth():
        os.system("sudo hciconfig hci0 down")
        os.system("sudo hciconfig hci0 up")
        try:
            return bluez.hci_open_dev(0)
        except:
            sys.exit(1)

    @staticmethod
    def packed_bdaddr_to_string(bdaddr_packed):
        return ':'.join('%02x' % i for i in struct.unpack("<BBBBBB", bdaddr_packed[::-1]))
