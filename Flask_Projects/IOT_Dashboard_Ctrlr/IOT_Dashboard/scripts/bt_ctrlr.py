import bluetooth


def run_bt_scanner():
    print("\n Scanning for Bluetooth Devices:")
    devices = bluetooth.discover_devices(lookup_names=True, lookup_class=True)
    number_of_devices = len(devices)
    print(number_of_devices, "devices found")
    
    for addr, name, device_class in devices:
        print("\nDevice Name:", name)
        print("Device MAC Address:", addr)
        print("Device Class:", device_class)

#run_bt_scanner()
