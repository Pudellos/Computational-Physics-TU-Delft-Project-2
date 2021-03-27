import numpy as np
import matplotlib.pyplot as plt
from Polymer import Polymer
from Ensemble import Ensemble

polymer_size = 1000     # Max length of polymer
num_polymer = 20        # Number of polymers
init_pos = [[450 + 5 * i, 500] for i in range(num_polymer)]

ensemble = Ensemble(num_polymer, polymer_size, init_pos)
ensemble.plot()

plt.axis('equal')
plt.show()