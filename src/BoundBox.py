import numpy as np
import sys

##this computes a boundbox and do intersections and hit tests
class BoundBox:

	#this is the initialization for bounndboxes.
    def __init__(self, maxx, minx, maxy, miny, maxz, minz):
        self.minX = minx
        self.maxX = maxx
        self.minY = miny
        self.maxY = maxy
        self.minZ = minz
        self.maxZ = maxz

	#return true for overlap boxes
    def overlap(self, box):
        if self.minX > box.maxX : return False
        if self.maxX < box.minX : return False
        if self.minY > box.maxY : return False
        if self.maxY < box.minY : return False
        if self.minZ > box.maxZ : return False
        if self.maxZ < box.minZ : return False
        return True

	#returns if a ray hits the box
    def hitTime(self, ray):
        tmin = -1.0
        tmax = float(sys.maxint)

        if ray.d[0] != 0.0 :
            tx1 = (self.minX - ray.o[0]) / ray.d[0]
            tx2 = (self.maxX - ray.o[0]) / ray.d[0]
            tmin = max(tmin, min(tx1, tx2))
            tmax = min(tmax, max(tx1, tx2))

        if ray.d[1] != 0.0 :
            ty1 = (self.minY - ray.o[1]) / ray.d[1]
            ty2 = (self.maxY - ray.o[1]) / ray.d[1]
            tmin = max(tmin, min(ty1, ty2))
            tmax = min(tmax, max(ty1, ty2))

        if ray.d[2] != 0.0 :
            tz1 = (self.minZ - ray.o[2]) / ray.d[2]
            tz2 = (self.maxZ - ray.o[2]) / ray.d[2]
            tmin = max(tmin, min(ty1, ty2))
            tmax = min(tmax, max(ty1, ty2))

        return tmax >= tmin

