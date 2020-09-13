import GoogleSheetManager
from datetime import datetime
from mongoengine import *
import os

connect(host=os.environ.get("MongoSecret"))


class Tenant(Document):
    casenumber = StringField(unique=True)
    plaintiff = StringField()
    sherifName = StringField()
    defendant = ListField()
    attorney = StringField()
    address = StringField()
    date = DateTimeField(default=datetime.now)
    geo = GeoPointField()
    url = StringField()
    casetype = StringField()

def AddTenantToDatabase(data):
    record = Tenant(
        casenumber = data[0],
        plaintiff = data[3],
        defendant = data[5].split(','),
        attorney = data[4],
        address = data[6],
        date = datetime.strptime(data[1], '%m/%d/%Y'),
        url = data[8],
        casetype = data[2]
    )
    try:
         record.save()
    except:
        print ("Duplicate ID")
        pass

def UpdateDatabaseFromSheets():
    SheetsManager = GoogleSheetManager
    fulllist = SheetsManager.GetListFromSheets()
    for cols in fulllist:
        AddTenantToDatabase(cols)

def UpdateDatabaseFromDate(targetDate):
    SheetsManager = GoogleSheetManager
    fulllist = SheetsManager.GetListFromSheets()
    for cols in fulllist:
        if(targetDate == datetime.strptime(cols[1], '%m/%d/%Y')):
            AddTenantToDatabase(cols)
