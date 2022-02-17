# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 16:18:07 2022

@author: amasilva
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob


class DuneEvolution:
    def __init__(self, **kwargs):
        self.filename =[]
        self.parameter ='h'
        
        # real time or model time (total time)
        self.use_real_time = False
       
        for key, value in kwargs.items():
            setattr(self, key, value)  
        
        
        with open(self.filename) as f:
            lines = f.readlines()
            
            self.paramslines = lines
        
            for line in self.paramslines:
                if 'NX =' in line:
                    self.nx = float((line.split('=')[1]).split()[0])
                if 'NY =' in line:
                    self.ny =  float((line.split('=')[1]).split()[0])
                if 'dx =' in line:
                    self.dx = float((line.split('=')[1]).split()[0])
                if 'Nt =' in line:
                    self.nt = float((line.split('=')[1]).split()[0])
                if 'save.every' in line:
                    self.save_every = float((line.split('=')[1]).split()[0]) 
                if 'save.dir' in line and 'save_directory' not in kwargs:
                    self.save_directory = ((line.split('=')[1]).split()[0])
                if 'dt_max =' in line:
                    self.dt_max = float((line.split('=')[1]).split()[0])
                if 'constwind.u' in line:
                    self.constwind_u = float((line.split('=')[1]).split()[0])
                if 'wind.fraction' in line:
                    self.wind_fraction = float((line.split('=')[1]).split()[0])
                if 'veget.xmin' in line:
                    self.veget_xmin = float((line.split('=')[1]).split()[0])
                if 'veget.zmin' in line:
                    self.veget_zmin = float((line.split('=')[1]).split()[0])
                if 'veget.Hveg' in line:
                    self.veget_Hveg = float((line.split('=')[1]).split()[0])
                if 'beach.angle' in line:
                    self.beach_angle = float((line.split('=')[1]).split()[0])
                if 'shore.MHWL' in line:
                    self.shore_MHWL = float((line.split('=')[1]).split()[0])
                if 'shore.sealevel' in line:
                    self.shore_sealevel = float((line.split('=')[1]).split()[0])
                if 'plain.Height' in line:
                    self.plain_Height = float((line.split('=')[1]).split()[0])                    
                if 'beach.h' in line:
                    self.beach_h  = float((line.split('=')[1]).split()[0])                    
                if 'veget.plain.Height' in line:
                    self.veget_plain_Height  = float((line.split('=')[1]).split()[0])
   
        
        self.n = int(self.nt/self.save_every)
        self.read_time_results()
        self.read_variable_results()
        
    def list_parameters(self):
        files_params = os.listdir(self.save_directory +'\\')
        params =[]
        for param in files_params:
            params.append(param.split('.')[0]) 
        
        params_list = np.unique(np.array(params))
        
        self.params_list = params_list.tolist()
        return params_list.tolist()
          
    def read_variable_results(self, parameter = 'h'):
        if not self.parameter == parameter:
            self.parameter = parameter
        
        file_list = glob.glob(self.save_directory +'\\'  + self.parameter + '.*.dat')
        
        
        ny = int(self.ny)
        nx = int(self.nx)
        n_times_variable = int(self.nt/self.save_every)
        
        if not np.shape(file_list)[0] == n_times_variable:
            print('error')
        
        variable_array=np.zeros([n_times_variable, nx, ny+1])
        iterations_variable = np.zeros([n_times_variable])
        
        for i, each_file in enumerate(file_list):
            # iterations_variable.append(each_file.split('.')[-2]) 
            iteration = np.int(each_file.split('.')[-2])
            iterations_order = np.int( iteration/self.dt_max -1)
            iterations_variable[iterations_order] = iteration
            file_data = pd.read_csv(each_file, sep =' ', header = None)
            variable_array[iterations_order, :, :] = np.array([file_data])
             
        self.iterations_variable = iterations_variable
        self.total_time = self.iterations_to_totaltime(self.iterations_variable)[0]
        self.real_time = self.total_time/self.wind_fraction
        self.variable = variable_array[:,:, :-1] # delete last column nan
        self.iterations_order = np.arange(0,n_times_variable)
        
    def totaltime_to_iteration(self, time_vector):
        
        it = np.array(time_vector) * 365*24*3600/self.dt_max
        
        if self.dt_max <= 1000:
            iterations_variable = np.around(it/5, -2)*5
        else:
            iterations_variable = np.around(it, -3)
        iterations_order = iterations_variable /self.save_every -1 
        
        if iterations_order[0]<0:
            iterations_order[0]=0
            
        return iterations_variable, iterations_order.astype(int)
    
    
    def iterations_to_totaltime(self, iterations_vector):
            
        totaltime = iterations_vector * self.dt_max/(365*24*3600)
        iterations_order = iterations_vector/self.save_every -1 
                
        return totaltime, iterations_order.astype(int)
    
    def convert_to_real_time(self):
        self.use_real_time = True
        
    def convert_to_total_time(self):
        self.use_real_time = False
        
      
    def read_time_results(self):
        columns = ['iterations', 'real time in yr', 'maximum height', 'maximum cover', 'volume / mass of sand', 'distance traveled by the dune in X', 'dune in flux', 'dune out flux', 'surge above MHWL']
        table_data = pd.read_csv((self.save_directory + '\\time.dat'), sep=' ', names = columns, header = 8)
        self.time_results = table_data
          
    def plot_time_results(self):
        
        self.time_results.plot('real time in yr', ['distance traveled by the dune in X','dune in flux', 'dune out flux', 'surge above MHWL'])
        self.time_results.plot('real time in yr', ['maximum height', 'maximum cover'])
        self.time_results.plot('real time in yr', 'volume / mass of sand')
       
            
    def plot_space_time(self, step = 1, time_vector_yrs = False, parameter = 'h'):
        
        if not time_vector_yrs:
            time_vector_order = np.arange(0,self.n, step)
        else:
            time_vector_order = self.totaltime_to_iteration(time_vector_yrs)[1]
          
        if not self.parameter == parameter:
            self.parameter = parameter
            self.read_variable_results(parameter=parameter)
        
        fig, ax = plt.subplots()
        c = ax.pcolor(self.variable[time_vector_order,:,1], cmap='plasma')
        fig.legend([self.parameter])
        fig.colorbar(c, ax=ax)
        ax.set_xlabel('number of grid columns' )
        if self.use_real_time:
            ax.set_ylabel('real time in yr')
        else:
            ax.set_ylabel('total time in yr')
        yticks = ax.get_yticks().astype(int)   
       
        if not time_vector_yrs:
            iter_yticks = yticks * step * self.dt_max + self.save_every
            if self.use_real_time:
                time_vector_yrs_yticks = self.iterations_to_totaltime(iter_yticks)[0]/self.wind_fraction
            else:
                time_vector_yrs_yticks = self.iterations_to_totaltime(iter_yticks)[0]
        else:
            temp = np.array(time_vector_yrs)
            if self.use_real_time:
                time_vector_yrs_yticks = temp[yticks[:-1]]/self.wind_fraction
            else:
                time_vector_yrs_yticks = temp[yticks[:-1]]
        
        yticks_yrs = np.around(time_vector_yrs_yticks, 3)
        ax.set_yticklabels(yticks_yrs)
    
    def plot_variable_animation(self, step = 1, time_vector_yrs = False, parameter = 'h'):
        
        
        if not time_vector_yrs:
            time_vector_order = np.arange(0,self.n, step)
        else:
            time_vector_order = self.totaltime_to_iteration(time_vector_yrs)[1]
          
        if not self.parameter == parameter:
            self.parameter = parameter
            self.read_variable_results(parameter=parameter)
        
        plt.rcParams['figure.figsize'] = [4.5, 6]
        plt.rcParams['figure.autolayout'] = True
        
        fig, ax = plt.subplots()
        x = np.linspace(0,self.variable.shape[2], self.variable.shape[2]*2)
        t = np.linspace(0,time_vector_order.shape[0], time_vector_order.shape[0])
        y = np.linspace(0, self.variable.shape[1], self.variable.shape[1])
        X3, Y3, T3 = np.meshgrid(x, y, t)
         
        vmin = min(np.array(self.variable[:,:,1]).min(axis=1))
        vmax = max(np.array(self.variable[:,:,1]).max(axis=1))
        cmap = 'viridis_r' #'rainbow'
        
        nax = ax.pcolor(self.variable[time_vector_order[0],:,:], vmin=vmin, vmax=vmax, cmap = cmap)
        fig.colorbar(nax)
        ax.set_xlabel('number of grid lines' )
        ax.set_ylabel('number of grid columns')     
        
        
        for it, time in enumerate(time_vector_order):
            ax.pcolor(self.variable[time_vector_order[it],:,:], vmin = vmin, vmax = vmax, cmap = cmap)
            yrs_legend = np.around(self.total_time[(time_vector_order[it])], 3)
            if self.use_real_time:
                hand = fig.legend(['param = ' + self.parameter + '\n' + 'real time = ' + str(yrs_legend/self.wind_fraction) + ' yrs'],loc = 9 )
            else:
                hand = fig.legend(['param = ' + self.parameter + '\n' + 'total time = ' + str(yrs_legend) + ' yrs'],loc = 9 )
            
            plt.pause(0.00001)
            hand.remove()
            
      
       
    def plot_time_steps(self, step= 1, time_vector_yrs = False, parameter = 'h'):
               
        if not time_vector_yrs:
            time_vector_order = np.arange(0,self.n, step)
        else:
            time_vector_order = self.totaltime_to_iteration(time_vector_yrs)[1]
          
        if not self.parameter == parameter:
            self.parameter = parameter
            self.read_variable_results(parameter=parameter)
            
        plt.rcParams['figure.figsize'] = [8, 5]
        plt.rcParams['figure.autolayout'] = True
        fig, ax = plt.subplots()
        for it, time in enumerate(time_vector_order):
            perc = it/time_vector_order.shape[0]
            cor = (1-perc, 1-perc/2, perc) #Verde -azul
            # print(color)
            # color = ((perc/2), 1-(perc/2), perc) #Verde -azul
            # color = ((1-perc)/2, 1-perc/2, 1-perc) #Verdes
            # color = ((1-perc)/2, (perc)/2, 1-perc) #roxo - preto
            # color = ((1-perc), perc/2, perc) #vermelho - azul
            # color = ((1-perc/2), perc/2, perc) #vermelho - roxo
            # ax.plot(self.variable[time,:,1].T, color=((1-perc)/2, perc/2, 1-perc/4))
            # ax.plot(self.variable[time,:,1].T, color=((1-perc)/1, 1-(perc/2), 1-perc))
            ax.plot(self.variable[time,:,1].T, color = cor)
            # ax.plot(self.variable[time,:,1].T, color=((1-perc), 1-perc/2, 1-perc/2)) #verdes
            if self.use_real_time:
                ax.legend(np.around(self.total_time[time_vector_order]/self.wind_fraction, 2), loc = 'upper left', ncol=8, mode = 'expand')
                plt.title('real time (yrs)', size= 10)
            else:
                ax.legend(np.around(self.total_time[time_vector_order], 2), loc='upper left', ncol=8, mode='expand')
                plt.title('total time (yrs)', size = 10)
            # ax.legend(loc=l, bbox_to_anchor=(0.6,0.5))
            ax.set_xlabel('number of grid columns' )
            ax.set_ylabel('parameter = ' + self.parameter)
                       
            
            
           
        return
    