#!/usr/bin/env python3

from math import *
from fractions import *
from sys import *
from random import *
import subprocess as sp
import os
import errno
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set()
sp.run("make", shell=True)

K = 20 # number of tests


def avancement(_,K):
	_=_+1
	print("\t\t\t\t|"+"#"*int(30*_/K)+" "*(30-int(30*_/K))+"|",_, "out of", K, "\t\t", end='\r')

def plot_avancement(_,K):
	_=_+1
	print(_, "out of", K, "\t\t\t\t\t\t\t\t", end='\r')

def ex1_get(alpha,beta,seed): #seed as string
	# Parameters
	N=100
	M=int(alpha*N)
	T=100000
	
	# File name
	filename = seed+"/ex1_" + str(alpha) + "_" + str(beta) + ".tmp"
	
	# Have confirmation of overwriting
	if os.path.isfile(filename):
		if input("File already exists. Do you want to overwrite it? [y/N]").lower() != 'y':
			exit(1)
		else:
			# Remove file
			sp.run('rm '+filename, shell=True)
	
	# Add the K tests data to the file
	for _ in range(K):
		avancement(_,K)
		arg = filename+" "+str(randint(0,10000))+" all "+str(N)+" "+str(M)+ " "+str(T)+ " "+str(beta)
		sp.run("./poulpe "+arg, shell=True)
	
	# Get the vector avg_energy
	avg_energy = [0]*(T+1)
	
	file = open(filename,'r')
	for _ in range(K):
		file.readline() # the first line is T
		for t in range(T+1):
			e_t = float(file.readline().split()[0]) # e_t is the 1st value
			avg_energy[t] += e_t/K
	return avg_energy
 
def ex1_plot(seed,alpha,beta):
	# Parameters
	T=100000
	
	X = [i for i in range(T+1)]
	Y = ex1_get(alpha,beta,seed)
	
	fig = plt.figure()
	plt.plot(X,Y)
	plt.xlabel('time')
	plt.ylabel('energy')
	plt.title('Energy evolution, alpha=%f, beta=%f' % (alpha,beta))
	fig.savefig('ex1-'+str(alpha)+'-'+str(beta)+'-'+seed+'.png')
	
	
	
	
	
def ex2_get(alpha,beta,seed): #seed as string
	# Parameters
	N = 100
	M = alpha*N
	T = 10000
	
	# File name
	filename = seed+"/ex2_" + str(alpha) + "_" + str(beta) + ".tmp"
	
	"""# Have confirmation of overwriting
	if os.path.isfile(filename):
		if input("File already exists. Do you want to overwrite it? [y/N]").lower() == 'y':
			# Remove file
			sp.run('rm '+filename, shell=True)
			
	# Add the K tests data to the file
	if not(os.path.isfile(filename)):
		for _ in range(K):
			avancement(_,K)
			arg = filename+" "+str(randint(0,10000))+" end "+str(N)+" "+str(M)+ " "+str(T)+ " "+str(beta)
			sp.run("./poulpe "+arg, shell=True)"""
	
	# Get the avg_energy
	avg_energy = 0
	
	file = open(filename,'r')
	for _ in range(K):
		e_T = float(file.readline().split()[0]) # e_T is the 1st value
		avg_energy += e_T/K

	return avg_energy
		
def ex2_plot(seed,res=0.1):
	# Parameters
	a_min = 0.1
	a_max = 10
	a_range = np.arange(a_min,a_max+res,res)
	l = len(a_range)
	
	# Heatmap
	heatmap_matrix = [[0 for _ in range(l)] for _ in range(l)]		 
	
	for i in range(l):
		for j in range(l):
			plot_avancement(i*l+j, l*l)
			heatmap_matrix[j][i] = ex2_get( a_range[i], a_range[j],seed)
	
	plt.figure()
	
	heatmap = sns.heatmap(heatmap_matrix, cmap="inferno", vmin=0, vmax=1)
	#heatmap.invert_yaxis()
	heatmap.set_title('Energy map depending on alpha,beta')
	heatmap.set_xlabel('alpha')
	heatmap.set_ylabel('beta')
	heatmap.set_xticklabels(a_range)
	heatmap.set_yticklabels(a_range)
	heatmap.figure.savefig('ex2-'+seed+'.png')
	
	
	
	
	
def ex3_get(alpha,beta,seed): #seed as string
	# Parameters
	N=100
	M=alpha*N
	T=10000
	
	# File name
	filename = seed+"/ex2_" + str(alpha) + "_" + str(beta) + ".tmp"
	
	"""# Have confirmation of overwriting
	if os.path.isfile(filename):
		if input("File already exists. Do you want to overwrite it? [y/N]").lower() != 'y':
			exit(1)
		else:
			# Remove file
			sp.run('rm '+filename, shell=True)
	
	# Add the K tests data to the file
	for _ in range(K):
		avancement(_,K)
		arg = filename+" "+str(randint(0,10000))+" end "+str(N)+" "+str(M)+" "+str(T)+" "+str(beta)
		sp.run("./poulpe "+arg, shell=True)
	"""
	
	# Get the avg_energy
	avg_q = 0
	
	file = open(filename,'r')
	for _ in range(K):
		q = float(file.readline().split()[1]) # q is the 2nd value
		avg_q += q/K

	return avg_q
	
def ex3_plot(seed,res=0.1):
	# Parameters
	a_min = 0.1
	a_max = 10
	a_range = np.arange(a_min,a_max+res,res)
	l = len(a_range)
	
	# Heatmap
	heatmap_matrix = [[0 for _ in range(l)] for _ in range(l)]		 
	
	for i in range(l):
		for j in range(l):
			plot_avancement(i*l+j, l*l)
			heatmap_matrix[j][i] = ex3_get( a_range[i], a_range[j],seed)
	
	plt.figure()
	
	heatmap = sns.heatmap(heatmap_matrix, cmap="bwr", vmin=-1, vmax=1)
	#heatmap.invert_yaxis()
	heatmap.set_title('Overlap map depending on alpha,beta')
	heatmap.set_xlabel('alpha')
	heatmap.set_ylabel('beta')
	heatmap.set_xticklabels(a_range)
	heatmap.set_yticklabels(a_range)
	heatmap.figure.savefig('ex3-'+seed+'.png') 
	
	
def setseed(s=None): 
	if(s == None):
		seed()
		s = randint(0,maxsize)
	seed(s)
	s = str(s)
	try:
		os.makedirs(s)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
	return str(s)
	
def delete(directory):
	for file in os.listdir(directory):
		os.remove(os.path.join(directory,file))
	os.rmdir(directory)

s = "2323132067031870085"#setseed()
#ex1_plot(s,1,1)
ex2_plot(s)
ex3_plot(s)