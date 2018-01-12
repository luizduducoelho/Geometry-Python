import numpy as np 
from sympy.geometry import *
from time import clock 

#p1, p2 = Point([0, 0]), Point([7, 7])
#p3, p4 = Point([5, 0]), Point([5, 5])

#segment1, segment2 =  Segment(p1, p2), Segment(p3,p4)
#print(segment1, segment2)

number_of_segments = 1000

#points = []
#for _ in range(2 * number_of_segments):
#	points.append(1000 * np.random.random_sample(2))
points = 1000 * np.random.random_sample([2*number_of_segments, 2])

segments = []
for i in range(number_of_segments):
	segments.append(Segment(points[2*i], points[2*i + 1]))

segments2 = segments
np.random.shuffle(segments2)
interceptions = []

inicial_time = clock()
for segment, segment2 in zip(segments, segments2):
	interceptions.append(intersection(segment, segment2))
final_time = clock()

time_spent = final_time - inicial_time
print("Time spent in calculating interceptions using sympy = {}".format(time_spent))