from math import tan, pi
import matplotlib.pyplot as plt 
verticeslist = [(1, 9), (1, 1), (7, 9), (7, 1)]
# point1 = (3, 4)
# point2 = (5,7)
# point3 = (9,1)
# point4 = (3,7)
# n_sides = 4
def is_ingate(point, vertices):
    result = False
    n = len(vertices)
    vertex = list(vertices[0])
    p1x = int(vertex[0])
    p1y = int(vertex[1])
    for a in range (n+1):
        vertex = list(vertices[a%n])
        p2x = int(vertex[0])
        p2y = int(vertex[1])
        if point[1] > min(p1y,p2y):
            if point[0] <= max(p1x,p2x):
                if p1y != p2y:
                    xinters = (point[1]-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                if p1x == p2x or point[0] <= xinters:
                    result = not result
        p1x,p1y = p2x,p2y
    print(result)
is_ingate((5,7), verticeslist)
is_ingate((5,6), verticeslist)
is_ingate((5,5), verticeslist)
is_ingate((4,3), verticeslist)
