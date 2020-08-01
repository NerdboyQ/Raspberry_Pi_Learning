import bluetooth
from bluetooth.ble import DiscoveryService
import json 

bt_devices = {
        "devices_classic" : {0: {}},
        "devices_ble" : {0:{}}
}

devices = bluetooth.discover_devices(lookup_names=True)
i = 0
for dev in devices:
    x,y = dev
    bt_devices["devices_classic"][i] = {"name": y, "addr": x} 
    i+=1

service = DiscoveryService()
devices = service.discover(2)
i=0
for key in devices.keys():
    bt_devices["devices_ble"][i] = {"name" : devices[key],"addr": key}
    i+=1

#(lambda x: print(devices[x]))(devices.keys)
#print(bt_devices)
json_devices = json.dumps(bt_devices, indent=4)
print(json_devices)

