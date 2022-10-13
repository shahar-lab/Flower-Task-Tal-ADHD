import psychopy
from psychopy import core, visual, gui, data, event, slider
from psychopy.hardware import keyboard
import pygame, time, ctypes
import numpy as np
from numpy.random import random

# Make a text file to save data
expInfo = {"subject": "0"}
dlg = gui.DlgFromDict(expInfo, title="Flowers Task")
fileName = "Flowers_Task_" + expInfo["subject"] + "_" + data.getDateStr()
dataFile = open(
    fileName + ".csv", "w"
)  # a simple text file with 'comma-separated-values'
dataFile.write("subject, block_type, block, condition, trial, right_offer, left_offer, offer_right_image, offer_left_image, exp_value_right, exp_value_left, exp_value_chosen, choice_location, choice_key, choice_card, unchosen_card, chosen_card_image, unchosen_card_image, rt, exp_value1, exp_value2, exp_value3, exp_value4, reward\n")
subjectN = expInfo["subject"]
# choise_key = 1 -> left, choice_key = 2 -> right
# Initializing game
#pygame.init()
#clock = pygame.time.Clock()
#keepPlaying = True
#j = pygame.joystick.Joystick(0)
#j.init()
kb = keyboard.Keyboard()
keys = psychopy.event.getKeys(keyList=["s", "k", "space"])

# create a window
win = visual.Window( [800, 600], fullscr = True, monitor="testMonitor", units="deg", color=(-1, -1, -1), useFBO=False)
mytimer = core.Clock()
win.mouseVisible = False

from random import sample
n = 25 # Number of trials
cond = "none"
stim_id = np.zeros(n)
won = visual.ImageStim(win, image="rw.png", pos=[0, 0], size=4)
lost = visual.ImageStim(win, image="ur.jpg", pos=[0, 0], size=4)
fixation = visual.TextStim(win, text="+", pos=[0, 0], color=(0, 0, 0))

# Stimuli Pics
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

event.clearEvents('keyboard')
slider.markerPos = 3
keys = event.getKeys()

if len(keys):
    if 'left' in keys:
        slider.markerPos = slider.markerPos - 1
    elif 'right' in keys:
        slider.markerPos = slider.markerPos  + 1 

# Experiment Flow Function    
def main():
    instructionsPhase = True
    trainPhase = False
    testPhase = False
    gamePhase = False
    
    # Start Instruction Phase
    if instructionsPhase:
        instructionsFunc()
        # Changing Phase to Test\Quiz Phase
        instructionsPhase = False
        testPhase = True
        trainPhase = False
        gamePhase = False
    
    # Start Test\Quiz Phase
    if testPhase:
        testFunc()
        # Changing Phase to Training Phase
        instructionsPhase = False
        testPhase = False
        trainPhase = True
        gamePhase = False

    if trainPhase:
        training1 = visual.ImageStim(win, image="train1.png",  units='norm', size=[2,2], interpolate = True)
        training1.draw()
        win.update()
        event.clearEvents()
        while True:
            keys = psychopy.event.getKeys(keyList=["s", "k", "space"])
            if ("space" in keys):
                # Changing Phase to Game Phase
                instructionsPhase = False
                testPhase = False
                trainPhase = False
                gamePhase = True
                break
    if gamePhase:
        blockCnt = 0
        # Start Practice Block
        mainExperimentModes(dataFile, blockCnt, subjectN, win, cond, 5, 'practice', picList[0])
        endPractice = visual.ImageStim(win, image="endTraining.png",  units='norm', size=[2,2], interpolate = True)
        endPractice.draw()
        win.update()
        event.clearEvents()
        while True:
            keys = psychopy.event.getKeys(keyList=["s", "k", "space"])
            if ("space" in keys):
                    break
        blockCnt = 1
        for x in range(8):
            currSet = picList[x]
            setpic = currSet.split("_")[2]
            blockstart = "startBlock" + blockCnt + ".png"
            blockend = "endBlock" + blockCnt + ".png"
            start = visual.ImageStim(win, image=blockstart,  units='norm', size=[2,2], interpolate = True)
            set = visual.ImageStim(win, image=setpic, pos=[0, -8], size=(2,2))
            start.draw()
            set.draw()
            win.update()
            event.clearEvents()
            #start block
            while True:
                keys = psychopy.event.getKeys(keyList=["s", "k", "space"])
                if ("space" in keys):
                    mainExperimentModes(dataFile, blockCnt, subjectN, win, cond, n, 'test', currSet)
                    break
            blockend.draw()
            win.update()
            event.clearEvents()
            # Wait for response to end block
            while True:
                keys = psychopy.event.getKeys(keyList=["s", "k", "space"])
                if ("space" in keys):
                    break
            blockCnt = blockCnt + 1


# # # # # # #
# Functions #
# # # # # # #

def WrongAnswerFunc():
    mistake = visual.ImageStim(win, image="mistake.jpg",  units='norm', size=[2,2], interpolate = True)    
    mistake.draw()
    win.update()
    event.clearEvents()
    while True:
        events = pygame.event.poll()
        if (events.type == pygame.JOYBUTTONDOWN):
            # Pressed A for "Try Again"
            if (events.button == 0):
                break
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
        event.clearEvents()
        while True:
            keys = psychopy.event.getKeys(keyList=["s", "k", "space"])
            if ("space" in keys):
                currSlide = currSlide + 1
                break

def testFunc():
    nTest = 1
    while nTest < 9:
        slideName = "test" + str(nTest) + ".jpg"
        testPic = visual.ImageStim(win, image=slideName,  units='norm', size=[2,2], interpolate = True)
        testPic.draw()
        win.update()
        event.clearEvents()
        while True:
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
                    # Event 2 -> Pressed X Button
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
                    elif (events.button == 0):
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
                    # Event 2 -> Pressed X Button
                    if events.button == 2:
                        nTest = nTest + 1
                        break
                    # Wrong Answer Case
                    # Event 0 -> Pressed A Button
                    # Event 1 -> Pressed B Button
                    elif (events.button == 0) or (events.button == 1):
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
                
                # Question 8
                if nTest == 8:
                    # Correct Answer Case
                    # Event 2 -> Pressed X Button
                    if events.button == 2:
                        nTest = nTest + 1
                        break
                    # Wrong Answer Case
                    # Event 0 -> Pressed A Button
                    # Event 1 -> Pressed B Button
                    elif (events.button == 0) or (events.button == 1):
                        WrongAnswerFunc()
                        # set nTest = 1 to start quiz from the start 
                        nTest = 1                        
                        break

def mainExperimentModes(dataFile, blockCnt, subjectN, win, cond, trials, blockType, currSet):
    for i in range(1,5):
            if i==1:
                card1=currSet[0]
            if i==2:
                card2=currSet[1]
            if i==3:
                card3=currSet[2]
            if i==4:
                card4=currSet[3]
    prob65 = sample(currSet, 2)
    
    if (card1 in prob65):
        card1_prob = 0.65
    else:
        card1_prob = 0.35
    if (card2 in prob65):
        card2_prob = 0.65 
    else: card2_prob = 0.35
    if (card3 in prob65):
        card3_prob = 0.65
    else: card3_prob = 0.35
    if (card4 in prob65):
        card4_prob = 0.65
    else: card4_prob = 0.35
    questionCnt = 0
    questionIdx = [2, 5, 7, 10, 12, 15, 17, 20, 22, 25]
    # Initilizing Game
    for t in range(1, trials+1):
        RTwarning = False
        mytimer = core.Clock()
        presented = sample(currSet, 2)
        unpresented_cards = []
        probs = []
        i = 0
        for card in currSet:
            if card not in presented:
                unpresented_cards.append(card)
            else: 
                if card == card1:
                    probs.append(card1_prob)
                elif card == card2:
                    probs.append(card2_prob)
                elif card == card3:
                    probs.append(card3_prob)
                elif card == card4:
                    probs.append(card4_prob)                                        
        stimL = visual.ImageStim(win, image=presented[0], pos=[-6, 0], size=(5,8))
        stimR = visual.ImageStim(win, image=presented[1], pos=[6, 0], size=(5,8))
        fixation.draw()
        win.update()
        core.wait(1)
        # Draw stims
        fixation.draw()
        stimL.draw()
        stimR.draw()
        win.update()
        event.clearEvents()
        mytimer.reset(0)
        while True:
            keys = psychopy.event.getKeys(keyList=["s", "k", "space"])
            #if (mytimer.getTime() > 6 and RTwarning == False):
            #    rt_warning = visual.ImageStim(win, image="RTWarning.jpg",  units='norm', size=[2,2], interpolate = True)
            #    rt_warning.draw()
            #    win.update()
            #    while True:
            #        events = pygame.event.poll()
            #        if (events.type == pygame.JOYBUTTONDOWN):
            #            if (events.button == 5):
            #                RTwarning = True
            #                break
            keys = psychopy.event.getKeys(keyList=["s", "k", "space"])
            if ("s" in keys):
                RT = str(mytimer.getTime())
                stimL.draw()
                fixation.draw()
                stim_id = (presented[0].split(".")[0])
                other_id = (presented[1].split(".")[0])
                prob1 = probs[1] # right prob
                prob2 = probs[0] #left prob
                curr_prob = prob2
                key = 1
                stimapr = "left"
                dataFile.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," 
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
                        stim_id,
                        other_id,
                        presented[0],
                        presented[1],
                        RT,
                        card1_prob,
                        card2_prob, 
                        card3_prob, 
                        card4_prob,
                    )
                )
                if (cond == "withDelay"):
                    # Rumble feedback
                    hourglass.draw()
                    win.update()
                    #core.wait(delayTime)
                    core.wait(delayTime)
                else: 
                    win.update()
                    core.wait(0.5)
                break
            elif ("k" in keys):
                RT = str(mytimer.getTime())
                stimR.draw()
                fixation.draw()
                stim_id = (presented[1].split(".")[0])
                other_id = (presented[0].split(".")[0])
                prob1 = probs[1] # right probability
                prob2 = probs[0] # left probability
                curr_prob = prob1
                key = 2
                stimapr = "right"
                dataFile.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," 
                    % (
                        subjectN,
                        blockType,
                        blockCnt,
                        cond,
                        t,
                        stim_id,
                        other_id,
                        presented[1],
                        presented[0],
                        prob1,
                        prob2,
                        prob1,
                        stimapr,
                        key,
                        stim_id,
                        other_id,
                        presented[1],
                        presented[0],
                        RT,
                        card1_prob,
                        card2_prob, 
                        card3_prob, 
                        card4_prob,
                    )
                )       
                if (cond == "withDelay"):
                    # Rumble feedback
                    hourglass.draw()
                    win.update()
                    #core.wait(delayTime)
                    core.wait(delayTime)
                else: 
                    win.update()
                    core.wait(0.5)
                break           
    
        ##########################################
        # outcome
        ##########################################
        if (random() < curr_prob):
            won.draw()
            dataFile.write("%i\n" % (1,))
        else:
            lost.draw()
            dataFile.write("%i,\n" % (0,))
        win.update()
        core.wait(0.75)
        if (t in questionIdx):
            questionCnt += 1
            #thougprobeQ.draw()
            #slider.draw()


main()


# keys = kb.getKeys(['right', 'left', 'quit'], waitRelease=True)
# if 'quit' in keys:
#    core.quit()