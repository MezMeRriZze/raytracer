"""
University of Illinois/NCSA Open Source License>
Copyright (c) 2016 University of Illinois
All rights reserved.
Developed by: 		Eric Shaffer
                  Department of Computer Science
                  University of Illinois at Urbana Champaign
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal with the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following
disclaimers.Redistributions in binary form must reproduce the above copyright notice, this list
of conditions and the following disclaimers in the documentation and/or other materials provided with the distribution.
Neither the names of <Name of Development Group, Name of Institution>, nor the names of its contributors may be
used to endorse or promote products derived from this Software without specific prior written permission.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS WITH THE SOFTWARE.
""" 


import numpy as np
import random
from math import *

class ViewPort:

    """ Simple viewport class center on z-axis """
    def __init__(self, e, l, up, d, mag, dim):
        def normalize(v):
            def magnitude(v):
                return sqrt(sum(v[i]*v[i] for i in range(len(v))))
            vmag = magnitude(v)
            print len(v)
            return np.array([ v[i]/vmag  for i in range(len(v)) ])

        self.e = e
        lookatV = l - e
        print l.shape
        print lookatV.shape
        self.l = normalize(lookatV)
        print self.l.shape
        center = e + self.l * d
        self.center = center
        self.up = normalize(up)
        self.mag = mag
        self.w = dim
        self.h = dim
        hori = np.cross(self.l, self.up)
        hori = normalize(hori)
        self.setCorners(center - float(mag) / 2 * self.up -  float(mag)/ 2 * hori, center -  float(mag) / 2 * self.up +  float(mag) / 2 * hori, center +  float(mag) / 2 * self.up -  float(mag) / 2 * hori, center +  float(mag) / 2 * self.up +  float(mag) / 2 * hori)
    #    def __init__(self, gamma = 1):
#        self.w=width
#        self.h=height
#        self.g = gamma
#        self.inv_g=1/gamma
#        self.setCorners(np.array([-1.0,-1.0,0.0]),np.array([1.0,1.0,0.0]))





#this is to set the corners for the viewport
    def setCorners(self,c1,c2,c3,c4):

        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4
        self.s=(self.c4[0]-self.c1[0])/self.w

#name switched my algorithm is doing the calculation by doing arithematic on vectors
    def getPixelCenter(self,r,c):
        #return np.array([self.s*(c - self.w/2.0 +0.5), self.s*(r - self.h/2.0 +0.5), self.minCorner[2]])
        return self.c1 + (self.c2 - self.c1) * (c + 0.5) / self.w + (self.c3 - self.c1) * (r + 0.5) / self.h


    #I got the name switched.....................
    def getMultiJitteredArray(self, r, c):
        ret = []
        p = 4
        for i in range(0, p):
            for j in range(0, p):
                temp = self.c1 + (self.c2 - self.c1) * (c + random.uniform(float(i) / p, (float(i+1)) / p)) / self.w + (self.c3 - self.c1) * (r + random.uniform(float(j) / p, (float(j + 1)) / p)) / self.h
                ret.append(temp)
        return ret

