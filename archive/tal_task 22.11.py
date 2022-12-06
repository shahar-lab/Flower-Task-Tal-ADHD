import psychopy
from psychopy import core, visual, gui, data
from psychopy.hardware import keyboard
import pygame, time, ctypes
import numpy as np
from numpy.random import random
from random import sample
import random
import pandas as pd

################################################################################################################
####set experiment configuration --------------

# number of trials and blocks
Ntrials          = 25
Nblocks          = 8

#timing in the trial
trial_timing =  {
  "ITI": [1], #fization at the start of the trial
  "RT_deadline": [6],
  "choice_feedback": [0.5],
  "outcome": [1]
}


#reward probabilities
arms_prob   =[0.35,0.45,0.55,0.65]

#delay included in the experiment
delay_array=[1,7]

#change to True/False to include section in the next run
instructionsPhase = False
quizPhase         = False
trainPhase        = False
gamePhase         = True
############################################################################################################





#### Make a text file to save data ---------------------------------------
expInfo  = {"subject": "0"}
dlg      = gui.DlgFromDict(expInfo, title="Tal's Delay ADHD RL Task")
fileName = "flowers_task_" + expInfo["subject"] + "_" + data.getDateStr()
dataFile = open(
    fileName + ".csv", "w"
)  # a simple text file with 'comma-separated-values'
dataFile.write("subject, block_type, block, delay_condition, trial, chosen, unchosen, offer_left_image, offer_right_image, exp_value_chosen, exp_value_unchosen, choice_location, choice_key, exp_value1, exp_value2, exp_value3, exp_value4, RT, reward, coins_per_block, coins_per_task,ITI_duration,rt_deadline,choice_feedback_duration,outcome_duration\n")
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


####set stimuli--------------
won        = visual.ImageStim(win, image="rw.png", pos=[0, 0], size=4)
lost       = visual.ImageStim(win, image="ur.png", pos=[0, 0], size=4)
fixation   = visual.TextStim(win, text="+", pos=[0, 0], color=(-1, -1, -1))
hourglass  = visual.ImageStim(win, image="hourglass.png", pos=[0,0], size=4)

#additional vars
coins_per_task  = 0 
coins_per_block = 0     
coordinates     =-9999


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


##### experiment -----------------------
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
        current_delay  = 1

        training_intro = visual.ImageStim(win, image="train1.png",  units='norm', size=[2,2], interpolate = True)
        training_intro.draw()
        win.update()
        while True:
            abort(win)
            events = pygame.event.poll()
            if (events.type == pygame.JOYBUTTONDOWN):
                #Event 4 -> Pressing down left button, Event 5 -> Pressing down right button
                if events.button == 4:


                    mainExperimentModes(dataFile, current_block, subjectN, win, current_delay, 5, 'practice', training_image_set,trial_timing)
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

            #set delay condition according to counterbalance and block. (This will give you an interleved desgin e.g., [1sec,7sec,1sec,...] or [7sec, 1sec, 7sec,...])
            if counterbalance==0:
                condition=current_block%2
            elif counterbalance==1:
                condition=1-current_block%2

            current_delay=delay_array[condition]
            

            #set stim images for current block
            currSet = picList[current_block]
                
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
                        mainExperimentModes(dataFile, current_block, subjectN, win, current_delay, Ntrials, 'test', currSet, trial_timing)
                        break

####end block feedback--------------
            #draw end block screen
            end.draw()
            coinsBox = visual.TextStim(win, text= str(coins_per_block), pos=[0,0], color=(0,0,0))
            coinsBox.draw()
            win.update()


            # wait for response to end block
            while True:
                abort(win)
                events = pygame.event.poll()
                if (events.type == pygame.JOYBUTTONDOWN):
                #Event 4 -> Pressing down left button, Event 5 -> Pressing down right button
                    if events.button == 4:
                        break
####end task feedback-----------------------
        blockend   = visual.ImageStim(win, image="outro.png",  units='norm', size=[2,2], interpolate = True)
        coinsBox   = visual.TextStim(win, text= str(coins_per_task), pos=[0,0], color=(0,0,0))
        blockend.draw()
        coinsBox.draw()

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

def mainExperimentModes(dataFile, current_block, subjectN, win, current_delay, trials, blockType, currSet,trial_timing):

 ####first trial initial vars ----------------
    
    #amount of rewards
    global coins_per_block    
    global coins_per_task

    coins_per_block = 0
    coins_per_task+=coins_per_block

       
    for t in range(1, trials+1):
        mytimer    = core.Clock()
        abort_trial= False
        #### STIMULI--------------

        #fixation
        fixation.draw()
        win.update()
        core.wait(trial_timing['ITI'][0])

        #target
        offer = sample(range(4),2)
        stimL = visual.ImageStim(win, image=currSet[offer[0]], pos=[-6, 0], size=(6,6))
        stimR = visual.ImageStim(win, image=currSet[offer[1]], pos=[6, 0], size=(6,6))
        fixation.draw()
        stimL.draw()
        stimR.draw()
        win.update()
        mytimer.reset(0)

        ####RESPONSE--------------

        while True:
            abort(win)
            
            #### RESPONSE TIMEOUT ----------------------------------------------------------------
            if (mytimer.getTime() > trial_timing['RT_deadline'][0] ):
                rt_warning = visual.TextStim(win, text= " רתוי רהמ ביגהל שי", pos=[0,0], color=(-1,-1,-1)) # יש להגיב מהר יותר
                rt_warning2 = visual.TextStim(win, text= "ךשמהל אוהשלכ שקמ לע ץוחלל שי", pos=[0,-10], color=(-1,-1,-1)) # יש ללחוץ על מקש כלשהוא להמשך
                rt_warning.draw()
                rt_warning2.draw()
                win.update()
                abort_trial=True
                while True:

                    events = pygame.event.poll()
                    if (events.type == pygame.JOYBUTTONDOWN):
                        # event 4 -> pressing down left button
                        if events.button == 4:
                            break
                break
            

            ##### COLLECT RESPONSE ------------------------------------------------------------------
            events = pygame.event.poll()

            if (events.type == pygame.JOYBUTTONDOWN):
                
                #sub pressed LEFT
                if events.button == 4:

                    RT = str(mytimer.getTime())

                    #choice feedback screen
                    stimL.draw()
 
                    #save vars
                    prob_chosen     = arms_prob[offer[0]] # left flower prob 
                    prob_unchosen   = arms_prob[offer[1]]  # right flower prob
                    chosen          = offer[0]
                    unchosen        = offer[1]
                    key             = 1
                    stimapr         = "left"               
                    
                    break

                elif events.button == 5:

                    RT = str(mytimer.getTime())

                    stimR.draw()
                    
                    #save vars
                    prob_chosen     = arms_prob[offer[1]] # right flower prob 
                    prob_unchosen   = arms_prob[offer[0]] # left flower prob
                    chosen          = offer[1]
                    unchosen        = offer[0]
                    key             = 2
                    stimapr         = "right"

                    break
                
        #choice feedback screen (choice was drawen above)
        fixation.draw()
        if abort_trial==False:
            win.update()
            core.wait(trial_timing['choice_feedback'][0])


        ##### DELAY  ------------------------------------------------------------------


        if abort_trial==False:
            # present hourglass
            hourglass.draw()
            win.update()
            core.wait(current_delay)
                               
    
        #### OUTCOME -------------------------------------
        if abort_trial==False:
            if (stimapr == "left"):
                stimL.draw()
            if (stimapr == "right"):
                stimR.draw()
            rand_prob = random.random()
            if ( rand_prob < prob_chosen):
                won.draw()
                coins_per_block+= 1
                coins_per_task += 1
                reward          = 1
            else:
                lost.draw()
                reward = 0

        if abort_trial==False:
            win.update()
            core.wait(trial_timing['outcome'][0])

        #Save data --------------------------------------------------------------------------------------
        if abort_trial==False:
        #save a line with choice-outcome data
            dataFile.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %f,%f,%f,%f,%f,%f\n" 
                            % (
                                subjectN,
                                blockType,
                                current_block+1,
                                current_delay,
                                t,
                                chosen+1,  
                                unchosen+1,
                                offer[0]+1,
                                offer[1]+1,
                                prob_chosen,
                                prob_unchosen,
                                stimapr, 
                                key,     
                                arms_prob[0],
                                arms_prob[1], 
                                arms_prob[2], 
                                arms_prob[3],
                                RT,
                                reward,
                                coins_per_block,
                                coins_per_task,
                                trial_timing['ITI'][0],
                                trial_timing['RT_deadline'][0],
                                trial_timing['choice_feedback'][0],
                                trial_timing['outcome'][0]
                            )
                        )
                        

        elif abort_trial==True:
            dataFile.write("%s, %s, %s, %s, %s\n" 
                        % (
                            subjectN,
                            blockType,
                            current_block+1,
                            current_delay,
                            t
                        )
                    )


main()

