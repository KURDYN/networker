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

def addr_div(addr):
    # dividing address into separate list of octets+mask
    addr_div = addr.split("/")
    addr_div[1] = int(addr_div[1])
    addr_div[0] = addr_div[0].split(".")
    for num in range(4):
        addr_div[0][num] = int(addr_div[0][num])
    return addr_div

def addr_dec_to_bin(addr_dec):
    # addr_dec = [[XXX][XXX][XXX][XXX]] (all int)
    # converting decimal address form to binary
    addr_bin = []
    # converting octets dec to bin
    for num in range(4):
        octet = bin(addr_dec[num])[2:]
        # filling octet with zeros at the beginning of the str if needed
        if len(octet) < 8:
            octet = (8 - len(octet)) * "0" + octet
        addr_bin.append(octet)
    return addr_bin

def addr_bin_to_dec(addr_bin):
    # addr_bin = [[XXXXXXXX][XXXXXXXX][XXXXXXXX][XXXXXXXX]] (all str)
    # converting decimal address form to binary
    addr_dec = []
    # converting octets bin to dec
    for octet in addr_bin:
        addr_dec.append(int(octet, 2))
    return addr_dec

def addr_dec_str(address):
    #converting bin/dec address list to dotted string form for __str__ function
    addr_dec = ""
    if isinstance(address[0], str):
        for octet in address:
            addr_dec += str(int(octet, 2)) + "."
    else:
        for octet in address:
            addr_dec += str(octet) + "."
    return addr_dec[:-1]

def set_prefix(address):
    if match("^([0-9]{1,3}\.){3}[0-9]{1,3}\/[0-9]{1,2}$", address):
        # extracting prefix
        addr = addr_div(address)
        prefix = addr_dec_to_bin(addr[0])
        # checking if the input is correct (an octet can't be greater than 255, mask must be between 23 and 31)
        if all(x < 256 for x in addr[0]) and addr[1] in range(24, 31):
            #further checking if the input is correct (network address cant be just any address)
            mask_bin = masks["/"+str(addr[1])]["bin"].split(".")
            prefix_correct = [[],[],[],[]]
            for i in range(4):
                octet = ""
                for j in range(8):
                    if mask_bin[i][j] == "1":
                        octet += prefix[i][j]
                    else:
                        octet += "0"
                prefix_correct[i] = octet
            if prefix_correct == prefix:
                return prefix
            else:
                print("address incorrect, the correct prefix for address " + addr_dec_str(prefix) + " with mask " + "/"+str(addr[1]) +" is " + addr_dec_str(prefix_correct) + ", use it instead")
        else:
            print("address incorrect, value of octet i 0-255 and value of mask 24-30")
    else:
        print("address incorrect, use template 'XXX.XXX.XXX.XXX/MM'")

def set_bcast(prefix, mask):
    mask_bin = masks[mask]["bin"].split(".")
    bcast = [[],[],[],[]]
    # extracting bin broadcast
    for i in range(4):
        octet = ""
        for j in range(8):
            if mask_bin[i][j] == "1":
                octet += prefix[i][j]
            else:
                octet += "1"
        bcast[i] = octet
    return bcast


def find_range(prefix, broadcast):
    range = [[],[]]
    range[0] = addr_bin_to_dec(prefix)
    range[0][3] = range[0][3] + 1
    range[1] = addr_bin_to_dec(broadcast)
    range[1][3] = range[1][3] - 1
    return range