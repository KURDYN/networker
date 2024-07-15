from networkClass import *
siec1 = Network("192.168.32.0/24")
print(siec1)
siec1.vlsm()
addr = "192.168.12.0/24"
"""dane_sieci = [
    {"nazwa": "Subnet1", "addr": "192.168.6.0/23"},
    {"nazwa": "Subnet2", "addr": "192.168.32.0/24"},
    {"nazwa": "Subnet3", "addr": "192.168.12.0/24"},
]

sieci = {}

for dane in dane_sieci:
    nazwa = dane["nazwa"]
    sieci[nazwa] = Network(dane["addr"])

for nazwa, siec in sieci.items():
    print(f"{nazwa}:\n{siec}", end="\n")"""






