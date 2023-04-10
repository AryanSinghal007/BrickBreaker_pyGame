import os
import json
import pygame
from tkinter import *
from pygame.locals import *
from functools import partial
from tkinter import messagebox


try:
    with open('../Scores.json') as f:
        scores = json.load(f)
except:
    with open('../Scores.json', 'w') as f:
        json.dump([[], [], []], f, indent=4)

    with open('../Scores.json') as f:
        scores = json.load(f)


def blockGame(root, level):
    level -= 1
    name, playerScore = nameEntry.get(), 0
    root.quit()
    root.destroy()

    pygame.init()

    """
    bgMusic = pygame.mixer.Sound('bgMusic.wav')
    BrickSound = pygame.mixer.Sound('BrickSound.wav')
    pygame.mixer.Channel(0).play(bgMusic)
    
    """

    width, height = 1000, 500
    bg1 = pygame.image.load('universe(bg1).jpeg')
    bg1 = pygame.transform.scale(bg1, [width, height])

    screen = pygame.display.set_mode((width, height))

    # RGB
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)

    # Set Speeds
    ballSpeed = 8 + level  # initial speed
    ballSpeedIncrement = 0.1 + (level * 0.1)  # How much the barSpeed will increase after breaking a brick
    barSpeed = 10 + level
    barSpeedIncrement = 0.1 + (level * 0.1)

    # Bar Initialize
    barHeight = 15
    barWidth = 150
    barX = width // 2 - barWidth // 2
    barY = height - barHeight - 5
    barMoveX = 0

    # Bricks Initialize
    brickWidth = 100
    brickHeight = 30
    gap = 5
    brickList = []
    nrows = 6
    ncols = width // brickWidth

    colors = []
    col_1 = red
    col_2 = blue

    for i in range(1, nrows + 1):
        for j in range(ncols):
            # pygame.Rect(x axis , y axis , width of rect, height)
            rect = pygame.Rect((brickWidth + gap) * j, (brickHeight + gap) * i, brickWidth, brickHeight)
            brickList.append(rect)
            if i % 2 == 0:
                colors.append(col_1)
            else:
                colors.append(col_2)

    # Ball initialize
    ballRadius = 8
    ballY = barY - ballRadius
    ballX = 0
    ballColor = white
    ballMoveX = 0
    ballMoveY = 0
    moveBall = False
    inBool = True

    while True:
        if not moveBall:
            ballX = barX + barWidth // 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    barMoveX = int(barSpeed)
                elif event.key == pygame.K_LEFT:
                    barMoveX = -1 * int(barSpeed)
                elif event.key == pygame.K_SPACE and inBool == True:
                    inBool = False
                    ballMoveX = int(ballSpeed)
                    ballMoveY = -1 * int(ballSpeed)
                    moveBall = True
            elif event.type == pygame.KEYUP:
                barMoveX = 0

        # screen.fill(jo colour chahiye)
        screen.blit(bg1, [0, 0])
        pygame.draw.rect(screen, blue, [barX, barY, barWidth, barHeight])  # bar banaya screen par
        barRect = pygame.Rect(barX, barY, barWidth, barHeight)

        barX += barMoveX
        ballX += ballMoveX
        ballY += ballMoveY

        for i in range(len(brickList)):  # bricks banayi screen par
            pygame.draw.rect(screen, colors[i], brickList[i])

        pygame.draw.circle(screen, ballColor, [ballX, ballY], ballRadius)  # ball banayi screen par
        ballRect = pygame.Rect(ballX, ballY, ballRadius, ballRadius)

        i = ballRect.collidelist(brickList)
        # i=-1 jab ball hawa mein hai

        if i != -1:
            # collision is going to happen here
            # i is index of the brick colliding with ball
            # pygame.mixer.Channel(1).play(BrickSound)
            del brickList[i]
            playerScore += 1
            ballSpeed += ballSpeedIncrement
            barSpeed += barSpeedIncrement
            del colors[i]
            ballMoveY = int(ballSpeed)
        if ballX > width - ballRadius:
            ballMoveX = -1 * int(ballSpeed)
        elif ballX < ballRadius:
            ballMoveX = int(ballSpeed)
        elif ballY < ballRadius:
            ballMoveY = int(ballSpeed)
        elif ballRect.colliderect(barRect):
            ballMoveY = -1 * int(ballSpeed)
        elif barX > width - barWidth:
            barX = width - barWidth
        elif barX < 0:
            barX = 0
        elif ballY > height - ballRadius:

            window = Tk()
            window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
            window.withdraw()

            if (0 if not scores[level] else (
            max([scores[level][i]['score'] for i in range(len(scores[level]))]))) >= playerScore:
                messagebox.showinfo(title='Score', message='Your Score is %d !' % playerScore)
            else:
                messagebox.showinfo(title='Score', message='NEW HIGH SCORE ! \nYour Score is %d' % playerScore)

            window.deiconify()
            window.destroy()
            window.quit()

            scores[level].append({"name": name, "score": playerScore})

            with open("ScoresTEMP.json", 'w') as tempFile:
                json.dump(scores, tempFile, indent=4)

            os.remove("../Scores.json")
            os.rename(r'ScoresTEMP.json', r'../Scores.json')

            pygame.quit()  # pygame se bahar
            quit()  # IDLE se bahar
        pygame.display.update()


start = Tk()
start.title('Start Menu')
start.geometry('500x500')
start.configure(bg="black")

topFrame = Frame(start, bg='#85c6dd')
topFrame.place(relx=0.1, rely=0.03, relheight=0.26, relwidth=0.8)

startLabel = Label(topFrame, text='Enter your name', bg='#85c6dd', font=('Autobus', 18))
startLabel.place(relx=0.1, rely=0.05, relheight=0.15, relwidth=0.8)

nameEntry = Entry(start, justify='center', font= ('Arial, 15'))
nameEntry.place(relx=0.15, rely=0.12, relwidth=0.7, relheight=0.1, )

midFrame = Frame(start, bg='#85c6dd')
midFrame.place(relx=0.1, rely=0.35, relwidth=0.8, relheight=0.6, anchor='nw')

lvlButtons, y = [1, 2, 3], 0.13
for i in range(len(lvlButtons)):
    lvlButtons[i] = Button(midFrame, text='Play Level ' + str(lvlButtons[i]), font=('Autobus, 14'),
                           command=partial(blockGame, start, lvlButtons[i]))
    lvlButtons[i].place(relx=0.02, rely=y, relwidth=0.5, relheight=0.2)

    # highScore = (0 if not scores[i] else (max([scores[i][j]['score'] for j in range(len(scores[i]))])))
    hs = []
    if not scores[i]:
        highScore = 0
    else:
        for j in range(len(scores[i])):
            hs.append(scores[i][j]['score'])
        highScore = max(hs)

    # highName = ('-' if not scores[i] else (max([scores[i][j]['name'] for j in range(len(scores[i]))])))
    hi = []
    if not scores[i]:
        highName = '-'
    else:
        for j in range(len(scores[i])):
            hi.append(scores[i][j]['name'])
        highName = max(hi)

    highScoreLabel = Label(midFrame, bg='#ffffff', text='High Score:: %d \nBy %s ' % (highScore, highName),
                           font=('Arial', 12))
    highScoreLabel.place(relx=0.55, rely=y, relwidth=0.42, relheight=0.2)
    y += 0.25


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit()


start.protocol("WM_DELETE_WINDOW", on_closing)
mainloop()
