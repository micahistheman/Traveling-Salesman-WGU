import csv

# Reads the OnlyDistance.csv file
distance_list = []
with open('WGUPS OnlyDistance.csv', mode='r') as distance_file:
     csvFile = csv.reader(distance_file)
     for lines in csvFile:
         distance_list.append(lines)
 # for address in distance_list:
 #     print(address)

# reads the PackageFile.csv file
# package_list = []
# with open('WGUPS PackageFile.csv', mode='r') as package_file:
#     csvFile = csv.reader(package_file)
#     for lines in csvFile:
#         package_list.append(lines)
    # for address in package_list:
    #  print(address)

    # reads the AddressTable.csv file
address_list = []
with open('WGUPS AddressTable.csv', mode='r') as address_file:
    csvFile = csv.reader(address_file)
    for lines in csvFile:
        address_list.append(lines)
    # for address in address_list:
    #  print(address)

class Package:
    def __init__(self, ID, pTruck, address, city, state, zip, deadline, weightKG, current_state, delivery):
        self.ID = ID
        self.pTruck = pTruck
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weightKG = weightKG
        self.current_state = current_state
        self.departure = None
        self.delivery = None


    def __str__(self): # "%s" string formats the output where each %s is the ID, then address etc"
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.pTruck, self.address, self.city, self.state, self.zip, self.deadline, self.weightKG, self.current_state, self.delivery)


    def get_address(address):
        for i in address_list:
            if address in i[2]:
                return int(i[0]) # returns the id of the address which corresponds to its row in the distance table
        return -1 # if an address is not in the address_list
    # print(get_address("1060 Dalton Ave S"))


    def package_status(self, currentTime):
        if self.delivery < currentTime:
            self.current_state = "Package delivered at.."
        elif self.departure > currentTime:
            self.current_state = "In transit. Estimated arrival.."
        else:
            self.current_state = "Waiting in hub. Expected delivery.."

    def distance_between_points(x, y):
        distance = distance_list[x][y] # used in conjunction with get_address function, takes the IDs of two addresses and returns the distance from the list
        # an example would be points x = 2 y = 1 would return 7.1 the distance between sugar house park and the international peace gardens
        if distance is None or distance == '':
            distance = distance_list[y][x] #will search for distance from y to x if x to y is not found
        return float(distance)
    # print(distance_between_points(3, 4))
