import os.path
import matplotlib.pyplot as plt
import numpy as np

def ex1_get(alpha,beta):
    # Parameters
    K=250 # number of tests
    N=1000
    M=alpha*N
    T=10000
    
    # File name
    filename = "ex1_" + str(alpha) + "_" + str(beta) + ".tmp"
    
    # Have confirmation of overwriting
    if os.path.isfile(filename):
        if input("File already exists. Do you want to overwrite it? [y/N]").lower() != 'y':
            exit(1)
    
    # Remove file
    run('rm '+filename, shell=True)
    
    # Add the K tests data to the file
    for _ in range(K):
        # launch script (T=N(logN))
    
    # Get the vector avg_energy
    avg_energy = [0]*(T+1)
    
    file = open(filename,'r')
    for _ in range(K):
        file.readline() # the first line is T
        for t in range(T+1):
            e_t = float(file.readline().split()[0]) # e_t is the 1st value
            avg_energy[t] += e_t/K

    # Plot E(w(t))
    X=[i for i in range(T+1)]
    plot(X,avg_energy)
 
def ex1_plot(alpha,beta):
    # Parameters
    T=10000
    
    X = [i for i in range(T+1)]
    Y = ex1_get(alpha,beta)
    
    plt.plot(X,Y)
    plt.xlabel('time')
    plt.ylabel('energy')
    plt.title('Energy evolution, alpha=%f, beta=%f' % (alpha,beta))
    plt.show()
    
    
    
    
    
def ex2_get(alpha,beta):
    # Parameters
    K = 250 # number of tests
    N = 1000
    M = alpha*N
    T = 10000
    
    # File name
    filename = "ex2_" + str(alpha) + "_" + str(beta) + ".tmp"
    
    # Have confirmation of overwriting
    if os.path.isfile(filename):
        if input("File already exists. Do you want to overwrite it? [y/N]").lower() != 'y':
            exit(1)
    
    # Remove file
    run('rm '+filename, shell=True)
    
    # Add the K tests data to the file
    for _ in range(K):
        # launch script (T=N(logN))
    
    # Get the avg_energy
    avg_energy = 0
    
    file = open(filename,'r')
    for _ in range(K):
        e_T = float(file.readline().split()[0]) # e_T is the 1st value
        avg_energy += e_T/K

    return avg_energy
        
def ex2_plot(res=0.1):
    # Parameters
    a_min = 0.5
    a_max = 5
    a_range = np.arange(a_min,a_max+res,res)
    l = len(a_range)
    
    # Vectors for plot
    X = [0]*l**2
    Y = [0]*l**2
    C = [0]*l**2
    
    for i in range(l):
        for j in range(l):
            X[i*l+j] = a_range[i]
            Y[i*l+j] = a_range[j]
            C[i*l+j] = ex2_get( a_range[i], a_range[j])
    
    plt.scatter(X,Y,c=C,cmap='Blues',marker='o',s=100/res)
    plt.colorbar(orientation='horizontal')
    plt.xlabel('alpha')
    plt.ylabel('beta')
    plt.title('Energy map depending on alpha,beta')
    plt.show()
    
    
    
    
    
def ex3_get(alpha,beta):
    # Parameters
    K=250 # number of tests
    N=1000
    M=alpha*N
    T=10000
    
    # File name
    filename = "ex3_" + str(alpha) + "_" + str(beta) + ".tmp"
    
    # Have confirmation of overwriting
    if os.path.isfile(filename):
        if input("File already exists. Do you want to overwrite it? [y/N]").lower() != 'y':
            exit(1)
    
    # Remove file
    run('rm '+filename, shell=True)
    
    # Add the K tests data to the file
    for _ in range(K):
        # launch script (T=N(logN))
    
    # Get the avg_energy
    avg_q = 0
    
    file = open(filename,'r')
    for _ in range(K):
        q = float(file.readline().split()[1]) # q is the 2nd value
        avg_q += q/K

    return avg_energy
    
def ex3_plot(res=0.1):
    # Parameters
    a_min = 0.5
    a_max = 5
    a_range = np.arange(a_min,a_max+res,res)
    l = len(a_range)
    
    # Vectors for plot
    X = [0]*l**2
    Y = [0]*l**2
    C = [0]*l**2
    
    for i in range(l):
        for j in range(l):
            X[i*l+j] = a_range[i]
            Y[i*l+j] = a_range[j]
            C[i*l+j] = ex3_get( a_range[i], a_range[j])
    
    plt.scatter(X,Y,c=C,cmap='Greens',marker='o',s=100/res)
    plt.colorbar(orientation='horizontal')
    plt.xlabel('alpha')
    plt.ylabel('beta')
    plt.title('Overlap map depending on alpha,beta')
    plt.show()