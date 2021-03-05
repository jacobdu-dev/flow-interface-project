from math import tan, pi
import matplotlib.pyplot as plt 
verticeslist = [(0,0), (2,7), (4,0), (2,4)]
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
is_ingate((1,3), verticeslist)
is_ingate((2,3), verticeslist)#no
is_ingate((4,2), verticeslist)#no
is_ingate((2,5), verticeslist)
