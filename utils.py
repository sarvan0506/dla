import numpy as np
import pandas as pd
import math

import matplotlib.pyplot as plt


def get_middle_matrix(dla_matrix, center_dim=10):
    
    """
    returns a cropped matrix from center
    
    Input Args:
        dla_matix: dla simulation matrix
        center_dim: size of the center crop
    returns: np.array
    """
    
    if center_dim < 1:
        center_dim = math.floor(center_dim * len(dla_matrix))
        
    arr = np.arange(len(dla_matrix))
    mid = math.ceil(len(arr) / 2)
    
    
    start = mid - (math.floor(center_dim/2)) - 1
    end = mid + (math.floor(center_dim/2))

    return dla_matrix[start:end, start:end]


def center_density_mm(dla_matrix, center_dim=0.1): 
    
    """
    Calculates Center Density based on middle matrix method.
    Computes center density from the square crop from the center.
    
    Input_Args:
        dla_matix: dla simulation matrix
        center_dim: size of the center crop to compute density
    returns: np.array, np.array
    """
    
    center_matrix = get_middle_matrix(dla_matrix, center_dim)
    center_density = sum(sum(center_matrix)) / (len(center_matrix)*len(center_matrix))
    
    return center_density, center_matrix

    
def create_circular_mask(size, center=None, radius=0.1):
    
    """
    Create a circular mask that can be used to filter 2D arrays
    
    Input_Args:
        size: size of the dla matrix
        center: position of mask center
        radius: radius of the mask
    returns: np.array
    """

    if center is None: # use the middle of the image
        center = (int(size/2), int(size/2))
    if radius < 1: # ratio of the center mask of the image
        radius = math.floor(radius * size)

    Y, X = np.ogrid[:size, :size]
    
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return mask


def center_density_cc(dla_matrix, center_dim=30): 
    
    """
    Calculates Center Density based on middle matrix method.
    Computes center density from the square crop from the center.
    
    Input_Args:
        dla_matix: dla simulation matrix
        center_dim: size of the center crop to compute density
    returns: np.array, np.array
    """
    
    mask = create_circular_mask(len(dla_matrix), radius=center_dim).astype(int)
    center_circle = dla_matrix * mask
    
    center_density = sum(sum(center_circle)) / sum(sum(mask))
    
    return center_density, center_circle

        
def getNeighbors(point, size):
    
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

    x, y = point
    neighbors = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                 (x, y - 1),                 (x, y + 1),
                 (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]

    # Remove points outside the image
    neighbors = list(filter(lambda x : x[0] > -1 and x[0] < size and \
                                            x[1] > -1 and x[1] < size, neighbors))
    return neighbors


def getNeighborStrength(matrix, crop=0.5):
    
    """
    Calculates neighbor strength of a cropped area from a dla_matrix
    
    Input_Args:
        matrix: dla matrix
        crop: ratio of crop that should be considered for computation
    return: float
    """
    
    _, cropped = center_density_mm(matrix, crop)
    size = len(cropped)
    
    neighbor_strength = []
    
    for i in range(size):
        for j in range(size):
            neighbors = [cropped[i] for i in getNeighbors((i,j), size)]
            neighbor_strength.append(sum(neighbors))
    
    avg_neighbor_strength = sum(neighbor_strength) / len(neighbor_strength)
    
    return avg_neighbor_strength