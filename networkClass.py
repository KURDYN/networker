from net_functions import *
class Network:
    """
    Network:
        property specs:

        __status - 'WORKING' - 1, 'NOT WORKING' - 0

        __prefix - network address

        __mask - subnet mask, between 24 and 30

        __broadcast - broadcast address,

        __range - host range

        __usable - amount of usable host addresses

        __hosts - list of host addresses and their status
    """

    def __init__(self, address):
        self.status = 0
        self.prefix = set_prefix(address)
        self.mask = address[-3:]
        self.broadcast = set_bcast(self.prefix, self.mask)
        self.usable = masks[self.mask]["usable"]
        self.range = find_range(self.prefix, self.broadcast)
        self.hosts = []

    def __str__(self):
        if self.status == 0:
            status = 'NOT WORKING'
        else:
            status = 'WORKING'
        output = 'Network prefix: ' + addr_dec_str(self.prefix)+'\n'
        output += 'Subnet mask: ' + self.mask + ', ' + masks[self.mask]["dec"] + '\n'
        output += 'Network broadcast address: ' + addr_dec_str(self.broadcast) + '\n'
        output += 'Usable addresses range: ' + addr_dec_str(self.range[0])+ " - " + addr_dec_str(self.range[1]) + '\n'
        output += 'Number of usable addresses: ' + str(self.usable) + ', used: ' + str(len(self.hosts)) + ' (' + str(
            masks[self.mask]["usable"]) + ' max)\n'
        output += 'Network status: ' + status + '\n'
        return output

    def view_stat(self):
        print(self.status)

    def on(self):
        if self.status == 0:
            self.status = 1
            print('Network is now on.\n')
        elif self.status == 1:
            print('Network is already on.\n')

    def off(self):
        if self.status == 1:
            self.status = 0
            print('Network is now off.\n')
        elif self.status == 0:
            print('Network is already off.\n')

    def add_host(self):
        print()