import gspread
import os

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

def authenticate():
    gc = gspread.service_account(filename=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
    sh = gc.open("evictions_served_Chicago")
    return sh


def AddListToSheets(self,tennantList):
    sheet = authenticate()
    worksheet = sheet.sheet1
    rowsToAdd = []
    for tennant in tennantList:
        new_row = (tennant.caseNumber,tennant.date,tennant.casetype,tennant.plaintiff,tennant.attorney,' '.join(tennant.defendant),tennant.address,"",tennant.url)
        rowsToAdd.append(new_row)
    worksheet.append_rows(rowsToAdd)

def UpdateSheet(self,tennantList):
    sheet = authenticate()
    worksheet = sheet.sheet1
    rowsToAdd = []
    for tennant in tennantList:
        new_row = (tennant.caseNumber,tennant.date,tennant.casetype,tennant.plaintiff,tennant.attorney,tennant.defendant[0]+","+tennant.defendant[1],tennant.address,"",tennant.url)
        rowsToAdd.append(new_row)
    worksheet.update('A2',rowsToAdd)

def GetListFromSheets():
    sheet = authenticate()
    worksheet = sheet.sheet1
    fulllist = worksheet.get_all_values()
    fulllist.remove(fulllist[0])
    return fulllist