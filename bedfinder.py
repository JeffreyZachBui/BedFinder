# For google maps
import googlemaps
import uuid
from datetime import datetime
from geopy.geocoders import Nominatim
import certifi
import ssl
import geopy.geocoders
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx


# Measuring distance
from geopy.distance import vincenty

# For csv files
import csv
import numpy as np
import pandas as pd
import io

# Key
gmaps = googlemaps.Client(key='AIzaSyBRwVTuOwLu23OQYwiacFMLopwC7dzMUJE')

# Below are global variables for user location
lat = 0
lng = 0
number_detoxcenters = 0
centers = []
centers_nearby = {}

keylist = centers_nearby.keys()


# Funciton definitons
# Counts the number of detox centers in csv file

def counter():
    file = open("DetoxCenters.csv")
    num = len(file.readlines())
    global number_detoxcenters
    number_detoxcenters = num

# Gets user coordinates in longitude and latitude
def get_coordinates():
    s="%012x"%uuid.getnode()
    mac = ':'.join(s[i*2:i*2+2] for i in range(6))
    dict = {"macAddress": mac}
    result = gmaps.geolocate(dict)
    global lat
    lat = result['location']['lat']
    global lng 
    lng = result['location']['lng']
    return_location(lat, lng)

# Convert latitude/longitude to an address
def return_location(x, y):
    print("Your location is:")
    print("Latitude: ", x, " ", "Longitude: ", y)
    a = str(x)
    b = str(y)
    geolocator = Nominatim()
    location = geolocator.reverse(a + ", " + b)
    print(location.address)

# Measure distances
def measure_distances(x, y):
    user_location = (lat, lng)
    destination = (x, y)
    return (vincenty(user_location, destination).miles)


# This will put all detox centers into an array
def csv_array():
    ifile = open('DetoxCenters.csv', 'rU')
    reader = csv.reader(ifile, delimiter=";")
    rownum = 0	
    global centers
    centers = []
    for row in reader:
        centers.append (row)
        rownum += 1
    ifile.close()


# This will get the distances from user location to each detox center
# First, this will extract each location of each detox center
def distance_keys():
    my_csv = pd.read_csv('DetoxCenters.csv')
    # Store longitude and latitude into arrays
    t_lat = []
    t_lat = my_csv.latitude
    t_long = []
    t_long = my_csv.longitude
    return_distances(t_lat, t_long)

# This will return the distance of each detox center
def return_distances(x, y):

    # Counter Variable
    j = 0
    while (j < number_detoxcenters-1):
        distance = measure_distances(x[j], y[j])
        assign_keys(distance, j)
        j += 1
    

# This will then make the distances to a key, then assign each key to
# a detox center in a hash table.
def assign_keys(x, y):
    
    global centers_nearby
    centers_nearby[x] = centers[y+1]

# This will then sort the detox centers (specifically the keys) by distance. Then,
# the keys will identify the detox center
def sort_centers():
    global keylist
    global min_center
    keylist = list(centers_nearby.keys())
    keylist.sort()
    string = "miles away"
    while (min_center < max_center):
        # Get the keys in order
        print("Distance (miles away):")
        key = (keylist[min_center])
        print(key)
        # Get detox center based on key
        print("Center:")
        print(centers_nearby[key])
        min_center += 1
    user_interface()

min_center = 0
max_center = 5

def load_more():
    global min_center
    global max_center
    min_center += 5
    max_center += 10
    sort_centers()
    

def user_interface():    
    load_button = input("press 1 to load 5 more offices\n")
    if (load_button == 1):
        load = True
        load_more()


def run_prog():
    counter()    
    get_coordinates()
    csv_array()
    distance_keys()
    print("Here are the nearest detox centers to you and their distances")
    sort_centers()


run_prog()