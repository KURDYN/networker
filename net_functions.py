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

def set_prefix(address):
    if match("^([0-9]{1,3}\.){3}[0-9]{1,3}\/[0-9]{1,2}$", address):
        # finding prefix
        addr = addr_div(address)
        prefix = addr_dec_to_bin(addr[0])
        # checking if the input is correct (an octet can't be greater than 255, mask must be between 23 and 31)
        if all(x < 256 for x in addr[0]) and addr[1] in range(24, 31):
            print("address correct\n")
            return prefix
        else:
            print("address incorrect, use template 'XXX.XXX.XXX.XXX/MM'")
    else:
        print("address incorrect, use template 'XXX.XXX.XXX.XXX/MM'")

def set_bcast(prefix, mask):
    mask = masks[mask]["bin"].split(".")
    bcast = [[],[],[],[]]
    # extracting bin broadcast
    for i in range(4):
        octet = ""
        for j in range(8):
            if mask[i][j] == "1":
                octet += prefix[i][j]
            else:
                octet += "1"
        bcast[i] = octet
    return bcast


def find_range(prefix, broadcast):
    first = prefix.split(".")
    first[3] = int(first[3]) + 1
    first_dec = ''
    for octet in first:
        first_dec += str(octet) + "."
    first_dec = first_dec[:-1]

    # last usable of range is the last octet of broadcast - 1
    last = broadcast.split(".")
    last[3] = int(last[3]) - 1
    last_dec = ''
    for octet in last:
        last_dec += str(octet) + "."
    last_dec = last_dec[:-1]
    return first_dec, last_dec