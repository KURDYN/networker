from random import choice
from re import match

def mac_gen():
    mac = ''
    for x in range(6):
        mac += ''.join(choice('ABCDEF1234567890') for x in range(2))+'-'
    return mac[:-1]

class host:
    """
    host
        property specs:
        __status - 'WORKING' - 1, 'NOT WORKING' - 0
        __address - host's network identifier, template 'XXX.XXX.XXX.XXX'
        __mask - subnet mask, template '/MM'
        __mac - host MAC address
    """
    def __init__(self):
        self.status = 0
        self.mac = mac_gen()
        self.address = 'None'

    def __str__(self):
        if self.status == 0:
            status = 'NOT WORKING'
        else:
            status = 'WORKING'
        output = 'Host MAC address: ' + self.mac + '\n'
        output += 'Host status: ' + status + '\n'
        output += "Host's network identifier: " + self.address+'\n'
        return output

    def view_stat(self):
        print(self.status)

    def on(self):
        if self.status == 0:
            self.status = 1
            print('Host is now on.\n')
        elif self.status == 1:
            print('Host is already on.\n')

    def off(self):
        if self.status == 1:
            self.status = 0
            print('Host is now off.\n')
        elif self.status == 0:
            print('Host is already off.\n')

    def set_address(self, address):
        if match("^([0-9]{1,3}\.){3}[0-9]{1,3}$", address):
            # dividing address into separate octets+mask
            addr_div = address.split(".")
            for num in range(4):
                addr_div[num] = int(addr_div[num])
            # checking if the input is correct (an octet can't be greater than 255, mask must be between 23 and 31)
            if all(x < 256 for x in addr_div):
                print("Address assigned.\n")
                self.address = address
            else:
                raise Exception("Address incorrect, an octet can't be greater than 255.")
        else:
            raise Exception("Address incorrect, use template 'XXX.XXX.XXX.XXX'")


