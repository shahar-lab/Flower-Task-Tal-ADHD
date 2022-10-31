import psychopy
from psychopy import core, visual, gui, data
from psychopy.hardware import keyboard
import pygame, time, ctypes
import numpy as np
from numpy.random import random
from random import sample



#### Make a text file to save data ---------------------------------------
expInfo  = {"subject": "0"}
dlg      = gui.DlgFromDict(expInfo, title="Yael's Flowers Task")
fileName = "flowers_task_" + expInfo["subject"] + "_" + data.getDateStr()
dataFile = open(
    fileName + ".csv", "w"
)  # a simple text file with 'comma-separated-values'
dataFile.write("subject, block_type, block, thought probe, trial, chosen, unchosen, offer_right_image, offer_left_image, exp_value_right, exp_value_left, choice_location, choice_key, exp_value1, exp_value2, exp_value3, exp_value4, RT, reward, vas, RT_vas, coins_per_block, coins_per_task, ntrial_to_prob, count_to_prob\n")
subjectN = expInfo["subject"]




####initializing game -----------------------------------------
#xbox controller
pygame.init()
clock       = pygame.time.Clock()
keepPlaying = True
j           = pygame.joystick.Joystick(0)
j.init()

# create a window
win     = visual.Window( [1920, 1080], fullscr = True, monitor="testMonitor", units="deg", color=(1, 1, 1), useFBO=False)
win.mouseVisible = False
mytimer = core.Clock()




####set global var--------------

# number of trials in each block
Ntrials     = 10 
Nblocks     = 1

#reward probabilities
arms_prob   =[0.35,0.45,0.55,0.65]

#delay included in the experiment
delay_array=[1,7]

#change to True/False to include section in the next run
instructionsPhase = False
quizPhase         = False
trainPhase        = False
gamePhase         = True

#additional vars
coins_per_task  = 0 
coins_per_block = 0     
coordinates     =-9999


####set stimuli--------------

won        = visual.ImageStim(win, image="rw.png", pos=[0, 0], size=4)
lost       = visual.ImageStim(win, image="ur.png", pos=[0, 0], size=4)
fixation   = visual.TextStim(win, text="+", pos=[0, 0], color=(-1, -1, -1))
hourglass  = visual.ImageStim(win, image="hourglass.png", pos=[0,0], size=4)


#### set counterbalance and images ------------------------
counterbalance     = (int(subjectN))%2 # set whether 1sec or 7sec is the first delay

training_image_set = [ "practice_1.png", "practice_2.png", "practice_3.png", "practice_4.png" ]

picList = sample([ [ "1.png", "2.png", "3.png", "4.png" ],
                   [ "5.png", "6.png", "7.png", "8.png" ] ,
                   [ "9.png", "10.png", "11.png", "12.png" ] , 
                   [ "13.png", "14.png", "15.png", "16.png" ], 
                   [ "17.png", "18.png", "19.png", "20.png" ], 
                   ["21.png", "22.png", "23.png", "24.png" ], 
                   [ "25.png", "26.png", "27.png", "28.png" ], 
                   [ "29.png", "30.png", "31.png", "32.png"] ], Nblocks)

# number of trials and constant pictures
n = 25 # number of trials in each block
coins = 0 #global var



# experiment flow
def main():

    #these controll which section of the experiment are going to be displayed
    global instructionsPhase
    global quizPhase
    global trainPhase
    global gamePhase
    
#### Instructions -----------------------------
    if instructionsPhase:
        instructionsFunc()
        # Changing Phase to quiz Phase
        instructionsPhase = False
        quizPhase = True
        trainPhase = False
        gamePhase = False
    
#### Quiz -----------------------------
    if quizPhase:
        quizFunc()
        # Changing Phase to Training Phase
        instructionsPhase = False
        quizPhase = False
        trainPhase = True
        gamePhase = False

#### Training -----------------------------
    if trainPhase:
        current_block  = 0
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
                    mainExperimentModes(dataFile, current_block, subjectN, win, "1 second", 5, 'practice', training_image_set)
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


#### Test -----------------------------
    if gamePhase:
        outro = visual.ImageStim(win, image="outro.png",  units='norm', size=[2,2], interpolate = True)

        for current_block in range(Nblocks):
            condition=0
            
            current_delay=delay_array[condition]
            #set stim images for current block
            currSet = picList[current_block]
            delayCond = "7 seconds"
                
            #block instructions screen
            startBlock  = "startBlock" + str(current_block+1) + ".png"
            endBlock    = "endBlock" + str(current_block+1) + ".png"
            start       = visual.ImageStim(win, image=startBlock,  units='norm', size=[2,2], interpolate = True)
            end         = visual.ImageStim(win, image=endBlock,  units='norm', size=[2,2], interpolate = True)
            stim1       = visual.ImageStim(win, image=currSet[0], pos=[-9, -5], size=(4,4))
            stim2       = visual.ImageStim(win, image=currSet[1], pos=[-3, -5], size=(4,4))
            stim3       = visual.ImageStim(win, image=currSet[2], pos=[+3, -5], size=(4,4))
            stim4       = visual.ImageStim(win, image=currSet[3], pos=[+9, -5], size=(4,4))
            start.draw()
            stim1.draw()
            stim2.draw()
            stim3.draw()
            stim4.draw()

            win.update()
            while True:
                abort(win)
                events = pygame.event.poll()
                # Wait for response to begin block
                if (events.type == pygame.JOYBUTTONDOWN):
                #Event 4 -> Pressing down left button, Event 5 -> Pressing down right button
                    if events.button == 4:
                        mainExperimentModes(dataFile, current_block, subjectN, win, current_delay, n, 'test', currSet)
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

def mainExperimentModes(dataFile, current_block, subjectN, win, current_delay, trials, blockType, currSet):

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
                            current_block,
                            current_delay,
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
                    core.wait(current_delay)
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
                            current_block,
                            current_delay,
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
                    core.wait(current_delay)
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

