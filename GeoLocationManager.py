from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
import MongoManager
import os

geolocator = Nominatim(user_agent=os.environ.get("NominatimSecret"))
geolocator2 = GoogleV3(api_key=os.environ.get("GoogleSecret"))

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