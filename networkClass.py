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
        self.mask = "/"+str(addr_div(address)[1])
        self.broadcast = set_bcast(self.prefix, self.mask)
        self.usable = masks[self.mask]["usable"]
        self.range = find_range(self.prefix, self.broadcast)
        self.vlsm_subnets = {"Network": "VLSM is not set up."}
        self.vlsm_info = []
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

    def vlsm(self):
        subnet_sizes = []
        num = 1
        sum = 0
        #vlsm stat trackers
        assigned = 0
        used = 0
        #checking if input is correct
        while True:
            size = input("\nInsert number of hosts in Subnet" + str(num) + ", or type 'end' to finish: \n")
            if size == 'end':
                break
            else:
                try:
                    size = int(size)
                    if size > 0:
                        right_mask = find_mask(size)
                        sum += masks[right_mask]["usable"]
                        assigned += masks[right_mask]["usable"]+2
                        if sum > self.usable-(2*(num-1)):
                            print("Your subnets exceed max number of usable addresses in this network (" + str(
                                self.usable) + "), try again. \n")
                            subnet_sizes = []
                            num = 0
                            sum = 0
                        else:
                            subnet_sizes.append([num, size])
                    else:
                        print("A subnet must contain at leasst 1 host. Try again.")
                        num -= 1
                except ValueError:
                    print("This is not a number. Try again.")
                    num -= 1
            num += 1
        #sorting sizes descending for vlsm
        subnet_sizes.sort(key=lambda x: x[1], reverse=True)
        #creating and storing Network objects for subsequent subnets
        vlsm = {}
        #first network
        first_mask = find_mask(subnet_sizes[0][1])
        vlsm["Subnet"+str(subnet_sizes[0][0])] = Network(f"{addr_dec_str(self.prefix)}{first_mask}")
        #the rest of networks
        for num in range(1, len(subnet_sizes)):
            right_mask = find_mask(subnet_sizes[num][1])
            right_prefix = addr_bin_to_dec(vlsm["Subnet"+str(subnet_sizes[num-1][0])].broadcast)
            right_prefix[3] += 1
            vlsm["Subnet" + str(subnet_sizes[num][0])] = Network(f"{addr_dec_str(right_prefix)}{right_mask}")
            num += 1
        self.vlsm_subnets = vlsm
        unassigned = self.usable - assigned
        for num in subnet_sizes:
            used += num[1]
        self.vlsm_info = [assigned, used, unassigned]
        print(f"Network subnetted succesfully. \nAssigned: {assigned} ({float(assigned)/float(self.usable)*100}% of main), Used: {used} ({float(used)/float(self.usable)*100}% of main), Unassigned: {unassigned} ({float(unassigned)/float(self.usable)*100}% of main)")

    def get_vlsm_info(self):
        for name, subnet in self.vlsm_subnets.items():
            print(f"{name}:\n{subnet}", end="\n")
        if len(self.vlsm_info) > 0:
            assigned = self.vlsm_info[0]
            used = self.vlsm_info[1]
            unassigned = self.vlsm_info[2]
            print(
            f"Assigned: {assigned} ({float(assigned) / float(self.usable) * 100}% of main), Used: {used} ({float(used) / float(self.usable) * 100}% of main), Unassigned: {unassigned} ({float(unassigned) / float(self.usable) * 100}% of main)")

    def add_host(self):
        print()

