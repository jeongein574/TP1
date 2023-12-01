from cmu_graphics import *
import datetime
import calendar
import copy
 
currentTime = datetime.datetime.now()
currentTimehour = f'0{currentTime.hour}' if currentTime.hour < 10 else currentTime.hour
currentTimeminute = f'0{currentTime.minute}' if currentTime.minute < 10 else currentTime.minute

year = 2023
month = 11
class FocusTimePage:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.labels = [
            '00', '25', '00',  # study
            '00', '05', '00',  # short
            '00', '10', '00'   # long
        ]
        
        self.studyIndex = 0
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
                        if int(userinput) < 10:
                            self.labels[i] = f'0{userinput}'
                        else:
                            self.labels[i] = f'{userinput}'
                        break
                    else:
                        userinput = app.getTextInput('Invalid input. Enter a number between 0 and 60:')

class MainPage:
    def __init__(self, width, height, FocusTimePage):
        self.width, self.height = width, height
        self.tomato = r"C:\Users\jeong\Documents\CMU\year 1\Fundamentals of Computer Science 15112\TP1\Images\tomato1.png"
        self.timer = True
        self.planner = False
        self.calendar = False
        self.focus = False
        self.taskAdd = False
        self.studyLabelNum = '00:25:00'
        self.studyLabel = 'Focus Time'
        self.mainColor = rgb(246, 246, 246)
        self.pomodoroList = []
        self.Labels = [
            '00', '25', '00',  # study
            '00', '05', '00',  # short
            '00', '10', '00'   # long
        ]

    def timerLabel(self, app):
        studyLabelIndex = app.FocusTimePage.studyIndex
        hour, minute, second = self.Labels[int(studyLabelIndex)*3 : int(studyLabelIndex)*3 + 3]
        studyLabels = ['Focus Time', 'Short Break', 'Long Break']

        if app.TimerPage.focusTimerRun or app.TimerPage.shortTimerRun or app.TimerPage.longTimerRun:
            hour, minute, second = int(hour), int(minute), int(second)
            second -= 1
            if second <= 0 and minute <= 0 and hour <= 0:
                second, minute, hour = 0, 0, 0
            if second < 0:
                second = 59
                minute -= 1
            if minute < 0:
                minute = 59
                hour -= 1
            if hour < 0:
                hour = 0
            
            if hour < 10: timerH = f'0{str(hour)}'
            else: timerH = str(hour)
            if minute < 10: timerM = f'0{str(minute)}'
            else: timerM = str(minute)
            if second < 10: timerS = f'0{str(second)}'
            else: timerS = str(second)

            self.Labels[int(studyLabelIndex)*3] = timerH
            self.Labels[int(studyLabelIndex)*3+1] = timerM
            self.Labels[int(studyLabelIndex)*3+2] = timerS
            self.studyLabelNum = f'{timerH}:{timerM}:{timerS}'
            self.studyLabel = studyLabels[studyLabelIndex]

        if self.studyLabel == 'Focus Time' and self.studyLabelNum == '00:00:00':
            if not self.pomodoroList:
                self.pomodoroList.append('Focus Time')
                if len(self.pomodoroList) == 4: 
                    app.TimerPage.focusTimerRun, app.TimerPage.shortTimerRun, app.TimerPage.longTimerRun = False, False, True
                    self.pomodoroList = []   
                    app.FocusTimePage.studyIndex = 2
                    self.Labels = copy.deepcopy(app.FocusTimePage.labels)
                else:
                    app.TimerPage.focusTimerRun, app.TimerPage.shortTimerRun, app.TimerPage.longTimerRun = False, True, False
                    app.FocusTimePage.studyIndex = 1
                    self.Labels = copy.deepcopy(app.FocusTimePage.labels)
        elif (self.studyLabel == 'Short Break' or self.studyLabel == 'Long Break') and self.studyLabelNum == '00:00:00':
            app.TimerPage.focusTimerRun, app.TimerPage.shortTimerRun, app.TimerPage.longTimerRun = False, False, False 
            self.Labels = copy.deepcopy(app.FocusTimePage.labels)
            self.studyLabel = studyLabels[0] 
            self.studyLabelNum = f'{self.Labels[0]}:{self.Labels[1]}:{self.Labels[2]}'
            
        if app.TimerPage.focusTimerRun: self.mainColor = rgb(252, 242, 239)
        elif app.TimerPage.shortTimerRun: self.mainColor = rgb(248, 247, 221)
        elif app.TimerPage.longTimerRun: self.mainColor = rgb(231, 243, 232)
        else: self.mainColor = rgb(246, 246, 246)

    def draw(self, app):
        drawRect(app.width/2, 0, app.width, app.height//3, align = 'top', fill = self.mainColor)
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
            self.timer, self.planner, self.calendar = True, False, False
            if not (app.width/2-225 <= mouseX <= app.width/2+225
                    and app.height/2-225 <= mouseY <= app.height/2+225):
                self.Labels = copy.deepcopy(app.FocusTimePage.labels)
                self.focus = False
        if self.focus == False and (930 < mouseX < 1140 and 100 < mouseY < 180):
            self.focus = True
        if app.TimerPage.subjectAddPage == True:
            self.timer, self.planner, self.calendar = True, False, False
        if app.CalendarPage.longestConsecutiveTime == True:
            self.timer, self.planner, self.calendar = False, False, True      

class CalendarPage:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.longestConsecutiveTime = False
        self.taskAdd = False
        self.schedule = []
        self.todayList = []
        self.taskAddTime = 0

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
        location = 470
        for task in self.schedule:
            taskTitle, startTime, endTime = task[0], task[2], task[3]
            index = self.schedule.index(task)
            location += 50*index

            drawLabel(taskTitle, app.width/2+100, location, font = 'monospace', size = 18, align = 'left')
            drawLabel(f'{startTime} - {endTime}', app.width-100, location, font = 'monospace', size = 18, align = 'right')
    
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
                
                self.taskAddTime = int(currentTimehour)*60 + currentTimeminute
                for i in range(1440-self.taskAddTime): # 1440 = minute of 24:00 (= 24*60)
                    self.todayList.append(0)
                    i += 1

                if app.TaskAddPage.optimize == True and app.TaskAddPage.optimizeTime != '00:00':
                    self.schedule.append((app.TaskAddPage.title, True, app.TaskAddPage.optimizeTime, app.TaskAddPage.importance))
                elif app.TaskAddPage.optimize == False and app.TaskAddPage.startTime != '00:00' and app.TaskAddPage.endTime != '00:00':
                    self.schedule.append((app.TaskAddPage.title, False, app.TaskAddPage.startTime, app.TaskAddPage.endTime))
        if self.taskAdd == False and (app.width-80 < mouseX < app.width-40 and app.height-80 < mouseY < app.height-40):
            self.taskAdd = True
            self.optimizeTask(app)

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

    def optimizeTask(self, app):
        optimizeTaskList = []
        noOptimizeTaskList = []

        for task in self.schedule:
            if task[1] == True: 
                optimizeTaskList.append(task)
            elif task[1] == False:
                noOptimizeTaskList.append(task)

        self.schedule = []

        optimizeTaskList.sort(key=lambda x: (x[3], x[0])) # importance, or alphabetical
        noOptimizeTaskList.sort(key=lambda x: x[2]) # startTime

        for task in optimizeTaskList:
            taskTitle, optimizeTime, importance = task[0], task[2], task[3]
            workSecond = int(task[2][:2])*3600 + int(task[2][3:])*60
            longestWorkTime = app.LongestConsecutiveTimePage.labels
            longestSecond = (int(longestWorkTime[0]))*3600 + (int(longestWorkTime[1]))*60 + (int(longestWorkTime[2]))
            
            if workSecond > longestSecond:
                while workSecond > longestSecond:
                    newWorkSecond = longestSecond
                    leftWorkSecond = workSecond - newWorkSecond
                    workSecond = leftWorkSecond

                    workHour = newWorkSecond // 3600
                    workMinute = newWorkSecond // 60 - 60*workHour
                    if workHour < 10: workHour = f'0{workHour}'
                    else: workHour = str(workHour)
                    if workMinute < 10: workMinute = f'0{workMinute}'
                    else: workMinute = str(workMinute)

                    optimizeTime = f'{workHour}:{workMinute}'
                    newTask = (taskTitle, True, optimizeTime, importance)
                    self.schedule.append(newTask)
            else:
                self.schedule.append(task)

        for task in noOptimizeTaskList:
            taskTitle, startTime, endTime = task[0], task[2], task[3]
            startMinute = int(startTime[:2])*60 + int(startTime[3:])
            endMinute = int(endTime[:2])*60 + int(endTime[3:])
            startIndex = startMinute - self.taskAddTime
            endIndex = endMinute - self.taskAddTime

            for i in range(startIndex, endIndex+1):
                self.todayList[i] = 1

        self.backtrack(self.schedule, optimizeTaskList)

    def isLegal(self, schedule, task):
        taskTitle, timeTaken, importance = task[0], task[2], task[3]
        timeTakenMinute = int(timeTaken[:2])*60 + int(timeTaken[3:])
        breakMinute = int(app.MainPage.labels[3])*60 + int(app.MainPage.labels[4])

        # if timeTakenMinute <= (length of 0's in between 1's) + breakMinute:
            # add the task next to 1, with a gap of 0's (gap is the length of breakMinute)
                # this means to change 0 to 1 for the added task, 
                # and to append the task into the schedule, as a tuple of: (taskTitle, False, startTime, endTime)
                    # startTime and endTime need to be made up...

    def backtrack(self, schedule, optimizeTasks):
        if not optimizeTasks:
            return schedule

        else:
            for task in optimizeTasks:
                if self.isLegal(schedule, task, self.todayList):
                    schedule.append(task)
                    optimizeTasks.remove(task)
                    schedule = self.backtrack(schedule, optimizeTasks)
                    if schedule != None:
                        return schedule
                    else:
                        schedule.remove(task)
                        optimizeTasks.append(task)

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
        self.subjectList = []
        self.subjectAddPage = False
        self.focusTimerRun = False
        self.shortTimerRun = False
        self.longTimerRun = False
        self.startTime = 0
        self.activeSubjectIndex = None

    def draw(self, app):
        drawRect(0, 330, app.width, app.height-330, fill='white')
        for subjectSubList in self.subjectList:
            subject, color, studyTime, location = subjectSubList[0], subjectSubList[1], subjectSubList[2], subjectSubList[3]
            index = self.subjectList.index(subjectSubList)
            location += 50*index

            drawLabel(subject, app.width/4, location, font = 'monospace', size = 18, align = 'left')
            drawLabel(studyTime, app.width*3/4, location, font = 'monospace', size = 18, align = 'left')
            drawCircle(app.width/5, location, 20, fill = color)
            if self.focusTimerRun and self.subjectList.index(subjectSubList) == self.activeSubjectIndex:
                drawRect(app.width/5, location, 12, 12, fill = 'white', align = 'center')
                drawRect(app.width/5, location, 3, 12, fill = color, align = 'center')
            elif self.focusTimerRun == False or self.subjectList.index(subjectSubList) != self.activeSubjectIndex:
                drawRegularPolygon(app.width/5, location, 10, 3, rotateAngle = 90, fill = 'white', align = 'center')
                

        drawRect(app.width/5, 400, 150, 40, fill=rgb(246, 246, 246), align='center')
        drawLabel('+ Subject', app.width/5, 400, font='monospace', size=18)

    def press(self, app, mouseX, mouseY):
        if self.subjectAddPage == True:
            if not (app.width/2-225 <= mouseX <= app.width/2+225 and 
                    app.height/2-150 <= mouseY <= app.height/2+150):
                self.subjectAddPage = False
        
        if self.subjectAddPage == False and (app.width/5 - 75 <= mouseX <= app.width/5 + 75 
                                           and 380 <= mouseY <= 420):
            self.subjectAddPage = True

        for subjectSubList in self.subjectList:
            location = subjectSubList[3]
            index = self.subjectList.index(subjectSubList)
            location += 50*index
            subjectX, subjectY = app.width/5, location
            if (subjectX - 10 <= mouseX <= subjectX + 10 and
                    subjectY - 10 <= mouseY <= subjectY + 10):
                if self.focusTimerRun or (self.activeSubjectIndex is not None and self.activeSubjectIndex != index):
                    self.stopTimer() 
                else:
                    self.startTimer(app)
                self.activeSubjectIndex = index
                break

    def startTimer(self, app):
        self.focusTimerRun, self.shortTimerRun, self.longTimerRun = True, False, False
        app.FocusTimePage.studyIndex = 0

    def stopTimer(self):
        self.focusTimerRun = False

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
        
        subjectExist = False
        for subjectSubList in app.TimerPage.subjectList:
            if self.subject == subjectSubList[0]:
                subjectExist = True
                break
        
        if self.subject != '' and selectedColor != None and subjectExist == False:
            app.TimerPage.subjectList.append([self.subject, selectedColor, '00:00:00', 470])
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
                userInput = app.getTextInput('Write in the format of "00:00" (e.g. 14:30)')
                if self.isValid(userInput):
                    self.startTime = userInput
                    break
        if app.width/2+120 <= mouseX <= app.width/2+200 and app.height/2-5 <= mouseY <= app.height/2+25:
            while True:
                userInput = app.getTextInput('Write in the format of "00:00" (e.g. 17:30)')
                if self.isValid(userInput):
                    self.endTime = userInput
                    break
        if app.width/2+120 <= mouseX <= app.width/2+200 and app.height/2+35 <= mouseY <= app.height/2+65:
            while True:
                userInput = app.getTextInput('Write in the format of "00:00" (hour:minute)')
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
    app.stepsPerSecond = 1
    app.timerCount = 0
    app.mainDisplay = True
    app.FocusTimePage = FocusTimePage(app.width, app.height)
    app.MainPage = MainPage(app.width, app.height, app.FocusTimePage)
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
    app.MainPage.timerLabel(app)
    global currentTime, currentTimehour, currentTimeminute
    currentTime = datetime.datetime.now()
    currentTimehour = f'0{currentTime.hour}' if currentTime.hour < 10 else currentTime.hour
    currentTimeminute = f'0{currentTime.minute}' if currentTime.minute < 10 else currentTime.minute
    app.MainPage.taskAdd = app.CalendarPage.taskAdd 
        
    if app.TimerPage.focusTimerRun == True and app.TimerPage.activeSubjectIndex is not None:
        subjectSubList = app.TimerPage.subjectList[app.TimerPage.activeSubjectIndex]
        
        subjectSecond = int(subjectSubList[2][6:])
        subjectMinute = int(subjectSubList[2][3:5])
        subjectHour = int(subjectSubList[2][0:2])
        
        subjectSecond += 1
        if subjectSecond >= 60:
            subjectSecond = 0
            subjectMinute += 1
        if subjectMinute >= 60:
            subjectMinute = 0
            subjectHour += 1

        if subjectHour < 10: studyHour = f'0{str(subjectHour)}'
        else: studyHour = str(subjectHour)
        if subjectMinute < 10: studyMinute = f'0{str(subjectMinute)}'
        else: studyMinute = str(subjectMinute)
        if subjectSecond < 10: studySecond = f'0{str(subjectSecond)}'
        else: studySecond = str(subjectSecond)

        subjectSubList[2] = f'{studyHour}:{studyMinute}:{studySecond}'

    if app.MainPage.calendar == True:
        app.CalendarPage.optimizeTask(app)

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