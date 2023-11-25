from cmu_graphics import *
import random
import datetime
import calendar
 
currentTime = datetime.datetime.now()
currentTimehour = f'0{currentTime.hour}' if currentTime.hour < 10 else currentTime.hour
currentTimeminute = f'0{currentTime.minute}' if currentTime.minute < 10 else currentTime.minute

year = 2023
month = 11


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
        drawRect(app.width/2, 0, app.width, app.height//3, align = 'top', fill = rgb(246, 246, 246))
        drawLine(0, 330, app.width, 330, fill = rgb(246, 246, 246))
        drawLabel(f'{currentTime.month}/{currentTime.day}/{currentTime.year}', app.width//2, 50, size = 22, font ='monospace')
        drawLabel(self.studyLabel, app.width*2/3, 100, size = 18, bold = True, font = 'monospace')
        drawLabel(self.studyLabelNum, app.width*2/3, 140, size = 40, bold = True, font = 'monospace')
        drawLabel(f'Now   {currentTimehour}:{currentTimeminute}', app.width*2/3, 180, size = 14, font = 'monospace')
        drawRegularPolygon(app.width*2/3-10, 180, 5, 3, rotateAngle = 90, align = 'center')


        drawLabel('Timer', app.width/4, 300, size = 20, bold = self.timer, font = 'monospace')
        drawLabel('Planner', app.width/2, 300, size = 20, bold = self.planner, font = 'monospace')
        drawLabel('Calendar', app.width*3/4, 300, size = 20, bold = self.calendar, font = 'monospace')

        tomatoWidth, tomatoHeight = getImageSize(self.tomato)
        drawImage(self.tomato, app.width/3, 130, align = 'center', width = tomatoWidth//5, height = tomatoHeight//5)

    def press(self, app, mouseX, mouseY):
        if 335 <= mouseX <= 435 and 270 <= mouseY <= 330:
            self.timer, self.planner, self.calendar = True, False, False
        if 720 <= mouseX <= 820 and 270 <= mouseY <= 330:
            self.timer, self.planner, self.calendar = False, True, False
        if 1105 <= mouseX <= 1205 and 270 <= mouseY <= 330:
            self.timer, self.planner, self.calendar = False, False, True
        if self.focus == True:
            if not (app.width/2-225 <= mouseX <= app.width/2+225
                    and app.height/2-225 <= mouseY <= app.height/2+225):
                self.focus = False
        if self.focus == False and (930 < mouseX < 1140 and 100 < mouseY < 180):
            self.focus = True
        if app.TimerPage.subjectAddPage == True:
            self.timer, self.planner, self.calendar = True, False, False

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
        drawLine(app.width/2, 340, app.width/2, app.height-30, fill = rgb(200, 200, 200))
        calendarView = calendar.month(year, month)
        lines = calendarView.split('\n')
        title = lines[0].strip()
        lineHeight = 40
        drawRect(428, 540, 310, 360, fill = None, border = rgb(200, 200, 200), align = 'center')  
        for i in range(1, len(lines)):
            drawLabel(lines[i], app.width/5, app.height/2 + i * lineHeight, align = 'left', font = 'monospace', size = 20)
        drawRect(428, app.height/2-10, 300, 50, fill = rgb(246, 246, 246), align = 'center')
        drawLabel(title, 428, app.height/2-10, font = 'monospace', size = 20, italic = True)
        drawRegularPolygon(328, app.height/2-10, 5, 3, rotateAngle = -90, align = 'center', fill = 'dimGray')
        drawRegularPolygon(528, app.height/2-10, 5, 3, rotateAngle = 90, align = 'center', fill = 'dimGray')

    def press(self, app, mouseX, mouseY):
        global month, year
        if 318 <= mouseX <= 338 and 380 <= mouseY <= 400:
            if month != 1:
                month -= 1
            else:
                month = 12
                year -= 1

        if 518 <= mouseX <= 538 and 380 <= mouseY <= 400:
            if month != 12:
                month += 1
            else:
                month = 1
                year += 1

class PlannerPage:
    def __init__(self, width, height):
        self.width, self.height = width, height

    def draw(self, app):
        drawRect(0, 330, app.width, app.height-330, fill='white')
        drawLabel('planner page', app.width/2, app.height/2)   

class TimerPage:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.subjectDict = dict()
        self.subjectAddPage = False


    def draw(self, app):
        drawRect(0, 330, app.width, app.height-330, fill='white')
        y = 470
        for subject in self.subjectDict:
                color, studyTime = self.subjectDict[subject]
                drawLabel(subject, app.width/4, y, font = 'monospace', size = 18, align = 'left')
                drawLabel(studyTime, app.width*3/4, y, font = 'monospace', size = 18, align = 'left')
                drawCircle(app.width/5, y, 20, fill = color)
                drawRegularPolygon(app.width/5, y, 10, 3, rotateAngle = 90, fill = 'white', align = 'center')
                y += 50

        drawRect(app.width/5, 400, 150, 40, fill=rgb(246, 246, 246), align='center')
        drawLabel('+ Subject', app.width/5, 400, font='monospace', size=18)

    def press(self, app, mouseX, mouseY):
        if self.subjectAddPage == True:
            if not (app.width/2 - 225 <= mouseX <= app.width/2 +225 and 
                    app.height/2 - 150 <= mouseY <= app.height/2 + 150):
                self.subjectAddPage = False
        if self.subjectAddPage == False and (app.width/5 - 75 <= mouseX <= app.width/5 + 75 
                                             and 380 <= mouseY <= 420):
            self.subjectAddPage = True

class SubjectAddPage:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.colorPalette = ['lightSalmon', 'powderBlue', 'thistle', 'moccasin', 'paleGreen', 'mediumAquamarine', 'rosyBrown', 'pink', 'lightSteelBlue', 'tan']
        self.subject = ''

    def draw(self, app):
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
        drawRect(app.width/2, app.height/2, 450, 300, fill = 'white', align = 'center')
        drawRect(app.width/2, app.height/2-100, 350, 50, fill = rgb(246, 246, 246), align = 'center')
        drawLabel('Subject Name:', app.width/2 - 100, app.height/2-100, font = 'monospace', bold = True, size = 16)
        drawLabel(self.subject, app.width/2, app.height/2-100, font = 'monospace', align = 'left', size = 16)

        paletteX, paletteY = app.width / 2 - 160, app.height / 2
        paletteSize = 30
        for color in self.colorPalette[:5]:
            drawCircle(paletteX, paletteY, paletteSize, fill=color)
            paletteX += 80

        paletteX, paletteY = app.width / 2 - 160, app.height / 2 + 80
        for color in self.colorPalette[5:]:
            drawCircle(paletteX, paletteY, paletteSize, fill=color)
            paletteX += 80

    def press(self,app,mouseX, mouseY):
        selectedColor = None
        if app.width/2 - 175 <= mouseX <= app.width/2 + 175 and app.height/2 - 125 <= mouseY <= app.height/2 -75:
            self.subject = app.getTextInput('e.g. CS, Math, History...')
 
        paletteX, paletteY = app.width/2 - 160, app.height/2
        paletteSize = 30
        for color in self.colorPalette:
            if (paletteX - paletteSize <= mouseX <= paletteX + paletteSize and
                    paletteY - paletteSize <= mouseY <= paletteY + paletteSize):
                selectedColor = color
                break
            paletteX += 80
            if paletteX > app.width/2 + 160:
                paletteX = app.width/2 - 160
                paletteY += 80
        if self.subject != '' and selectedColor != None and self.subject not in app.TimerPage.subjectDict:
            app.TimerPage.subjectDict[self.subject] = [selectedColor, '00:00:00']
            self.subject, color = '', None
            app.TimerPage.subjectAddPage = False

#---Animation functions---------------------------------
def onAppStart(app):
    app.mainDisplay = True
    app.MainPage = MainPage(app.width, app.height)
    app.FocusTimePage = FocusTimePage(app.width, app.height)
    app.TimerPage = TimerPage(app.width, app.height)
    app.PlannerPage = PlannerPage(app.width, app.height)
    app.CalendarPage = CalendarPage(app.width, app.height)
    app.SubjectAddPage = SubjectAddPage(app.width, app.height)

def onMousePress(app, mouseX, mouseY):
    app.MainPage.press(app, mouseX, mouseY)
    if app.MainPage.focus:
        app.FocusTimePage.press(app, mouseX, mouseY)
    if app.MainPage.calendar:
        app.CalendarPage.press(app, mouseX, mouseY)
    if app.MainPage.timer:
        app.TimerPage.press(app, mouseX, mouseY)
    if app.TimerPage.subjectAddPage:
        app.SubjectAddPage.press(app, mouseX, mouseY)
        

def onStep(app):
    if app.MainPage.focus:
        app.MainPage.timerLabel(app)
    global currentTime, currentTimehour, currentTimeminute
    currentTime = datetime.datetime.now()
    currentTimehour = f'0{currentTime.hour}' if currentTime.hour < 10 else currentTime.hour
    currentTimeminute = f'0{currentTime.minute}' if currentTime.minute < 10 else currentTime.minute


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
    if app.TimerPage.subjectAddPage:
        app.SubjectAddPage.draw(app)
    

runApp(width = 1540, height = 800)