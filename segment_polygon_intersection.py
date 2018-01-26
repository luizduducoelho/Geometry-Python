import numpy as np
from line_segment_time import segment_intersection

def segment_polygon_intersection(P, seg):
    '''
    Return the intersection points between a segment and Polygon
    The output is a list of numpy arrays 
    '''
    n = len(P)
    points = []
    for i in range(n):
        j = (i+1)%n
        edge = np.array([P[i], P[j]])
        p = segment_intersection(edge, seg)
        if len(p)>0: # In the case collinear segments
            points.extend(p)
    if points:
        return list(np.unique(points, axis=0))
    else:
        return []