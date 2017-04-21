import numpy as np
from random import uniform
from math import *
from PIL import Image

class NoiseText:

    def __init__(self, priori1, priori2, rng = 2000, text=  None):
        self.text = text
        if text != None : 
            print self.text
            self.text = Image.open(self.text)
            self.h = self.text.size[1]
            self.text = self.text.load()
        self.x = {} 
        self.y = {} 
        self.z = {}
        self.priori1 = priori1
        self.priori2 = priori2
        self.rng = rng
        self.perm = np.random.permutation(256)
        self.value = []
        for i in range(256):
            r = uniform(.0, 1.0)
            self.value.append(1.0 - 2.0 * r)

    def index(self,i,j,k):
        def perm(i):
            if i < 0 : i = 0
            if i > 255 : i = 255
            return self.perm[int(i)]
        return perm(i + perm(j + perm(k)))


    def trunc(self, point):
        rng = 255
        point = [int(i) for i in point]
        if point[0] > rng : point[0] = rng
        if point[1] > rng : point[1] = rng
        if point[2] > rng : point[2] = rng
        return point

            
    def generate(self, point):
        def lerp(f, p1, p2):
            return f * p1 + (1.0 - f) * p2
        point /= self.rng
        point *= 256
        point = self.trunc(point)
        x = floor(point[0])
        y = floor(point[1])
        z = floor(point[2])
        fx = point[0] - x
        fy = point[1] - y
        fz = point[2] - z
#        print x,y,z,fx,fy,fz
        d = []
        for i in range(2):
            for j in range(2):
                for k in range(2):
                   temp = self.value[self.index(x + i, y + j, z + k)]
#                   print temp
                   d.append(temp)
        x0 = lerp(fx, d[0], d[1])
        x1 = lerp(fx, d[2], d[3])
        x2 = lerp(fx, d[4], d[5])
        x3 = lerp(fx, d[6], d[7])
        y0 = lerp(fy, x0, x1)
        y1 = lerp(fy, x2, x3)
        z = lerp(fz, y0, y1)
        if self.text == None :
            return z
        z += 1.0
        temp = z / 2.0 * self.h
        temp = self.text[0,temp]
        ret = np.array([float(temp[0]) / 255, float(temp[1]) / 255, float(temp[2]) / 255])
        return ret
