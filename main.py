import sys
import numpy as np
import matplotlib.pyplot as plt
from Polymer import Polymer
from Ensemble import Ensemble

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
    L = 20
    weights = np.zeros(N)
    r_sq = np.zeros(N)
    lengths = np.zeros(N)

    for i in range(N):
        box = np.zeros(shape=(3 * L, 3 * L))
        polymer = Polymer(L, [L, L], box)
        
        weights[i] = polymer.weight
        r_sq[i] = polymer.end_to_end_dist()**2       
        lengths[i] = polymer.length()

    avg_r_sq = sum(weights * r_sq) / sum(weights)
    print(weights, r_sq, lengths)
    print(sum([1 for i in weights if i == 0 ]))
    print(avg_r_sq)
    
# If you want to run this, run this in the terminal -> python main.py r_sq_vs_L

#Model to be fitted to the data:
from scipy.odr import *
def func(p, x):
    m, c = p
    return m*(x**(3/2)) + c
model = Model(func)
m,c,fit_error_m,fit_error_c=np.zeros(30),np.zeros(30),np.zeros(30),np.zeros(30)

colors=['red','blue','green']

if(sys.argv[1] == "r_sq_vs_L"):
    col=0
    for j in [1000,2000,3000]:
        print(j)
        N = j
        L = 50
        avg_r_sq= np.zeros(L)
        s=np.zeros(L)
        for l in range(L):
            weights = np.zeros(N)
            r_sq = np.zeros(N)
            for i in range(N):
                    box = np.zeros(shape=(3 * L, 3 * L))
                    polymer = Polymer(l, [L, L], box)
                    weights[i] = polymer.weight
                    r_sq[i] = polymer.end_to_end_dist()**2       
            avg_r_sq[l] = sum(weights * r_sq) / sum(weights)
            s[l] = ( ( N / (N - 1) ) * ( sum( ( (weights)**2 ) * (r_sq - avg_r_sq[l])**2 ) )/ ( sum(weights)**2) )**(1/2)
        #I have not yet found out how to plot the figure within the terminal.
        length=np.arange(0,L)
        plt.figure(1,figsize=(11,9))
        plt.errorbar(length, avg_r_sq, s, label = r'Simulated average $r^2$, N = %s' %(j),color=colors[col],alpha=0.5)
        
        #Validating the model (proportional to L^(3/2)):
        s[(np.where(s==0))]=0.00001
        data = RealData(length, avg_r_sq, sx=np.full(L,1/np.sqrt(L)), sy=s)
        odr = ODR(data, model, beta0=[0., 1.])
        out = odr.run()
        plt.plot(np.linspace(length[0], length[-1], 1000), func(out.beta, np.linspace(length[0], length[-1], 1000)),color=colors[col],label='fit$\propto L^{3/2}$ to data')  
        m[col],c[col],fit_error_m[col],fit_error_c[col]=out.beta[0],out.beta[1],out.sd_beta[0],out.sd_beta[1]
        col+=1
        
    plt.title('Radius of gyration vs polymer length, based on data from N polymers')
    plt.xlabel('L')
    plt.ylabel(r'Radius of gyration $\langle r^2(L) \rangle$')
    plt.legend()
    plt.show() 
    
    print('fit parameters for the modelled curves (in order of appearing in the legend), (for meaning of symbols look at the model):')    
    print('m=',m[np.where(m!=0)],'std_of_m=',fit_error_m[np.where(fit_error_m!=0)],'c=',c[np.where(c!=0)],'std_of_c=',fit_error_c[np.where(fit_error_c!=0)])