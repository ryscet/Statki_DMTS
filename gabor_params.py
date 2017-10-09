#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Gabors for variables related to psychopy
"""
from psychopy import visual, core,  monitors, gui, data, event #import some libraries from PsychoPy

import pygame 
from psychopy import prefs

import numpy as np
import pandas as pd
import random 
import os 
import math
import glob
from numpy import linspace
from scipy import pi,sin,cos

RunningExp = True
if RunningExp:
    # Initial window prompting for subject name
    expName = u'Exp start'  # from the Builder filename that created this script
    expInfo = {u'participant': u''}
    dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
    if dlg.OK == False: core.quit()  # user pressed cancel
    expInfo['date'] = data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName
    
    #Define the main application window
    mon = monitors.Monitor('dell', width= 54.61, distance=57)
    mon.setSizePix((1920, 1080))
    win = visual.Window( size=[1920,1080], fullscr = False, winType  ='pyglet', screen =0, waitBlanking = True, checkTiming = True, monitor = mon)
   # win = visual.Window([1920,1080],monitor="testMonitor", units="deg")
    #win.mouseVisible = False
    #event.Mouse(win = win).setVisible(False)

gabor_size = 11
fixation_cross_size = 0.02



class instructions_params(object):

    dir_path = os.path.dirname(os.path.realpath(__file__))


    def __init__(self):
        
        self.left_response = visual.TextStim(win, '', color='red', pos = (-0.5, 0.0))
        self.middle_response = visual.TextStim(win, 'don\'t know', color=[-0.5,-0.5,-0.5], pos = (0.0, 0.0))
        
        self.right_response = visual.TextStim(win,'', color='blue', pos = (0.5, 0.0))
     
        self.pause_screen = visual.TextStim(win,'Please take a break.\n\nPress any key to continue.', color='white', pos = (0.0, 0.0))
        
        
# multiply by height to width ratio to get perfect square - 1080/1920
        #self.fixation_1 = visual.Line(win=win, start=(-fixation_cross_size * 0.56, 0.0), end=(fixation_cross_size * 0.56, 0.0), **{'lineColor':'white', 'lineWidth' :5.0})
        #self.fixation_2 = visual.Line(win=win, start=(0.0, -fixation_cross_size), end=(0.0,fixation_cross_size), **{'lineColor':'white', 'lineWidth' :5.0})
        
        self.fixation_1 = visual.Circle(win = win, units = 'pix', radius = 10, **{'pos' : (0,0), 'fillColor': 'white'})
        self.fixation_2 = visual.Circle(win = win, units = 'pix', radius = 3, **{'pos' : (0,0), 'fillColor': 'black', 'lineColor' : 'black'})
        

        self.fixation_1.setAutoDraw(True)
        self.fixation_2.setAutoDraw(True)
        

    def randomize_response_instruction(self, condition):

        instruction_dict = {'match' : ['non-match', 'match'],
                            'non-match' : ['non-match', 'match'],
                            'control_horizontal' : ['vertical', 'horizontal'],
                            'control_vertical' : ['vertical', 'horizontal']}
        
        instructions = instruction_dict[condition]
        #coin toss
        if(np.random.choice([True, False])):
            instructions = list(reversed(instructions))


        self.left_response.text = instructions[0]
        self.right_response.text = instructions[1]

        return instructions



    def toggle_fixation(self):
        self.fixation_1.setAutoDraw(not self.fixation_1.autoDraw)
        self.fixation_2.setAutoDraw(not self.fixation_2.autoDraw)

    def set_fixation_color(self, color):
        self.fixation_1.setFillColor(color)
        self.fixation_1.setLineColor(color)



class trial_controller(object):
    # The gabor which appears first
    width = 0.025/2
    height = 0.040/2
    
    frame_draw = True
    
    frame_color = 'DarkGreen'
    
    left = visual.Rect(win = win, width = width, height = 1, 
                        **dict(units='norm',  fillColor=frame_color, fillColorSpace='rgb', lineColor= None,
                               pos=(-1, 0), size=2,  interpolate=False,
                               autoDraw=frame_draw))
    right = visual.Rect(win = win, width = width, height = 2, 
                        **dict(units='norm',  fillColor=frame_color, fillColorSpace='rgb', lineColor= None,
                               pos=(1, 0), size=2,  interpolate=False,
                               autoDraw=frame_draw))

    top = visual.Rect(win = win, width = 1, height = height, 
                        **dict(units='norm',  fillColor=frame_color, fillColorSpace='rgb', lineColor= None,
                               pos=(0, 1), size=2,  interpolate=False,
                               autoDraw=frame_draw))
    bottom = visual.Rect(win = win, width = 1, height = height, 
                        **dict(units='norm',  fillColor= frame_color, fillColorSpace='rgb', lineColor= None,
                               pos=(0, -1), size=2,  interpolate=False,
                               autoDraw=frame_draw))

    
    

    all_names = glob.glob('Statki/szkice_*')
    
    a_ship = glob.glob('Statki/*a.png')
    b_ship = glob.glob('Statki/*b.png')
    
    pair_dict = dict(zip(a_ship, b_ship))
    pair_dict.update(dict(zip(b_ship, a_ship)))
    
    def __init__(self, num_trials):
        
        self.trial_types = self.create_trial_types(num_trials)

    def prepare_trial(self):
        t_type = self.trial_types.pop()
        idx = np.random.randint(0, len(self.all_names))
        
        sample_ship_name = self.all_names[idx]
        
        self.sample_ship = visual.ImageStim(win=win, image= sample_ship_name)

        if 'match' in t_type:
            if t_type =='non-match': target_ship_name = self.pair_dict[sample_ship_name]
            if t_type =='match': target_ship_name = sample_ship_name
            self.target_ship = visual.ImageStim(win=win, image= target_ship_name)
            
        if 'control' in t_type:
            e = self.ellipse(t_type,0)
            self.target_ship = visual.ShapeStim(win=win, vertices = e.T, units = 'deg')
            target_ship_name = 'ellipse'

        trial_params= {'t_type' : t_type, 'sample_ship' : sample_ship_name, 'target_ship' : target_ship_name}

        return trial_params
    
    def toggle_frame(self,toggle):
        self.left.setAutoDraw(toggle)
        self.right.setAutoDraw(toggle)
        self.top.setAutoDraw(toggle)
        self.bottom.setAutoDraw(toggle)

    def set_frame_color(self, color):
        self.left.fillColor = color
        self.right.fillColor = color
        self.top.fillColor = color
        self.bottom.fillColor = color
    
    

    def ellipse(self, t_type, ang,Nb=50):
        '''
        ra - major axis length
        rb - minor axis length
        ang - angle
        x0,y0 - position of centre of ellipse
        Nb - No. of points that make an ellipse
        '''
        xpos,ypos=0,0
        if 'vertical' in t_type: 
            radm,radn=8,7
        if 'horizontal' in t_type:
            radm,radn=7,8
        
            
        
        co,si=cos(ang),sin(ang)
        the=linspace(0,2*pi,Nb)
        X=radm*cos(the)*co-si*radn*sin(the)+xpos
        Y=radm*cos(the)*si+co*radn*sin(the)+ypos
        arr =  np.stack((X,Y))
        return arr
        



    def create_trial_types(self, num_trials):
        # Define proportion of trials for each angle value
        num_diff= int(num_trials * 0.3) # Non match

        num_same = int(num_trials * 0.3) # Match
        
        num_control_horizontal = int(num_trials * 0.2) # Control
        num_control_vertical = int(num_trials * 0.2) # Control
        

        # Add the angle values in the amounts specified bu num trials proportions
        trial_list = ['match' for s in range(num_same)]
        trial_list.extend(['non-match' for d in range(num_diff)])
        trial_list.extend(['control_vertical' for c in range(num_control_vertical)])
        trial_list.extend(['control_horizontal' for c in range(num_control_horizontal)])
        # put the list in random order the list
        random.shuffle(trial_list)
        

        return list(trial_list)




