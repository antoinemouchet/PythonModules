import json
import math as m
import matplotlib as mil
# Add it before launching matplotlib
mil.use('TkAgg') 
import matplotlib.pyplot as plt

class Agent:
    """
    Class of the actual agent
    """
    # Constructor
    def __init__(self, position, **agent_attributes):
        self.position = position
        # Loop to get all attributes of agent
        for attr_name, attr_value in agent_attributes.items():
            setattr(self, attr_name, attr_value)



class Position:
    """
    Class of a position
    """
    # Constructor
    def __init__(self, longitudeDegrees, latitudeDegrees):
        self.latitudeDegrees = latitudeDegrees
        self.longitudeDegrees = longitudeDegrees

    # Change longitude and latitude to radian
    @property
    def longitude(self):
        return self.longitudeDegrees * m.pi / 180
    
    @property
    def latitude(self):
        return self.latitudeDegrees * m.pi / 180
    


class Zone:
    """
    Class of an area
    """

    # Class atttributes, to be respected for each instance
    MIN_LONGITUDE_DEGREES = -180
    MAX_LONGITUDE_DEGREES = 180
    MIN_LATITUDE_DEGREES = -90
    MAX_LATITUDE_DEGREES = 90
    EARTH_RADIUS_KILOMETERS = 6371
    # Degrees of longitude
    WIDTH_DEGREES = 1
    # Degrees of latitude
    HEIGHT_DEGREES = 1

    # Store each new zone
    ZONES = []

    # Constructor
    def __init__(self, corner1, corner2):

        # Top right and bottom left corners
        self.corner1 = corner1
        self.corner2 = corner2

        # Inhabitants 
        self.inhabitants = []

    def addInhabitant(self, inhabitant):
        self.inhabitants.append(inhabitant)

    @property
    def population(self):
        return len(self.inhabitants)
 
    # Create a zone for each combinaison of latitude and longitude
    @classmethod
    def _initializeZones(cls):
        # Loop on latitude
        for latitude in range (cls.MIN_LATITUDE_DEGREES, cls.MAX_LATITUDE_DEGREES, cls.HEIGHT_DEGREES):
            # Loop on longitude
            for longitude in range(cls.MIN_LONGITUDE_DEGREES, cls.MAX_LONGITUDE_DEGREES, cls.WIDTH_DEGREES):
                bottom_left_corner = Position(longitude, latitude)
                top_right_corner = Position(longitude + cls.WIDTH_DEGREES, latitude + cls.HEIGHT_DEGREES)
                # Add the new zone in list of zone
                zone = Zone(bottom_left_corner, top_right_corner)
                cls.ZONES.append(zone)
        print(len(cls.ZONES))

    def contains(self, position):
        return position.longitude >= min(self.corner1.longitude, self.corner2.longitude) and \
            position.longitude < max(self.corner1.longitude, self.corner2.longitude) and \
            position.latitude >= min(self.corner1.latitude, self.corner2.latitude) and \
            position.latitude < max(self.corner1.latitude, self.corner2.latitude)
                
    @classmethod
    def findZoneThatContains(cls, position):

        # Initialize zones automatically if necessary
        if not cls.ZONES:
            cls._initializeZones()
    
        # Compute the index in the ZONES array that contains the given position
        longitudeIndex = int((position.longitudeDegrees - cls.MIN_LONGITUDE_DEGREES)/ cls.WIDTH_DEGREES)
        latitudeIndex = int((position.latitudeDegrees - cls.MIN_LATITUDE_DEGREES)/ cls.HEIGHT_DEGREES)
        # 180-(-180) / 1
        longitudeBins = int((cls.MAX_LONGITUDE_DEGREES - cls.MIN_LONGITUDE_DEGREES) / cls.WIDTH_DEGREES)

        # Get index of zone
        zone_index = latitudeIndex * longitudeBins + longitudeIndex

        # Just checking that the index is correct
        zone = cls.ZONES[zone_index]
        assert zone.contains(position)

        return zone

    @property
    def width(self):
       return abs(self.corner1.longitude - self.corner2.longitude) * self.EARTH_RADIUS_KILOMETERS
       
    @property
    def height(self):
        return abs(self.corner1.latitude - self.corner2.latitude) * self.EARTH_RADIUS_KILOMETERS

    @property
    def area(self):
        """Compute the zone area, in square kilometers"""
        return self.height * self.width

    def population_density(self):
        """Population density of the zone, (people/km²)"""
        # Note that this will crash with a ZeroDivisionError if the zone has 0
        # area, but it should really not happen
        return self.population / self.area

    def average_agreeableness(self):
        # If there is no inhabitants in the zone
        if not self.inhabitants:
            return 0
        
        # Initialize list to store all agreeableness
        agreeableness = []

        # Loop on the inhabitants of the zone
        for inhabitant in self.inhabitants:
            agreeableness.append(inhabitant.agreeableness)
        
        # Get the average 
        return sum(agreeableness) / self.population

class BaseGraph:

    def __init__(self):
        self.title = "Your graph title"
        self.x_label = "X-axis label"
        self.y_label = "X-axis label"
        self.show_grid = True

    def show(self, zones):
        # x_values = gather only x_values from our zones
        # y_values = gather only y_values from our zones
        x_values, y_values = self.xy_values(zones)
        plt.plot(x_values, y_values, '.')
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)
        plt.grid(self.show_grid)
        plt.show()

    def xy_values(self, zones):
        raise NotImplementedError


class AgreeablenessGraph(BaseGraph):

    def __init__(self):
        super().__init__()
        self.title = "Nice people live in the countryside"
        self.x_label = "population density"
        self.y_label = "agreeableness"

    def xy_values(self, zones):
        x_values = [zone.population_density() for zone in zones]
        y_values = [zone.average_agreeableness() for zone in zones]
        return x_values, y_values



def main():

    # Loop on agents in json file
    for agent_attributes in json.load(open("agents-100k.json")):
        # Get latitude and longitude of agent
        latitude = agent_attributes.pop("latitude")
        longitude = agent_attributes.pop("longitude")
        position = Position(longitude, latitude)
        #
        agent = Agent(position, **agent_attributes)
        zone = Zone.findZoneThatContains(position)
        zone.addInhabitant(agent)
    
    agreeableness_graph = AgreeablenessGraph()
    agreeableness_graph.show(Zone.ZONES)

if __name__ == "__main__":
    main()