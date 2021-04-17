import numpy as np
import matplotlib.pyplot as plt

class Polymer:

    def __init__(self, size, init_pos, WorldMap, color = 'k'):
        self.size = size
        self.init_pos = init_pos
        self.body = [init_pos]
        self.weight = 1
        self.step = 0   
        self.color = color          
        self.WM = WorldMap
        self.WM[init_pos[0], init_pos[1]] = 1

    # Updates the coordinates in the given direction and returns the new coordinates
    def walk(self, direction):
        x_old = self.body[self.step][0]
        y_old = self.body[self.step][1]
        x_new = x_old
        y_new = y_old

        if(direction == 1):
            y_new += 1
        if(direction == 2):
            y_new -= 1
        if(direction == 3):
            x_new += 1
        if(direction == 4):
            x_new -= 1

        return [x_new, y_new]

    # Updates the polymer. It chooses a random direction and checks if the new spot is empty.
    def update(self):   

        directions = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])
        

        max_it = 0  # Max number of iterations, to stop the loop if the polymer gets stuck
        while(max_it < 10):
            m_i = 0
            for i in range(0, 4):
                if(self.is_empty(self.body[self.step] + directions[i])):
                    m_i += 1  

            i = np.random.randint(1, 5)         # Choose a random direction
            new_coords = self.walk(i)           # Walk in that direction

            if(self.is_empty(new_coords)):      # Check is that new spot is empty. If yes, then add the new position to body 
                self.body.append(new_coords)    # and update worldmap. If no, choose new direction and repeat. 
                self.WM[new_coords[0], new_coords[1]] = 1
                self.weight *= m_i
                self.step += 1
                break
            max_it += 1     
        pass

    # Generate polymer
    def generate(self):            
        for _ in range(self.size):
            self.update()

    # Get the end-to-end distance of the polymer
    def end_to_end_dist(self):
        self.body = np.array(self.body) 
        diff = np.array(self.body[-1] - self.body[0])
        return np.linalg.norm(diff)

    # Returns the length of the polymer
    def length(self):
        return len(self.body)

    # Plot polymer
    def plot(self):
        body = self.body
        x = [body[i][0] for i in range(len(body))]
        y = [body[i][1] for i in range(len(body))]
        plt.plot(x, y, color = self.color, marker = '.')

    # Checks if the coordinate is occupied on the worldmap
    def is_empty(self, coord):
        x = coord[0]
        y = coord[1]

        if(self.WM[x, y] == 0):
            return True
        if(self.WM[x, y] == 1):
            return False

