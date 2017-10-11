#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Experiment:
	Delayed-Match-To-Sample Experiment. 
	Pair of stimuli is presented and subjects decide if the two objects are the same or different.

    Method used for accurate time tracking in the experiment:
    classmethod datetime.now([tz])
        Return the current local date and time. If optional argument tz is None or not specified, this is like today(), 
        but, if possible, supplies more precision than can be gotten from going through a time.time() timestamp 
        (for example, this may be possible on platforms supplying the C gettimeofday() function). - think this is only for unix
    
"""

# This class has all the setup for the experiment. 
# Here we define stimuli, gui elements (like fixation point and instructions),configure trials and some more small stuff
# By importing this class we automatically open psychopy window
import gabor_params as params #helper class

#Regular imports
import pandas as pd
import numpy as np
from datetime import datetime
from collections import OrderedDict
import pickle 
import os 

#Psychopy imports
from psychopy import event, core
from psychopy import prefs


### Setup Parameters ###
refresh_rate = 60 # screen refresh rate in Hz. Compare it against check results returned by check.py

num_trials = 100 # First draft of staircase length, use fixed num of trials

# Stimulus timings (in seconds, ex: 1.5 means 1sec 500ms):
sample_presentation_time = 1.5  # First ship time
probe_time = 1.5                # Second ship and ellipsis time
ISI = 5.0                       # Delay time (aka Inter-Stimulus-Interval) empty screen between first and second ship/ellipsis.
ITI = 6.0                       # Inter-Trial-Interval, time from subject pressing response button untill beggining of a new trial. In the half of this time, before new trial a color frame appears.
response_wait = 1.0

### Time Calibration ###
#Calibration measures the real screen refresh rate and it's variabillity. It needs to be performed for a monitor once.
assert os.path.exists('CALIBRATION_RESULaTS.npy'), 'SCREEN CALIBRATION WAS NOT CONDUCTED. Run check.py'
refresh_rate = float(np.load('CALIBRATION_RESULTS.npy')) # check.py saves the screen refresh rate, here we read it.
# !!!! NOTE !!!! The precision of stimulus presentation timing will depend on refresh rate and it's variabillity. 
# The formula for calculating number of frames for stimulus presentation is: int(refresh_rate * seconds). This will be rounded down to the nearest frame.

### Conntroller Object ###

trial_controler = params.trial_controller(num_trials) # Main helper object responsible for trial sequencing, selecting angles mainly
#ADD ASSERTION TESTS TO TRIAL_CONTROLLER ships dict
gui = params.instructions_params() # gui elements like written instructions, fixation cross etc

dir_path = os.path.dirname(os.path.realpath(__file__))

#TODO ADD ASSERTION TO TIMINGS - assert timedelta == time in seconds +/- variabillity * 2 
#TODO rename scripts, remove stuff related to gabors


def main(t_control):
    """Main loop for presenting consecutive trials. 
       Each trial is made of a sequence of pseudo-randomly (shuffle) stimuli presented in the same order:
       
       1) Color frame informing about the condition (experimental or control) and a fixation point
       2) first object to be rememebered (experimental condition) or ignored  (control condition)
       3) Empty screen for the delay
       4) Second stimuli probing the memory (experimental condition) or perception (control condition)
       5) Response screen 
       6) Empty screen between trials.
    
    Each stimulus is presented in a loop of the same structure using psychopy library:
    for frame in range(number of frames):
        stimulus.draw()
        win.flip()
    """
    ### LOG VARIABLES ###
    saved_db = OrderedDict() # Log is a dictionary, key is trial number, value is a tuple with all parameters: (thisResp, response_time, diff_index, step_list[diff_index], angle, orientation)

    responses = np.zeros(1) # Array (will get extended) keeping track of all responses.    
    pd_log = pd.DataFrame() # pandas log for online analysis

    # Initialize timestamps
    START_TIME = pd.to_datetime(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    clock = core.MonotonicClock()
    
    for trial in range(num_trials):    

        #if trial = int(num_trials /2.0):
        if trial == 60:
            gui.pause_screen.draw()
            params.win.flip()
            event.waitKeys()

        
        trial_params = t_control.prepare_trial() # Generates angles from shuffled list
        
        t_type, sample_ship_name, target_ship_name = trial_params['t_type'], trial_params['sample_ship'], trial_params['target_ship']

        print('t_type: ' + t_type)
        # Selected in params.prepare_trial
        sample_ship = t_control.sample_ship
        target_ship = t_control.target_ship

        # COLOR FRAME for trial type, hold (DMTS) or drop (control)
        if('control' in t_type):
            #gui.set_fixation_color('Red') # Old function, not used
            t_control.set_frame_color('DarkGreen')

        else:
           # gui.set_fixation_color('Green')
            t_control.set_frame_color('DarkRed')


        
        #### ITI ####
        ITI_time = pd.to_datetime(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        ITI_time_psychopy = clock.getTime()
	
        print('start: ' + str(pd.to_datetime(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))))
        for frame in range(int(ITI * refresh_rate)):
            if(frame == int((ITI * refresh_rate )/ 2)): t_control.toggle_frame(True);print('middle: ' +str(pd.to_datetime(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))))
            params.win.flip()
        print('end: ' + str(pd.to_datetime(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))))

        #### SAMPLE ####
        target_appeared = pd.to_datetime(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        target_appeared_psychopy = clock.getTime()
        
        gui.toggle_fixation()
        for frame in range(int(sample_presentation_time * refresh_rate)):

            sample_ship.draw() # First cue,
                            
            params.win.flip()

    
        ### ISI ###
        
        ISI_time = pd.to_datetime(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        ISI_time_psychopy = clock.getTime()
        gui.toggle_fixation()
        for frame in range(int(ISI * refresh_rate)):
           # if frame == int(ISI * refresh_rate / 10.0) : t_control.toggle_frame(False) # Hide the frame informing about trial type

            params.win.flip() #Empty screen, only fixation cross
        

        #### TARGET ####
        
        probe_appeared = pd.to_datetime(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        probe_appeared_psychopy = clock.getTime()
        gui.toggle_fixation()

        for frame in range(int(probe_time * refresh_rate)):

            target_ship.draw() # Second gabor or in case of control, an ellipse3
            params.win.flip()

        gui.toggle_fixation()
        ### EMPTY ###

        for frame in range(int(response_wait * refresh_rate)):
            params.win.flip() # Draw an empty screen for short period after probe and then show the anwsers's instructions

        t_control.toggle_frame(False)

        ### RESPONSE ###
        #t_control.toggle_frame(False)

        #gui.set_fixation_color('white')

        instructions = gui.randomize_response_instruction(t_type)

        instruction_appeared_time = pd.to_datetime(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        instruction_appeared_time_psychopy = clock.getTime()
        gui.toggle_fixation() # Turn fix off
        
        thisResp = None
        while thisResp==None:
            gui.left_response.draw()
            gui.right_response.draw()
            gui.middle_response.draw()
            params.win.flip() # appear instruction

            allKeys=event.waitKeys()
            for thisKey in allKeys:
                    
                if thisKey== 'num_4' or thisKey== 'a' :
                    thisResp = 'left'
                    print('left instruction: ' + instructions[0])
                    correct = check_response(t_type, instructions[0])
                
                if thisKey == 'num_5' or thisKey== 's':
                    thisResp = 'middle'
                    correct = 'dont know'
                    print('response: dont know')

                        
                elif thisKey == 'num_6' or thisKey== 'd':
                    thisResp = 'right'
                    print('right instruction: ' +instructions[1])
                    correct = check_response(t_type, instructions[1])

        
                elif thisKey in ['escape']:
                    OnQuit(pd_log, saved_db)
                    event.clearEvents() #must clear other (eg mouse) events - they clog the buffer
                    params.win.close()
                    core.quit() #abort experiment        

        # Time of keypress
        key_time = pd.to_datetime(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        key_time_psychopy = clock.getTime()

        
        responses = np.append(responses, thisResp)
        
        
        saved_db[trial] = { 'trial_logged' : trial,
                            'sample_ship' : sample_ship_name, 
                            'target_ship' : target_ship_name,
                            'raw_key' : thisKey,
                            'response' : thisResp,
                            'accuracy' : correct,
                            'ITI_time' : ITI_time,
                            'ITI_time_psychopy' : ITI_time_psychopy,
                            'ISI_time' : ISI_time, 
                            'ISI_time_psychopy' : ISI_time_psychopy,
                            'instruction_time' : instruction_appeared_time,
                            'instruction_time_psychopy' : instruction_appeared_time_psychopy,
                            'order' : instructions[0] + '_' + instructions[1], 
                            'trial_type' : t_type,
                            'target_time' : target_appeared,
                            'target_time_psychopy' : target_appeared_psychopy,
                            'probe_time' : probe_appeared,
                            'probe_time_psychopy' : probe_appeared_psychopy,
                            'key_time' : key_time,
                            'key_time_psychopy' : key_time_psychopy,
                            'participant' : params.expInfo['participant'],
                            'start_time' : START_TIME,
                            'radm':trial_params['radm'], 
                            'radn':trial_params['radn'], 
                            'titlt' : trial_params['tilt']
                            }
    
                            
        
        pd_log = log_trial(pd_log, trial, **saved_db[trial])
        gui.toggle_fixation() # Turn fix on

        ### ITI 2###
 #       for frame in range(int( ITI_2 * refresh_rate)):
#            params.win.flip() 
#
    
    params.win.close()
    
    # Saves the logs   
    OnQuit(pd_log, saved_db)
    
    core.quit()
    
    
def log_trial(pd_log, trial, **kwargs):
    
    pd_log = pd_log.append(pd.DataFrame(kwargs, [trial]))
    
    return pd_log


def check_response(trial_type, response):

    response_dict = {'match' : {'match' : 'correct', 'non_match' : 'wrong'},
                     'non_match' : {'match' : 'wrong', 'non_match' : 'correct'},
                     'control_horizontal' : {'horizontal' : 'correct', 'vertical' : 'wrong'},
                     'control_vertical' : {'vertical' : 'correct', 'horizontal' : 'wrong'}
                    }

    response = response_dict[trial_type][response]
    print('response: ' + response + '\n')
    

    return response

def OnQuit(pd_log, saved_db):
    """Called at the end of script and saves logs to disk"""    
    print('Saving logs')

    file = open(dir_path +'\\exp_logs\\'+ params.expInfo['participant'] + '.csv', 'a')

    file.write('#Experiment Started\n')

    pd_log.to_csv(file, index_label = 'index_copy')

    file.write('#Experiment Ended:' + str(pd.to_datetime(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))))

    with open(dir_path + '\\exp_logs\\' + params.expInfo['participant'] + datetime.now().strftime('_%Y_%m_%d_') + 'log.pickle', 'wb') as handle:
        pickle.dump(saved_db, handle)
    print('logs saved')


    
if __name__ == '__main__':
    main(trial_controler)
