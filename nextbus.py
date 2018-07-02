import json
import requests
import sys
import string


def readRoutes():
    '''Reads route data from routes.json file'''

    # Open file for reading
    f = open("routes.json", "r")
    contents = f.read()

    # Close file
    f.close()
    
    return contents


def updateRoutes():
    '''Retrieves route data from API to update routes.json file'''

    # Open file for writing
    f = open("routes.json", "w")
    
    # Request the list of bus routes
    response = requests.get("http://svc.metrotransit.org/NexTrip/Routes?format=json")
    
    if(response.status_code == 200):
        # Store results into a list
        f.write(response.content.decode('utf-8'))
        print("Routes file updated")
    else:
        print("Error: [BUS ROUTE] Code - " + response.status_code)

    f.close()


def getRouteNumberFromFile(BUS_ROUTE):
    '''Gets Route Number from the input route name using routes.json'''

    route = ""

    route_array = json.loads(readRoutes())
        
    for item in route_array:
        # Find the route number of the specified route
        if(BUS_ROUTE.upper() in item["Description"].upper()):
            route = item["Route"]
    if(not route):
        print("Error: [BUS ROUTE] The requested bus route does not exist.")

    return route


def getDirection(DIRECTION):
    '''Gets Direction # from user's string'''
    
    # d is so the program will work regardless of the inputs caps
    d = DIRECTION.upper()
    
    if  (d == "SOUTH"):
        direction = 1
    elif(d == "EAST" ):
        direction = 2
    elif(d == "WEST" ):
        direction = 3
    elif(d == "NORTH"):
        direction = 4
    else:
        print("Error: [DIRECTION] Please enter one of the following: north, south, east, west")
        direction = 0

    return direction


def getRouteNumber(BUS_ROUTE):
    '''Gets Route Number from the input route name'''

    route = ""

    # Request the list of bus routes
    response = requests.get("http://svc.metrotransit.org/NexTrip/Routes?format=json")
    
    if(response.status_code == 200):
        # Store results into a list
        route_array = json.loads(response.content.decode('utf-8'))
        
        for item in route_array:
            # Find the route number of the specified route
            if(BUS_ROUTE.upper() in item["Description"].upper()):
                route = item["Route"]
        if(not route):
            print("Error: [BUS ROUTE] The requested bus route does not exist.")
    else:
        print("Error: [BUS ROUTE] Code - " + response.status_code)

    return route


def getStopId(BUS_ROUTE, DIRECTION, BUS_STOP_NAME):
    '''Gets Bus Stop ID from the given route ID, direction, and bus stop name'''

    stop = ""
    
    # Request the bus stops on the specified route and bearing
    response = requests.get("http://svc.metrotransit.org/NexTrip/Stops/" + str(BUS_ROUTE) + "/" + str(DIRECTION) + "?format=json")

    if(response.status_code == 200):

        # Store results into a list
        stop_array = json.loads(response.content.decode('utf-8'))
        
        for item in stop_array:
            # Find the ID code of the specified bus stop
            if(BUS_STOP_NAME.upper() in item["Text"].upper()):
                stop = item["Value"]
        if(not stop):
            print("Error: [STOP ID] The requested bus stop ID does not exist.") 
    else:
        print("Error: [STOP ID] Code - " + response.status_code)
        
    return stop


def getNextBus(BUS_ROUTE, DIRECTION, STOP_ID):
    '''Gets the number of minutes until the next bus departs'''

    minutes = ""

    # Request the departure data for our parameters
    response = requests.get("http://svc.metrotransit.org/NexTrip/" + str(BUS_ROUTE) + "/" + str(DIRECTION) + "/" + STOP_ID + "?format=json")

    if(response.status_code == 200):
        # Store results into a list
        bus_array = json.loads(response.content.decode('utf-8'))

        # If any results, pick the first one
        if(len(bus_array) > 0):
            minutes = bus_array[0]["DepartureText"]
    else:
        print("Error: [NEXT BUS] The requested departure data does not exist. Code - " + response.status_code)

    return minutes

# nextbus.py "Brklyn Center - Fremont - 26th Av - Chicago - MOA" "7th St  and Olson Memorial Hwy" "north"

# Handle arguments
# always 3 arguments

if(len(sys.argv) < 4):
    print("Error: Not enough arguments. Format is: nextbus.py {BUS ROUTE} {BUS STOP NAME} {DIRECTION}")
elif(len(sys.argv) > 4):
    print("Error: Too many arguments. Format is: nextbus.py {BUS ROUTE} {BUS STOP NAME} {DIRECTION}")
else:
    # Pull arguments from argv array
    BUS_ROUTE, BUS_STOP_NAME, DIRECTION = sys.argv[1], sys.argv[2], sys.argv[3]
    
    direction = getDirection(DIRECTION)

    # Using route data from server
    route = getRouteNumber(BUS_ROUTE)

    # Using route data from file.
    #updateRoutes()
    #route = getRouteNumberFromFile(BUS_ROUTE)
    
    if(route and direction):
        
        stop_id = getStopId(route, direction, BUS_STOP_NAME)
        
        if(stop_id):
            next_bus = getNextBus(route, direction, stop_id)
            print(next_bus)

#updateRoutes()




