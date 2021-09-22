from __future__ import division
from pygame import Rect
def calculateGradient(p1, p2):
   if (p1[0] != p2[0]):
       m = (p1[1] - p2[1]) / (p1[0] - p2[0])
       return m
   else:
       return None
def calculateYAxisIntersect(p, m):
   return  p[1] - (m * p[0])
def getIntersectPoint(p1, p2, p3, p4):
   m1 = calculateGradient(p1, p2)
   m2 = calculateGradient(p3, p4)
   if (m1 != m2):
       if (m1 is not None and m2 is not None):
           b1 = calculateYAxisIntersect(p1, m1)
           b2 = calculateYAxisIntersect(p3, m2)   
           x = (b2 - b1) / (m1 - m2)       
           y = (m1 * x) + b1           
       else:
           if (m1 is None):
               b2 = calculateYAxisIntersect(p3, m2)   
               x = p1[0]
               y = (m2 * x) + b2
           elif (m2 is None):
               b1 = calculateYAxisIntersect(p1, m1)
               x = p3[0]
               y = (m1 * x) + b1           
           else:
               assert False
       return ((x,y),)
   else:
       b1, b2 = None, None
       if m1 is not None:
           b1 = calculateYAxisIntersect(p1, m1)
       if m2 is not None:   
           b2 = calculateYAxisIntersect(p3, m2)
       if b1 == b2:
           return p1,p2,p3,p4
       else:
           return None
def calculateIntersectPoint(p1, p2, p3, p4):
    p = getIntersectPoint(p1, p2, p3, p4)
    if p is not None:               
        width = p2[0] - p1[0]
        height = p2[1] - p1[1]       
        r1 = Rect(p1, (width , height))
        r1.normalize()
        width = p4[0] - p3[0]
        height = p4[1] - p3[1]
        r2 = Rect(p3, (width, height))
        r2.normalize()  
        tolerance = 1
        if r1.width < tolerance:
            r1.width = tolerance   
        if r1.height < tolerance:
            r1.height = tolerance
        if r2.width < tolerance:
            r2.width = tolerance
        if r2.height < tolerance:
            r2.height = tolerance
        for point in p:                 
            try:    
                res1 = r1.collidepoint(point)
                res2 = r2.collidepoint(point)
                if res1 and res2:
                    point = [int(pp) for pp in point]                                
                    return point
            except:
                str = "point was invalid  ", point                
                print(str)
        return None            
    else:
        return None