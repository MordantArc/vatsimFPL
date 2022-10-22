from cmu_graphics import *

import math
app.stepsPerSecond = 60 # 60hz std rfrsh rate


#Every step, rotate the line counter clockwise
#have two dots in an "end" group, line needs to be by itself
#have a current xy of the arc point(Arc [T]ravel Point) and one for the home point(rotation axis point, RAPT)

app.coordStepper = 0
app.multStepper = 0
app.multSeverity = 10
app.multSpeed = 2.5
app.decay = 0.05

app.rotPSec = 0

app.logRate = 8 #sps/current number is logs per sec(and relative trail)

app.multTF = 0

ttRTF = False

app.rotationMultiplier = 5
app.curRotation = 90

app.angVelocity = 0

app.trails = True
trail = Group()

app.rFF = True

app.xATP = 200
app.yATP = 200
xATPList = []
yATPList = []

app.xRAPT = 250
app.yRAPT = 200
xRAPTList = []
yRAPTList = []

curAng = 90

app.lineCenterX = pythonRound(((app.xATP + app.xRAPT)/2),2)
app.lineCenterY = pythonRound(((app.yATP + app.yRAPT)/2),2)
app.spinVelocity = ((2*math.pi)*25)/app.stepsPerSecond

app.opRot = (((app.curRotation/360)-1)*180)

Rect(0,0,50,50)
xLabel = Label(0,12.5,15,bold=True,fill="white")
yLabel = Label(0,37.5,15,bold=True,fill="white")
dirLine = Line(10,40,30,40,arrowEnd=True,fill="white",lineWidth = 1)
disLabel = Label(0,35,40,bold=True,fill="white",font="grenze")

Rect(350,0,50,30)
fknLabel = Label(0,365,7.5,bold=True,fill="white",font="grenze")
Label("RPS",365,20,bold=True,fill="white",size=10)
Label("Rev.",389,7.5,bold=True,size=10,fill="white")
Label("Sec.",389,22.5,bold=True,size=10,fill="white")

backLine = Line(app.xATP,app.yATP,app.xRAPT,app.yRAPT,lineWidth=10,fill="darkRed")
backLine.visible = False
mainLine = Line(app.xATP,app.yATP,app.xRAPT,app.yRAPT,lineWidth=2,fill="darkSlateBlue")
ATPDot = Circle(app.xATP,app.yATP,5,fill="darkSlateGray",border="aqua",borderWidth=2)
RAPTDot = Circle(app.xRAPT, app.yRAPT,5,fill="darkSlateGray",border="fuchsia",borderWidth=2)

def retCircle(val):
    if val <= 0:
        app.curRotation += 360

def updLine():
    if app.rFF == True:
        calcRot = (app.curRotation - app.rotationMultiplier)
        x, y = getPointInDir(app.xATP,app.yATP,calcRot,50)
        RAPTDot.radius = 5
        ATPDot.radius = 7.5
        app.xRAPT = x
        app.yRAPT = y
        app.curRotation = calcRot
        retCircle(calcRot) 
        mainLine.x2 = app.xRAPT
        mainLine.y2 = app.yRAPT
        backLine.x2 = app.xRAPT
        backLine.y2 = app.yRAPT
        RAPTDot.centerX = app.xRAPT
        RAPTDot.centerY = app.yRAPT

    elif app.rFF == False:
        calcRot = (app.curRotation - app.rotationMultiplier)
        x, y = getPointInDir(app.xRAPT,app.yRAPT,calcRot,50)
        RAPTDot.radius = 7.5
        ATPDot.radius = 5
        app.xATP = x
        app.yATP = y
        app.curRotation = calcRot
        retCircle(calcRot)
        mainLine.x1 = app.xATP
        mainLine.y1 = app.yATP
        backLine.x1 = app.xATP
        backLine.y1 = app.yATP
        ATPDot.centerX = app.xATP
        ATPDot.centerY = app.yATP

def drawTrail():
    circOne = Circle(app.xATP,app.yATP,1,fill="steelBlue")
    trail.add(circOne)
    circTwo = Circle(app.xRAPT,app.yRAPT,1,fill="maroon")
    trail.add(circTwo)

def writeCoords():
    drawTrail()
    xATPList.append(pythonRound(app.xATP,1))
    yATPList.append(pythonRound(app.yATP,1))
    xRAPTList.append(pythonRound(app.xRAPT,1))
    yRAPTList.append(pythonRound(app.yRAPT,1))

def onKeyPress(key):
    if key == ("n") or (key == "a") or (key == "left"):
        if app.rFF == False:
            app.curRotation -= 180
            retCircle(app.curRotation)
            app.rFF = True
            app.multTF += 1
            app.rotationMultiplier += app.multSpeed
            app.spinVelocity = (((2*math.pi)*25)/app.stepsPerSecond)
    if key == ("m") or (key == "d") or (key == "right"):
        if app.rFF == True: 
            app.curRotation -= 180
            retCircle(app.curRotation)
            app.rFF = False
            app.multTF += 1
            app.rotationMultiplier += app.multSpeed
            app.spinVelocity = (((2*math.pi)*25)/app.stepsPerSecond)

def controlMult():
    app.multStepper += 1
    if app.rotationMultiplier > 5:
        app.rotationMultiplier -= app.decay
        app.multTF -= 1

def timeToRotate():
    app.rotPSec = pythonRound(
        (app.rotationMultiplier*app.stepsPerSecond)/360
        ,1
        )
    RPM = app.rotPSec*60
    angVel = RPM*6
    app.angVelocity = rounded(angVel)

def guiUpt():
    if app.rFF == False:
        app.lineCenterX = pythonRound(app.xRAPT,2)
        app.lineCenterY = pythonRound(app.yRAPT,2)
    elif app.rFF == True:
        app.lineCenterX = pythonRound(app.xATP,2)
        app.lineCenterY = pythonRound(app.yATP,2)
    xLabel.value = rounded(app.lineCenterX)
    yLabel.value = rounded(app.lineCenterY)
    z = angleTo(200,200,app.lineCenterX,app.lineCenterY)
    x, y = getPointInDir(10,40,z,5)
    dirLine.x2 = x
    dirLine.y2 = y
    v = pythonRound(distance(200,200,app.lineCenterX,app.lineCenterY),1)
    disLabel.value = v
    timeToRotate()
    fknLabel.value = app.rotPSec#app.angVelocity
    
    
def onStep():
    updLine()
    guiUpt()
    app.coordStepper += 1
    if app.coordStepper == app.logRate:
        app.coordStepper = 0
        #writeCoords()
    controlMult()
    if app.rotPSec >= 2:
        backLine.visible = True
    elif app.rotPSec < 2:
        backLine.visible = False



def printCoords():
    print("xATP:\n",xATPList)
    print("yATP:\n",yATPList,"\n")
    print("xRAPT:\n",xRAPTList)
    print("yRAPT:\n",yRAPTList)

cmu_graphics.run()