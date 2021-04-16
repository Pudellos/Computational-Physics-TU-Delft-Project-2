import numpy as np
import matplotlib.pyplot as plt
from Polymer import Polymer

# An ensemble of polymers, takes the number of polymers, their size and initial positions
class Ensemble(Polymer):

    polymers = []

    def __init__(self, num_polymers, size, init_pos):
        self.size = size
        self.init_pos = init_pos
        self.num_polymers = num_polymers
        self.lengths = []
 
        
        
        for i in range(num_polymers):
            self.polymers.append(Polymer(size, init_pos[i], np.random.uniform(0, 1, size= 3)))
            
            
        for polymer in self.polymers:
            polymer.generate()
            self.lengths.append(polymer.length)
            

    def plot(self):
        for polymer in self.polymers:
            polymer.plot()

