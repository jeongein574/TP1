from cmu_graphics import *
import random
import datetime
 
# using now() to get current time
currentTime = datetime.datetime.now()

class MainPage:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.tomato = r"C:\Users\jeong\Documents\CMU\year 1\Fundamentals of Computer Science 15112\TP1\Images\tomato1.png"
        self.timer = True
        self.planner = False
        self.calendar = False
        self.focus = False
        self.studyLabelNum = '00:25:00'
        self.studyLabel = 'Focus Time'

    def timerLabel(self, app):
        studyLabel = app.FocusTimePage.studyLabel
        hour, minute, second = app.FocusTimePage.labels[studyLabel*3 : studyLabel*3 + 3]
        self.studyLabelNum = f'{hour}:{minute}:{second}'
        studyLabels = ['Focus Time', 'Short Break', 'Long Break']
        self.studyLabel = studyLabels[studyLabel]
    
    def draw(self, app):
        drawRect(app.width/2, 0, app.width, app.height//3, align = 'top', fill = rgb(246, 246, 246) )
        drawLine(0, 330, app.width, 320, fill = rgb(246, 246, 246))
        drawLabel(f'{currentTime.month}/{currentTime.day}/{currentTime.year}', app.width//2, 50, size = 22, font ='monospace')
        drawLabel(self.studyLabel, app.width*2/3, 100, size = 18, bold = True, font = 'monospace')
        drawLabel(self.studyLabelNum, app.width*2/3, 140, size = 40, bold = True, font = 'monospace')
        drawLabel(f'Now   {currentTime.hour}:{currentTime.minute}', app.width*2/3, 180, size = 14, font = 'monospace')
        drawLabel('⇦', app.width*2/3-5, 180, size=14, font='symbols')
        
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
        self.labels = [
            '00', '25', '00',  # study
            '00', '05', '00',  # short
            '00', '10', '00'   # long
        ]
        
        self.studyLabel = 0
        self.buttonPositions = []

        for y in range(-140, 141, 140):
            for x in range(-140, 141, 140):
                self.buttonPositions.append((self.width/2 + x, self.height/2 + y))

    def draw(self, app):
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
        drawRect(app.width/2, app.height/2, 450, 450, fill = 'white', align = 'center')
        drawLabel('Focus Time', app.width/2-150, app.height/2-200, size = 16, font ='monospace')
        drawLabel('Short Break', app.width/2-150, app.height/2-60, size = 16, font ='monospace')
        drawLabel('Long Break', app.width/2-150, app.height/2+80, size = 16, font ='monospace')
        drawLabel(':   :', app.width/2, app.height/2-140, size = 60, font ='monospace')
        drawLabel(':   :', app.width/2, app.height/2, size = 60, font ='monospace')
        drawLabel(':   :', app.width/2, app.height/2+140, size = 60, font ='monospace')
        # drawLabel('cancel     save', app.width/2+140, app.height/2+200, size = 14, font ='monospace')

        for x, y in self.buttonPositions:
            drawRect(x, y, 70, 70, fill=rgb(246, 246, 246), align='center')

        for i in range(len(self.labels)):
            drawLabel(self.labels[i], app.width/2+(i % 3-1)*140, app.height/2+(i // 3)*140-140, size=50, bold=True, font='monospace')

    def press(self, app, mouseX, mouseY):
        for i in range(len(self.buttonPositions)):
            buttonX, buttonY = self.buttonPositions[i]
            if buttonX - 35 <= mouseX <= buttonX + 35 and buttonY - 35 <= mouseY <= buttonY + 35:
                while True:
                    userinput = app.getTextInput('Enter a number between 0 and 60:')
                    if userinput.isdigit() and 0 <= int(userinput) <= 60:
                        if int(userinput) < 10 and userinput[0] != '0':
                            self.labels[i] = f'0{userinput}'
                        else:
                            self.labels[i] = f'{userinput}'
                        self.studyLabel = i // 3
                        break
                    else:
                        userinput = app.getTextInput('Invalid input. Enter a number between 0 and 60:')


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
    if app.MainPage.focus:
        app.FocusTimePage.press(app, mouseX, mouseY)
        

def onStep(app):
    if app.MainPage.focus:
        app.MainPage.timerLabel(app)

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