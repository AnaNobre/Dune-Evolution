
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 16:54:16 2022

@author: amasilva
"""
import duneevolution as devo
import numpy as np
# import matplotlib.pyplot as plt


# =============================================================================
# Read the model results based on the information of the parameters file
# this includes the save_directory read frim the information in the *.par file
# include the save_directory path only if the path is not the same as in *.par file
# =============================================================================

# save_directory path to the folder where the resultsare saved (if not the same defined in the *.par file) 
save_directory = 'D:\\...\\Results_S1'
filename ='params_S1.par'

# Use real time (True) or modelation total time (False - default)
# if True the plots are labeled with real time instead of model total time (total time = real time * wind fraction )
use_real_time = False


# read model data and results into a dune evolution Object
RunS1 = devo.DuneEvolution(filename = filename, save_directory = save_directory, use_real_time=use_real_time)

#%%

# define the time vector (yrs) {time_vector_yrs} for results exploration (in total time reference)
# time vetor defined as start time in years {yrs_start}, a step {yrs_step} and end time {yrs_end} 
#                        OR 
# define iterations steps {step} , the default is iteration step = 1 (use all saved steps)



############   time steps  #### this is the default with step =1
step = 1
RunS1.plot_space_time(step = step, parameter = 'h')


############ with user defined time vector related to total time (model)
yrs_start = 0.5 # minimum is equal to #.total_time[0]
yrs_step = 0.04 
yrs_end = 3.1   # maximum value is the #.total_time[-1]
timevector = np.array(np.arange(yrs_start, yrs_end, yrs_step))
time_vector_yrs = timevector.tolist()

RunS1.plot_space_time(time_vector_yrs = time_vector_yrs, parameter = 'h')

#%% Parameters

# to check which where to modeled parameters (except time that is a combination of main results)
RunS1.list_parameters()


#%%            PLOTS 

# plot_time_results 
# plots the results in the file results (refers to real time)
# in this case no parameters is selected plots the mais results
RunS1.plot_time_results()


#%%
# plot_time_steps
# plot results for diferent sumulation step or time 
RunS1.plot_time_steps()

# examples with parameters and time vector user definition
# RunS1.plot_time_steps(step=4, parameter = 'dhdt')
# RunS1.plot_time_steps(time_vector_yrs = time_vector_yrs, parameter = 'dhdt')


#%%
# plot_space_time
# plot time space time results  
RunS1.plot_space_time()

# other examples
# RunS1.plot_space_time(step=4, parameter = 'dhdt')
# RunS1.plot_space_time(time_vector_yrs = time_vector_yrs, parameter = 'stall')


#%%
# plot_variable_animation
# plot evolution in time using an animated plot
RunS1.plot_variable_animation(step =1, parameter = 'h')

# other examples
# RunS1.plot_variable_animation(step =3, parameter = 'h')

#%% convert labets between real time and total time

# RunS1.convert_to_real_time()
# RunS1.convert_to_total_time()

