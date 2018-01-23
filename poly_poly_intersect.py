import numpy as np 
import sympy.geometry as sp
from time import clock

def gift_wrapper(np_points):
    '''
    Returns the convex hull for a set of points
    They are returned sorted in counter-clockwise order
    '''
    
    # Number of points
    n = len(np_points)
    
    # Find leftmost point 
    i0 = np.argmin(np_points, axis=0)[0]
    point_on_hull = np_points[i0]
    
    # Creating Hull and its iterator 
    i = i0
    H = []
    
    # Build the Hull until back to the first point 
    while True:
        
        # Adding point in the Hull 
        H.append(np_points[i])
        
        # k stores the point of smallest angle (ccw of all others), inicializing here 
        k = (i+1)%n
        
        # Loop on all the other points 
        for j in (x for x in range(n) if x != i):
            if is_ccw(np_points[i], np_points[j], np_points[k]):  # If there is a point j more cck than the current, change
                k = j 
        i = k
        
        if (i == i0):
            break
    
    return np.array(H)


def is_ccw(p1, p2, p3):  # Is CounterClockwise 
    # Checking if slope of p1p2 is less than slope of p2p3
    s1 = (p2[1] - p1[1]) * (p3[0] - p2[0])
    s2 = (p3[1] - p2[1]) * (p2[0] - p1[0]) 
    if s1 <= s2:
        return True
    else:
        return False 


def convex_intersect(P, Q):
    
    # Inicializing variables
    a, b = 0, 0              # Indices of P and Q respectivaly
    aa, ba, = 0, 0           # Advvances on a and b
    n, m = len(P), len(Q)    # Number of vertices of polygons
    inflag = 'Unknow'        # Which polygon is 'inside' 
    FirstPoint = True 
    i = 0 
    I = []  # The intersection polygon
    
    # Main loop
    while ((aa < n) or (ba < m)) and (aa < 2*n) and (ba < 2*m) :   #If both looped or one looped twice through polygon
        i += 1
        # a-1 and b-1, respectivaly 
        a1 = (a + n - 1) % n
        b1 = (b + m - 1) % m 
        
        # A and B are the subvectors that describe a1 to a (the edge of polygon)
        A = P[a] - P[a1]
        B = Q[b] - Q[b1]
      
        # Cheching cross products to predict advance
        origin = np.array([0, 0])
        cross = area_sign(origin, A, B)
        aHB = area_sign(Q[b1], Q[b], P[a])  # a is in the halfplane to the left of B
        bHA = area_sign(P[a1], P[a], Q[b])  # b is in the halfplane to the left of A
        #print("Cross", cross)
        
        # If A and B intersect, change the inflag 
        # code is the kind of intersection, p and q are the intersetion points, if exists
        code, p, q = segsegint(P[a1], P[a], Q[b1], Q[b])
        if code == 1 or code =='v':
            if inflag == 'Unknow' and FirstPoint:
                aa, ab = 0, 0 
                FirstPoint = False 
                p0 = p    # p0 is the first point
            inflag, I = inout(p, inflag, aHB, bHA, I)
        
        # ADVANCE RULES
        
        # Special case: A & B overlap and oppositely oriented
        if code == 'e' and np.dot(A, B) < 0:
            #raise SystemExit
            #print("Special case interception")
            I.append(p)
            if q.any() != None:
                I.append(q)
        
        # Special case: A & B parallel and separated
        if cross == 0 and aHB < 0 and bHA < 0:
            print("P and Q are disjoint, parallel edge")
            #raise SystemExit
            return []
        
        # Special case: A & B are collinear
        elif cross == 0 and aHB == 0 and bHA == 0:
            if inflag == 'Pin':
                b, ba = advance(b, ba, m, inflag=='Qin', Q[b])
            else:
                a, aa = advance(a, aa, n, inflag=='Pin', P[a])
        
        # Generic cases
        elif cross >= 0:
            if bHA > 0:
                a, aa = advance(a, aa, n, inflag=='Pin', P[a])
            else:
                b, ba = advance(b, ba, m, inflag=='Qin', Q[b])
        
        else:  # cross<0
            if aHB > 0:
                b, ba = advance(b, ba, m, inflag=='Qin', Q[b])
            else:
                a, aa = advance(a, aa, n, inflag=='Pin', P[a])
        
    if inflag == "Unknow":
        pass
        #print("The boundaries of P and Q do not cross")
    
    # If intersection is only one point, avoid duplicates
    return(np.unique(I, axis=0))


def segsegint(a1, a, b1, b):
    '''
     SegSegInt: Finds the point of intersection p between two closed
     segments ab and cd.  Returns p and a char with the following meaning:
       'e': The segments collinearly overlap, sharing a point.
       'v': An endpoint (vertex) of one segment is on the other segment,
            but 'e' doesn't hold.
       '1': The segments intersect properly (i.e., they share a point and
            neither 'v' nor 'e' holds).
       '0': The segments do not intersect (i.e., they share no points).
     Note that two collinear segments that share just one point, an endpoint
     of each, returns 'e' rather than 'v' as one might expect.  

     For math reference see https://stackoverflow.com/questions/563198/whats-the-most-efficent-way-to-calculate-where-two-line-segments-intersect
     segment1 = (p, p+r) =  p + t*r 
     segment2 = (q, q+s) =  q + u*s , parametric form

     Line intersects if there is t and u, so that 
     p + t*r = q + u*s
     Or, using cross product with pt2
     t*(r X s) = (q - p) X s
     '''
    
    code = '?'
    p = a1
    q = b1
    r = (a - a1)
    s = (b - b1)
    r_cross_s = np.cross(r, s) 
    
    if r_cross_s == 0:
        if np.cross(q-p, r) == 0:
            # Segments are colinear
            code = 'e'
            seg = return_overlapping(p, q, r, s)
            return code, seg[0], seg[1]
            
        else:
            # Segments are parallel and non-intersecting
            code = 0
            return code, None, None

    t = np.cross(q-p, s) / r_cross_s
    u = np.cross(q-p, r) / r_cross_s

    if (0 <= t <= 1) and (0 <= u <= 1):
        #Segments intersect in one point
        if t==0 or t==1 or u==0 or u==1:
            code = 'v'
        else:
            code = 1
        return code, p + t*r, None
    else:
        # Segments do not intersect 
        code = 0
        return code, None, None
    
def return_overlapping(p,q,r,s):
    
    t0 = np.dot(q-p,r)/np.dot(r,r)
    t1 = np.dot(q+s-p,r)/np.dot(r,r)
    seg = []
    
    if (np.dot(s,r) >= 0):
        
        if t1 < 0 or t0 > 1:
            return [None, None]
        elif t1 == 0:
            return (p, None)
        elif t0 == 1:
            return (p+r, None)
        if (0 < t0 < 1):
            seg.append(p+t0*r)
        elif t0 <= 0: 
            seg.append(p) 
        if (0 < t1 < 1):
            seg.append(p+t1*r)
        elif t1 >= 1: 
            seg.append(p+r)
            

    elif (np.dot(s,r) < 0):
        if t0 < 0 or t1 > 1:
            return [None, None]
        elif t0 == 0:
            return (p, None)
        elif t1 == 1:
            return (p+r, None)
        if (0 < t1 < 1):
            seg.append(p+t1*r)
        elif t1 <= 0: 
            seg.append(p) 
        if (0 < t0 < 1):
            seg.append(p+t0*r)        
        elif t0 >= 1:
            seg.append(p+r)
                    
    return seg


def inout(p, inflag, aHB, bHA, I):
    #Add point
    I.append(p)
    
    # Update inflag
    if aHB > 0:
        return 'Pin', I
    elif bHA > 0:
        return 'Qin', I
    else:     #Keep status quo
        return inflag, I

def advance(a, aa, n, inside, v):
    aa += 1
    return (a+1) % n, aa

def area_sign(o, a, b):
    '''
    Verify if the cross product of
    oa X ob is positive, negative or zero
    o stands of origin, a and b are vectors
    '''
    A = a - o 
    B = b - o 
    area = np.cross(A, B)
    
    if area > 0:
        return 1 
    elif area < 0:
        return -1
    else:
        return 0


def polygon_area(np_points):
    n = len(np_points)
    area = 0 
    origin = np_points[0]
    for i in range(n-1):
        if i == 0:
            continue 
        j = i + 1
        
        #Triangle vectors 
        A = np_points[i] - origin
        B = np_points[j] - origin 
        
        area += np.cross(A, B)/2
    
    return area