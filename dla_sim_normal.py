import numpy as np
import math, random

import matplotlib.pyplot as plt
from datetime import datetime


class DLA_Sim():

    def __init__(self, size, k=1, folder="./simulation_outputs/"):
        
        """
        initializes DLA_Sim object
        
        Input args:
            size: size of the square matrix
            k: stickiness
        """
        
        self.size = size
        self.k = k
        self.matrix = np.zeros((size, size), dtype = int)
        c = math.ceil(size/2) - 1
        self.matrix[c, c] = 1
        self.filename = folder

    def getSeed(self):
        
        '''
            Returns a randomly sampled initial position
            for a particle. 
            Returns (x, y) tuple
        '''
        
        p = int(np.random.rand() / 0.25)    # select edge
        
        possible = [(0, np.random.randint(self.size - 1)),               # Each edge has size - 1 points
                    (np.random.randint(self.size - 1), self.size - 1),   # Corners shouldn't get double prob
                    (self.size - 1, np.random.randint(1, self.size)), 
                    (np.random.randint(1, self.size), 0)]
        
        return possible[p]
    
    def getNeighbors(self, p):
        
        '''
            Returns Neighbors to Point p within image bounds
                            N|N|N
                            N|p|N
                            N|N|N
                 
            Input args:
                p : (x, y) tuple
            Returns:
                List of Neighboring points
        '''
        
        x, y = p
        neighbors = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                          (x, y - 1),                 (x, y + 1),
                          (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
        
        # Remove points outside the image
        neighbors = list(filter(lambda x : x[0] > -1 and x[0] < self.size and \
                                                x[1] > -1 and x[1] < self.size, neighbors))
        return neighbors
    
    
    def checkForStop(self, p):
        
        '''
            Check if point p stops provided if any neighboring cell is 1
            and point p is un-occupied i.e value of point p not equal to 1
     
            Input args:
                p : (x, y) tuple
            Returns True/False
        '''
        
        neighbors = self.getNeighbors(p)
        return any(map(lambda x : self.matrix[x] == 1, neighbors)) and np.random.rand() < self.k and  self.matrix[p] != 1
    
    
    def getNextPosition(self, p):
        
        '''
            Get next position. Brownian motion is order 1 markov process
            
            Input args:
                p : (x, y) tuple
            Returns:
                (x, y) coordinate of next position
        '''
        
        neighbors = self.getNeighbors(p)  
        s = np.random.randint(len(neighbors))
        next_point = neighbors[s]
        
        return next_point

        
    def addPoint(self, n=1):
        
        """
        add a new point following the brownian motion and the stickiness
        
        """

        self.filename = self.filename + str(self.k) + "_" + str(self.size) + "_" + str(n)
        
        count = 0
        t1 = datetime.now()
        totalt1 = t1
        while count < n:
            
            if (count + 1) % 1 == 0:
                print('added', count + 1, "time taken", (datetime.now()-t1).seconds)
                t1 = datetime.now()
            
            p = self.getSeed() # Get random initial position
            
            while not self.checkForStop(p):
                p = self.getNextPosition(p)
            self.matrix[p] = 1

            count += 1
            
        print("Total time taken", (datetime.now()-totalt1).seconds)
        
        print(sum(sum(self.matrix)))
        
        np.save(self.filename + ".npy", self.matrix)
        
        
    def plot(self):
        
        plt.figure(figsize=(7, 7))
        plt.imshow(self.matrix, cmap="gray")
        plt.imsave(self.filename + ".png", self.matrix)