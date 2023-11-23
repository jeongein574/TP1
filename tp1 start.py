from cmu_graphics import *
import random

class MainPage:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.tomato = r"C:\Users\jeong\Documents\CMU\year 1\Fundamentals of Computer Science 15112\TP1\Images\tomato1.png"
        self.timer = True
        self.planner = False
        self.calendar = False
        self.focus = False
    
    def draw(self, app):
        drawRect(app.width/2, 0, app.width, app.height//3, align = 'top', fill = rgb(246, 246, 246) )
        drawLine(0, 330, app.width, 320, fill = rgb(246, 246, 246))
        drawLabel('Date', app.width//2, 50, size = 22, font ='monospace')
        drawLabel('Focus Time', app.width*2/3, 100, size = 18, bold = True, font = 'monospace')
        drawLabel('00:25:00', app.width*2/3, 140, size = 40, bold = True, font = 'monospace')
        drawLabel('Now   5:45 PM', app.width*2/3, 180, size = 14, font = 'monospace')
        drawLabel('⇦', app.width*2/3-20, 180, size=14, font='symbols')
        
        drawLabel('Timer', app.width/4, 300, size = 20, bold = self.timer, font = 'monospace')
        drawLabel('Planner', app.width/2, 300, size = 20, bold = self.planner, font = 'monospace')
        drawLabel('Calendar', app.width*3/4, 300, size = 20, bold = self.calendar, font = 'monospace')

        tomatoWidth, tomatoHeight = getImageSize(self.tomato)
        drawImage(self.tomato, app.width/3, 130, align = 'center', width = tomatoWidth//5, height = tomatoHeight//5)

    def press(self, app, mouseX, mouseY):
        if 335 <= mouseX <= 435 and 270 <= mouseY <= 330:
            self.timer = True
            self.planner = False
            self.calendar = False
        if 720 <= mouseX <= 820 and 270 <= mouseY <= 330:
            self.timer = False
            self.planner = True
            self.calendar = False
        if 1105 <= mouseX <= 1205 and 270 <= mouseY <= 330:
            self.timer = False
            self.planner = False
            self.calendar = True
        if self.focus == True:
            if not (app.width/2-225 <= mouseX <= app.width/2+225
                    and app.height/2-225 <= mouseY <= app.height/2+225):
                self.focus = False
        if self.focus == False and (930 < mouseX < 1140 and 100 < mouseY < 180):
            self.focus = True

class FocusTimePage:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.studyHour, self.studyMinute, self.studySecond = 0, 25, 0
        self.shortHour, self.shortMinute, self.shortSecond = 0, 5, 0
        self.longHour, self.longMinute, self.longSecond = 0, 10, 0

    def draw(self, app):
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
        drawRect(app.width/2, app.height/2, 450, 450, fill = 'white', align = 'center')
        drawLabel('Focus Time', app.width/2-150, app.height/2-200, size = 16, font ='monospace', fill = 'black')
        drawLabel('Short Break', app.width/2-150, app.height/2-60, size = 16, font ='monospace', fill = 'black')
        drawLabel('Long Break', app.width/2-150, app.height/2+80, size = 16, font ='monospace', fill = 'black')
        drawLabel(':   :', app.width/2, app.height/2-140, size = 60, font ='monospace', fill = 'black')
        drawLabel(':   :', app.width/2, app.height/2, size = 60, font ='monospace', fill = 'black')
        drawLabel(':   :', app.width/2, app.height/2+140, size = 60, font ='monospace', fill = 'black')
        drawLabel('cancel     save', app.width/2+140, app.height/2+200, size = 14, font ='monospace', fill = 'black')

class CalendarPage:
    def __init__(self, width, height):
        self.width, self.height = width, height

    def draw(self, app):
        drawRect(0, 330, app.width, app.height-330, fill='white')
        drawLabel('calendar page', app.width/2, app.height/2) 

class PlannerPage:
    def __init__(self, width, height):
        self.width, self.height = width, height

    def draw(self, app):
        drawRect(0, 330, app.width, app.height-330, fill='white')
        drawLabel('planner page', app.width/2, app.height/2)   

class TimerPage:
    def __init__(self, width, height):
        self.width, self.height = width, height

    def draw(self, app):
        drawRect(0, 330, app.width, app.height-330, fill='white')
        drawLabel('timer page', app.width/2, app.height/2)

#---Animation functions---------------------------------
def onAppStart(app):
    app.mainDisplay = True
    app.MainPage = MainPage(app.width, app.height)
    app.FocusTimePage = FocusTimePage(app.width, app.height)
    app.TimerPage = TimerPage(app.width, app.height)
    app.PlannerPage = PlannerPage(app.width, app.height)
    app.CalendarPage = CalendarPage(app.width, app.height)

def onMousePress(app, mouseX, mouseY):
    app.MainPage.press(app, mouseX, mouseY)

        

def onStep(app):
    pass

def redrawAll(app):
    app.MainPage.draw(app)
    if app.MainPage.timer:
        app.TimerPage.draw(app)
    if app.MainPage.planner:
        app.PlannerPage.draw(app)
    if app.MainPage.calendar:
        app.CalendarPage.draw(app)
    if app.MainPage.focus:
        app.FocusTimePage.draw(app)
    

runApp(width = 1540, height = 800)