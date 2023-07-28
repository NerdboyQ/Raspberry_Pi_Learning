import asyncio, bluetooth, pexpect, subprocess, sys, time
from bleak import BleakClient, BleakScanner
from random import randrange
#from bluetooth.ble import DiscoveryService # not working yet

BT_CLASSIC_PIN="1887"

"""
BT Msg breakdown:
    Messages will be comprised of 64 bit long (integer) HEX values.

    **** Byte 0 - 4 will be for LED RGB control and intensity ****
    Byte 4 : Intensity 0-100% intensity, which equates to the hex range of: 0x00->0x64
    Byte 3 : Red
    Byte 1 : Green
    Byte 0 : Blue
"""

class BT_Device:
    def __init__ (self, name, addr, isBLE):
        self.name = name
        self.addr = addr
        self.isBLE = isBLE
        self.client = None
        self.connected = False
        self.isOpen = False

    def connect(self):
        if not self.isBLE:
            if self.isPreviouslyPairedDevice():
                if not self.isConnected():
                    self.connect_NonBLE()

                color_test = [
                "ffff0000", #red
                "ff00ff00", #green
                "ff0000ff"  #blue
                ]

                color_str = str(hex(randrange(126,255)))[2:] + str(hex(randrange(10,255)))[2:] + str(hex(randrange(10,255)))[2:] + str(hex(randrange(10,255)))[2:]
                if self.isOpen:
                    self.sendMsg(msg="00"+color_str)
                    self.isOpen = False
                else:
                    self.sendMsg(msg="01"+color_str)
                    self.isOpen = True
            else:
                self.pair_NonBLE()
                self.connect_NonBLE()
                self.sendMsg(msg="af")

        elif self.isBLE:
            print(f"connect ble device: {self.addr}")

    def pair_NonBLE(self):
        analyzer = pexpect.spawn(command='bluetoothctl', encoding='utf-8')
        analyzer.expect("# ")
        print(analyzer.before)

        for cmd in ['scan on', 'scan off',f"pair {self.addr}", BT_CLASSIC_PIN, 'exit']:
            print(f"Trying {cmd}...")
            analyzer.sendline(cmd)
            print(analyzer.before)
            stop_time = time.time() + 10
            while time.time() < stop_time:
                time.sleep(1)
            analyzer.expect('# ')

        print(f"Device {self.name} has been paired successfully.")
    
    def isConnected(self):
        o = subprocess.Popen(["bluetoothctl", "info", self.addr], stdout=subprocess.PIPE, text=True)
        # Communicate returns a tuple of 2 values: 0 - the output, 1 - the error (If applicable)
        if o.communicate()[0].find("Connected: no") > -1:
            print(f"Device {self.name} is not connected.")
            return False

        self.connected = True
        print(f"Device {self.name} is connected.")
        return True

    def connect_NonBLE(self):
        self.client = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.client.connect((self.addr, 1))
        self.connected = True
        print(f"Connected NonBLE device: {self.name} {self.addr}")

    def sendMsg(self, msg):
        byte_arr = []
        for n in range(len(msg)-2,-2,-2):
            v = msg[n:n+2]
            byte_arr.append(v)
            print(f"sending 0x{v} to {self.name}")
            self.client.send(bytes([int(v, 16)]))
            #time.sleep(1)

        print(byte_arr)
        """
        if not self.isBLE:
            self.client.send(msg)
            self.client.send(bytes(byte_arr))
            print(f"sent msg {msg} to nonBLE device {self.name}")
        """
    def isPreviouslyPairedDevice(self):
        paired_devices = subprocess.check_output(["bluetoothctl", "paired-devices"], text=True)
        for dev in paired_devices.split("\n"):
            if dev.find(self.addr) > -1:
                print(f"Device {self.name} is a previously paired device.")
                return True

        print(f"Devise {self.name} is not a previously paired device.")
        return False

    def disconnect(self):
        self.client.disconnect()
        print(f"Disconnecting from device {self.name}")


        
#def scan_for_BLE_devices():
#    service = DiscoveryService()
#    devices = service.discover(2)
#    device_list = []

#    for address, name in devices.items():
#        print("name: {}, address: {}".format(name, address))
#        device_list.append(BT_Device(name=name,addr=address,isBLE=False))

#    return device_list

async def scan_for_BLE_devices():
    print("Scanning for BLE enabled devices…")
    device_list = []
    devices = await BleakScanner.discover()
    for d in devices:
        if d.name.replace("-", ":") != d.address:
            print(f"  {d.address} - {d.name}")
            device_list.append(BT_Device(name=d.name,addr=d.address,isBLE=True))

    return device_list

def scan_for_NonBLE_devices():
    print("Scanning for BT devices…")
    device_list = []
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    for addr, name in nearby_devices:
            print("  {} - {}".format(addr, name))
            device_list.append(BT_Device(name=name,addr=addr,isBLE=False))

    return device_list

def run_bt_scanner():
    print("\n Scanning for Bluetooth Devices:")
    discovered_devices = scan_for_NonBLE_devices()
    for dev1 in asyncio.run(scan_for_BLE_devices()):
        found_dev = False
        for dev2 in discovered_devices:
            if dev1.addr == dev2.addr:
                dev2.isBLE = True
                found_dev = True
                break
        if not found_dev:
            discovered_devices.append(dev1)

    return discovered_devices



#run_bt_scanner()
