from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, timedelta
import time
import GoogleSheetManager
import GeoLocationManager
import MongoManager

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = GOOGLE_CHROME_PATH

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

def DocketSearch(date):
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    browser.get('http://www.cookcountyclerkofcourt.org/CourtCaseSearch/DocketSearch.aspx')
    try:
        division_form = browser.find_element_by_id('ctl00_MainContent_ddlDatabase_Input')
    except:
        return
    division_form.send_keys('Civil')
    type_form = browser.find_element_by_id('ctl00_MainContent_rbSearchType_ctl01')
    type_form.click()
    time.sleep(3)
    date_form = browser.find_element_by_id('ctl00_MainContent_dtFilingDate')
    date_form.send_keys(date)
    submit_button = browser.find_element_by_id('ctl00_MainContent_btnSearch')
    submit_button.click()

    try:
        element_present = EC.presence_of_element_located((By.ID, 'MainContent_gvResults'))
        WebDriverWait(browser, 60).until(element_present)
    except NoSuchElementException:
        return
    table = browser.find_element_by_id("MainContent_gvResults")
    rows = table.find_elements_by_tag_name("tr")
    for row in rows:
        cols = row.find_elements_by_tag_name("td")
        if(len(cols)>4):
              if((cols[4].text == "JOINT ACTION" or cols[4].text == "FORCIBLE ENTRY AND DETAINER") and cols[3].text == "P"):
                report = Tennant(cols[1].text)
                report.date = date
                report.casetype = cols[4].text
                tennantList.append(report)
    return 

def SheriffSearch(tennant):
    casenumberlookup = tennant.caseNumber.translate({ord(i): None for i in '-M'})
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    browser.get('https://civilprocess.ccsheriff.org/default1.asp')
    number_form = browser.find_element_by_id('casenum')
    number_form.send_keys(casenumberlookup)
    sumbit_btn = browser.find_element_by_id('Submit2')
    sumbit_btn.click()

    try:
        WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
    except NoSuchElementException:
        tennant.address = ''
        browser.close()
        return
    except TimeoutException:
        tennant.address =''
        browser.close()
        return
    table = browser.find_element_by_tag_name('tbody')
    rows = table.find_elements_by_tag_name("tr")
    if(len(rows)>1):
        cols = rows[2].find_elements_by_tag_name("td")
        if(len(cols)>2):
            print(cols[3].text)
            tennant.address = cols[3].text
    browser.close()
    return

def GetAllRecordsByDate(date):
    DocketSearch(date)
    print("DocketSearch Complete! Found ", len(tennantList))
    #GeoManager = GeoLocationManager
    for tennant in tennantList:
        time.sleep(10)
        progress = str(tennantList.index(tennant))
        totalLength = str(len(tennantList))
        print(progress +" out of "+totalLength)
        DocketSearchCase(tennant)
        SheriffSearch(tennant)
        #if(tennant.address != ""):
        #   tennant = GeoManager.FindLocation(tennant)
    print("SheriffSearch Complete! Found ", len(tennantList))
    SheetsManager = GoogleSheetManager
    SheetsManager.AddListToSheets(SheetsManager,tennantList)
    return

def DocketSearchCase(tennant):
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    browser.get('http://www.cookcountyclerkofcourt.org/CourtCaseSearch/DocketSearch.aspx')
    try:
        division_form = browser.find_element_by_id('ctl00_MainContent_ddlDatabase_Input')
    except:
        return
    division_form.send_keys('Civil')
    case_year = browser.find_element_by_id('ctl00_MainContent_txtCaseYear')
    case_year.send_keys(tennant.caseNumber[:4])
    division_code = browser.find_element_by_id('ctl00_MainContent_txtCaseCode')
    division_code.send_keys(tennant.caseNumber[5:7]) 
    case = browser.find_element_by_id('ctl00_MainContent_txtCaseNumber')
    case.send_keys(tennant.caseNumber[8:])
    submit_button = browser.find_element_by_id('ctl00_MainContent_btnSearch')
    submit_button.click()
    try:
        element_present = EC.presence_of_element_located((By.ID, 'body'))
        WebDriverWait(browser, 60).until(element_present)
    except NoSuchElementException:
        browser.close()
        return
    except UnexpectedAlertPresentException:
        browser.close()
        return
    link = browser.find_element_by_link_text("Print View")
    tennant.url = link.get_attribute("href")
    browser.switch_to.frame('MainContent_iFrameID')
    try:
        tennant.plaintiff = browser.find_element_by_xpath('//*[@id="objCaseDetails"]/table[2]/tbody/tr[2]/td[1]').text
    except NoSuchElementException:
        return
    tennant.attorney = browser.find_element_by_xpath('/html/body/form/div[5]/div[2]/table[2]/tbody/tr[2]/td[3]').text
    tennant.defendant = []
    try: 
        tennant.defendant.append(browser.find_element_by_xpath('/html/body/form/div[5]/div[2]/table[2]/tbody/tr[7]/td[1]').text)
    except NoSuchElementException:
        pass
    try:
        tennant.defendant.append(browser.find_element_by_xpath('/html/body/form/div[5]/div[2]/table[2]/tbody/tr[8]/td[1]').text)
    except NoSuchElementException:
        pass
    browser.close()
    return 

def IncrementDate(date):
    newdate = (datetime.strptime(date, '%m/%d/%Y') + timedelta(days=1)).strftime('%m/%d/%Y')
    return newdate

def GetAllRecordsBetweenDates(startDate,endDate):
    currentdate = startDate
    while currentdate != endDate:
        tennantList.clear()
        GetAllRecordsByDate(currentdate)
        currentdate = IncrementDate(currentdate)
        print(currentdate)
    return
    
def SearchAllCases():
    SheetsManager = GoogleSheetManager
    fulllist = SheetsManager.GetListFromSheets()
    for cols in fulllist:
        record = Tennant(cols[0])
        record.date = cols[1]
        record.casetype = cols[2]
        DocketSearchCase(record)
        time.sleep(10)

    SheetsManager.AddListToSheets(SheetsManager,tennantList)

def SherifSearchAll():
    SheetsManager = GoogleSheetManager
    fulllist = SheetsManager.GetListFromSheets()
    for cols in fulllist:
        tennant = PopulateTennant(cols)
        SheriffSearch(tennant)
        time.sleep(10)
    print("SheriffSearch Complete! Found ", len(tennantList))
    SheetsManager.AddListToSheets(SheetsManager,tennantList)
    return

def PopulateTennant(data):
    record = Tennant(data[0])
    if(len(data) > 1):
        record.date = data[1]
    if(len(data) > 2):
        record.casetype = data[2]
    if(len(data) > 3):
        record.plaintiff = data[3]
    if(len(data) > 4):
        record.attorney = data[4]
    if(len(data) > 5):
        record.defendant = data[5]
    if(len(data) > 6):
        record.address = data[6]
    if(len(data) > 8):
        record.url = data[8]
    return record

def UpdateLocation():
    for tenant in MongoManager.Tenant.objects(address__ne=' '):
        if not tenant.geo:
            return
        else:
            GeoLocationManager.FindLocation(tenant)
            tenant.save()

tennantList = []
GetAllRecordsByDate((datetime.today() - timedelta(days=3)).strftime('%m-%d-%Y'))
MongoManager.UpdateDatabaseFromSheets()
UpdateLocation()