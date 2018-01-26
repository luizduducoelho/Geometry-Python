import numpy as np
from poly_poly_intersect import gift_wrapper, convex_intersect, polygon_area
from point_in_polygon import polygon_inside_points

def polygon_intersect_area(P, Q):
    '''
    Returns the area shared by two convex polygons
    '''
    
    # Test for convexity
    n = len(P)
    m = len(Q)
    P = gift_wrapper(P)
    Q = gift_wrapper(Q)
    assert n == len(P), "First polygon is not convex"
    assert m == len(Q), "Second polygon is not convex"
    
    # Find intersection points of polygons edges
    I = convex_intersect(P, Q)
    
    # Find points of P inside Q and vice-versa
    t = polygon_inside_points(P, Q)
    s = polygon_inside_points(Q, P)
    
    # Concatenate points 
    if len(t) > 0:
        I = np.concatenate([I, t], axis=0)
    if len(s) > 0:
        I = np.concatenate([I, s], axis=0)
    
    # If there are points, make their order sequential
    if len(I)>0:
        I = gift_wrapper(I)
        # Return area
        return polygon_area(I), I
    
    else:
        return []
    
    