def is_ingate(point, vertices):
   x = point[0]
   y = point[1]
   inside = False
   # check if point is a vertex
   if (x,y) in vertices: 
       inside = True
   # check if point is on a boundary
   if inside == False:
       for i in range(len(vertices)):
          p1 = None
          p2 = None
          if i==0:
             p1 = vertices[0]
             p2 = vertices[1]
          else:
             p1 = vertices[i-1]
             p2 = vertices[i]
          if p1[1] == p2[1] and p1[1] == y and x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):     
             inside = True
   n = len(vertices)
   p1x,p1y = vertices[0]
   # check if point is in polygon
   if inside == False: 
       for i in range(n+1):
          p2x,p2y = vertices[i % n]
          if y > min(p1y,p2y):
             if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                   if p1y != p2y:
                      xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                   if p1x == p2x or x <= xints:
                      inside = not inside
          p1x,p1y = p2x,p2y
   print(inside)
   #return inside
vertices = [(1,3), (-5, 3), (-5, -3), (1, -3)]
is_ingate((-3, 1), vertices)
is_ingate((0, -1), vertices)
is_ingate((7, 5), vertices)
is_ingate((-5, -5), vertices)



