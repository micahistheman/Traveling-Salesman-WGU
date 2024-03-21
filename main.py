# Micah Harwood StudentID:011037496
# C950 Data Structures and Algorithms II
import csv
import datetime
from PackageClass import Package
import TruckClass
from ChainingHash import ChainingHashTable

# Reference for load_package_data: WGU C950 - Webinar 2 - Getting Greedy, who moved my data
def load_package_data(csv_file, hash_table):
    with open("WGUPS PackageFile.csv") as package_csv:
        package_data = csv.reader(package_csv)
        for packages in package_data:
            pID = int(packages[0])
            pTruck = "Awaiting Truck Assignment"
            pAddress = packages[1]
            pCity = packages[2]
            pState = packages[3]
            pZIP = packages[4]
            pDeadline = packages[5]
            pWeight_KG = packages[6]
            pCurrent_State = "In hub. Estimated delivery.."
            pDelivery = None

            p = Package(pID, pTruck, pAddress, pCity, pState, pZIP, pDeadline, pWeight_KG, pCurrent_State, pDelivery)
            hash_table.insert(pID, p)

# Creates an instance of the hash table from the ChainingHash.py file
package_hashed = ChainingHashTable()
# Loads data from the specified csv file to the hash table instance via the load_package_data function
load_package_data("WGUPS PackageFile.csv", package_hashed)

# function to show the initial status of the packages prior to truck departure; called in the Main class
def initial_status():
    for i in range (len(package_hashed.table)):
        print (package_hashed.search((i + 1)))

#Create an instance of each Truck object representing the three trucks sent to deliver packages
truckOne = TruckClass.Truck(18, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East", datetime.timedelta(hours=8))
truckTwo = TruckClass.Truck(18, [3, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))
truckThree = TruckClass.Truck(18, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0, "4001 South 700 East", datetime.timedelta(hours=9))
#delivery_in_truck function defines the nearest neighbor algorithm
def delivery_in_truck(truck):
    to_deliver = []
    #print(len(truck.packages))
    for i in range(0, len(truck.packages)):
        #cycles through each package ID in the truck instance to search for
        # the correct package and its data in the hash table and places that data into the to_deliver list
        truck_package = truck.packages[i]
        load_package = package_hashed.search(truck_package)
        to_deliver.append(load_package)
        #print(load_package)
# print(delivery_in_truck(truckOne))
    truck.packages.clear()  # removes the packages list in the truck object to be replaced in nearest neighbor order by the while loop
    #delivery_length = len(to_deliver)
    # print(to_deliver)

    while len(to_deliver) > 0: # Goes through all items in to_deliver and finds the package
                               # with the shortest distance from the package at i
        next_address = 5000 # assigned to a number large enough to ensure the if statement executes
        nearest_package = None
        for i in to_deliver:
            #print(i.address)
            if Package.distance_between_points(Package.get_address(truck.address), Package.get_address(i.address)) <= next_address:
                next_address = Package.distance_between_points(Package.get_address(truck.address), Package.get_address(i.address))
                nearest_package = i
        truck.packages.append(nearest_package.ID) #adds the package the shortest distance away to the Truck packages list
        # print(truck.packages)
        truck.timeUpdate += datetime.timedelta(hours=next_address / 18) #calculates time taken to travel to the next address going 18 MPH where next_address is the distance in miles
        # print("Package", nearest_package.ID, "delivered: ", truck.timeUpdate)

        to_deliver.remove(nearest_package)
        truck.miles += next_address # adds the miles traveled to the next address on the trucks's "odometer"
        truck.address = nearest_package.address # updates the address of the truck as being at the delivery point of the current package
        nearest_package.delivery = truck.timeUpdate # logs the delivery time of the package
        nearest_package.departure = truck.departure # updates the package's departure time to track
                                                 # the package's state for the package_status function in the Package class
        nearest_package.pTruck = truck.truckNum # Assigns the package's truck number to the truck its loaded on


# the main class contains the user interface
#the user must use military time to check the status of one or all packages at that time
class Main:

   print("Welcome to the Western Governors University Parcel Service Portal!")
   userInput = input("To begin, enter 'Start' or enter 'Q' to quit:")
   if userInput == "Start":
       currentTime = input("In HH:MM enter the current time to check the details and current state of the packages")
       (h, m) = currentTime.split(":")
       inputToTime = datetime.timedelta(hours=int(h), minutes=int(m))
       priorToDeparture = datetime.timedelta(hours=(8))
       finalPackageDelivered = datetime.timedelta(hours=12, minutes=30)
       if inputToTime < priorToDeparture:
           initial_status() # returns the packages in their initial state "in hub" if given a time before the first truck departs

       else:
           # begin the process of sending each truck to deliver it's packages in their respective nearest neighbor order
           truckOne.truckNum = "Truck One"
           delivery_in_truck(truckOne)

           truckTwo.truckNum = "Truck Two"
           delivery_in_truck(truckTwo)

           truckThree.truckNum = "Truck Three"
           # Truck One finishes first so Truck 3's departure time will be the time Truck One made its last delivery
           truckThree.departure = truckOne.timeUpdate
           # print(truckThree.departure)

           if inputToTime >= datetime.timedelta(hours=10, minutes=20):
               package_nine = package_hashed.search(9)
               package_nine.address = "410 S State St"
               package_nine.zip = "84111"

           delivery_in_truck(truckThree) # implement after the possible address update of package 9

           if inputToTime > finalPackageDelivered: # prints total miles traveled by all 3 trucks if the user enters a time where all trucks finished their deliveries
               print("All packages delivered. Total miles traveled:", (truckOne.miles + truckTwo.miles + truckThree.miles))
           allOrNone = input("Type 'All' to see the status of all packages or 'One' to view a specific package")
           if allOrNone == "All":
               for package_ID in range(1, 41): # cycles through each package stored in the hash by its ID
                   package = package_hashed.search(package_ID)
                   package.package_status(inputToTime)
                   print(package)

           elif allOrNone == "One":
               userPackage = input("Enter the ID # of the package you'd like to check")
               package = package_hashed.search(int(userPackage)) #assigns package to the package object in the hash specified by the ID given by the user
               package.package_status(inputToTime)
               print(package)
           else:
               print("Invalid option. Program terminating...")
   else:
       print("You have chosen to quit. Program terminating...")

