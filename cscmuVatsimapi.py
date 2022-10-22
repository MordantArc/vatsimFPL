from mimetypes import init
from cmu_graphics import *
import requests
import math
import json
import time

app.ticksPerSecond = 60

app.background = rgb(125,157,189)

app.currentRefreshTick = 0
refreshTick = 1200

vatsimID = 0

response = requests.get("https://api.vatsim.net/api/")

baseLink = "https://api.vatsim.net/api/"

initGroup = Group()


#Labels n shit that displays changable values from the fp
squawkG = Label("0000",375,15,bold=True)
squawkD = Label("Squawk:",335,15)
altitudeG = Label("0000",375,30,bold=True)
altitudeD = Label("Filed Alt:",330,30)
callsign = Label("-----",370,45,bold=True)
callsignD = Label("Callsign:",315,45)
cruisespdG = Label("000"+"kts",375,60,bold=True)
cruisespdD = Label("Cruise Speed:",315,60)
arrow = Line(75,350,325,350,lineWidth=10,arrowEnd=True)
dep = Label("----",20,350,bold=True,size=24,align='left')
arr = Label("----",380,350,bold=True,size=24,align='right')
altD = Label("Alt",200,365,size=12.5)
alt = Label("----",200,385,bold=True,size=15)
guiGroup = Group(squawkG,altitudeG,squawkD,altitudeD,callsign,callsignD,cruisespdD,cruisespdG,arrow,dep,arr,alt,altD)
guiGroup.visible = False

#ignore these
FTF = {}
text = ""

#Just asks if the gui is being shown, kinda stupid because we can just call guiGroup.visible and use an If statement
guiUp = False

#prints any given JSON
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

#finds the vatsim CID from the txt file
CID = open('vatsimcid.txt','r')
vatsimID = CID.read().split('\n')[1] 
CID.close()

'''
This is the juicy shit. Val must be a JSON and what it does is it grabs the info from
the "result" entry in the main dict. The result from that is a list containing the
sub-dicts that outline each flight. 

Eg: printResult(main JSON of fp) = [{fp1:'fp1'},{fp2_info:'fp2_data'}]
'''
def printResult(val):
    filterToFlights = val['results']
    FTF = filterToFlights.pop(0)
    for i in FTF:
        print(i,'->',FTF[i])
    return FTF

'''
Initial text, virtually invisible. Just spits stuff out as it tests the connection.
It also grabs the current fp when opening to use as the base of the gui. This all gets
updated later, just so that we have info for the GUI off the bat
'''
def testSample(lS):
    r1 = requests.get((baseLink+"ratings/"+str(vatsimID)+"/flight_plans/")) #My Id in Vatsim is 1669884
    rr1 = r1.json()
    FTFF = printResult(rr1)
    routeFF = FTFF['route']
    flPln = Label(("Current Flight Plan:"),5,lS,align="left",font="calibri",size=15,bold=True)
    lS += 25
    actFlPln = Label(routeFF,5,lS,align="left",font="calibri",size=15,bold=True)
    lS += 25
    allInfo = Label(FTFF,200,lS,align="left",font="calibri",size=7.5,bold=True)
    lS += 25
    initGroup.add(flPln,actFlPln,allInfo)
    sleep(1.5)
    return FTFF


connectAttempt = response.status_code  
initGroupLineMaker = 25    
if (connectAttempt == 200):
    print("Return", connectAttempt)
    print("Connection success.")
    sucCon = Label("Connected to Vatsim API.",5,initGroupLineMaker,align="left",font="calibri",size=15,bold=True)
    initGroupLineMaker += 25
    initGroup.add(sucCon)
    FTFF = testSample(initGroupLineMaker)
else:
    print("Error",connectAttempt)
    erCon = Label(("Error",connectAttempt),5,initGroupLineMaker,align="left",font="calibri",size=15,bold=True)
    initGroup.add(erCon)
    initGroupLineMaker += 25
    print("An unknown error has occured.")
    erCon2 = Label("An unknown error has occured.",5,initGroupLineMaker,align="left",font="calibri",size=15,bold=True)
    initGroup.add(erCon2)
    initGroupLineMaker += 25
    stopApp = Label("Stopping the App.",5,initGroupLineMaker,align="left",font="calibri",size=15,bold=True)
    app.stop()

eUI = "yes" # app.getTextInput("Enter GUI?").lower()
if (eUI == "yes"):
    initGroup.visible = False
    guiUp = True
    guiGroup.visible = True
elif (eUI == "no"):
    clA = app.getTextInput("Close Program?").lower()
    if (clA == "yes"):
        print("App stopped intentionally. Closing the program.")
        app.stop()
    else:
        pass

app.currentRefreshTick = 1200

def onStep():
    if (guiUp == False):
        pass
    elif (guiUp == True):
        if (app.currentRefreshTick >= refreshTick):
            app.currentRefreshTick = 0
            FTFF = testSample(0)
            squawkG.value = FTFF['assignedsquawk'] # note - maybe make an alert to show a change in code? Alteration etc
            altitudeG.value = FTFF['altitude']
            callsign.value = FTFF['callsign']
            cruisespdG.value = FTFF['cruisespeed']+"kts"
            dep.value = FTFF['dep']
            arr.value = FTFF['arr']
            alt.value = FTFF['alt']
    app.currentRefreshTick += 1


cmu_graphics.run()