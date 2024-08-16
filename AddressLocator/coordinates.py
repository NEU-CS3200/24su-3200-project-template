from geopy.geocoders import Nominatim

#Function that converts an address into coordinates
def getCoordinates(address):
    # Initialize the geocoder
    geolocator = Nominatim(user_agent="homefinder") 

    # Geocoding the address
    location = geolocator.geocode(address)

    # Extract latitude and longitude
    latitude = location.latitude
    longitude = location.longitude

    # Print the results

    return [latitude,longitude]
