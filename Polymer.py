import numpy as np
import matplotlib.pyplot as plt
import random, copy

class Polymer:

    def __init__(self, size, init_pos, WorldMap, color = 'k', ensemble = False, PERM = False):
        self.size = size
        self.init_pos = init_pos
        self.body = [init_pos]
        self.weight = 1
        self.step = 0   
        self.color = color          
        
        if(ensemble):
            self.WM = WorldMap # If you generate a ensemble, you want to use the same worldmap for every polymer
            self.WM[init_pos[0], init_pos[1]] = 1

        if(not ensemble and not PERM):
            self.WM = copy.deepcopy(WorldMap) # When using PERM, you want a different map for each polymer, therefore the deepcopy
            self.WM[init_pos[0], init_pos[1]] = 1
            self.generate()

    # Updates the polymer. It chooses a random direction and checks if the new spot is empty.
    def update(self):   

        current_coords = self.body[self.step]
        directions = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])
        possible_dirs = []  

        for direction in directions:
            if(self.is_empty(current_coords + direction)):
                possible_dirs.append(direction)
        
        m = len(possible_dirs)
        
        if(m != 0):
            new_coords = current_coords + random.choice(possible_dirs)
            self.body.append(list(new_coords))
            self.WM[new_coords[0], new_coords[1]] = 1
            self.weight *= m
            self.step += 1
        else:
            self.weight *= m
            pass

    # Generate polymer
    def generate(self):            
        for _ in range(self.size):
            self.update()

    # Get the end-to-end distance of the polymer
    def end_to_end_dist(self):
        self.body = np.array(self.body) 
        diff = np.array(self.body[-1] - self.body[0])
        self.body = list(self.body)
        return np.linalg.norm(diff)

    # Returns the length of the polymer
    def length(self):
        return len(self.body) - 1

    # Plot polymer
    def plot(self):
        body = self.body
        x = [body[i][0] for i in range(len(body))]
        y = [body[i][1] for i in range(len(body))]
        plt.plot(x, y, color = self.color, marker = '.')

    # Checks if the coordinate is occupied on the worldmap
    def is_empty(self, coord):
        x, y = coord[0], coord[1]

        if(self.WM[x, y] == 0):
            return True
        if(self.WM[x, y] == 1):
            return False