import asyncio, bluetooth
from bleak import BleakScanner
#from bluetooth.ble import DiscoveryService # not working yet

class BT_Device:
    def __init__ (self, name, addr, isBLE):
        self.name = name
        self.addr = addr
        self.isBLE = isBLE
        
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
