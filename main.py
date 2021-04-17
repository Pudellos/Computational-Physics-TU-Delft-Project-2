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
    L = 5
    weights = np.zeros(N)
    r_sq = np.zeros(N)

    for i in range(N):
        WorldMap = np.zeros(shape=(3 * L, 3 * L))
        polymer = Polymer(L, [L, L], WorldMap)
        polymer.generate()    
        
        weights[i] = polymer.weight
        r_sq[i] = int(polymer.end_to_end_dist())**2       

    avg_r_sq = sum([weights[i] * r_sq[i] for i in range(N)]) / sum(weights)

    print(weights, r_sq)    
    print(avg_r_sq)