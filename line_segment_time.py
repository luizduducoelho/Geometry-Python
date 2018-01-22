import numpy as np 
from sympy.geometry import Segment, intersection
from time import clock 

def return_overlapping(p,q,r,s):
    
    t0 = np.dot(q-p,r)/np.dot(r,r)
    t1 = np.dot(q+s-p,r)/np.dot(r,r)
    seg = []
    
    if (np.dot(s,r) >= 0):
        
        if t1 < 0 or t0 > 1:
            #print("Here1")
            return []
        elif t1 == 0:
            #print("Here2")
            return p
        elif t0 == 1:
            #print("Here3")
            return p+r
        if (0 < t0 < 1):
            #print("Here4")
            seg.append(p+t0*r)
        elif t0 <= 0: 
            #print("Here5")
            seg.append(p) 
        if (0 < t1 < 1):
            #print("Here6")
            seg.append(p+t1*r)
        elif t1 >= 1: 
            #print("Here7")
            seg.append(p+r)
            

    elif (np.dot(s,r) < 0):
        if t0 < 0 or t1 > 1:
            #print("here1")
            return []
        elif t0 == 0:
            #print("here2")
            return p
        elif t1 == 1:
            #print("here3")
            return p+r
        if (0 < t1 < 1):
            #print("here4")
            seg.append(p+t1*r)
        elif t1 <= 0: 
            #print("here5")
            seg.append(p) 
        if (0 < t0 < 1):
            #print("here6")
            seg.append(p+t0*r)        
        elif t0 >= 1:
            #print("here7")
            seg.append(p+r)
                    
    return seg

def np_intersection(segment1, segment2):
    # For math reference see https://stackoverflow.com/questions/563198/whats-the-most-efficent-way-to-calculate-where-two-line-segments-intersect
    # segment1 = (p, p+r) =  p + t*r 
    # segment2 = (q, q+s) =  q + u*s , parametric form

    # Line intersects if there is t and u, so that 
    # p + t*r = q + u*s
    # Or, using cross product with pt2
    # t*(r X s) = (q - p) X s

    p = segment1[0]
    q = segment2[0]
    r = (segment1[1] - segment1[0])
    s = (segment2[1] - segment2[0])
    r_cross_s = np.cross(r, s)  

    if r_cross_s == 0:
        if np.cross(q-p, r) == 0:
            # Segments are colinear
            seg = return_overlapping(p, q, r, s)
            return seg
            
        else:
            # Segments are parallel and non-intersecting
            return []

    t = np.cross(q-p, s) / r_cross_s
    u = np.cross(q-p, r) / r_cross_s

    if (0 <= t <= 1) and (0 <= u <= 1):
        #Segments intersect in one point 
        return [p + t*r]
    else:
        # Segments do not intersect 
        return []

if __name__ == "__main__":

    number_of_segments = 1000
    points = 1000 * np.random.random_sample([2*number_of_segments, 2])
    points2 = 1000 * np.random.random_sample([2*number_of_segments, 2])

    segments = []
    segments2 = []
    for i in range(number_of_segments):
        segments.append(Segment(points[2*i], points[2*i + 1]))
        segments2.append(Segment(points2[2*i], points2[2*i + 1]))

    # Sympy
    interceptions = []
    inicial_time = clock()
    for segment1, segment2 in zip(segments, segments2):
       interceptions.append(intersection(segment1, segment2))
    final_time = clock()
    time_spent = final_time - inicial_time
    print("Time spent in calculating interceptions using sympy = {}".format(time_spent))


    # Numpy implementation
    np_interceptions = []
    inicial_time = clock()
    for i in range(1000):
        np_interceptions.append(np_intersection(np.stack((points[2*i], points[2*i+1])), np.stack((points2[2*1],points2[2*1+1] ))))
    final_time = clock()
    time_spent = final_time - inicial_time
    print("Time spent in calculating interceptions using numpy only = {}".format(time_spent))
