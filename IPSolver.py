from re import match

'''-----------[subnet mask information]-----------'''
masks = {
    "/30": {
        "bin": "11111111.11111111.11111111.11111100",
        "dec": "255.255.255.252",
        "usable": 2
    },
    "/29": {
        "bin": "11111111.11111111.11111111.11111000",
        "dec": "255.255.255.248",
        "usable": 6
    },
    "/28": {
        "bin": "11111111.11111111.11111111.11110000",
        "dec": "255.255.255.240",
        "usable": 14
    },
    "/27": {
        "bin": "11111111.11111111.11111111.11100000",
        "dec": "255.255.255.224",
        "usable": 30
    },
    "/26": {
        "bin": "11111111.11111111.11111111.11000000",
        "dec": "255.255.255.192",
        "usable": 62
    },
    "/25": {
        "bin": "11111111.11111111.11111111.10000000",
        "dec": "255.255.255.128",
        "usable": 126
    },
    "/24": {
        "bin": "11111111.11111111.11111111.00000000",
        "dec": "255.255.255.0",
        "usable": 254
    },
}


'''-----------[address input]-----------'''
while True:
    addr = input("Insert an address and its subnet mask.\n")
    # checking if the input is correct (initial regex)
    if match("^([0-9]{1,3}\.){3}[0-9]{1,3}\/[0-9]{1,2}$", addr):
        # dividing address into separate octets+mask
        addr_div = addr.split("/")
        addr_div[1] = int(addr_div[1])
        addr_div[0] = addr_div[0].split(".")
        for num in range(4):
            addr_div[0][num] = int(addr_div[0][num])

        # checking if the input is correct (an octet can't be greater than 255, mask must be between 23 and 31)
        if all(x < 256 for x in addr_div[0]) and addr_div[1] in range(24, 31):
            print("address correct\n")
            break
        else:
            print("address incorrect, use template 'XXX.XXX.XXX.XXX/MM'")
    else:
        print("address incorrect, use template 'XXX.XXX.XXX.XXX/MM'")

# creating network dict
network = {
    "prefix": None,
    "mask": "/"+str(addr_div[1]),
    "broadcast": None,
    "usable": str(masks["/"+str(addr_div[1])]["usable"]),
    "range": None
}


'''-----------[finding network prefix]-----------'''
prefix = []

# trasforming every octet to bin
for num in range(4):
    octet = bin(addr_div[0][num])[2:]
    # filling octet with zeros at the beginning of the str if needed
    if len(octet) < 8:
        octet = (8 - len(octet)) * "0" + octet
    prefix.append(octet)
mask = masks["/"+str(addr_div[1])]["bin"].split(".")

# extracting bin prefix
for i in range(4):
    octet = ""
    for j in range(8):
        if mask[i][j] == "1":
            octet += prefix[i][j]
        else:
            octet += "0"
    prefix[i] = octet

# transforming prefix to dec and adding to network dict
prefix_dec = ''
for octet in prefix:
    prefix_dec += str(int(octet, 2)) + "."
network["prefix"] = prefix_dec[:-1]

'''-----------[finding broadcast address]-----------'''
bcast = prefix

# extracting bin broadcast
for i in range(4):
    octet = ""
    for j in range(8):
        if mask[i][j] == "1":
            octet += prefix[i][j]
        else:
            octet += "1"
    bcast[i] = octet

# transforming broadcast to dec and adding to network dict
bcast_dec = ''
for octet in bcast:
    bcast_dec += str(int(octet, 2)) + "."
network["broadcast"] = bcast_dec[:-1]

'''-----------[finding host range]-----------'''
# fist usable of range is the last octet of prefix + 1
first = network["prefix"].split(".")
first[3] = int(first[3])+1
first_dec = ''
for octet in first:
    first_dec += str(octet) + "."
first_dec = first_dec[:-1]

# last usable of range is the last octet of broadcast - 1
last = network["broadcast"].split(".")
last[3] = int(last[3])-1
last_dec = ''
for octet in last:
    last_dec += str(octet) + "."
last_dec = last_dec[:-1]

# adding to dict
network["range"] = first_dec+' - '+last_dec

# program output
output = 'Network prefix: '+network['prefix']+',\n'
output += 'Subnet mask: '+network['mask']+', '+masks[network['mask']]["dec"]+',\n'
output += 'Usable addresses: '+network['usable']+', host range: '+network['range']+',\n'
output += 'Broadcast address: '+network['broadcast']+'\n'
print(output)