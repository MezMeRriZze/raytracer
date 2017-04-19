import numpy as np
from math import *

class PhongShading:

    pi = 3.1415926
	#this is simply normalizing a vector
    def normalize(self, v):
        def magnitude(v):
            return sqrt(sum(v[i]*v[i] for i in range(len(v))))
        vmag = magnitude(v)
        return np.array([ v[i]/vmag  for i in range(len(v)) ])

	#this shading class is for point light
    def __init__(self, p, c, l):
        self.point = p
        self.color = c
        self.factor = l

	#ambient light
    def ambientRender(self, ka, ca):
        return ka * ca * self.factor * self.color
    
	#this is for lights without ambient shading , since if we have multiple lights, we are not actually computing ambient light multiple times
    def multiRender(self, ka, ca, kd, cd, ks, alpha, normal, intersect,cam):
        view = self.normalize(intersect - cam)
        direction = self.normalize(intersect - self.point)
        temp  = 0
        temp += kd * cd * self.factor * self.color * np.dot(normal, direction) / pi
        temp += ks * pow(np.dot((2 * np.dot(direction, normal) * normal - direction), view), alpha) * self.factor * self.color * np.dot(normal, direction)
        return temp

	#this is full shading model
    def render(self, ka, ca, kd, cd, ks, alpha, normal, intersect, cam):
        temp = ka * ca * self.factor * self.color
        return temp + self.multiRender(ka,ca,kd,cd,ks,alpha, normal, intersect, cam)

	#this is assuming color of obj is same across three models 
    def simpleRender(self, ka, kd, ks, c, mat, normal, intersect, cam):
        return self.render(ka, c, kd, c, ks, mat, normal, intersect, cam)

	#also assuming same coefficient
    def evenSimpler(self, k, c, mat, normal, intersect, cam):
        return self.simpleRender(k,k,k,c,mat,normal, intersect, cam)

