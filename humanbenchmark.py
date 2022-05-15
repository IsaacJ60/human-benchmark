from pygame import *
from random import *
from timeit import default_timer as timer

init()

WIDTH, HEIGHT = 1200, 800
WIN = display.set_mode((WIDTH, HEIGHT))
RED = (255, 0, 0)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
BLUE = (43, 135, 209)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

test = -1
seconds = 0
isTesting = False
testRect = (0, 0, 1200, 500)
time.set_timer(USEREVENT, 1000)
clock = time.Clock()
waitTime = randint(1, 5)
isTesting1 = False
isStartTime = True
startTime = 0
reactionTime = 0
isReacted = False
randNum = 0
userNum = ""
timer3s = 0
keys3 = False
numRoof = 10
numFloor = 1

### button4 global variables
score = 0
lives = 3
seenWords = []
seenOrNew = -1
wordsFile = open("assets/words.txt", "r")
tempWordList = wordsFile.readlines()
wordsFile.close()
newWords = []
for i in range(0, len(tempWordList), 2):
    newWords.append(tempWordList[i].strip())
randomWordIndex = randint(0, len(newWords) - 1)
randomWord = newWords[randomWordIndex]
alive = True

menuFont = font.SysFont("Arial", 30)
menuFontBig = font.SysFont("Arial", 60)
menuimg = image.load("assets/menuimg.png").convert_alpha()
menuimgNames = ["assets/button1.png", "assets/button3.png", "assets/button4.png",
                "assets/button5.png", "assets/button6.png", "assets/button8.png"]
button4gameover = False

menuRects = []
counter = 0
for y in range(200, 600, 330):  # "i" represents y-coord of img
    for x in range(115, 1000, 370):  # "j" represents x-coord of img
        draw.rect(WIN, WHITE, (x, y, 225, 225))  # produce imgs in rows
        img = image.load(menuimgNames[counter])
        WIN.blit(img, (x, y))
        menuRects.append((x, y, 225, 225))
        counter += 1

countdownN = 3


points = [-1 for i in range(6)]


def countdown():
    global countdownN
    countText = menuFontBig.render(str(countdownN), True, GREY)
    WIN.blit(countText, (585, 200))


def menu():
    global test, isTesting
    if -1 not in points:
        avPoints = "%.1f" %(sum(points)/6)
        pointText = menuFont.render("Score: " + str(avPoints), True, WHITE)
        WIN.blit(pointText, (525, 120))
    else:
        testsLeft = points.count(-1)
        pointText = menuFont.render("Tests Left:" + str(testsLeft), True, WHITE)
        WIN.blit(pointText, (510, 120))
    waitText = menuFontBig.render("HUMAN BENCHMARKING", True, WHITE)
    WIN.blit(waitText, (230, 30))
    for i in range(len(menuRects)):
        if Rect(menuRects[i]).collidepoint(mx, my) and mb[0]:
            test = i
            isTesting = True
            break


def button0():
    global waitTime, isTesting1, isStartTime, startTime, reactionTime, isReacted
    WIN.fill(BLACK)
    draw.rect(WIN, BLUE, testRect, 0)
    if countdownN > 0:
        countdown()
        waitTime = randint(1, 5)
    else:
        isTesting1 = True
        waitText = menuFontBig.render("Wait for Green", True, WHITE)
        WIN.blit(waitText, (400, 200))
        if waitTime == 0:
            if isStartTime:
                startTime = timer()
                isStartTime = False
            isTesting1 = False
            draw.rect(WIN, GREEN, testRect, 0)
            clickText = menuFontBig.render("Click Now", True, WHITE)
            WIN.blit(clickText, (450, 200))
            if mb[0] and isReacted == False:
                isReacted = True
                endTime = timer()
                reactionTime = round((endTime - startTime), 3)
    if isReacted:
        WIN.fill(BLACK)
        reactionText = menuFontBig.render(str(reactionTime) + " seconds", True, WHITE)
        WIN.blit(reactionText, (420, 300))
        reactionText = menuFont.render("Enter to Exit", True, WHITE)
        WIN.blit(reactionText, (50, 50))
        if reactionTime < 0.15:
            points[0] = 10
        elif reactionTime < 0.18:
            points[0] = 9
        elif reactionTime < 0.21:
            points[0] = 8
        elif reactionTime < 0.24:
            points[0] = 7
        elif reactionTime < 0.27:
            points[0] = 6
        elif reactionTime < 0.3:
            points[0] = 5
        elif reactionTime < 0.33:
            points[0] = 4
        elif reactionTime < 0.36:
            points[0] = 3
        elif reactionTime < 0.39:
            points[0] = 2
        elif reactionTime < 0.41:
            points[0] = 1


targetCount = 15
randx, randy = 500, 200
timer2s = 0
timer2d = 0
whiffs = 0
hits = 0
totalClicks = 0


def button2():
    global targetCount, click, randx, randy, timer2s, timer2d, whiffs, hits, totalClicks
    WIN.fill(BLACK)
    draw.rect(WIN, BLUE, testRect, 0)
    if countdownN > 0:
        countdown()
        timer2s = seconds
    else:
        if click and randx - 40 < mx < randx + 40 and randy - 40 < my < randy + 40:
            randx, randy = randint(300, 900), randint(50, 450)
            targetCount -= 1
            hits += 1
            totalClicks += 1
            if targetCount == 0:
                timer2d = seconds - timer2s
                click = False
        elif click:
            totalClicks += 1
            whiffs += 1
        reactionText = menuFont.render("Time per target (s): " + str("%.2f" % (timer2d / 15)), True, WHITE)
        WIN.blit(reactionText, (100, 600))
        reactionText = menuFont.render("Misses: " + str(whiffs), True, WHITE)
        WIN.blit(reactionText, (550, 600))
        accuracy = round((hits/totalClicks if totalClicks > 0 else 1.0)*100, 2)
        reactionText = menuFont.render("Accuracy: " + str(accuracy), True, WHITE)
        WIN.blit(reactionText, (900, 600))
        if targetCount == 0:
            reactionText = menuFont.render("Click to Exit", True, WHITE)
            WIN.blit(reactionText, (50, 50))
            if click:
                b2points = 0
                avTime = timer2d / 15
                if avTime < 0.3:
                    b2points += 8
                elif avTime < 0.35:
                    b2points += 7
                elif avTime < 0.4:
                    b2points += 6
                elif avTime < 0.45:
                    b2points += 5
                elif avTime < 0.5:
                    b2points += 4
                elif avTime < 0.6:
                    b2points += 3
                elif avTime < 0.7:
                    b2points += 2
                else:
                    b2points += 1

                if accuracy > 90:
                    b2points += 2
                elif accuracy > 70:
                    b2points += 1

                points[1] = b2points

                exitTest()

        else:
            draw.circle(WIN, WHITE, (randx, randy), 40)


b3level = 1
b3over = False


def button3():
    global randNum, seconds, timer3s, userNum, countdownN, keys3, numRoof, numFloor, b3level, b3over, click
    WIN.fill(BLACK)
    draw.rect(WIN, BLUE, testRect, 0)
    if countdownN > 0:
        countdown()
        randNum = randint(numFloor, numRoof - 1)
        timer3s = seconds
    else:
        b3levelText = menuFontBig.render("Current Level: " + str(b3level), True, WHITE)
        WIN.blit(b3levelText, (370, 550))
        if seconds - timer3s > 3:
            numText = menuFontBig.render("What was the number? (click to enter)", True, WHITE)
            WIN.blit(numText, (100, 130))
            keys3 = True

            numText = menuFontBig.render(str(userNum), True, WHITE)
            WIN.blit(numText, (595-(len(userNum)*15), 200))

            if userNum != '' and int(userNum) == randNum and mb[0]:
                b3level += 1
                draw.rect(WIN, BLUE, testRect, 0)
                countdownN = 3
                userNum = ''
                keys3 = False
                numRoof *= 10
                numFloor *= 10
            if b3over:
                WIN.fill(BLACK)
                b3levelText = menuFontBig.render("Best Level: " + str(b3level), True, WHITE)
                WIN.blit(b3levelText, (330, 400))
                b3levelText = menuFontBig.render("Correct Number: " + str(randNum), True, WHITE)
                WIN.blit(b3levelText, (330, 300))
                reactionText = menuFont.render("Click to Exit", True, WHITE)
                WIN.blit(reactionText, (50, 50))
                if click:
                    if b3level > 13:
                        points[2] = 10
                    elif b3level > 12:
                        points[2] = 9
                    elif b3level > 11:
                        points[2] = 8
                    elif b3level > 8:
                        points[2] = 7
                    elif b3level > 6:
                        points[2] = 5
                    elif b3level > 5:
                        points[2] = 3
                    elif b3level > 4:
                        points[2] = 2
                    elif b3level > 3:
                        points[2] = 1

                    exitTest()
            if click and userNum != '' and int(userNum) != randNum:
                b3over = True

        else:
            numText = menuFontBig.render(str(randNum), True, BLACK)
            WIN.blit(numText, (595-(len(str(randNum))*15), 200))
            numText = menuFontBig.render("Remember:", True, WHITE)
            WIN.blit(numText, (450, 130))


def button4():
    global score, lives, seenOrNew, randomWord, seenWords, newWords, randomWordIndex, alive, button4gameover
    WIN.fill(BLACK)
    draw.rect(WIN, BLUE, testRect, 0)
    if alive:
        seenRect = Rect(400, 600, 100, 25)
        newRect = Rect(700, 600, 100, 25)

        FONT = font.SysFont("Arial", 50)
        livesText = FONT.render("Lives | " + str(lives), True, (170, 207, 237))
        scoreText = FONT.render("Score | " + str(score), True, (170, 207, 237))
        WIN.blit(livesText, (200, 150))
        WIN.blit(scoreText, (800, 150))

        draw.rect(WIN, YELLOW, seenRect)
        draw.rect(WIN, YELLOW, newRect)
        RectFont = font.SysFont("Arial", 23)
        seenRectText = RectFont.render("SEEN", True, BLACK)
        newRectText = RectFont.render("NEW", True, BLACK)
        WIN.blit(seenRectText, (422, 600))
        WIN.blit(newRectText, (722, 600))

        if click and score < 5:
            if seenRect.collidepoint(mx, my):
                if randomWord in seenWords:
                    score += 1
                else:
                    lives -= 1
                del newWords[randomWordIndex]
                seenWords.append(randomWord)
                randomWordIndex = randint(0, len(newWords) - 1)
                randomWord = newWords[randomWordIndex]
            elif newRect.collidepoint(mx, my):
                if randomWord in newWords:
                    score += 1
                else:
                    lives -= 1
                del newWords[randomWordIndex]
                seenWords.append(randomWord)
                randomWordIndex = randint(0, len(newWords) - 1)
                randomWord = newWords[randomWordIndex]

        elif click and score >= 5:
            if seenRect.collidepoint(mx, my):
                if randomWord in seenWords:
                    score += 1
                else:
                    lives -= 1
                del newWords[randomWordIndex]
                seenWords.append(randomWord)
                if randint(0, 1) == 0:
                    randomWordIndex = randint(0, len(newWords) - 1)
                    randomWord = newWords[randomWordIndex]
                else:
                    randomWordIndex = randint(0, len(seenWords) - 1)
                    randomWord = seenWords[randomWordIndex]
            elif newRect.collidepoint(mx, my):
                if randomWord in newWords:
                    score += 1
                else:
                    lives -= 1
                del newWords[randomWordIndex]
                seenWords.append(randomWord)
                if randint(0, 1) == 0:
                    randomWordIndex = randint(0, len(newWords) - 1)
                    randomWord = newWords[randomWordIndex]
                else:
                    randomWordIndex = randint(0, len(seenWords) - 1)
                    randomWord = seenWords[randomWordIndex]

        wordFont = font.SysFont("Arial", 100)
        wordText = FONT.render(randomWord, True, (170, 207, 237))
        WIN.blit(wordText, (600-(len(randomWord)*12), 250))

        if lives == 0:
            alive = False
    else:
        FONT = font.SysFont("Arial", 50)
        WIN.fill(BLACK)
        endText = FONT.render(str(score) + " words", True, WHITE)
        WIN.blit(endText, (500, 300))
        button4gameover = True
        if click:
            if score <= 10:
                points[3] = 1
            elif score <= 20:
                points[3] = 2
            elif score <= 30:
                points[3] = 3
            elif score <= 40:
                points[3] = 4
            elif score <= 50:
                points[3] = 5
            elif score <= 60:
                points[3] = 6
            elif score <= 70:
                points[3] = 7
            elif score <= 80:
                points[3] = 8
            elif score <= 100:
                points[3] = 9
            elif score <= 120:
                points[3] = 10

            exitTest()


### button5 global variables
started = False
solved = True
numbers = 4
button5lives = 3
board = [[-2 for i in range(8)] for i in range(5)]
filled = [[False for i in range(8)] for i in range(5)]
numCount = 1
while numCount != 5:
    randInt = randint(0, 39)
    if not filled[randInt // 8][randInt % 8]:
        board[randInt // 8][randInt % 8] = numCount
        filled[randInt // 8][randInt % 8] = True
        numCount += 1
        rectList = [-1 for i in range(numCount)]
        currSquare = 0
numCount -= 1


def button5():
    global button5lives, numbers, solved, board, rectList, numCount, currSquare, started, click
    FONT = font.SysFont("Calibri", 50)
    WIN.fill((43, 135, 209))
    dispayScoreAndLives = FONT.render("Lives | " + str(button5lives) + "              Score | " + str(numbers), True,
                                      BLACK)
    WIN.blit(dispayScoreAndLives, (100, 25))
    if solved:
        board = [[-2 for i in range(8)] for i in range(5)]
        filled = [[False for i in range(8)] for i in range(5)]
        numCount = 1
        while numCount != numbers + 1:
            randInt = randint(0, 39)
            if filled[randInt // 8][randInt % 8] == False:
                board[randInt // 8][randInt % 8] = numCount
                filled[randInt // 8][randInt % 8] = True
                numCount += 1
        numCount -= 1
        rectList = [-1 for i in range(numCount)]
        currSquare = 0
        started = False
        solved = False

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != -2:
                if started:
                    rectColor = WHITE
                    rectWidth = 0
                else:
                    rectColor = (65, 147, 214)
                    rectWidth = 5
                boxNumText = FONT.render(str(board[i][j]), True, WHITE)
                WIN.blit(boxNumText, (225 + (100 * j), 125 + (100 * i)))
                draw.rect(WIN, rectColor, (200 + (100 * j), 100 + (100 * i), 95, 95), rectWidth)
                rectList[board[i][j] - 1] = (200 + (100 * j), 100 + (100 * i), 95, 95)
                for c in range(currSquare):
                    draw.rect(WIN, (43, 135, 209), (rectList[c]))
    if click:
        for i in range(numCount):
            if Rect(rectList[i]).collidepoint(mx, my):
                if i == currSquare:
                    currSquare += 1
                    started = True
                    if currSquare == numbers:
                        solved = True
                        numbers += 1
                else:
                    button5lives -= 1
                    solved = True
                    click = False

    if button5lives <= 0:
        WIN.fill(BLACK)
        endText = FONT.render("Score | " + str(numbers), True, WHITE)
        WIN.blit(endText, (500, 300))
        if click:
            if numbers <= 6:
                points[4] = 1
            elif numbers == 7:
                points[4] = 2
            elif numbers == 8:
                points[4] = 3
            elif numbers == 9:
                points[4] = 4
            elif numbers == 10:
                points[4] = 5
            elif numbers == 11:
                points[4] = 6
            elif numbers == 12:
                points[4] = 7
            elif numbers == 13:
                points[4] = 8
            elif numbers == 14:
                points[4] = 9
            elif numbers >= 15:
                points[4] = 10

            exitTest()


typingFile = open("assets/typingtest.txt", "r")
typeListTemp = typingFile.readlines()
typeList = []
for word in typeListTemp:
    typeList.append(word.strip())
shuffle(typeList)
typeIndex = 0
isTypeTest = False
typeText = ""
typingTestTime = 30
numChars = 0


def button7():
    global typeIndex, isTypeTest, typeText, typingTestTime, numChars
    WIN.fill(BLACK)
    draw.rect(WIN, BLUE, testRect, 0)
    if countdownN > 0:
        countdown()
    else:
        countText = menuFontBig.render(str(typingTestTime), True, WHITE)
        WIN.blit(countText, (595, 200))
        isTypeTest = True
        numText = menuFont.render(
            (str(typeList[typeIndex]) + " " + str(typeList[typeIndex + 1]) + " " + str(typeList[typeIndex + 2])),
            True, BLACK)
        WIN.blit(numText, (50, 400))
        typeText1 = menuFont.render(typeText, True, WHITE)
        WIN.blit(typeText1, (50, 350))
        wpm = round(((numChars/5) / (30-typingTestTime) if (30-typingTestTime) != 0 else 1)*100)
        typeText1 = menuFont.render("WPM: " + str(wpm), True, WHITE)
        WIN.blit(typeText1, (50, 200))
        if typeText == str(typeList[typeIndex]) + " ":
            numChars += len(typeList[typeIndex])
            typeIndex += 1
            typeText = ""
        if typingTestTime == 0:
            isTypeTest = False
            typeText1 = menuFont.render("WPM: " + str(wpm), True, WHITE)
            WIN.blit(typeText1, (50, 200))
            if click:
                if wpm > 110:
                    points[5] = 10
                elif wpm > 100:
                    points[5] = 9
                elif wpm > 90:
                    points[5] = 8
                elif wpm > 80:
                    points[5] = 7
                elif wpm > 70:
                    points[5] = 6
                elif wpm > 60:
                    points[5] = 5
                elif wpm > 50:
                    points[5] = 4
                elif wpm > 40:
                    points[5] = 3
                elif wpm > 30:
                    points[5] = 2
                elif wpm > 20:
                    points[5] = 1

                exitTest()


def exitTest():
    global countdownN, test, isStartTime, isTesting, isTesting1, isReacted, \
        score, lives, seenWords, seenOrNew, wordsFile, tempWordList, newWords, \
        randomWordIndex, randomWord, alive, seconds, waitTime, startTime, \
        reactionTime, randNum, userNum, timer3s, keys3, numRoof, numFloor, \
        targetCount, whiffs, b3over, b3level, typeIndex, isTypeTest, typeText, \
        typingTestTime, started, solved, numbers, button5lives, board, filled, \
        numCount, randInt, rectList, currSquare, totalClicks, hits
    shuffle(typeList)
    typeIndex = 0
    isTypeTest = False
    typeText = ""
    typingTestTime = 30
    b3level = 1
    b3over = False
    targetCount = 15
    whiffs = 0
    countdownN = 3
    test = -1
    isStartTime = True
    isReacted = False
    counter1 = 0
    isTesting = False
    isTesting1 = False
    test = -1
    seconds = 0
    numChars = 0
    waitTime = randint(1, 5)
    startTime = 0
    reactionTime = 0
    randNum = 0
    userNum = ""
    timer3s = 0
    keys3 = False
    numRoof = 10
    numFloor = 1
    WIN.fill(BLACK)
    for yy in range(200, 600, 330):  # "i" represents y-coord of img
        for xx in range(115, 1000, 370):  # "j" represents x-coord of img
            draw.rect(WIN, WHITE, (xx, yy, 225, 225))  # produce imgs in rows
            img1 = image.load(menuimgNames[counter1])
            WIN.blit(img1, (xx, yy))
            menuRects.append((xx, yy, 225, 225))
            counter1 += 1

    score = 0
    lives = 3
    seenWords = []
    seenOrNew = -1
    wordsFile = open("assets/words.txt", "r")
    tempWordList = wordsFile.readlines()
    wordsFile.close()
    newWords = []
    for j in range(0, len(tempWordList), 2):
        newWords.append(tempWordList[j].strip())
    randomWordIndex = randint(0, len(newWords) - 1)
    randomWord = newWords[randomWordIndex]
    alive = True
    started = False
    solved = True
    numbers = 4
    button5lives = 3
    board = [[-2 for i in range(8)] for i in range(5)]
    filled = [[False for i in range(8)] for i in range(5)]
    numCount = 1
    while numCount != 5:
        randInt = randint(0, 39)
        if not filled[randInt // 8][randInt % 8]:
            board[randInt // 8][randInt % 8] = numCount
            filled[randInt // 8][randInt % 8] = True
            numCount += 1
            rectList = [-1 for i in range(numCount)]
            currSquare = 0
    numCount -= 1
    totalClicks = 0
    hits = 0


running = True
while running:
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()
    click = False

    for evt in event.get():
        if evt.type == QUIT:
            running = False
        if evt.type == MOUSEBUTTONUP:
            click = True
        if evt.type == USEREVENT:
            seconds += 1
            if isTypeTest and typingTestTime > 0:
                typingTestTime -= 1
            if isTesting:
                countdownN -= 1
            if isTesting1:
                waitTime -= 1
        if evt.type == KEYUP:
            if isTypeTest:
                if evt.key == K_BACKSPACE:  # slicing string is backspace
                    typeText = typeText[:-1]
                else:  # take normal keyboard input
                    typeText += evt.unicode
            if evt.key == K_RETURN:
                if isReacted:
                    exitTest()
                if button4gameover:
                    exitTest()
            if keys3:
                if evt.key == K_1:
                    userNum += "1"
                if evt.key == K_2:
                    userNum += "2"
                if evt.key == K_3:
                    userNum += "3"
                if evt.key == K_4:
                    userNum += "4"
                if evt.key == K_5:
                    userNum += "5"
                if evt.key == K_6:
                    userNum += "6"
                if evt.key == K_7:
                    userNum += "7"
                if evt.key == K_8:
                    userNum += "8"
                if evt.key == K_9:
                    userNum += "9"
                if evt.key == K_0:
                    userNum += "0"
                if evt.key == K_BACKSPACE:
                    userNum = userNum[:-1]

    if test == 0:
        button0()
    elif test == 1:
        button2()
    elif test == 2:
        button3()
    elif test == 3:
        button4()
    elif test == 4:
        button5()
    elif test == 5:
        button7()
    else:
        menu()

    display.flip()
    clock.tick(30)
quit()
