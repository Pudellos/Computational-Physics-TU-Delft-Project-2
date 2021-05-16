import numpy as np
import matplotlib.pyplot as plt
from Polymer import Polymer

# An ensemble of polymers, takes the number of polymers, their size and initial positions
class Ensemble(Polymer):

    polymers = []

    def __init__(self, num_polymers, size, init_pos, WorldMap):
        self.size = size
        self.init_pos = init_pos
        self.num_polymers = num_polymers
        self.lengths = []
        self.colors = []
        self.WM = WorldMap
         
        # Create an instance of the polymers, each a random color and different position in the same map
        for i in range(num_polymers):
            self.polymers.append(Polymer(size, init_pos[i], self.WM, np.random.uniform(0, 1, size= 3), ensemble=True, PERM=False))
                      
        # Grow each polymer one step at a time
        for polymer in self.polymers:
            polymer.generate()
            l = polymer.length()
            self.lengths.append(l)
            self.colors.append(str(polymer.color))
       
    def plot(self):
        for polymer in self.polymers:
            polymer.plot()
