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
        self.taskAdd = False
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
        if app.CalendarPage.longestConsecutiveTime == True:
            self.timer, self.planner, self.calendar = False, False, True

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
                    userinput = app.getTextInput('Enter a number between 0 and 59:')
                    if userinput.isdigit() and 0 <= int(userinput) <= 59:
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
        self.longestConsecutiveTime = False
        self.taskAdd = False
        #add a task list

    def draw(self, app):
        drawRect(0, 330, app.width, app.height-330, fill='white')
        drawLine(app.width/2, 340, app.width/2, app.height-30, fill = rgb(200, 200, 200))

        #calendar
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

        #longestConsecutiveTime
        for i in range(3):
            drawLine(app.width/2+50, 370 + 5*i, app.width/2+70, 370 + 5*i, fill = rgb(200, 200, 200))

        #taskAdd
        drawCircle(app.width-60, app.height-60, 20, fill = 'tomato')
        drawLabel('+', app.width-60, app.height-60, size = 60, fill = 'white', align = 'center')

        #task display
            #task title, allotted time
            #order of the tasks in the task list may switch according to optimization

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
        
        if self.longestConsecutiveTime == True:
            if not (app.width/2-225 <= mouseX <= app.width/2+225 and 
                    app.height/2-150 <= mouseY <= app.height+150):
                self.longestConsecutiveTime = False
        if self.longestConsecutiveTime == False and (app.width/2+50 <= mouseX <= app.width/2+70 
                                             and 370 <= mouseY <= 380):
            self.longestConsecutiveTime = True

        if self.taskAdd == True:
            if not (app.width/2-225 <= mouseX <= app.width/2+225
                    and app.height/2-225 <= mouseY <= app.height/2+225):
                self.taskAdd = False
                # if TaskAddPage.optimize == True and optimizeTime != '00:00':
                    # append the task to the task list as a tuple of (title, True, estimated time to finish, importance)
                # elif TaskAddPage.optimize == False and startTime != '00:00' and endTime != '00:00'
                    # append the task to the task list as a tuple of (title, False, start time, end time)
        if self.taskAdd == False and (app.width-80 < mouseX < app.width-40 and app.height-80 < mouseY < app.height-40):
            self.taskAdd = True

    # def optimization
        # create new lists: optimizeTaskList, noOptimizeTaskList
        # from task list, if the second elem == True: append the task tuple into optimizeTaskList, else noOptimizeTaskList
        # set the task list as empty
        # from the optimizeTaskList, rearrange the tuples according to the order of importance. if same importance, alphabetical order
        # from the noOptimizeTaskList, rearrange the tuples according to the order ot startTime

        #do backtracking
            # the tasks in optimizeTaskList cannot have a conflicting study period as other tasks in both optimizeTaskList noOptimizeTaskList
            # allot the tasks in optimizeTaskList into the available times in between the time now and 24:00, without conflicts with the fixed tasks
            # if the task hour exceeds the longest consecutive work time, split the task and add long break in between. or add a different task in the next order of importance in between the splited tasks
        # append each tuple from optimizeTaskList and noOptimizeTaskList into the task list, according to the start and end time

    def optimizeTask(self):
        optimizeTaskList = []
        noOptimizeTaskList = []

        for task in self.taskList:
            if task[1]: 
                optimizeTaskList.append(task)
            else:
                noOptimizeTaskList.append(task)

        self.taskList = []

        optimizeTaskList.sort(key=lambda x: (x[3], x[0]))
        noOptimizeTaskList.sort(key=lambda x: x[2])

        self.backtrack(self.taskList, optimizeTaskList, noOptimizeTaskList)

    def isLegal(self, schedule, task):
        # Implement your rules to check if a move is legal
        # For example, check if the task can be added to the schedule without conflicts
        # You can also consider the longest consecutive work time, etc.
        if not task['checked']:
            return False

        longestConsecutiveWorkTime = app.LongestConsecutiveTimePage.labels

        if task['duration'] > longestConsecutiveWorkTime:
            return False
        
        index = len(schedule)
        
        if index > 0 and (schedule[index - 1] == 'break' or schedule[index - 1]['duration'] > longestConsecutiveWorkTime):
            return False
        
        return True

    def backtrack(self, schedule, optimizeTasks, noOptimizeTasks):
        if not optimizeTasks and not noOptimizeTasks:
            self.taskList = schedule.copy()
            return

        else:
            for task in optimizeTasks:
                if self.isLegal(schedule, task):
                    schedule.append(task)
                    optimizeTasks.remove(task)
                    self.backtrack(schedule, optimizeTasks, noOptimizeTasks)
                    schedule.pop()
                    optimizeTasks.append(task)

            for task in noOptimizeTasks:
                if self.isLegalMove(schedule, task):
                    schedule.append(task)
                    noOptimizeTasks.remove(task)
                    self.backtrack(schedule, optimizeTasks, noOptimizeTasks)
                    schedule.pop()
                    noOptimizeTasks.append(task)

class LongestConsecutiveTimePage:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.labels = ['00', '25', '00']
        self.positions = []
        for x in range(-140, 141, 140):
            self.positions.append((self.width/2+x, self.height/2-50))

    def draw(self, app):
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
        drawRect(app.width/2, app.height/2, 450, 300, fill = 'white', align = 'center')
        drawLabel(':   :', app.width/2, app.height/2-50, size = 60, font ='monospace')
        drawLabel('Longest Consecutive Worktime:', app.width/2, app.height/2-120, size = 20, bold = True, font ='monospace')
        drawLabel('This function allows the app to',  app.width/2, app.height/2+30, size = 17, align = 'top', font ='monospace')
        drawLabel('make optimized study plan for you.',  app.width/2, app.height/2+55, size = 17, align = 'top', font ='monospace')
        drawLabel('A single task exceeding this time will',  app.width/2, app.height/2+80, size = 17, align = 'top', font ='monospace')
        drawLabel('be allotted at multiple time periods.', app.width/2, app.height/2+105, size = 17, align = 'top', font ='monospace')

        for i in range(3):
                x, y = self.positions[i]
                drawRect(x, y, 70, 70, fill=rgb(246, 246, 246), align = 'center')
                drawLabel(self.labels[i], x, y, size = 50, bold = True, font = 'monospace')
    
    def press(self, app, mouseX, mouseY):
        for i in range(3):
            buttonX, buttonY = self.positions[i]
            if buttonX - 35 <= mouseX <= buttonX + 35 and buttonY - 35 <= mouseY <= buttonY + 35:
                while True:
                    userinput = app.getTextInput('Enter a number between 0 and 60:')
                    if userinput.isdigit() and 0 <= int(userinput) <= 60:
                        if int(userinput) < 10 and userinput[0] != '0':
                            self.labels[i] = f'0{userinput}'
                        else:
                            self.labels[i] = f'{userinput}'
                        break
                    else:
                        userinput = app.getTextInput('Invalid input. Enter a number between 0 and 60:')

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
        self.currentSubject = None
        self.currentTime = datetime.datetime.now()
        self.timerRun = False
        self.startTime = 0
        self.subjectLocation = 470

    def draw(self, app):
        drawRect(0, 330, app.width, app.height-330, fill='white')
        self.subjectLocation = 470
        for subject in self.subjectDict:
            color, studyTime = self.subjectDict[subject]
            drawLabel(subject, app.width/4, self.subjectLocation, font = 'monospace', size = 18, align = 'left')
            drawLabel(studyTime, app.width*3/4, self.subjectLocation, font = 'monospace', size = 18, align = 'left')
            drawCircle(app.width/5, self.subjectLocation, 20, fill = color)
            drawRegularPolygon(app.width/5, self.subjectLocation, 10, 3, rotateAngle = 90, fill = 'white', align = 'center')
            self.subjectLocation += 50

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

        for subject in self.subjectDict:
            color, studyTime = self.subjectDict[subject]
            subjectX, subjectY = app.width/5, self.subjectLocation
            if (subjectX - 10 <= mouseX <= subjectX + 10 and
                    subjectY - 10 <= mouseY <= subjectY + 10):
                if self.currentSubject == subject and self.timerRun:
                    self.stopTimer()
                else:
                    self.startTimer(subject, studyTime)
                break

    def startTimer(self, subject, studyTime):
        self.currentSubject = subject
        self.timerRun = True
        if not self.startTime:
            self.startTime = datetime.datetime.now()
        elapsedTime = self.currentTime - self.startTime
        self.subjectDict[self.currentSubject][1] = elapsedTime

    def stopTimer(self):
        if self.timerRun:
            self.timerRun = False
            elapsedTime = datetime.datetime.now() - self.startTime
            passedSeconds = elapsedTime.total_seconds()

            studyTimeHalf = self.subjectDict[self.currentSubject][1].split(':')
            studyMinutes, studySeconds = int(studyTimeHalf[0]), int(studyTimeHalf[1])
            totalStudyTime = studyMinutes * 60 + studySeconds
            updatedTotalStudyTime = totalStudyTime + passedSeconds

            updatedMinutes = int(updatedTotalStudyTime // 60)
            updatedSeconds = int(updatedTotalStudyTime % 60)

            newTime = f'{updatedMinutes:02d}:{updatedSeconds:02d}'
            self.subjectDict[self.currentSubject][1] = newTime

            self.currentSubject = None
            self.startTime = 0

class SubjectAddPage:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.colorPalette = ['lightSalmon', 'powderBlue', 'thistle', 'moccasin', 'paleGreen', 'mediumAquamarine', 'rosyBrown', 'pink', 'lightSteelBlue', 'tan']
        self.subject = ''

    def draw(self, app):
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
        drawRect(app.width/2, app.height/2, 450, 300, fill = 'white', align = 'center')
        drawRect(app.width/2, app.height/2-100, 350, 50, fill = rgb(246, 246, 246), align = 'center')
        drawLabel('Subject Name:', app.width/2 - 100, app.height/2-100, font = 'monospace', size = 16)
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

class TaskAddPage:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.startTime = '00:00'
        self.endTime = '00:00'
        self.optimizeTime = '00:00'
        self.title = ''
        self.optimize = False
        self.importance = 5
        self.importanceBar = [0]*10

    def draw(self, app):
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
        drawRect(app.width/2, app.height/2, 450, 450, fill = 'white', align = 'center')
        drawRect(app.width/2, app.height/2-160, 400, 70, fill = rgb(246, 246, 246), border = rgb(200, 200, 200), align = 'center')
        drawLabel('Title:', app.width/2-160, app.height/2-160, size = 16, font ='monospace')
        drawLabel(self.title, app.width/2-100, app.height/2-160, font = 'monospace', align = 'left', size = 16)

        drawLabel('Let the app optimize the best Time?', app.width/2-200, app.height/2-80, size = 16, font ='monospace', bold = True, align = 'left')
        drawRect(app.width/2+160, app.height/2-80, 20, 20, fill = None, border = 'black', borderWidth = 0.5, align = 'center')
        if self.optimize == True:
            drawLabel('V', app.width/2+160, app.height/2-80, size = 16, fill = 'tomato')

        if self.optimize == False: color = 'black'  
        else: color = rgb(200, 200, 200)        
        drawLabel(f'Start Time:', app.width/2-200, app.height/2-30, size = 16, font ='monospace', align = 'left', fill = color)
        drawRect(app.width/2+160, app.height/2-30, 80, 30, align = 'center', fill = rgb(246, 246, 246), border = rgb(200, 200, 200))
        drawLabel(self.startTime, app.width/2+160, app.height/2-30, size = 16, font ='monospace', fill = color)
        drawLabel(f'End Time:', app.width/2-200, app.height/2+10, size = 16, font ='monospace', align = 'left', fill = color)
        drawRect(app.width/2+160, app.height/2+10, 80, 30, align = 'center', fill = rgb(246, 246, 246), border = rgb(200, 200, 200))
        drawLabel(self.endTime, app.width/2+160, app.height/2+10, size = 16, font ='monospace', fill = color)

        drawLabel(f'Estimated Time to Finish:', app.width/2-200, app.height/2+50, size = 16, font ='monospace', align = 'left')     
        drawRect(app.width/2+160, app.height/2+50, 80, 30, align = 'center', fill = rgb(246, 246, 246), border = rgb(200, 200, 200))
        drawLabel(self.optimizeTime, app.width/2+160, app.height/2+50, size = 16, font ='monospace')
        
        drawLabel('importance: ', app.width/2-200, app.height/2+90, size = 16, font ='monospace', align = 'left')
        drawLabel('1  2  3  4  5  6  7  8  9  10', app.width/2+208, app.height/2+110, size = 11, font = 'monospace', align = 'right')
        barSize = 20
        for i in range(10):
            x = app.width / 2 + 10 + i * barSize
            y = app.height / 2 + 90
            color = rgb(246, 246, 246)
            if self.importanceBar[i]:
                color = 'tomato'
            drawRect(x, y, barSize, 20, fill=color, border=rgb(200, 200, 200), align='center')
            
    def press(self, app, mouseX, mouseY):
        if app.width/2 - 200 <= mouseX <= app.width/2 + 200 and app.height/2 - 195 <= mouseY <= app.height/2 -125:
            self.title = app.getTextInput('Task Title: ')
        if app.width/2+150 <= mouseX <= app.width/2+170 and app.height/2-90 <= mouseY <= app.height/2-70:
            self.optimize = not self.optimize
        if app.width/2+120 <= mouseX <= app.width/2+200 and app.height/2-45 <= mouseY <= app.height/2-15:
            while True:
                userInput = app.getTextInput('Write in the format of "00:00"')
                if self.isValid(userInput):
                    self.startTime = userInput
                    break
        if app.width/2+120 <= mouseX <= app.width/2+200 and app.height/2-5 <= mouseY <= app.height/2+25:
            while True:
                userInput = app.getTextInput('Write in the format of "00:00"')
                if self.isValid(userInput):
                    self.endTime = userInput
                    break
        if app.width/2+120 <= mouseX <= app.width/2+200 and app.height/2+35 <= mouseY <= app.height/2+65:
            while True:
                userInput = app.getTextInput('Write in the format of "00:00"')
                if self.isValid(userInput):
                    self.optimizeTime = userInput
                    break
        if app.width/2+10 <= mouseX <= app.width/2+210 and app.height/2+90 <= mouseY <= app.height/2+110:
            barIndex = int((mouseX - (app.width/2+10)) / 20)
            self.importanceBar = [0]*10
            for i in range(barIndex + 1):
                self.importanceBar[i] = 1

    def isValid(self, userInput):
        if len(userInput) != 5:
            return False
        if not (userInput[0].isdigit() and userInput[1].isdigit() and userInput[3].isdigit() and userInput[4].isdigit()):
            return False
        if not (0 <= int(userInput[0:2]) <= 23 and 0 <= int(userInput[3:]) <= 59):
            return False
        if userInput[2] != ':':
            return False
        return True

#---Animation functions---------------------------------
def onAppStart(app):
    app.mainDisplay = True
    app.MainPage = MainPage(app.width, app.height)
    app.FocusTimePage = FocusTimePage(app.width, app.height)
    app.TimerPage = TimerPage(app.width, app.height)
    app.PlannerPage = PlannerPage(app.width, app.height)
    app.CalendarPage = CalendarPage(app.width, app.height)
    app.SubjectAddPage = SubjectAddPage(app.width, app.height)
    app.LongestConsecutiveTimePage = LongestConsecutiveTimePage(app.width, app.height)
    app.TaskAddPage = TaskAddPage(app.width, app.height)

def onMousePress(app, mouseX, mouseY):
    app.MainPage.press(app, mouseX, mouseY)
    if app.MainPage.focus:
        app.FocusTimePage.press(app, mouseX, mouseY)
    if app.MainPage.calendar:
        app.CalendarPage.press(app, mouseX, mouseY)
    if app.CalendarPage.longestConsecutiveTime:
        app.LongestConsecutiveTimePage.press(app, mouseX, mouseY)
    if app.MainPage.timer:
        app.TimerPage.press(app, mouseX, mouseY)
    if app.TimerPage.subjectAddPage:
        app.SubjectAddPage.press(app, mouseX, mouseY)
    if app.MainPage.taskAdd:
        app.TaskAddPage.press(app, mouseX, mouseY)

def onStep(app):
    if app.MainPage.focus:
        app.MainPage.timerLabel(app)
    global currentTime, currentTimehour, currentTimeminute
    currentTime = datetime.datetime.now()
    currentTimehour = f'0{currentTime.hour}' if currentTime.hour < 10 else currentTime.hour
    currentTimeminute = f'0{currentTime.minute}' if currentTime.minute < 10 else currentTime.minute
    app.MainPage.taskAdd = app.CalendarPage.taskAdd 

    if app.TimerPage.timerRun == True:
        app.TimerPage.currentTime = datetime.datetime.now()

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
    if app.CalendarPage.longestConsecutiveTime:
        app.LongestConsecutiveTimePage.draw(app)
    if app.MainPage.taskAdd:
        app.TaskAddPage.draw(app)

runApp(width = 1540, height = 800)