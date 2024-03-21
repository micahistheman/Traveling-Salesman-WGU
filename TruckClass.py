class Truck:
    def __init__(self, MPH, packages, miles, address, departure):
        self.MPH = MPH
        self.packages = packages
        self.miles = miles
        self.address = address
        self.departure = departure
        self.timeUpdate = departure
        self.truckNum = None

    def __str__(self):
        return "%s, %s, %s, %s, %s" % (self.MPH, self.packages, self.miles, self.address, self.departure)