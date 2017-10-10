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
    win = visual.Window( size=[1920,1080], fullscr = True, winType  ='pyglet', screen =0, waitBlanking = True, checkTiming = True, monitor = mon)
    #win = visual.Window( size=[720,480], fullscr = False, winType  ='pyglet', screen =0, waitBlanking = True, checkTiming = True, monitor = mon)
    win.mouseVisible = False
    event.Mouse(win = win).setVisible(False)

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

        instruction_dict = {'match' : ['non_match', 'match'],
                            'non_match' : ['non_match', 'match'],
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

    
    
    def __init__(self, num_trials):
        
        self.trial_types, self.ships_dict = self.create_trial_types(num_trials)

    def prepare_trial(self):
        t_type = self.trial_types.pop()
        ships = self.ships_dict[t_type].pop()
        
        sample_ship_name = ships[0]
        target_ship_name =ships[1]


        self.sample_ship = visual.ImageStim(win=win, image= sample_ship_name)

        radm, radn, tilt_angle = None, None, None

        if 'match' in t_type:
            self.target_ship = visual.ImageStim(win=win, image= target_ship_name)

        if 'control' in t_type:
            tilt_angle = np.random.uniform(-0.1,0.1)
            ellipse_vertices, radm, radn = self.ellipse(t_type,tilt_angle)
            self.target_ship = visual.ShapeStim(win=win, vertices = ellipse_vertices.T, units = 'deg')
            target_ship_name = 'ellipse'
        
        trial_params= {'t_type' : t_type, 'sample_ship' : sample_ship_name, 'target_ship' : target_ship_name, 'radm':radm, 'radn':radn, 'tilt' : tilt_angle}
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
    
    

    def ellipse(self, t_type, ang,Nb=300):
        '''
        ra - major axis length
        rb - minor axis length
        ang - angle
        x0,y0 - position of centre of ellipse
        Nb - No. of points that make an ellipse
        '''
        xpos,ypos=0,0
        if 'horizontal' in t_type: 
            radm,radn=8,7 + np.random.uniform(-0.8,0.8)
        if 'vertical' in t_type:
            radm,radn=7 + np.random.uniform(-0.8,0.8),8
        
            
        
        co,si=cos(ang),sin(ang)
        the=linspace(0,2*pi,Nb)
        X=radm*cos(the)*co-si*radn*sin(the)+xpos
        Y=radm*cos(the)*si+co*radn*sin(the)+ypos
        arr =  np.stack((X,Y))
        return arr, radm, radn
        



    def create_trial_types(self, num_trials):
        # Define number of trials for each condition
        num_match = int(num_trials * 0.25) # Same ships
        num_non_match= int(num_trials * 0.25) # Different ships

        num_control_horizontal = int(num_trials * 0.25) # Control ellipse horizontal
        num_control_vertical = int(num_trials * 0.25) # Control ellipse vertical
        

        # Add the angle values in the amounts specified bu num trials proportions
        trial_list = ['match' for s in range(num_match)]
        trial_list.extend(['non_match' for d in range(num_non_match)])
        trial_list.extend(['control_vertical' for c in range(num_control_vertical)])
        trial_list.extend(['control_horizontal' for c in range(num_control_horizontal)])
        # put the list in random order the list
        random.shuffle(trial_list)
        
        trial_types = {'match':num_match, 'non_match': num_non_match, 'control_vertical':num_control_vertical, 'control_horizontal':num_control_horizontal}
        ships_dict = {}
        for t_type, num_of_type in trial_types.items():
            ships_dict[t_type] = []
            ships_dict =  self.make_ships_list(t_type, num_of_type, ships_dict)


        return trial_list, ships_dict

    def make_ships_list(self, t_type, num_of_type, ships_dict):
        #TODO add assertions
        #TODO right now there will be the same ships in a and b lists, which results in half of ships being used. Try to condition ship b to be from a different pair.
        a_ship = glob.glob('Statki/*a.png')
        b_ship = glob.glob('Statki/*b.png')
        
            
        pair_dict = dict(zip(a_ship, b_ship))
        pair_dict.update(dict(zip(b_ship, a_ship)))
        
        
        for i in range(int(math.ceil(num_of_type / 2.0))):
            
            idx = np.random.randint(0, len(a_ship))
            
            if(t_type == 'non_match'):
                ships_dict[t_type].append((a_ship[idx],  pair_dict[a_ship[idx]]))     
                ships_dict[t_type].append((b_ship[idx],  pair_dict[b_ship[idx]]))
    
    
            if(t_type == 'match'):
                ships_dict[t_type].append((a_ship[idx],  a_ship[idx]))     
                ships_dict[t_type].append((b_ship[idx],  b_ship[idx]))
                
                
            if('control' in t_type):
                ships_dict[t_type].append((a_ship[idx],  None))     
                ships_dict[t_type].append((b_ship[idx],  None))
                
            del a_ship[idx]
            del b_ship[idx]
        
        random.shuffle(ships_dict[t_type])
        
        return ships_dict
            
        
        
        
        
        
        
        
        
        
        