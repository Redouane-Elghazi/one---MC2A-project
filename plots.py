#!/usr/bin/env python3


## Imports ## 

import math
import sys
import random as rd
import subprocess as sp
import os
import errno
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()



## Parameters ##

K = 20 # number of tests
N = 100
T = 1000

seed = '0' # seed for the tests
res_path = 'results/'

a_min = 0.5 # min for alpha,beta
a_max = 5 # max for alpha,beta





## Auxiliary functions ##

def call(filename,alpha,beta,mode,pace,delta):
    """generates the random walk with the given parameters"""
    M = int(alpha*N)
    arg = ( filename+" "+str(rd.randint(0,10000))+" "+mode+" "+str(N)+" "+str(M)+
           " "+str(T)+ " "+str(beta)+ " "+pace+" "+delta )
    sp.run("./poulpe "+arg, shell=True)
    
def avancement(_,K):
    """displays the state of the computations"""
    _=_+1
    print("\t\t\t\t|"+"#"*int(30*_/K)+" "*(30-int(30*_/K))+"|",_, "out of", K, "\t\t", end='\r')

def plot_avancement(_,K):
    """displays the state of the plotting"""
    _=_+1
    print(_, "out of", K, "\t\t\t\t\t\t\t\t", end='\r')
	
def set_seed(s=None):
    global seed
    """generates the random seed to be used in the following tests \n
    the seed can be chosen by passing it as the parameter"""
    if(s == None):
        rd.seed()
        s = rd.randint(0,sys.maxsize)
    rd.seed(s)
    s = str(s)
    try:
        os.makedirs(s)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    seed = str(s)
    print('seed set to '+seed+'\n')
    
def set_N(new_N):
    global N,T
    N = new_N
    print('N set to '+str(N))
    if T< N*math.log(N):
        T = N*math.log(N)
        print('T set to '+str(T))
    
def set_K(new_K):
    global K
    K = new_K
    print('K set to '+str(K))
	
	
def delete(directory):
    """deletes the directory given as an argument \n
    a directory name is the seed under which computations have been made"""
    for file in os.listdir(directory):
        os.remove(os.path.join(directory,file))
    os.rmdir(directory)
    
def quit(erase=True):
    """quits the python environment \n
    by defaults it deletes the data created \n
    use quit(False) to keep the data"""
    if erase:
        delete(seed)
    sys.exit(0)

    
    
    
## Initialization ##


sp.run("make", shell=True) # compile C++ files
set_seed() # initialize seed
print('To modify a parameter p1, use set_p1(#new_value)')


## Main functions ##

def ex1_create(alpha,beta,pace,delta):
    """generates K random walks with parameters alpha,beta \n
    at every instant t, the normalized energy is stored"""
    
    filename = seed+"/ex1_a"+str(alpha)+"_b"+str(beta)+".tmp"
    
    # generate the K random walks
    for _ in range(K):
        avancement(_,K)
        call(filename,alpha,beta,'all',pace,delta)
        
def ex1_get(alpha,beta,pace,delta):
    """returns the average energy vector"""
    
    filename = seed+"/ex1_a"+str(alpha)+"_b"+str(beta)+".tmp"
        
    # get the avg_energy vector
    avg_energy = [0]*T
    file = open(filename,'r')
    for _ in range(K):
        file.readline() # the first line contains T
        for t in range(T):
            e_t = float(file.readline().split()[0]) # e_t is the 1st value
            avg_energy[t] += e_t/K

    return avg_energy
    
def ex1_plot(pace="",delta=""):
    """plots a set of graphs \n
    on the first column, alpha is fixed \n
    on the second column, beta is ficex \n
    the graphs represent the evolution of the normalized energy \n
    """
    # safety
    pace = str(pace)
    delta = str(delta)
    
    # parameters
    a_range = [0.5,2,5] # different values of alpha,beta
    l = len(a_range)
    c = [ ['#FFA13D', '#7DD85F', '#8EBFFF'],
          ['#FF1C1C', '#0EA03C', '#0B6DDD'],
          ['#960019', '#155B00', '#0A0AA8']]
    X = [i for i in range(T)]
         
    fig,axes = plt.subplots(l,2, sharex=True, sharey=True, figsize=(10,15))
    
    plt.xlabel('Time')
    plt.ylabel('Energy')
    plt.ylim(0,0.6)
    
    # create the data
    for i in range(l):
        alpha = a_range[i]
        for j in range(l):
            plot_avancement(l*i+j,l*l)
            beta = a_range[j]
            ex1_create(alpha,beta,pace,delta)
    
    # get the data
    for i in range(l):
        alpha = a_range[i]
        for j in range(l):
            beta = a_range[j]
            Y = ex1_get(alpha,beta,pace,delta)
            axes[i,0].plot(X,Y,label='beta='+str(beta),color=c[i][j])
            axes[j,1].plot(X,Y,label='alpha='+str(alpha),color=c[i][j])
            
            if i==l-1:
                axes[j,1].set_title('Energy evolution for beta='+str(beta))
                axes[j,1].legend() 

        axes[i,0].set_title('Energy evolution for alpha='+str(alpha))
        axes[i,0].legend()       
        
    
    dest_file = res_path+'ex1_'+seed+'.png'
    fig.savefig(dest_file)
    print('\nEnergy evolution plots saved in '+dest_file)
    
        
def ex2_3_create(alpha,beta,pace,delta):
    """generates K random walks with parameters alpha,beta \n
    The final normalized energy and final overlap are stored"""
    
    filename = seed+"/ex2_a"+str(alpha)+"_b"+str(beta)+".tmp"
    
    # generate the K random walks
    for _ in range(K):
        avancement(_,K)
        call(filename,alpha,beta,'end',pace,delta)
     
        
def ex2_3_get(alpha,beta,pace,delta):
    """returns the average energy and average overlap"""  
    
    filename = seed+"/ex2_a"+str(alpha)+"_b"+str(beta)+".tmp"
    
    # get the avg_energy and avg_overlap
    avg_energy = 0
    avg_overlap = 0
    
    file = open(filename,'r')
    for _ in range(K):
        data = file.readline().split()
        e_T,q_T = float(data[0]),float(data[1])
        avg_energy += e_T/K
        avg_overlap += q_T/K
    
    return avg_energy, avg_overlap
    
    
def ex2_3_plot(res=0.5,pace="",delta=""):
    
    # safety
    pace = str(pace)
    delta = str(delta)
    
    # parameters
    a_range = np.arange(a_min,a_max+res,res)
    l = len(a_range)
    
    heatmap_energy = [[0 for _ in range(l)] for _ in range(l)]
    heatmap_overlap = [[0 for _ in range(l)] for _ in range(l)]
    
    # create the data
    for i in range(l):
        for j in range(l):
            plot_avancement(i*l+j, l*l)
            ex2_3_create(a_range[i], a_range[j],pace,delta)

    # get the data
    for i in range(l):
        for j in range(l):
            avg_energy,avg_overlap = ex2_3_get(a_range[i], a_range[j],pace,delta)
            heatmap_energy[j][i] = avg_energy
            heatmap_overlap[j][i] = avg_overlap
    
    # save the heatmaps
    fig = plt.figure()
    hm_energy = sns.heatmap(heatmap_energy, cmap="YlGnBu", vmin=0, vmax=0.3)
    hm_energy.set_title('Energy map depending on alpha,beta')
    hm_energy.set_xlabel('alpha')
    hm_energy.set_ylabel('beta')
    hm_energy.set_xticklabels(a_range[::-1])
    hm_energy.set_yticklabels(a_range[::-1]) 
    
    dest_file = res_path+'ex2_'+seed+'.png'
    fig.savefig(dest_file)
    print('\nEnergy heatmap saved in '+dest_file)
    
    fig = plt.figure()
    hm_overlap = sns.heatmap(heatmap_overlap, cmap="YlOrRd", vmin=-1, vmax=1)
    hm_overlap.set_title('Overlap map depending on alpha,beta')
    hm_overlap.set_xlabel('alpha')
    hm_overlap.set_ylabel('beta')
    hm_overlap.set_xticklabels(a_range[::-1])
    hm_overlap.set_yticklabels(a_range[::-1])
    
    dest_file = res_path+'ex3_'+seed+'.png'
    fig.savefig(dest_file)
    print('Overlap heatmap saved in '+dest_file)
    
def ex1(pace="",delta="",new_seed=0):
    if new_seed == 0:
        set_seed()
    else:
        set_seed(new_seed)
    
    ex1_plot(pace,delta)
    
def ex2_3(res=0.5,pace="",delta="",new_seed=0):
    if new_seed == 0:
        set_seed()
    else:
        set_seed(new_seed)
    
    ex2_3_plot(res,pace,delta)