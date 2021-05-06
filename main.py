import sys, time, copy
import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import *
from Polymer import Polymer
from Ensemble import Ensemble

def calc_avg_r_sq(l, N, L):
    weights = np.zeros(N)
    r_sq = np.zeros(N)
    for i in range(N):
        box = np.zeros(shape=(3 * L, 3 * L))
        polymer = Polymer(l, [L, L], box)
        weights[i] = polymer.weight
        r_sq[i] = polymer.end_to_end_dist()**2       
    avg_r_sq = sum(weights * r_sq) / sum(weights)
    s = ( ( N / (N - 1) ) * ( sum( ( (weights)**2 ) * (r_sq - avg_r_sq)**2 ) )/ ( sum(weights)**2) )**(1/2)
    return avg_r_sq, s

# If you want to run this, run this in the terminal -> python main.py ensemble_example
if(sys.argv[1] == "ensemble_example"):
    worldsize = 5000
    WorldMap = np.zeros(shape=(worldsize, worldsize))

    polymer_size = 1000     # Max length of polymer
    num_polymer = 20        # Number of polymers
    init_pos = [[450 + 5 * i, 500] for i in range(num_polymer)]

    ensemble = Ensemble(num_polymer, polymer_size, init_pos, WorldMap)
    ensemble.plot()
    print('lengths that polymers reach:')
    # print(ensemble.colors) # unfortunatley colors aren't a name, but as RGB values for now. 
                        # But lengths printed correspond to a particular polymer, identified based on it's color.
    print(ensemble.lengths)

    plt.axis('equal')
    plt.show()

# If you want to run this, run this in the terminal -> python main.py r_sq_example
if(sys.argv[1] == "r_sq_example"):
    N = 100
    L = 1
    weights = np.zeros(N)
    r_sq = np.zeros(N)
    lengths = np.zeros(N)

    for i in range(N):
        box = np.zeros(shape=(3 * L, 3 * L))
        polymer = Polymer(L, [L, L], box)
        
        weights[i] = polymer.weight
        r_sq[i] = polymer.end_to_end_dist()**2       
        lengths[i] = polymer.length()
        print(weights[i], "\t", round(r_sq[i], 2), "\t", lengths[i])

    avg_r_sq = sum(weights * r_sq) / sum(weights)
    print(sum([1 for i in weights if i == 0 ]))
    print(avg_r_sq)

if(sys.argv[1] == "r_sq_vs_L"):

    #Model to be fitted to the data:
    func = lambda m, x : m * ( x**(3/2) )
    model = Model(func)
    m, fit_error_m = np.zeros(30), np.zeros(30)

    L = 20
    avg_r_sq = np.zeros(L)
    s = np.zeros(L)

    for i, N in enumerate([1000,2000,3000]):
        t1 = time.time()
        for l in range(L):
            avg_r_sq[l], s[l] = calc_avg_r_sq(l, N, L)
            print("Running... (N = %s, L = %s)" %(N, l), end='\r')

        # Plot the "measured" results
        colors = ['red','blue','green']
        length = np.arange(0,L)
        plt.figure(1, figsize=(11, 9))
        plt.errorbar(length, avg_r_sq, s, label = r'Simulated average $r^2$, N = %s' %(N), color=colors[i],alpha=0.5)
        
        # Validating the model (proportional to L^(3/2)):
        s[(np.where(s==0))]=0.00001
        data = RealData(length, avg_r_sq, sx = np.full(L, 1 / np.sqrt(L)), sy = s)
        odr = ODR(data, model, beta0 = [0.])
        out = odr.run()
        m[i], fit_error_m[i] = out.beta[0], out.sd_beta[0]

        length_ = np.linspace(length[0], length[-1], 1000)
        plt.plot(length_, func(m[i], length_), color = colors[i], label = 'fit$\propto L^{3/2}$ to data')  

        t2 = time.time()
        print("N = %s took %.2f seconds to run for L_max = %s." %(N, t2-t1, L) + 20 * " ", flush=True)
    
    print('Fit parameters for the modelled curves (in order of appearing in the legend), (for meaning of symbols look at the model):')    
    print('\tm = \t\t', m[np.where(m!=0)], '\n\tstd_of_m = \t', fit_error_m[np.where(fit_error_m!=0)])  

    plt.title('Radius of gyration vs polymer length, based on data from N polymers')
    plt.xlabel('L')
    plt.ylabel(r'Radius of gyration $\langle r^2(L) \rangle$')
    plt.legend()
    plt.show() 

if(sys.argv[1] == "test"):
    for i in range(10):
        print(i, end='\r')
        time.sleep(1)

if(sys.argv[1] == "PERM"):
    
    #Model to be fitted to the data:
    func = lambda m, x : m * ( x**(3/2) )
    model = Model(func)
    m, fit_error_m = np.zeros(30), np.zeros(30)

    # Constants
    Lmax = 50
    N = 1000
    cp = 10
    cm = 1

    s = np.zeros(Lmax)
    avg_r_sq = np.zeros(Lmax)

    # Initialize polymers
    box = np.zeros(shape=(3 * Lmax, 3 * Lmax))
    polymers = [Polymer(Lmax, [Lmax, Lmax], box, PERM= True) for _ in range(N)]
    dead = np.ones(len(polymers))
    
    # PERM Algorithm 
    for L in range(1, Lmax):

        # Grow all polymers by one step
        weights = np.zeros(len(polymers))
        r_sq = np.zeros(len(polymers))

        for i, polymer in enumerate(polymers):
            if(dead[i] == 1):
                polymer.update()
                weights[i] = polymer.weight
                r_sq[i] = polymer.end_to_end_dist()**2
                
            
        # Calculate average weight and W+, W-
        Wavg = np.mean(weights)
        Wp = cp * Wavg
        Wm = cm * Wavg

        for i, polymer in enumerate(polymers):
            # Pruning
            if(polymer.weight < Wm):
                rand = np.random.uniform(0, 1)
                if(rand < 0.5):
                    weights[i] = 0 # This polymer is not used calculation for <r^2(L)>
                    dead[i] = 0
                else:
                    polymer.weight *= 2 # Next weight
                    weights[i] *= 2 # Current weight
            # Enrichment
            if(polymer.weight > Wp):
                polymer.weight *= 0.5
                polymers.append(copy.deepcopy(polymer))

                weights[i] *= 0.5
                weights = np.append(weights, np.array(weights[i]) )
                r_sq = np.append(r_sq, np.array(r_sq[i]) )
                dead = np.append(dead,1)
        alive = len( dead [ dead == 1 ] )
        avg_r_sq[L] = sum(weights * r_sq) / sum(weights)        
        s[L] = ( ( alive / (alive - 1) ) * ( sum( ( (weights)**2 ) * (r_sq - avg_r_sq[L])**2 ) )/ ( sum(weights)**2) )**(1/2)


    length = np.arange(0, Lmax)
    plt.figure(1, figsize=(11, 9))
    plt.errorbar(length, avg_r_sq, s, label = r'Simulated average $r^2$')
    

    # Validating the model (proportional to L^(3/2)):
    s[(np.where(s==0))]=0.00001
    data = RealData(length, avg_r_sq, sx = np.full(Lmax, 1 / np.sqrt(Lmax)), sy = s)
    odr = ODR(data, model, beta0 = [0.])
    out = odr.run()
    m, fit_error_m = out.beta[0], out.sd_beta[0]

    length_ = np.linspace(length[0], length[-1], 1000)
    plt.plot(length_, func(m, length_), label = 'fit$\propto L^{3/2}$ to data')  
    plt.show()

        

      

     