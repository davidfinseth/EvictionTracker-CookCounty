from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
import MongoManager
import credentials


class Tennant:
    plaintiff = ""
    sherifName = ""
    defendant = []
    attorney = ""
    address = ""
    date = ""
    lat = ""
    long = ""
    url = ""
    casetype = ""
    caresActProtected = False
    def __init__(self,case_number):
        self.caseNumber = case_number

geolocator = Nominatim(user_agent=credentials.login['NominatimSecret'])
geolocator2 = GoogleV3(api_key=credentials.login['GoogleSecret'])

def FindLocation(tenant: MongoManager.Tenant) -> MongoManager.Tenant:
    try:
        location = geolocator.geocode(tenant.address)
    except:
        location == None
        pass
    if(location == None):
        try: 
            location = geolocator2.geocode(tenant.address)
        except:
            return
    print(location.address)
    latlong = [location.latitude,location.longitude]
    tenant.geo = latlong

def FindLocation2(data):

    try:
        location = geolocator.geocode(data)
    except:
        location == None
        pass
    if(location == None):
        try: 
            location = geolocator2.geocode(data)
        except:
            return
    print(location.address)
    latlong = [location.latitude,location.longitude]
    print(latlong)


def PrintZip(address):
    response = geolocator2.geocode(address)
    print(address)
    print(response.latitude)
    print(response.longitude)

