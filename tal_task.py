import psychopy
from psychopy import core, visual, gui, data
from psychopy.hardware import keyboard
import pygame, time, ctypes
import numpy as np
from numpy.random import random

# Make a text file to save data
expInfo = {"subject": "0"}
dlg = gui.DlgFromDict(expInfo, title="Tal's Flowers Task")
fileName = "flowers_task_" + expInfo["subject"] + "_" + data.getDateStr()
dataFile = open(
    fileName + ".csv", "w"
)  # a simple text file with 'comma-separated-values'
dataFile.write("subject, block_type, block, condition, trial, right_offer, left_offer, offer_right_image, offer_left_image, exp_value_right, exp_value_left, exp_value_chosen, choice_location, choice_key, choice_card, unchosen_card, chosen_card_image, unchosen_card_image, exp_value1, exp_value2, exp_value3, exp_value4, reward\n")
subjectN = expInfo["subject"]
# choice_key = 1 -> left, choice_key = 2 -> right
#initializing game
pygame.init()
clock = pygame.time.Clock()
keepPlaying = True
j = pygame.joystick.Joystick(0)
j.init()

# create a window
win = visual.Window( [800, 600], fullscr = True, monitor="testMonitor", units="deg", color=(1, 1, 1), useFBO=False)
win.mouseVisible = False
mytimer = core.Clock()

# number of trials and constant pictures
from random import sample
n = 25 # number of trials in each block
#stim_id = np.zeros(n)
coins = 0 #global var
won = visual.ImageStim(win, image="rw.png", pos=[0, 0], size=4)
lost = visual.ImageStim(win, image="ur.png", pos=[0, 0], size=4)
fixation = visual.TextStim(win, text="+", pos=[0, 0], color=(-1, -1, -1))
hourglass = visual.ImageStim(win, image="hourglass.png", pos=[0,0], size=4)
#left_rect = visual.Rect(win, size = [6,6], lineColor=(-1, -1, 1)
#ImageStim(win, image=presented[0], pos=[-6, 0], size=(6,6))
#coinsBox = visual.TextStim(win, text= str(coins), pos=[0,0], color=(0,0,0))

# counterbalance and picture sets
subject_id = (int(subjectN))%2 # previously x
flower_set1 = [ "1.png", "2.png", "3.png", "4.png" ]
flower_set2 = [ "5.png", "6.png", "7.png", "8.png" ] 
flower_set3 = [ "a.png", "b.png", "c.png", "d.png" ] 
flower_set4 = [ "e.png", "f.png", "g.png", "h.png" ] 
flower_set5 = [ "i.png", "j.png", "k.png", "l.png" ] 
flower_set6 = [ "m.png", "n.png", "o.png", "p.png" ] 
flower_set7 = [ "q.png", "r.png", "s.png", "t.png" ] 
flower_set8 = [ "u.png", "v.png", "w.png", "x.png" ] 
deckList = [ [ "1.png", "2.png", "3.png", "4.png" ], [ "5.png", "6.png", "7.png", "8.png" ] , [ "a.png", "b.png", "c.png", "d.png" ] , [ "e.png", "f.png", "g.png", "h.png" ], [ "i.png", "j.png", "k.png", "l.png" ], ["m.png", "n.png", "o.png", "p.png" ], [ "q.png", "r.png", "s.png", "t.png" ], [ "u.png", "v.png", "w.png", "x.png"] ]
deck = [flower_set1, flower_set2, flower_set3, flower_set4, flower_set5, flower_set6, flower_set7, flower_set8]
picList = sample(deckList, 8)

# experiment flow
def main():
    instructionsPhase = True
    trainPhase = False
    quizPhase = False
    gamePhase = False
    
    # Start Instruction Phase
    if instructionsPhase:
        instructionsFunc()
        # Changing Phase to quiz Phase
        instructionsPhase = False
        quizPhase = True
        trainPhase = False
        gamePhase = False
    
    # Start Test\Quiz Phase
    if quizPhase:
        quizFunc()
        # Changing Phase to Training Phase
        instructionsPhase = False
        quizPhase = False
        trainPhase = True
        gamePhase = False

    # start training
    if trainPhase:
        blockCnt = 0
        training_intro = visual.ImageStim(win, image="train1.png",  units='norm', size=[2,2], interpolate = True)
        training_intro.draw()
        win.update()
        while True:
            abort(win)
            events = pygame.event.poll()
            if (events.type == pygame.JOYBUTTONDOWN):
                #Event 4 -> Pressing down left button, Event 5 -> Pressing down right button
                if events.button == 4:
                    delayCond = "1 second"
                    mainExperimentModes(dataFile, blockCnt, subjectN, win, "1 second", 5, 'practice', flower_set1)
                    end_training = visual.ImageStim(win, image="end_training.png",  units='norm', size=[2,2], interpolate = True)
                    end_training.draw()
                    win.update()
                    # wait for response to end practice block
                    while True:
                        events = pygame.event.poll()
                        if (events.type == pygame.JOYBUTTONDOWN):
                            #Event 4 -> Pressing down left button
                            if events.button == 4:
                                break
                    # Changing Phase to Game Phase
                    instructionsPhase = False
                    quizPhase = False
                    trainPhase = False
                    gamePhase = True
                    break
    # start game:

    if gamePhase:
        outro = visual.ImageStim(win, image="outro.png",  units='norm', size=[2,2], interpolate = True)
        blockCnt = 0
        # Counterbalance block order
        possibleOrder = [ [0,1,0,1,0,1,0,1], [1,0,1,0,1,0,1,0] ]
        # 0 -> delay 7 secs
        # 1 -> delay 1 second
        for x in possibleOrder[subject_id]:
            if (x == 0):
                delayCond = "7 seconds"
                blockCnt = blockCnt + 1
                currSet = picList[blockCnt-1]
                startBlock = "startBlock" + str(blockCnt) + ".png"
                endBlock = "endBlock" + str(blockCnt) + ".png"
                start = visual.ImageStim(win, image=startBlock,  units='norm', size=[2,2], interpolate = True)
                end = visual.ImageStim(win, image=endBlock,  units='norm', size=[2,2], interpolate = True)
                start.draw()
                win.update()
                while True:
                    abort(win)
                    events = pygame.event.poll()
                    # Wait for response to begin block
                    if (events.type == pygame.JOYBUTTONDOWN):
                    #Event 4 -> Pressing down left button, Event 5 -> Pressing down right button
                        if events.button == 4:
                            mainExperimentModes(dataFile, blockCnt, subjectN, win, delayCond, n, 'test', currSet)
                            break
                end.draw()
                win.update()
                # Wait for response to end block
                while True:
                    abort(win)
                    events = pygame.event.poll()
                    if (events.type == pygame.JOYBUTTONDOWN):
                    #Event 4 -> Pressing down left button, Event 5 -> Pressing down right button
                        if events.button == 4:
                            break
            if (x == 1):
                delayCond = "1 second"
                blockCnt = blockCnt + 1
                currSet = picList[blockCnt-1]
                startBlock = "startblock" + str(blockCnt) + ".png"
                endBlock = "endblock" + str(blockCnt) + ".png"
                start = visual.ImageStim(win, image=startBlock,  units='norm', size=[2,2], interpolate = True)
                end = visual.ImageStim(win, image=endBlock,  units='norm', size=[2,2], interpolate = True)
                start.draw()
                win.update()
                # Wait for response to begin block
                while True:
                    abort(win)
                    events = pygame.event.poll()
                    if (events.type == pygame.JOYBUTTONDOWN):
                    #Event 4 -> Pressing down left button, Event 5 -> Pressing down right button
                        if events.button == 4:          
                            mainExperimentModes(dataFile, blockCnt, subjectN, win, delayCond, n, 'test', currSet)
                            break
                end.draw()
                win.update()
                # Wait for response to end block
                while True:
                    abort(win)
                    events = pygame.event.poll()
                    if (events.type == pygame.JOYBUTTONDOWN):
                    #Event 4 -> Pressed left Button
                        if events.button == 4:
                            break
        #coinsBox = visual.TextStim(win, text= str(coins), pos=[0,0], color=(0,0,0))
        #coinsBox.draw()
        outro.draw()
        win.update()
        while True:
                    abort(win)
                    events = pygame.event.poll()
                    if (events.type == pygame.JOYBUTTONDOWN):
                    #Event 4 -> Pressed left Button
                        if events.button == 4:
                            break



# # # # # # #
# Functions #
# # # # # # #

def abort(window):
    # check keyboard presses
    kb = keyboard.Keyboard()
    kb.start()
    keys = kb.getKeys(["escape"])
    if "escape" in keys:
        window.close()
        core.quit()

def WrongAnswerFunc():
    mistake = visual.ImageStim(win, image="mistake.png",  units='norm', size=[2,2], interpolate = True)    
    mistake.draw()
    win.update()
    while True:
        abort(win)
        events = pygame.event.poll()
        if (events.type == pygame.JOYBUTTONDOWN):
            # Pressed A for "Try Again"
            if (events.button == 0):
                break
            # Pressed B for "Go over instructions"
            elif (events.button == 1):
                instructionsFunc()
                break

def instructionsFunc():
    currSlide = 1
    while currSlide < 11:
        slideName = "slide" + str(currSlide) + ".png"
        slidePic = visual.ImageStim(win, image=slideName,  units='norm', size=[2,2], interpolate = True)
        slidePic.draw()
        win.update()
        while True:
            abort(win)
            events = pygame.event.poll()
            if (events.type == pygame.JOYBUTTONDOWN):
                #Event 4 -> Pressing down left button, Event 5 -> Pressing down right button
                if events.button == 4:
                    currSlide = currSlide + 1
                    break
                if (events.button == 5 and currSlide > 1) :
                    currSlide = currSlide - 1
                    break

def quizFunc():
    nTest = 1
    while nTest < 8:
        slideName = "quizQ" + str(nTest) + ".png"
        testPic = visual.ImageStim(win, image=slideName,  units='norm', size=[2,2], interpolate = True)
        testPic.draw()
        win.update()
        while True:
            abort(win)
            events = pygame.event.poll()
            if (events.type == pygame.JOYBUTTONDOWN):
                # Question 1
                if nTest == 1:
                    # Correct Answer Case
                    # Event 1 -> Pressed B Button
                    if events.button == 1:
                        nTest = nTest + 1
                        break
                    # Wrong Answer Case
                    # Event 0 -> Pressed A Button
                    # Event 2 -> Pressed X Button
                    elif (events.button == 0) or (events.button == 2):
                        WrongAnswerFunc()
                        # set nTest = 1 to start quiz from the start 
                        nTest = 1
                        break    
                
                # Question 2
                if nTest == 2:
                    # Correct Answer Case
                    # Event 0 -> Pressed A Button
                    if events.button == 0:
                        nTest = nTest + 1
                        break
                    # Wrong Answer Case
                    # Event 1 -> Pressed B Button
                    # 
                    elif (events.button == 1) or (events.button == 2):
                        WrongAnswerFunc()
                        # set nTest = 1 to start quiz from the start 
                        nTest = 1                        
                        break 
                
                # Question 3
                if nTest == 3:
                    # Correct Answer Case
                    # Event 1 -> Pressed B Button
                    if events.button == 1:
                        nTest = nTest + 1
                        break
                    # Wrong Answer Case
                    # Event 0 -> Pressed A Button
                    # Event 2 -> Pressed X Button
                    elif (events.button == 0) or (events.button == 2):
                        WrongAnswerFunc()
                        # set nTest = 1 to start quiz from the start 
                        nTest = 1                        
                        break

                # Question 4
                if nTest == 4:
                    # Correct Answer Case
                    # Event 0 -> Pressed A Button
                    if events.button == 0:
                        nTest = nTest + 1
                        break
                    # Wrong Answer Case
                    # Event 1 -> Pressed B Button
                    elif (events.button == 1):
                        WrongAnswerFunc()
                        # set nTest = 1 to start quiz from the start 
                        nTest = 1                        
                        break

                # Question 5
                if nTest == 5:
                    # Correct Answer Case
                    # Event 1 -> Pressed B Button
                    if events.button == 1:
                        nTest = nTest + 1
                        break
                    # Wrong Answer Case
                    # Event 0 -> Pressed A Button
                    elif (events.button == 0):
                        WrongAnswerFunc()
                        # set nTest = 1 to start quiz from the start 
                        nTest = 1                        
                        break

                # Question 6
                if nTest == 6:
                    # Correct Answer Case
                    # Event 0 -> Pressed A Button
                    if events.button == 0:
                        nTest = nTest + 1
                        break
                    # Wrong Answer Case
                    # Event 1 -> Pressed B Button
                    elif (events.button == 1):
                        WrongAnswerFunc()
                        # set nTest = 1 to start quiz from the start 
                        nTest = 1                        
                        break

                # Question 7
                if nTest == 7:
                    # Correct Answer Case
                    # Event 1 -> Pressed B Button
                    if events.button == 1:
                        nTest = nTest + 1
                        break
                    # Wrong Answer Case
                    # Event 0 -> Pressed A Button
                    elif (events.button == 0):
                        WrongAnswerFunc()
                        # set nTest = 1 to start quiz from the start 
                        nTest = 1                        
                        break

def mainExperimentModes(dataFile, blockCnt, subjectN, win, cond, trials, blockType, currSet):
    delay_time = 0
    for i in range(1,5):
            if i==1:
                card_1=currSet[0]
            if i==2:
                card_2=currSet[1]
            if i==3:
                card_3=currSet[2]
            if i==4:
                card_4=currSet[3]
    probs = sample([0.35,0.45,0.55,0.65], 4)
    card_1_prob = probs[0]
    card_2_prob = probs[1]
    card_3_prob = probs[2]
    card_4_prob = probs[3]
    # Initilizing Game
    pygame.init()
    clock = pygame.time.Clock()
    j = pygame.joystick.Joystick(0)
    j.init()
    if (cond == "1 second"):
        delay_time = 1
    elif (cond == "7 seconds"):
        delay_time = 7
    for t in range(1, trials+1):
        RTwarning = False
        mytimer = core.Clock()
        # Draw the stimuli and update the window
        presented = sample(currSet, 2)
        unpresented_cards=[]
        presented_probs = []
        for card in currSet:
            if card not in presented:
                unpresented_cards.append(card)
            else:
                # presented_probs.append(probs[int(card.split("_")[1])-1])
                if card == card_1:
                    presented_probs.append(card_1_prob)
                elif card == card_2:
                    presented_probs.append(card_2_prob)
                elif card == card_3:
                    presented_probs.append(card_3_prob)
                elif card == card_4:
                    presented_probs.append(card_4_prob)  
        stimL = visual.ImageStim(win, image=presented[0], pos=[-6, 0], size=(6,6))
        stimR = visual.ImageStim(win, image=presented[1], pos=[6, 0], size=(6,6))
        fixation.draw()
        win.update()
        core.wait(1)
        #draw stims
        fixation.draw()
        stimL.draw()
        stimR.draw()
        win.update()
        mytimer.reset(0)
        while True:
            abort(win)
            if (mytimer.getTime() > 6 and RTwarning == False):
                rt_warning = visual.TextStim(win, text= " רתוי רהמ ביגהל שי", pos=[0,0], color=(-1,-1,-1)) # יש להגיב מהר יותר
                rt_warning.draw()
                win.update()
                while True:
                    events = pygame.event.poll()
                    if (events.type == pygame.JOYBUTTONDOWN):
                        # event 4 -> pressing down left button
                        if (events.button == 4):
                            RTwarning = True
                            break
            events = pygame.event.poll()
            if (events.type == pygame.JOYBUTTONDOWN):
                # event 4 -> Pressing down left button, Event 5 -> Pressing down right button
                if events.button == 4:
                    RT = str(mytimer.getTime())
                    stimL.draw()
                    fixation.draw()
                    win.update()
                    core.wait(0.5)
                    stim_id = (presented[0].split(".")[0])
                    other_id = (presented[1].split(".")[0])
                    prob1 = presented_probs[1] # right flower prob 
                    prob2 = presented_probs[0] # left flower prob
                    curr_prob = prob2
                    key = 1
                    stimapr = "left"
                    dataFile.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," 
                        % (
                            subjectN,
                            blockType,
                            blockCnt,
                            cond,
                            t,
                            other_id,
                            stim_id,
                            presented[1],
                            presented[0],
                            prob1,
                            prob2,
                            prob2,
                            stimapr,
                            key,
                            str(stim_id),
                            str(other_id),
                            presented[0],
                            presented[1],
                            card_1_prob,
                            card_2_prob, 
                            card_3_prob, 
                            card_4_prob,
                        )
                    )
                    # present delay
                    hourglass.draw()
                    win.update()
                    core.wait(delay_time)
                    break
                elif events.button == 5:
                    RT = str(mytimer.getTime())
                    stimR.draw()
                    fixation.draw()
                    win.update()
                    core.wait(0.5)
                    stim_id = (presented[1].split(".")[0])
                    other_id = (presented[0].split(".")[0])
                    prob1 = presented_probs[1] # right flower prob 
                    prob2 = presented_probs[0] # left flower prob
                    curr_prob = prob1
                    key = 2
                    stimapr = "right"
                    dataFile.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," 
                        % (
                            subjectN,
                            blockType,
                            blockCnt,
                            cond,
                            t,
                            str(stim_id),
                            str(other_id),
                            presented[1],
                            presented[0],
                            prob1,
                            prob2,
                            prob1,
                            stimapr,
                            key,
                            str(stim_id),
                            str(other_id),
                            presented[1],
                            presented[0],
                            card_1_prob,
                            card_2_prob, 
                            card_3_prob, 
                            card_4_prob,
                        )
                    )       
                    # present delay
                    hourglass.draw()
                    win.update()
                    core.wait(delay_time)
                    break           
    
        ##########################################
        # outcome using Random Walk for n trials #
        ##########################################
        if (stimapr == "left"):
            stimL.draw()
        if (stimapr == "right"):
            stimR.draw()
        if (random() < curr_prob):
            won.draw()
            #coins += 1
            dataFile.write("%i\n" % (1,))
        else:
            lost.draw()
            dataFile.write("%i,\n" % (0,))
        win.update()
        core.wait(2)



main()

