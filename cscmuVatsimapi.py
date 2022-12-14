from asyncore import write
from datetime import date
import calendar
from mimetypes import init
from cmu_graphics import *
import requests
import math
import json
import time
import os
import csv
from ccvaClasses import *

app.ticksPerSecond = 60

app.background = rgb(125,157,189)

app.currentRefreshTick = 0
refreshTick = 1200

vatsimID = 0

logNo = 0

response = requests.get("https://api.vatsim.net/api/")

baseLink = "https://api.vatsim.net/api/"

curDT = str(time.time_ns())

curfile = "./data/datafile"+curDT+".csv"

initGroup = Group()
routeGroup = Group()

curDate = ((str(time.asctime())).replace(":","-")).replace(" ","_")
print(curDate)

#Labels that display changable values from the fp
squawkG = Label("0000",375,15,bold=True)
squawkD = Label("Squawk:",335,15)
altitudeG = Label("0000",375,30,bold=True)
altitudeD = Label("Filed Alt:",330,30)
callsign = Label("-----",370,45,bold=True)
callsignD = Label("Callsign:",315,45)
cruisespdG = Label("000"+"kts",375,60,bold=True)
cruisespdD = Label("Cruise Speed:",315,60)
arrow = Line(75,350,325,350,lineWidth=5,arrowEnd=True)
dep = Label("----",20,350,bold=True,size=24,align='left')
arr = Label("----",380,350,bold=True,size=24,align='right')
altD = Label("Alt",200,365,size=12.5)
alt = Label("----",200,385,bold=True,size=15)
routeLabel = Label("Route:",10,25,size=20,bold=True,align='left')
weightD = Label('Weight Catagory:',305,75)
weightG = Label('----',370,75,bold=True)
guiGroup = Group(squawkG,altitudeG,squawkD,altitudeD,
    callsign,callsignD,cruisespdD,cruisespdG,arrow,
    dep,arr,alt,altD,weightD,weightG)
guiGroup.visible = False
routeGroup.visible = False

#ignore these, just the dicts and lists for the FTF and route list
FTF = {}
text = ""
routeList = []
log = {}

#Just asks if the gui is being shown, kinda unecessary because we can just call guiGroup.visible and use an If statement
guiUp = False

#prints any given JSON
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

#finds the vatsim CID from the txt file
CID = open('vatsimcid.txt','r')
vatsimID = CID.read().split('\n')[1] 
CID.close()

def writeSomethingCSV(file,subj,body,notes):
    csvCur = CurCSV(file)
    curt = str(time.time_ns())
    csvCur.writeFile(curt,subj,body,notes)

'''
This is the juicy stuff*. Val must be a JSON and what it does is it grabs the info from
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

def separateRoute(val):
    route = val['route']
    print("Filed Route Below:")
    routeList = route.split()
    mstrRouteList = route
    routeLength = len(routeList)
    for x in range(routeLength):
        routeSnippet = routeList.pop(0)
        print(routeSnippet)
    return mstrRouteList

def initRoute(val):
    route = val['route']
    routeList = route.split()
    routeLength = len(routeList)
    lS2 = 50
    for x in range(routeLength):
        routeSnippet = routeList.pop(0)
        line = Label(routeSnippet,15,lS2,bold=True,size=15,align='left')
        routeGroup.add(line)
        lS2 += 20

def stdLogUpt(subj):
    route = ('./logs/log' + curDate + '.txt')
    with open(route, 'a') as f:
        f.write('( /// Time /// -' + curDate + ")\n")
        f.write(f"({subj})\n\n")
        f.write("(>~<)\n\n")

def initLogDir():
    try:
        open = open('./logs/logs.txt','r')
    except FileNotFoundError:
        os.mkdir("./logs/")
        stdLogUpt("DIR UPD","'logs' dir not found. Creating new logs dir.")
    try:
        os.mkdir("./data/")
    except:
        pass

def uptLogPiece(subj):
    route = ('./logs/log' + curDate + '.txt')
    with open(route, 'a') as f:
        f.write(subj)

def uptLog(subj,notes):
    curTime = str(time.asctime())
    uptLogPiece(f'/// Time /// - {curTime}\n')
    uptLogPiece(f'Subject {subj}\n')
    uptLogPiece(f'Notes: {notes}\n\n')
    uptLogPiece("-------------------------|-------------------------\n\n")

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
    time.sleep(1.5)
    return FTFF

connectAttempt = response.status_code  
initGroupLineMaker = 25    
if (connectAttempt == 200):
    writeSomethingCSV(curfile,'Subject','Body Info','Notes(post scriptum)')
    print("Return", connectAttempt)
    print("Connection success.")
    sucCon = Label("Connected to Vatsim API.",5,initGroupLineMaker,align="left",font="calibri",size=15,bold=True)
    initGroupLineMaker += 25
    initGroup.add(sucCon)
    uptLog('INIT APP','App opened and is running properly.')
    FTFF = testSample(initGroupLineMaker)
    writeSomethingCSV(curfile,'INIT APP','App opened and is running properly.','Below is data recorded from SimConnect.')

else:
    print("Error",connectAttempt)
    erCon = Label(("Error",connectAttempt),5,initGroupLineMaker,align="left",font="calibri",size=15,bold=True)
    initGroup.add(erCon)
    initGroupLineMaker += 25
    print("An unknown error has occured.")
    uptLog("XX -|- FATAL ERROR -|- XX","An unknown error has occured. Network error No.",connectAttempt)
    writeSomethingCSV(curfile,'FATAL ERROR','An unknown network error has occured.',f'Error code: {connectAttempt}')
    erCon2 = Label("An unknown error has occured.",5,initGroupLineMaker,align="left",font="calibri",size=15,bold=True)
    initGroup.add(erCon2)
    initGroupLineMaker += 25
    stopApp = Label("Stopping the App.",5,initGroupLineMaker,align="left",font="calibri",size=15,bold=True)
    writeSomethingCSV(curfile,'APP STOP COMMAND','App is stopping.','This is the end of the file.')
    app.stop()

eUI = "yes" # app.getTextInput("Enter GUI?").lower()
if (eUI == "yes"):
    initGroup.visible = False
    guiUp = True
    guiGroup.visible = True
    routeGroup.visible = True
    uptLog("GUI START","GUI has been entered, exiting startup stage.")
elif (eUI == "no"):
    clA = app.getTextInput("Close Program?").lower()
    if (clA == "yes"):
        print("App stopped intentionally. Closing the program.")
        uptLog("APP STOP", "App stopped intentionally.")
        writeSomethingCSV(curfile,'APP STOP COMMAND','App is stopping.','This is the end of the file.')
        app.stop()
    else:
        pass

app.currentRefreshTick = 1200

def refreshRoute():
    routeGroup.clear()
    initRoute(FTFF)

def updateData():
    writeSomethingCSV(curfile,'----','DATA PACKET START','----')
    writeSomethingCSV(curfile,'NO DATA','No data is available to display.','This feature is not available, however if you see this it works :)')
    writeSomethingCSV(curfile,'----','DATA PACKET END','----')
    pass

def logMasterUpdate(alt,aspd,squawk,notes=None):
    mstrRoute = separateRoute(FTFF)
    routeString = str(mstrRoute)
    print(routeString)
    stdLogUpt(f'Route Fetch: {routeString})\n(Altitude Assg {alt})\n(Airspeed assg {aspd})\n(Squawk Assigned {squawk})')

def getWeight():
    global FTFF
    aircraftFull = FTFF['aircraft']
    print(f'Aircraft Type: {aircraftFull}')
    weightClass = aircraftFull[-2]
    print(f'Weight Class: {weightClass}')
    if weightClass == 'L':
        weightG.value = "Light"
    elif weightClass == 'M':
        weightG.value = 'Medium'
    elif weightClass == 'H':
        weightG.value = 'Heavy'
        callsign.value += 'Heavy'
    elif weightClass == 'S':
        weightG.value = 'Super'
        callsign.value += 'Super'

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
            getWeight()
            logMasterUpdate(altitudeG.value, cruisespdG, squawkG, notes="Assigned")
            refreshRoute()
    updateData()
    app.currentRefreshTick += 1


cmu_graphics.run()
