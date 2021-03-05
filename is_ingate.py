def point_in_poly(x,y,poly):
   inside = False
   # check if point is a vertex
   if (x,y) in poly: 
       
       inside = True

   # check if point is on a boundary
   if inside == False:
       for i in range(len(poly)):
          p1 = None
          p2 = None
          if i==0:
             p1 = poly[0]
             p2 = poly[1]
          else:
             p1 = poly[i-1]
             p2 = poly[i]
          if p1[1] == p2[1] and p1[1] == y and x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):
             
             inside = True

   n = len(poly)
   p1x,p1y = poly[0]
   if inside == False: 
       for i in range(n+1):
          p2x,p2y = poly[i % n]
          if y > min(p1y,p2y):
             if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                   if p1y != p2y:
                      xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                   if p1x == p2x or x <= xints:
                      inside = not inside
          p1x,p1y = p2x,p2y

   if inside: print ("IN")
   else: print ("OUT")
poly = [(10, 3), (2, 2), (9, 4), (8, 8), (6, 1), (10, 0), (6, 4)]
point_in_poly(6, 1, poly)
point_in_poly(5, 5, poly)
point_in_poly(7, 5, poly)
point_in_poly(9, 1, poly)
