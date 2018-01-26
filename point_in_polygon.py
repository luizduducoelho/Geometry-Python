import numpy as np
from poly_poly_intersect import gift_wrapper

def is_convex(P):
    
    n = len(P)
    m = len(gift_wrapper(P))
    
    return m == n 


def polygon_inside_points(P, Q):
    '''
    Check which vertices of P are inside Q and return them

    The function expect the points to be sequncialy in order
    If thats not the case, run gift_wrapper in the points before 
    calling this function
    '''
    points = []
    for point in P:
        if point_in_polygon(Q, point):
            points.append(point)
    return points


def point_in_polygon(P, a):
    '''
    Check if point a is inside polygon P
    Return True or False

    The function expect the points to be sequncialy in order
    If thats not the case, run gift_wrapper in the points before 
    calling this function
    '''
    
    # Assure that P is convex and its points are in counter-clockwise order 
    #P = gift_wrapper(P)
    
    n = len(P)
    for i in range(n):
        j = (i+1)%n
        if not left(P[i], P[j], a):
            return False
    
    return True
    

def left(a,b,c):
    '''
    Calculate cross product between vectors AB and AC
    If positive, c is to the left of line ab, return True
    '''
    V = b - a
    U = c - a
    area = np.cross(V, U)
    return area > 0

