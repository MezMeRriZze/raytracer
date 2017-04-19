import numpy as np
from numpy.linalg import norm   
from math import * 
from BoundBox import BoundBox
from PIL import Image 

class Triangle:

    kEpsilon = 0.0000001
        
    def normalize(self, v):
        def magnitude(v):
            return sqrt(sum(v[i]*v[i] for i in range(len(v))))
        vmag = magnitude(v)
        return np.array([ v[i]/vmag  for i in range(len(v)) ])

    def getPixel(self, point):
        def magnitude(v):
            return sqrt(sum(v[i]*v[i] for i in range(len(v))))
        return  self.truncate([int(np.dot((point - self.ori), self.hori) / magnitude(self.hori) / magnitude(self.hori)   * self.im_w),  int(np.dot((point - self.ori), self.verti) / magnitude(self.verti) / magnitude(self.verti)   * self.im_h) ])

    def truncate(self, pix):
        if pix[0] < 0 : pix[0] = 0 
        if pix[1] < 0 : pix[1] = 0  
        if pix[0] >= self.im_w : pix[0] = self.im_w - 1 
        if pix[1] >= self.im_h : pix[1] = self.im_h - 1 
        return pix

    def __init__(self, p1, p2, p3, color, ka, kd, ks, mat, ref, name, texture = None, noiseTexture = False, origin = 0, flip = False, hori = None, verti = None, norm = None, trans = None, transDeg = 0.0, glossy = None):
        self.trans = trans
        self.glossy = glossy
        self.transDeg = transDeg
        self.texture = texture
        self.im_w = 0
        self.im_h = 0
        if self.texture != None :
            self.texture = Image.open(self.texture)
            print self.texture.size
            self.im_w = self.texture.size[0]
            self.im_h = self.texture.size[1]
            self.texture = self.texture.load()
#            self.im_w = self.texture.
        self.noiseTexture = noiseTexture
        self.name = name
        self.p1 = p1
	self.ref= ref
        self.p2 = p2
        self.p3 = p3
        if origin == 0:
            self.ori = self.p1
            self.hori = self.p2 - self.p1
            self.verti = self.p3 - self.p1
        elif origin == 1:
            self.ori = self.p2
            self.hori = self.p3 - self.p2
            self.verti = self.p1 - self.p2
        else : 
            self.ori = self.p3
            self.hori = self.p1 - self.p3
            self.verti = self.p2 - self.p3
        if flip :
            temp = self.hori
            self.hori = self.verti
            self.verti = temp
        if hori != None : self.hori = hori
        if verti != None : self.verti = verti
        self.color = color
        self.mat = mat
        self.ka = ka
        self.kd = kd
        self.ks = ks
#        self.n = np.cross(p1 - p3, p1 - p2)
        self.n = np.cross(p3 - p1, p2 - p1)
        self.n = self.normalize(self.n)
        if norm != None : self.n  = norm
        maxx = max(p1[0], p2[0], p3[0])
        minx = min(p1[0], p2[0], p3[0])
        maxy = max(p1[1], p2[1], p3[1])
        miny = min(p1[1], p2[1], p3[1])
        maxz = max(p1[2], p2[2], p3[2])
        minz = min(p1[2], p2[2], p3[2])
#        print p1
#        print p2
#        print p3
        self.box = BoundBox(maxx, minx, maxy, miny, maxz, minz)
#        print maxx, minx, maxy, miny, maxz, minz
        
        
    def getColor(self, hitPoint):
        if self.texture == None :
            return self.color
        else : 
            temp = self.getPixel(hitPoint)
            ret = self.texture[temp[0], temp[1]]
            ret = np.array([float(ret[0]) / 255, float(ret[1]) / 255, float(ret[2]) / 255])
            return ret
            

    def intersectRay(self, ray):
    	def area(a,b,c):
	        return 0.5 * norm( np.cross(b - a, c - a) )
        def SameSide(p1,p2, a,b):
            cp1 = np.cross(b-a, p1-a)
            cp2 = np.cross(b-a, p2-a)
            if np.dot(cp1, cp2) >= 0 : return True
            else :return False

        def PointInTriangle(p, a,b,c):
            if SameSide(p,a, b,c) and SameSide(p,b, a,c) and SameSide(p,c, a,b) : return True
            else : return False
        temp = ray.d
        t = np.dot(temp, self.n)
        if t == 0 : return None
        temp = self.p1 - ray.o
        temp  =np.dot(temp,self.n)
        t = temp / t
        p = ray.o + t*ray.d
        if t <= 0 :
            return None
        if PointInTriangle(p, self.p1, self.p2, self.p3) :
            return t
        else  : return None
#        areaWhole = area(self.p1, self.p2, self.p3)
#        area1 = area(self.p1, self.p2, p)
#        area2 = area(self.p2, self.p3, p)
#        area3 = area(self.p3, self.p1, p)
#        b1 = area1 / areaWhole
#        b2 = area2 / areaWhole
#        b3 = area3 / areaWhole
#        if 0 <= b1 and b1 <= 1 and 0 <= b2 and b2 <= 1 and 0 <= b3 and b3 <= 1 :
#            print p
#            print b1, b2, b3
#            return t
#        else :
#			return None
#


    def getNormal(self,xp):
        return self.n

   
