# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import sys
sys.path.append('/home/pi/Desktop/Projet-Tresseuse/YoctoLib.python.29837/Sources')
from PyQt4 import QtGui, QtCore, Qt
from yocto_api import *
from yocto_relay import *
from yocto_pwmoutput import *
from yocto_pwminput import *
import subprocess
import time
player = None
winder1Relay = None
winder1PwmOut = None
winder1PwmIn = None
winder2Relay = None
winder2PwmOut = None
winder2PwmIn = None

#Connection to Yocto modules

errmsg1 = YRefParam()
if YAPI.RegisterHub("172.24.1.2", errmsg1) != YAPI.SUCCESS:
    print("No Yocto-Wifi (172.24.1.2) detected")
else:
    winder1Relay = YRelay.FindRelay("Yocto-Relay1.relay1")
    if winder1Relay is None:
        print("No Yocto-relay1 detected")
    else:
        winder1Relay.set_state(True)
    winder1PwmOut = YPwmOutput.FindPwmOutput("Yocto-PWM-Tx1.pwmOutput1")
    if winder1PwmOut is None:
        print("No Yocto-pwm-output1 detected")
    else:
        winder1PwmOut.set_frequency(5000)
        winder1PwmOut.set_enabled(YPwmOutput.ENABLED_TRUE)
        winder1PwmOut.set_dutyCycle(0)
    winder1PwmIn = YPwmInput.FindPwmInput("Yocto-PWM-Rx1.pwmInput1")
    if winder1PwmIn is None:
        print("No Yocto-pwm-input1 detected")
    else:
        winder1PwmIn.resetCounter()

errmsg2 = YRefParam()
if YAPI.RegisterHub("172.24.1.3", errmsg2) != YAPI.SUCCESS:
   print("No Yocto-Wifi (172.24.1.3) detected")
else:
    winder2Relay = YRelay.FindRelay("Yocto-Relay2.relay1")
    if winder2Relay is None:
        print("No Yocto-relay2 detected")
    else:
        winder2Relay.set_state(True)
    winder2PwmOut = YPwmOutput.FindPwmOutput("Yocto-PWM-Tx2.pwmOutput1")
    if winder2PwmOut is None:
        print("No Yocto-pwm-output2 detected")
    else:
        winder2PwmOut.set_frequency(5000)
        winder2PwmOut.set_enabled(YPwmOutput.ENABLED_TRUE)
        winder2PwmOut.set_dutyCycle(0)
    winder2PwmIn = YPwmInput.FindPwmInput("Yocto-PWM-Rx2.pwmInput1")
    if winder2PwmIn is None:
        print("No Yocto-pwm-input2 detected")
    else:
        winder2PwmIn.resetCounter()
 
#Get saved parameters
parameterFile = open("/home/pi/Desktop/Projet-Tresseuse/braiderParameters", "r")
speed = int(parameterFile.readline())
speedPump1 = int(parameterFile.readline())
speedPump2 = int(parameterFile.readline())
speedWinder1 = int(parameterFile.readline())
speedWinder2 = int(parameterFile.readline())
parameterFile.close()

totalPulse1=0
previousTotal1=0
previousPulse1=0
pulse1Ok = False
index1 = False
speed1 = 0
totalPulse2=0
previousTotal2=0
previousPulse2=0
pulse2Ok = False
index2 = False
speed2 = 0
speed1Computed = False
speed2Computed = False
counterReset=0
mousePressed = False


class verticalLabel1(QtGui.QWidget):
    def __init__(self, parent, text):
        QtGui.QWidget.__init__(self, parent)
        #self.setFixedHeight(400)
        #self.setFixedWidth(30)
        self.text = text

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        #painter.fillRect(event.rect(), QtCore.Qt.red)
        painter.setPen(QtCore.Qt.white)
        painter.setFont(QtGui.QFont('Arial', 20))
        painter.translate(5,76)
        painter.rotate(90)
        painter.drawText(0, 0, self.text)
        
class verticalLabel2(QtGui.QWidget):
    def __init__(self, parent, text):
        QtGui.QWidget.__init__(self, parent)
        #self.setFixedHeight(150)
        self.setFixedWidth(30)
        self.text = text

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.white)
        painter.setFont(QtGui.QFont('Arial', 16))
        painter.translate(5,25)
        painter.rotate(90)
        painter.drawText(0, 0, self.text)

class verticalLabel3(QtGui.QWidget):
    def __init__(self, parent, text):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedWidth(60)
        self.setFixedHeight(78)
        self.text = text

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.white)
        painter.setFont(QtGui.QFont('Arial', 16))
        painter.translate(20,0)
        painter.rotate(90)
        painter.drawText(0, 0, self.text)
        
class verticalLabel4(QtGui.QWidget):
    def __init__(self, parent, text):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedWidth(60)
        self.setFixedHeight(40)
        self.text = text

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.white)
        painter.setFont(QtGui.QFont('Arial', 16))
        painter.translate(20,0)
        painter.rotate(90)
        painter.drawText(0, 0, self.text)

class verticalLabel5(QtGui.QWidget):
    def __init__(self, parent, text):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedWidth(60)
        self.setFixedHeight(62)
        self.text = text

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.white)
        painter.setFont(QtGui.QFont('Arial', 16))
        painter.translate(20,0)
        painter.rotate(90)
        painter.drawText(0, 0, self.text)

class verticalLabel6(QtGui.QWidget):
    def __init__(self, parent, text):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedWidth(60)
        self.setFixedHeight(23)
        self.text = text

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.white)
        painter.setFont(QtGui.QFont('Arial', 16))
        painter.translate(20,0)
        painter.rotate(90)
        painter.drawText(0, 0, self.text)

class verticalLabel7(QtGui.QWidget):
    def __init__(self, parent, text):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedWidth(60)
        self.setFixedHeight(45)
        self.text = text

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.white)
        painter.setFont(QtGui.QFont('Arial', 16))
        painter.translate(20,0)
        painter.rotate(90)
        painter.drawText(0, 0, self.text)

class customButtonStart(QtGui.QPushButton):
    def __init__(self, parent):
        QtGui.QPushButton.__init__(self, parent)
        self.setFixedHeight(60)
        self.setFixedWidth(60)
        self.state = False
        self.warning = False
        self.error = False

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if self.error:
            painter.fillRect(event.rect(), QtCore.Qt.red)
        elif self.warning:
            painter.fillRect(event.rect(), QtCore.Qt.yellow)
        elif self.state:
            painter.fillRect(event.rect(), QtCore.Qt.green)
        else:
            painter.fillRect(event.rect(), QtCore.Qt.gray)
        painter.setPen(QtGui.QPen(QtCore.Qt.white, 4))
        painter.drawRect(event.rect())
        painter.setPen(QtCore.Qt.black)
        painter.setFont(QtGui.QFont('Arial', 11, weight=QtGui.QFont.Bold))
        painter.translate(25,4)
        painter.rotate(90)
        painter.drawText(0,0,"START")

            
class customButtonControl(QtGui.QPushButton):
    def __init__(self, parent, text):
        QtGui.QPushButton.__init__(self, parent)
        self.setFixedHeight(60)
        self.setFixedWidth(60)
        self.text = text

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(event.rect(), QtCore.Qt.gray)
        painter.setPen(QtGui.QPen(QtCore.Qt.white, 4))
        painter.drawRect(event.rect())
        painter.setPen(QtCore.Qt.black)
        painter.setFont(QtGui.QFont('Arial', 22, weight=QtGui.QFont.Bold))
        if self.text == "+":
            painter.translate(21,18)
        else:
            painter.translate(21,25)
        painter.rotate(90)
        painter.drawText(0,0,self.text) 

class customButtonReset(QtGui.QPushButton):
    def __init__(self, parent, text):
        QtGui.QPushButton.__init__(self, parent)
        self.setFixedHeight(60)
        self.setFixedWidth(60)
        self.text = text
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(15,0, 30, 60, QtCore.Qt.gray)
        painter.setPen(QtGui.QPen(QtCore.Qt.white, 2))
        painter.drawRect(15,0, 30, 60)
        painter.setPen(QtCore.Qt.black)
        painter.setFont(QtGui.QFont('Arial', 11, weight=QtGui.QFont.Bold))
        painter.translate(24,4)
        painter.rotate(90)
        painter.drawText(0,0,self.text)

class customButtonLed(QtGui.QPushButton):
    def __init__(self, parent):
        QtGui.QPushButton.__init__(self, parent)
        self.setFixedHeight(60)
        self.setFixedWidth(60)
        self.state = False
        self.blink = False
        self.index = False
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if self.state:
            painter.setBrush(QtGui.QBrush(QtCore.Qt.green))
        elif self.blink:
            self.index = not self.index
            if self.index:
                painter.setBrush(QtGui.QBrush(QtCore.Qt.red))
        painter.setPen(QtGui.QPen(QtCore.Qt.white, 4))
        painter.drawEllipse(5,5,50,50)
    

class circle(QtGui.QPushButton):
    def __init__(self, parent, x, y):
        QtGui.QPushButton.__init__(self, parent)
        self.setGeometry(x,y,50,50)
        self.x = x
        self.y = y
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.white, 3))
        painter.drawEllipse(6, 6, 38, 38)
        painter.setPen(QtCore.Qt.white)
        painter.setFont(QtGui.QFont('Arial', 19, weight=QtGui.QFont.Bold))
        painter.translate(16,15)
        painter.rotate(90)
        painter.drawText(0,0,"H")
        
class customExitButton(QtGui.QPushButton):
    def __init__(self, parent):
        QtGui.QPushButton.__init__(self, parent)
        self.setGeometry(740,365,50,50)
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.white, 3))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.red)) 
        painter.drawEllipse(6, 6, 38, 38)
        painter.setPen(QtCore.Qt.white)
        painter.setFont(QtGui.QFont('Arial', 19, weight=QtGui.QFont.Bold))
        painter.translate(16,16)
        painter.rotate(90)
        painter.drawText(0,0,"X")

class customLockButton(QtGui.QPushButton):
    def __init__(self, parent):
        QtGui.QPushButton.__init__(self, parent)
        self.setGeometry(740,61,50,50)
        self.state = False
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.white, 3))
        if self.state:
            painter.setBrush(QtGui.QBrush(QtCore.Qt.gray)) 
        painter.drawEllipse(6, 6, 38, 38)
        painter.setPen(QtGui.QPen(QtCore.Qt.white, 2))
        painter.drawEllipse(18, 16, 18, 18)
        painter.setPen(QtGui.QPen(QtCore.Qt.white, 1))
        painter.fillRect(16, 14, 12, 23, QtCore.Qt.white)

class mouseWheelDisplay(QtGui.QPushButton):
    def __init__(self, parent):
        QtGui.QPushButton.__init__(self, parent)
        self.setGeometry(276,210,60,60)
        self.angle = 0
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.white, 3))
        painter.drawEllipse(6, 6, 48, 48)
        painter.setPen(QtGui.QPen(QtCore.Qt.white, 1))
        painter.translate(30,30)
        painter.rotate(self.angle)
        painter.translate(-30,-30)
        painter.fillRect(28, 30, 4, 20, QtCore.Qt.white)

class generalSliderVertical(QtGui.QSlider):
    def __init__(self, parent):
        QtGui.QSlider.__init__(self,QtCore.Qt.Vertical, parent)
    def wheelEvent(self,event):
        if event.delta() > 0:
            self.parent().wheelDisplay.angle=self.parent().wheelDisplay.angle+10
        else:
            self.parent().wheelDisplay.angle=self.parent().wheelDisplay.angle-10
        self.parent().wheelDisplay.update()

class generalSliderHorizontal(QtGui.QSlider):
    def __init__(self, parent):
        QtGui.QSlider.__init__(self,QtCore.Qt.Horizontal, parent)
    def wheelEvent(self,event):
        if event.delta() > 0:
            self.parent().wheelDisplay.angle=self.parent().wheelDisplay.angle+10
        else:
            self.parent().wheelDisplay.angle=self.parent().wheelDisplay.angle-10
        self.parent().wheelDisplay.update()
    
class panel(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(-5,0,805,480)
        self.setWindowTitle("Braider")
        self.setStyleSheet("background-color:black;")
        self.setCursor(QtCore.Qt.BlankCursor)

        #Init timer to compute length and speed
        self.timerComputeLength1 = QtCore.QTimer(self)
        self.timerComputeLength1.timeout.connect(self.computeLength1)
        self.timerComputeLength1.setInterval(1200)
        self.timerComputeLength1.start()
        
        #self.timerComputeLength2 = QtCore.QTimer(self)
        #self.timerComputeLength2.timeout.connect(self.computeLength2)
        #self.timerComputeLength2.setInterval(1500)

        self.timerReset = QtCore.QTimer(self)
        self.timerReset.timeout.connect(self.resetReset)
        self.timerReset.setInterval(5000)
        
        #Draw Hublot screws
        circle1 = circle(self,0,0)
        circle2 = circle(self,0,430)
        circle3 = circle(self,750,0)
        circle4 = circle(self,750,430)

        #Draw mouse wheel display
        self.wheelDisplay=mouseWheelDisplay(self)
        
        #Button for general control
        label = verticalLabel1(self, "General control")
        self.btnInc = customButtonControl(self, "+")
        self.btnDec = customButtonControl(self, "-")
        self.btnStart = customButtonStart(self)
        self.btnLed1 = customButtonLed(self)
        self.btnLed2 = customButtonLed(self)

        self.btnStart.clicked.connect(self.startPressed)
        self.btnInc.clicked.connect(self.incPressed)
        self.btnDec.clicked.connect(self.decPressed)
        self.btnLed1.clicked.connect(self.startLed1Pressed)
        self.btnLed2.clicked.connect(self.startLed2Pressed)
        
        #Slider for general control
        self.slider = generalSliderVertical(self)
        self.slider.setStyleSheet(self.stylesheet1())
        self.slider.setMinimumSize(50,50)
        self.slider.setMinimum(0)
        self.slider.setMaximum(95)
        self.slider.setValue(100-speed)
        self.slider.sliderMoved.connect(self.sliderMoved)
        
        #Layout of general control
        gridGeneral = QtGui.QGridLayout()
        #gridGeneral.setVerticalSpacing(40)
        gridGeneral.setHorizontalSpacing(20)
        gridGeneral.addWidget(label, 1, 3, 5, 1)
        gridGeneral.addWidget(self.btnLed1, 1, 2)
        gridGeneral.addWidget(self.btnLed2, 5, 2)
        gridGeneral.addWidget(self.btnInc, 4, 2)
        gridGeneral.addWidget(self.btnDec, 2, 2)
        gridGeneral.addWidget(self.btnStart, 3, 2)
        gridGeneral.addWidget(self.slider, 1, 1, 5, 1)
    
        #Buttons for controlling speed of pump 1
        labelPump1 = verticalLabel2(self, "Pump L")
        self.btnIncPump1 = customButtonControl(self, "+")
        self.btnDecPump1 = customButtonControl(self, "-")
        self.btnStartPump1 = customButtonStart(self)

        self.btnStartPump1.clicked.connect(self.startPump1Pressed)
        self.btnIncPump1.clicked.connect(self.incPump1Pressed)
        self.btnDecPump1.clicked.connect(self.decPump1Pressed)
        
        #Slider for controlling speed of pump 1
        self.sliderPump1 = generalSliderHorizontal(self)
        self.sliderPump1.setStyleSheet(self.stylesheet2())
        self.sliderPump1.setMinimum(5)
        self.sliderPump1.setMaximum(100)
        self.sliderPump1.setValue(speedPump1)
        self.sliderPump1.sliderMoved.connect(self.sliderPump1Moved)
        
        #Layout of pump 1
        gridPump1 = QtGui.QGridLayout()
        gridPump1.setHorizontalSpacing(10)
        gridPump1.setVerticalSpacing(20)
        gridPump1.addWidget(self.btnIncPump1, 1, 3)
        gridPump1.addWidget(self.btnDecPump1, 1, 1)
        gridPump1.addWidget(self.btnStartPump1, 1, 2)
        gridPump1.addWidget(self.sliderPump1, 2, 1, 1, 3)
        gridPump1.addWidget(labelPump1, 1, 4, 2, 1)

        #Buttons for controlling speed of pump 2
        labelPump2 = verticalLabel2(self, "Pump R")
        self.btnIncPump2 = customButtonControl(self, "+")
        self.btnDecPump2 = customButtonControl(self, "-")
        self.btnStartPump2 = customButtonStart(self)
        
        self.btnStartPump2.clicked.connect(self.startPump2Pressed)
        self.btnIncPump2.clicked.connect(self.incPump2Pressed)
        self.btnDecPump2.clicked.connect(self.decPump2Pressed)
        
        #Slider for controlling speed of pump 2
        self.sliderPump2 = generalSliderHorizontal(self)
        self.sliderPump2.setStyleSheet(self.stylesheet2())
        self.sliderPump2.setMinimum(5)
        self.sliderPump2.setMaximum(100)
        self.sliderPump2.setValue(speedPump2)
        self.sliderPump2.sliderMoved.connect(self.sliderPump2Moved)
        
        #Layout of pump 2
        gridPump2 = QtGui.QGridLayout()
        gridPump2.setHorizontalSpacing(10)
        gridPump2.setVerticalSpacing(20)
        gridPump2.addWidget(self.btnIncPump2, 1, 3)
        gridPump2.addWidget(self.btnDecPump2, 1, 1)
        gridPump2.addWidget(self.btnStartPump2, 1, 2)
        gridPump2.addWidget(self.sliderPump2, 2, 1, 1, 3)
        gridPump2.addWidget(labelPump2, 1, 4, 2, 1)

        #Buttons for controlling speed of winder 1
        labelWinder1 = verticalLabel2(self, "Winder")
        self.btnStartWinder1 = customButtonStart(self)
        self.btnIncWinder1 = customButtonControl(self, "+")
        self.btnDecWinder1 = customButtonControl(self, "-")

        self.btnStartWinder1.clicked.connect(self.startWinder1Pressed)
        self.btnIncWinder1.clicked.connect(self.incWinder1Pressed)
        self.btnDecWinder1.clicked.connect(self.decWinder1Pressed)
        
        #Slider for controlling speed of winder 1
        self.sliderWinder1 = generalSliderHorizontal(self)
        self.sliderWinder1.setStyleSheet(self.stylesheet2())
        self.sliderWinder1.setMinimum(5)
        self.sliderWinder1.setMaximum(100)
        self.sliderWinder1.setValue(speedWinder1)
        self.sliderWinder1.sliderMoved.connect(self.sliderWinder1Moved)
        
        #Layout of winder 1
        gridWinder1 = QtGui.QGridLayout()
        gridWinder1.setHorizontalSpacing(10)
        gridWinder1.setVerticalSpacing(20)
        gridWinder1.addWidget(self.btnIncWinder1, 1, 3)
        gridWinder1.addWidget(self.btnDecWinder1, 1, 1)
        gridWinder1.addWidget(self.btnStartWinder1, 1, 2)
        gridWinder1.addWidget(self.sliderWinder1, 2, 1, 1, 3)
        gridWinder1.addWidget(labelWinder1, 1, 4, 2, 1)

        #Buttons for controlling speed of winder 2
        labelWinder2 = verticalLabel2(self, "Braider")
        self.btnStartWinder2 = customButtonStart(self)
        self.btnIncWinder2 = customButtonControl(self, "+")
        self.btnDecWinder2 = customButtonControl(self, "-")

        self.btnStartWinder2.clicked.connect(self.startWinder2Pressed)
        self.btnIncWinder2.clicked.connect(self.incWinder2Pressed)
        self.btnDecWinder2.clicked.connect(self.decWinder2Pressed)
        
        #Slider for controlling speed of winder 2
        self.sliderWinder2 = generalSliderHorizontal(self)
        self.sliderWinder2.setStyleSheet(self.stylesheet2())
        self.sliderWinder2.setMinimum(5)
        self.sliderWinder2.setMaximum(100)
        self.sliderWinder2.setValue(speedWinder2)
        self.sliderWinder2.sliderMoved.connect(self.sliderWinder2Moved)
        
        #Layout of winder 2
        gridWinder2 = QtGui.QGridLayout()
        gridWinder2.setHorizontalSpacing(10)
        gridWinder2.setVerticalSpacing(20)
        gridWinder2.addWidget(self.btnIncWinder2, 1, 3)
        gridWinder2.addWidget(self.btnDecWinder2, 1, 1)
        gridWinder2.addWidget(self.btnStartWinder2, 1, 2)
        gridWinder2.addWidget(self.sliderWinder2, 2, 1, 1, 3)
        gridWinder2.addWidget(labelWinder2, 1, 4, 2, 1)

        #Informations length 
        lengthLabel = verticalLabel3(self, "Length:")
        self.lengthValue = verticalLabel4(self, "0")
        meterLabel = verticalLabel6(self, "m")
        btnResetLength = customButtonReset(self, "RESET")
        btnResetLength.clicked.connect(self.resetPressed)
        gridLength = QtGui.QVBoxLayout()
        gridLength.addWidget(lengthLabel)
        gridLength.addWidget(self.lengthValue)
        gridLength.addWidget(meterLabel)
        gridLength.addWidget(btnResetLength)

        #Informations ratio 
        ratioLabel = verticalLabel5(self, "Ratio:")
        self.ratioValue = verticalLabel7(self, "0.00")
        gridLength.addWidget(ratioLabel)
        gridLength.addWidget(self.ratioValue)
        gridLength.setSpacing(2)
        
        #Main layout
        grid = QtGui.QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)
        grid.addLayout(gridLength, 1, 0, 2, 1)
        grid.addLayout(gridGeneral, 1, 3, 2, 1)
        grid.addLayout(gridPump1, 1, 2)
        grid.addLayout(gridPump2, 2, 2)
        grid.addLayout(gridWinder1, 1, 1)
        grid.addLayout(gridWinder2, 2, 1)
        self.setLayout(grid)

        #Draw exit cross
        btnExit = customExitButton(self)
        btnExit.clicked.connect(self.exitPressed)

        #Draw lock button
        self.btnLock = customLockButton(self)
        self.btnLock.clicked.connect(self.lockPressed)

        self.show()
        
    def mousePressEvent(self,QMouseEvent):
        if QMouseEvent.button()==2:
            global mousePressed
            mousePressed = True
            self.btnStart.state = False
            self.btnStart.error = True
            self.btnStart.update()
            self.btnStartWinder1.state = False
            self.btnStartWinder2.state = False
            self.btnStartWinder1.update()
            self.btnStartWinder2.update()
            if winder1PwmOut:
                winder1PwmOut.set_dutyCycle(0)
            if winder2PwmOut:
                winder2PwmOut.set_dutyCycle(0)
            pwm1.ChangeDutyCycle(0)
            GPIO.output(19, 0)
            self.btnStartPump1.state = False
            self.btnStartPump1.update()
            pwm2.ChangeDutyCycle(0)
            GPIO.output(20, 0)
            self.btnStartPump2.state = False
            self.btnStartPump2.update()
            GPIO.output(12, 0)
            self.btnLed1.state  = False
            self.btnLed1.blink = False
            self.btnLed1.update()
            GPIO.output(16, 0)
            self.btnLed2.state  = False
            self.btnLed2.blink = False
            self.btnLed2.update()
            global player
            player = subprocess.Popen(["aplay", "/home/pi/Desktop/Projet-Tresseuse/audioAlert.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
    def mouseReleaseEvent(self,QMouseEvent):
        if QMouseEvent.button()==2:
            global mousePressed
            mousePressed = False
            self.btnStart.error = False
            self.btnStart.update()
            global player
            player.kill()

            
    def wheelEvent(self, event):
        if event.delta() > 0:
            self.wheelDisplay.angle=self.wheelDisplay.angle+10
        else:
            self.wheelDisplay.angle=self.wheelDisplay.angle-10
        self.wheelDisplay.update()
        
    def stylesheet1(self):
        return """
            QSlider{
                min-height: 100px;
                min-width: 70px;
                }
            QSlider::groove:vertical {
                border: 2px solid white;
                background: black;
                width: 5px;
                }
            QSlider::handle:vertical{
                border: 2px solid white;
                background: black;
                height: 40px;
                margin: 0 -30px;
                }
        """
    def stylesheet2(self):
        return """
            QSlider{
                min-height: 70px;
                min-width: 70px;
                }
            QSlider::groove:horizontal {
                border: 2px solid white;
                background: black;
                height: 5px;
                }
            QSlider::handle:horizontal{
                border: 2px solid white;
                background: black;
                height: 60px;
                width: 40px;
                margin: -30px 0;
                }
        """

        
    def startPressed(self):
        if self.btnStartWinder1.error | self.btnStartWinder2.error | mousePressed:
            pass
        else:
            self.btnStart.state =  not self.btnStart.state
            if self.btnStart.state:
                #Start pump 1
                self.btnStartPump1.state = True
                pwm1.ChangeDutyCycle(50)
                GPIO.output(19, 1)
                #Start pump 2
                self.btnStartPump2.state = True
                pwm2.ChangeDutyCycle(50)
                GPIO.output(20, 1)
                #Start winder 1
                if not self.btnStartWinder1.state:
                    #self.timerComputeLength1.start()
                    self.btnStartWinder1.state = True
                if winder1PwmOut:
                    winder1PwmOut.set_dutyCycle(speedWinder1*speed/100)
                #Start winder 2
                if not self.btnStartWinder2.state:    
                    #self.timerComputeLength2.start()
                    self.btnStartWinder2.state = True
                if winder2PwmOut:
                    winder2PwmOut.set_dutyCycle(speedWinder2*speed/100)
                if not self.btnLed1.state:
                    self.btnLed1.blink = True
                if not self.btnLed2.state:
                    self.btnLed2.blink = True
                    
            else:
                self.btnStart.start = False
                #Stop pump 1
                self.btnStartPump1.state = False
                pwm1.ChangeDutyCycle(0)
                GPIO.output(19, 0)
                #Stop pump 2
                self.btnStartPump2.state = False
                pwm2.ChangeDutyCycle(0)
                GPIO.output(20, 0)
                #Stop winder 1
                #self.timerComputeLength1.stop
                self.btnStartWinder1.state = False
                self.btnStartWinder1.warning = False
                if winder1PwmOut:
                    winder1PwmOut.set_dutyCycle(0)
                #Stop winder 2
                #self.timerComputeLength2.stop()
                self.btnStartWinder2.state = False
                self.btnStartWinder2.warning = False
                if winder2PwmOut:
                    winder2PwmOut.set_dutyCycle(0)
                #Turn off the leds
                GPIO.output(12, 0)
                self.btnLed1.state  = False
                self.btnLed1.blink = False
                self.btnLed1.index = False
                self.btnLed1.update()
                GPIO.output(16, 0)
                self.btnLed2.state  = False
                self.btnLed2.blink = False
                self.btnLed2.state  = False
                self.btnLed2.index = False
                self.btnLed2.update()
            self.btnStart.update()
            self.btnStartPump1.update()
            self.btnStartPump2.update()
            self.btnStartWinder1.update()
            self.btnStartWinder2.update()
        
    def startPump1Pressed(self):
        self.btnStartPump1.state = not self.btnStartPump1.state
        if self.btnStartPump1.state:
            pwm1.ChangeDutyCycle(50)
            GPIO.output(19, 1)
        else:
            pwm1.ChangeDutyCycle(0)
            GPIO.output(19, 0)
        self.btnStartPump1.update()

    def startPump2Pressed(self):
        self.btnStartPump2.state = not self.btnStartPump2.state
        if self.btnStartPump2.state:
            pwm2.ChangeDutyCycle(50)
            GPIO.output(20, 1)
        else:
            pwm2.ChangeDutyCycle(0)
            GPIO.output(20, 0)
        self.btnStartPump2.update()

    def startWinder1Pressed(self):
        if self.btnStartWinder1.error:
            self.btnStartWinder1.error = False
            self.btnStartWinder1.warning = False
        else:
            self.btnStartWinder1.state = not self.btnStartWinder1.state
            self.btnStartWinder1.warning = False
            if self.btnStartWinder1.state:
                if winder1PwmOut:
                    winder1PwmOut.set_dutyCycle(speedWinder1*speed/100)
                #self.timerComputeLength1.start()
            else:
                if winder1PwmOut:
                    winder1PwmOut.set_dutyCycle(0)
                #self.timerComputeLength1.stop()
        self.btnStartWinder1.update()
        
    def startWinder2Pressed(self):
        if self.btnStartWinder2.error:
            self.btnStartWinder2.error = False
            self.btnStartWinder2.warning = False
        else:
            self.btnStartWinder2.state = not self.btnStartWinder2.state
            self.btnStartWinder2.warning = False
            if self.btnStartWinder2.state:
                if winder2PwmOut:
                    winder2PwmOut.set_dutyCycle(speedWinder2*speed/100)
                #self.timerComputeLength2.start()
            else:
                if winder2PwmOut:
                    winder2PwmOut.set_dutyCycle(0)
                #self.timerComputeLength2.stop()
        self.btnStartWinder2.update()

    def startLed1Pressed(self):
        self.btnLed1.state = not self.btnLed1.state
        if self.btnLed1.state:
            GPIO.output(12, 1)
            self.btnLed1.blink = False
            self.btnLed1.index = False
        else:
            GPIO.output(12, 0)
            if self.btnStart.state:
                self.btnLed1.blink = True
        self.btnLed1.update()

    def startLed2Pressed(self):
        self.btnLed2.state = not self.btnLed2.state
        if self.btnLed2.state:
            GPIO.output(16, 1)
            self.btnLed2.blink = False
            self.btnLed2.index = False
        else:
            GPIO.output(16, 0)
            if self.btnStart.state:
                self.btnLed2.blink = True
        self.btnLed2.update()

    def incPressed(self):
        global speed
        speed = speed + 5
        if speed > 95:
            speed = 95
        self.slider.setValue(100-speed)
        pwm1.ChangeFrequency(8*speedPump1*speed/100)
        pwm2.ChangeFrequency(8*speedPump2*speed/100)
        if self.btnStartWinder1.state:
            if winder1PwmOut:
                winder1PwmOut.set_dutyCycle(speedWinder1*speed/100)
        if self.btnStartWinder2.state:
            if winder2PwmOut:
                winder2PwmOut.set_dutyCycle(speedWinder2*speed/100)
        
    def decPressed(self):
        global speed
        speed = speed - 5
        if speed < 5:
            speed = 5
        self.slider.setValue(100-speed)
        pwm1.ChangeFrequency(8*speedPump1*speed/100)
        pwm2.ChangeFrequency(8*speedPump2*speed/100)
        if self.btnStartWinder1.state:
            if winder1PwmOut:
                winder1PwmOut.set_dutyCycle(speedWinder1*speed/100)
        if self.btnStartWinder2.state:
            if winder2PwmOut:
                winder2PwmOut.set_dutyCycle(speedWinder2*speed/100)
        
    def incPump1Pressed(self):
        global speedPump1
        speedPump1 = speedPump1 + 5
        if speedPump1 > 100:
            speedPump1 = 100
        self.sliderPump1.setValue(speedPump1)
        pwm1.ChangeFrequency(8*speedPump1*speed/100)
        
    def decPump1Pressed(self):
        global speedPump1
        speedPump1 = speedPump1 - 5
        if speedPump1 < 5:
            speedPump1 = 5
        self.sliderPump1.setValue(speedPump1)
        pwm1.ChangeFrequency(8*speedPump1*speed/100)
            
    def incPump2Pressed(self):
        global speedPump2
        speedPump2 = speedPump2 + 5
        if speedPump2 > 100:
            speedPump2 = 100
        self.sliderPump2.setValue(speedPump2)
        pwm2.ChangeFrequency(8*speedPump2*speed/100)
        
    def decPump2Pressed(self):
        global speedPump2
        speedPump2 = speedPump2 - 5
        if speedPump2 < 5:
            speedPump2 = 5
        self.sliderPump2.setValue(speedPump2)
        pwm2.ChangeFrequency(8*speedPump2*speed/100)

    def incWinder1Pressed(self):
        global speedWinder1
        speedWinder1 = speedWinder1 + 5
        if speedWinder1 > 100:
            speedWinder1 = 100
        self.sliderWinder1.setValue(speedWinder1)
        if self.btnStartWinder1.state:
            if winder1PwmOut:
                winder1PwmOut.set_dutyCycle(speedWinder1*speed/100)
            
    def decWinder1Pressed(self):
        global speedWinder1
        speedWinder1 = speedWinder1 - 5
        if speedWinder1 < 5:
            speedWinder1 = 5
        self.sliderWinder1.setValue(speedWinder1)
        if self.btnStartWinder1.state:
            if winder1PwmOut:
                winder1PwmOut.set_dutyCycle(speedWinder1*speed/100)

    def incWinder2Pressed(self):
        global speedWinder2
        speedWinder2 = speedWinder2 + 5
        if speedWinder2 > 100:
            speedWinder2 = 100
        self.sliderWinder2.setValue(speedWinder2)
        if self.btnStartWinder2.state:
            if winder2PwmOut:
                winder2PwmOut.set_dutyCycle(speedWinder2*speed/100)
        
    def decWinder2Pressed(self):
        global speedWinder2
        speedWinder2 = speedWinder2 - 5
        if speedWinder2 < 5:
            speedWinder2 = 5
        self.sliderWinder2.setValue(speedWinder2)
        if self.btnStartWinder2.state:
            if winder2PwmOut:
                winder2PwmOut.set_dutyCycle(speedWinder2*speed/100)

    def sliderMoved(self):
        global speed
        speed = 100 - self.slider.value()
        pwm1.ChangeFrequency(8*speedPump1*speed/100)
        pwm2.ChangeFrequency(8*speedPump2*speed/100)

    def sliderPump1Moved(self):
        global speedPump1
        speedPump1 = self.sliderPump1.value()
        pwm1.ChangeFrequency(8*speedPump1*speed/100)

    def sliderPump2Moved(self):
        global speedPump2
        speedPump2 = self.sliderPump2.value()
        pwm2.ChangeFrequency(8*speedPump2*speed/100)

    def sliderWinder1Moved(self):
        global speedWinder1
        speedWinder1 = self.sliderWinder1.value()

    def sliderWinder2Moved(self):
        global speedWinder2
        speedWinder2 = self.sliderWinder2.value()

    def resetPressed(self):
        global counterReset
        counterReset += 1
        if counterReset == 1:
            self.timerReset.start()
        if counterReset==3:
            global totalPulse1
            global previousTotal1
            global previousPulse1
            totalPulse1 = 0
            previousTotal1 = 0
            previousPulse1 = 0
            if winder1PwmIn:
                winder1PwmIn.resetCounter()
            self.lengthValue.text = "0"
            self.lengthValue.update()
            counterReset=0

    def resetReset(self):
        global counterReset
        counterReset = 0

    def lockPressed(self):
        self.btnLock.state = not self.btnLock.state
        self.btnLock.update()
        if self.btnLock.state:
            self.btnInc.setEnabled(False)
            self.btnDec.setEnabled(False)
            self.slider.setEnabled(False)
            self.btnStartPump1.setEnabled(False)
            self.btnIncPump1.setEnabled(False)
            self.btnDecPump1.setEnabled(False)
            self.sliderPump1.setEnabled(False)
            self.btnStartPump2.setEnabled(False)
            self.btnIncPump2.setEnabled(False)
            self.btnDecPump2.setEnabled(False)
            self.sliderPump2.setEnabled(False)
            self.btnStartWinder1.setEnabled(False)
            self.btnIncWinder1.setEnabled(False)
            self.btnDecWinder1.setEnabled(False)
            self.sliderWinder1.setEnabled(False)
            self.btnStartWinder2.setEnabled(False)
            self.btnIncWinder2.setEnabled(False)
            self.btnDecWinder2.setEnabled(False)
            self.sliderWinder2.setEnabled(False)
            self.btnLed1.setEnabled(False)
            self.btnLed2.setEnabled(False)
        else:
            self.btnInc.setEnabled(True)
            self.btnDec.setEnabled(True)
            self.slider.setEnabled(True)
            self.btnStartPump1.setEnabled(True)
            self.btnIncPump1.setEnabled(True)
            self.btnDecPump1.setEnabled(True)
            self.sliderPump1.setEnabled(True)
            self.btnStartPump2.setEnabled(True)
            self.btnIncPump2.setEnabled(True)
            self.btnDecPump2.setEnabled(True)
            self.sliderPump2.setEnabled(True)
            self.btnStartWinder1.setEnabled(True)
            self.btnIncWinder1.setEnabled(True)
            self.btnDecWinder1.setEnabled(True)
            self.sliderWinder1.setEnabled(True)
            self.btnStartWinder2.setEnabled(True)
            self.btnIncWinder2.setEnabled(True)
            self.btnDecWinder2.setEnabled(True)
            self.sliderWinder2.setEnabled(True)
            self.btnLed1.setEnabled(True)
            self.btnLed2.setEnabled(True)
            

    def computeLength1(self):
        global pulse1Ok
        global pulse2Ok
        global totalPulse1
        global previousTotal1
        global previousPulse1
        global speed1
        global index1
        global totalPulse2
        global previousTotal2
        global previousPulse2
        global speed2
        global index2
        if self.btnLed1.blink:
            self.btnLed1.update()
        if self.btnLed2.blink:
            self.btnLed2.update()    
        if self.btnStartWinder1.state:
            if winder1PwmIn:
                if index1:
                    winder1PwmOut.set_dutyCycle(speedWinder1*speed/100.0)
                    pulse1 = winder1PwmIn.get_pulseCounter()
                    pulse1Ok = True
                else:
                    index1 = True
        else:
            index1 = False
        if self.btnStartWinder2.state:
            if winder2PwmIn:
                if index2:
                    winder2PwmOut.set_dutyCycle(speedWinder2*speed/100.0)
                    pulse2 = winder2PwmIn.get_pulseCounter()
                    pulse2Ok = True
                else:
                    index2 = True
        else:
            index2 = False
        if pulse1Ok:
            totalPulse1 = previousTotal1 + pulse1
            speed1 = pulse1 - previousPulse1*1.0
            self.lengthValue.text = str(int(totalPulse1/100.0))
            self.lengthValue.update()
            previousPulse1 = pulse1
        if pulse2Ok:
            totalPulse2 = previousTotal2 + pulse2
            speed2 = pulse2 - previousPulse2*1.0
            previousPulse2 = pulse2
        if pulse1Ok & pulse2Ok:
            if speed2 != 0:
                self.ratioValue.text = str(round(speed1/speed2, 2))
            else:
                self.ratioValue.text = "inf."
        elif pulse1Ok:
            self.ratioValue.text = "inf."
        elif pulse2Ok:
            self.ratioValue.text = "0.00"
        self.ratioValue.update()
        if pulse1Ok:
            if speed1*23 < speedWinder1*speed:
                self.btnStartWinder1.warning = True
            else:
                self.btnStartWinder1.warning = False
            if speed1*80 < speedWinder1*speed & speedWinder1*speed > 400:
                self.btnStart.state = False
                self.btnStart.update()
                self.btnStartWinder1.error = True
                self.btnStartWinder1.state = False
                self.btnStartWinder2.state = False
                self.btnStartWinder2.warning = False
                self.btnStartWinder2.update()
                winder1PwmOut.set_dutyCycle(0)
                winder2PwmOut.set_dutyCycle(0)
                pwm1.ChangeDutyCycle(0)
                GPIO.output(19, 0)
                self.btnStartPump1.state = False
                self.btnStartPump1.update()
                pwm2.ChangeDutyCycle(0)
                GPIO.output(20, 0)
                self.btnStartPump2.state = False
                self.btnStartPump2.update()
                GPIO.output(12, 0)
                self.btnLed1.state  = False
                self.btnLed1.update()
                GPIO.output(16, 0)
                self.btnLed2.state  = False
                self.btnLed2.update()
            self.btnStartWinder1.update()    
            if pulse1 > 5000000:
                previousTotal1 = previousTotal1 + winder1PwmIn.get_pulseCounter()
                winder1PwmIn.resetCounter()
                previousPulse1=0
            pulse1Ok = False
        if pulse2Ok:
            if speed2*23 < speedWinder2*speed:
                self.btnStartWinder2.warning = True
            else:
                self.btnStartWinder2.warning = False
            if speed2*80 < speedWinder2*speed & speedWinder2*speed > 400:
                self.btnStart.state = False
                self.btnStart.update()
                self.btnStartWinder2.error = True
                self.btnStartWinder1.state = False
                self.btnStartWinder1.warning = False
                self.btnStartWinder2.state = False
                self.btnStartWinder1.update()
                winder1PwmOut.set_dutyCycle(0)
                winder2PwmOut.set_dutyCycle(0)
                pwm1.ChangeDutyCycle(0)
                GPIO.output(19, 0)
                self.btnStartPump1.state = False
                self.btnStartPump1.update()
                pwm2.ChangeDutyCycle(0)
                GPIO.output(20, 0)
                self.btnStartPump2.state = False
                self.btnStartPump2.update()
                GPIO.output(12, 0)
                self.btnLed1.state  = False
                self.btnLed1.update()
                GPIO.output(16, 0)
                self.btnLed2.state  = False
                self.btnLed2.update()
            self.btnStartWinder2.update()    
            if pulse2 > 5000000:
                previousTotal2 = previousTotal2 + winder2PwmIn.get_pulseCounter()
                winder2PwmIn.resetCounter()
                previousPulse2=0
            pulse2Ok = False

    def computeLength2(self):
        if self.btnStartWinder2.state:
            if winder2PwmIn:
                winder2PwmOut.set_dutyCycle(speedWinder2*speed/100.0)
                pulse2 = winder2PwmIn.get_pulseCounter()
                global totalPulse2
                global previousTotal2
                global previousPulse2
                global speed2
                global speed1Computed
                global speed2Computed
                totalPulse2 = previousTotal2 + pulse2
                speed2 = pulse2 - previousPulse2*1.0
                if speed2*23 < speedWinder2*speed:
                    self.btnStartWinder2.warning = True
                else:
                    self.btnStartWinder2.warning = False
                if speed2*60 < speedWinder2*speed:
                    self.btnStart.state = False
                    self.btnStart.update()
                    self.btnStartWinder2.error = True
                    self.btnStartWinder1.state = False
                    self.btnStartWinder2.state = False
                    self.btnStartWinder1.update()
                    winder1PwmOut.set_dutyCycle(0)
                    winder2PwmOut.set_dutyCycle(0)
                    pwm1.ChangeDutyCycle(0)
                    GPIO.output(19, 0)
                    self.btnStartPump1.state = False
                    self.btnStartPump1.update()
                    pwm2.ChangeDutyCycle(0)
                    GPIO.output(20, 0)
                    self.btnStartPump2.state = False
                    self.btnStartPump2.update()
                    GPIO.output(12, 0)
                    self.btnLed1.state  = False
                    self.btnLed1.update()
                    GPIO.output(16, 0)
                    self.btnLed2.state  = False
                    self.btnLed2.update()
                    self.timerComputeLength1.stop()
                    self.timerComputeLength2.stop()
                self.btnStartWinder2.update()  
                previousPulse2 = pulse2
                speed2Computed = True
                if pulse2 > 5000000:
                    previousTotal2 = previousTotal2 + winder2PwmIn.get_pulseCounter()
                    winder2PwmIn.resetCounter()
                    previousPulse2=0
                if speed1Computed & speed2Computed:
                    speed1Computed = False
                    speed2Computed = False
                    if speed2 != 0:
                        self.ratioValue.text = str(round(speed1/speed2, 2))
                    else:
                        self.ratioValue.text = "inf."
                    self.ratioValue.update()
        else:
            if winder2PwmIn:
                winder2PwmOut.set_dutyCycle(0)

    def exitPressed(self):
        pwm1.ChangeDutyCycle(0)
        GPIO.output(19, 0)
        pwm2.ChangeDutyCycle(0)
        GPIO.output(20, 0)
        self.timerComputeLength1.stop
        if winder1PwmOut:
            winder1PwmOut.set_dutyCycle(0)
        #self.timerComputeLength2.stop()
        if winder2PwmOut:
            winder2PwmOut.set_dutyCycle(0)
        parameterFile = open("/home/pi/Desktop/Projet-Tresseuse/braiderParameters", "w")
        parameterFile.write(str(speed))
        parameterFile.write("\n")
        parameterFile.write(str(speedPump1))
        parameterFile.write("\n")
        parameterFile.write(str(speedPump2))
        parameterFile.write("\n")
        parameterFile.write(str(speedWinder1))
        parameterFile.write("\n")
        parameterFile.write(str(speedWinder2))
        parameterFile.write("\n")
        parameterFile.close()
        GPIO.cleanup()
        sys.exit(0)
        
        
app = QtGui.QApplication(sys.argv)
tresseusePanel = panel(None)

#Setup output pins 
GPIO.setmode(GPIO.BCM)
#Step pump 1
GPIO.setup(26, GPIO.OUT)
pwm1 = GPIO.PWM(26,8*speedPump1)
pwm1.start(0)
#Sleep pump 1
GPIO.setup(19, GPIO.OUT)
GPIO.output(19, 0)
#S1 pump 1&2
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, 1)
#S2 pump 1&2
GPIO.setup(6, GPIO.OUT)
GPIO.output(6, 1)
#Step pump 2
GPIO.setup(21, GPIO.OUT)
pwm2 = GPIO.PWM(21,8*speedPump2)
pwm2.start(0)
#Sleep pump 2
GPIO.setup(20, GPIO.OUT)
GPIO.output(20, 0)
#Led 1
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, 0)
#Led 2
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, 0)

app.exec_()
GPIO.cleanup()

