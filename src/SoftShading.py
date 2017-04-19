import numpy as np
from PhongShading import PhongShading
import random
from math import *


#this is for softshadowing 
class SoftShading:

	def __init__(self, p1 ,p2 ,p3 ,p4, c, l):
		self.p1 = p2
		self.p2 = p2
		self.p3 = p3
		self.p4 = p4
		self.p = (p1 + p2 + p3 + p4) / 4
		self.phong = PhongShading(self.p, c, l)

	def ambientRender(self, ka, ca):
		return self.phong.ambientRender(ka, ca)

	def multiRender(self, ka, ca, kd, cd, ks, alpha, normal, intersect, cam):
		return self.phong.multiRender(ka,ca, kd, cd, ks, alpha, normal, intersect, cam)

	def render(self, ka, ca, kd, cd, ks, alpha, normal, intersect, cam):
		return self.phong.render(ka,ca,kd,cd,ks,alpha, normal, intersect, cam)

	def simpleRender(self, ka, kd, ks, c, mat, normal, intersect, cam):
		return self.phong.simpleRender(ka,kd,ks,c,mat,normal, intersect, cam)

	def evenSimpler(self, k, c, mat, normal, intersect, cam):
		return self.phong.evenSimpler(k,c,mat,normal,intersect, cam)

# all other methods are the same as regular phong shading , while this one is to return a sampled array of points on the area light .
	def getSampleArr(self):
		ret = []
		p = 4
		for i in range(0, p):
			for j in range(0, p):
				temp = self.p1 + (self.p2 - self.p1) * random.uniform(0.0, 1.0) + (self.p3 - self.p1) * random.uniform(0.0, 1.0)
				ret.append(temp)
		return ret


