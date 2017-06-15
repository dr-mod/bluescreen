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
        self._lock = threading.Lock()
        self._messages = []
        self._sock = self._init_bluetooth()

    def run(self):
        self._sock.getsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, 14)
        cmd_pkt = struct.pack("<BB", 0x01, 0x00)
        bluez.hci_send_cmd(self._sock, OGF_LE_CTL, OCF_LE_SET_SCAN_ENABLE, cmd_pkt)

        while True:
            old_filter = self._sock.getsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, 14)
            flt = bluez.hci_filter_new()
            bluez.hci_filter_all_events(flt)
            bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
            self._sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, flt)

            pkt = self._sock.recv(255)
            ptype, event, plen = struct.unpack("BBB", pkt[:3])

            if event == LE_META_EVENT:
                sub_event, = struct.unpack("B", pkt[3])
                pkt = pkt[4:]
                if sub_event == EVT_LE_CONN_COMPLETE:
                    le_handle_connection_complete(pkt)
                elif sub_event == EVT_LE_ADVERTISING_REPORT:
                    mac = self._packed_bdaddr_to_string(pkt[3:9])
                    rssi = struct.unpack("b", pkt[-1])[0]
                    data_frame = pkt[14:-1]
                    payload = struct.unpack("B"*len(data_frame), data_frame)
                    self._lock.acquire()
                    self._messages.append((mac, rssi, payload))
                    self._lock.release()

            self._sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, old_filter)

    def pop_messages(self):
        self._lock.acquire()
        result = self._messages
        self._messages = []
        self._lock.release()
        return result

    @staticmethod
    def _init_bluetooth():
        os.system("sudo hciconfig hci0 down")
        os.system("sudo hciconfig hci0 up")
        try:
            return bluez.hci_open_dev(0)
        except:
            sys.exit(1)

    @staticmethod
    def _packed_bdaddr_to_string(bdaddr_packed):
        return ':'.join('%02x' % i for i in struct.unpack("<BBBBBB", bdaddr_packed[::-1]))
