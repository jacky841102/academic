"""Follows Tkinter design pattern as using classes that are widgets rather than
creating high level object that would not be embeddable.

http://www.pythonware.com/library/tkinter/introduction/canvas.htm
http://effbot.org/tkinterbook/canvas.htm"""

from Tkinter import *

__author__ = "Calum J. Eadie"
__copyright__ = "Copyright (c) 2012, Calum J. Eadie"
__license__ = "MIT"

class Point:
    """Responsible for representing points on the whiteboard or canvas.
    """

    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def __str__(self):
        return "Point({0},{1})".format(self.x,self.y)
        
    def __add__(self,other):
        return Point(self.x+other.x,self.y+other.y)
        
    def __sub__(self,other):
        return Point(self.x-other.x,self.y-other.y)
        
    def __mul__(self,factor):
        # http://docs.python.org/reference/datamodel.html
        if isinstance(factor,int) or isinstance(factor,float):
            return Point(self.x*factor,self.y*factor)
        else:
            return NotImplemented
            
    __rmul__ = __mul__
            
    def __div__(self,factor):
        if isinstance(factor,int) or isinstance(factor,float):
            return Point(self.x/factor,self.y/factor)
        else:
            return NotImplemented
    
    @staticmethod
    def fromPoint(point):
        return Point(point.x,point.y)
        
    def get_int_point(self):
        return Point(int(self.x),int(self.y))

class Whiteboard(Canvas):
    """Provides a widget with basic drawing capabilities. Coordinate system has origin at bottom left.
    """

    def __init__(self,master,width,height,scaling):
    
        self.wwidth = width
        self.wheight = height
        self.scaling = scaling # relationship between whiteboard and canvas coordinate systems
        
        self.cwidth = width*scaling
        self.cheight = height*scaling
    
        Canvas.__init__(self,master,width=self.cwidth,height=self.cheight)
        
        self.pack(fill=BOTH,expand=YES)
        
    def printOutOfRangeErr(self,point0,point1):
        print "Out of range: {0} -> {1}".format(point0,point1)
        
    def getCPoint(self,point):
        """Get canvas point from whiteboard point.
        """
    
        wpoint = Point.fromPoint(point)
    
        outOfRange = False
        if wpoint.x < 0:
            outOfRange = True
            wpoint.x = 0
        elif wpoint.x >= self.wwidth:
            outOfRange = True
            wpoint.x = self.wwidth-1
            
        if wpoint.y < 0:
            outOfRange = True
            wpoint.y = 0
        elif wpoint.y >= self.wheight:
            outOfRange = True
            wpoint.y = self.wheight-1
            
        if outOfRange:
            self.printOutOfRangeErr(point,wpoint)
    
        cpoint = Point(wpoint.x*self.scaling,self.cheight-(wpoint.y*self.scaling))
        return cpoint
        
    def draw(self,wpoint,colour):
    
        cpoint = self.getCPoint(wpoint)
        self.create_rectangle(cpoint.x,cpoint.y,cpoint.x+self.scaling,cpoint.y-self.scaling,outline=colour,fill=colour)
        
    def clear(self):
    
        # Niave clear implementation. Canvas appears not to have one?
        self.create_rectangle(0,0,self.cwidth,self.cheight,outline="white",fill="white")
