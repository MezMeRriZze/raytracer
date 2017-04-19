import matplotlib.pyplot as pt
import random

from PIL import Image
from Sphere import Sphere
from Ray import Ray
from ViewPort import ViewPort
from Plane import Plane
from Triangle import Triangle
from operator import itemgetter
from PhongShading import PhongShading
from math import *
from Octree import Onode, Octree
from SoftShading import SoftShading
from math import *
import numpy as np 
from Instance import Instance 


class Reflect:

	def __init__(self, objarr):
		self.ins = objarr

	def ref(self, ray, dep, light):
		def normColor(temp):
			temp[0] = 1.0 if temp[0] > 1.0 else temp[0]
			temp[0] = 0 if temp[0] < 0 else temp[0]
			temp[1] = 1.0 if temp[1] > 1.0 else temp[1]
			temp[1] = 0 if temp[1] < 0 else temp[1]
			temp[2] = 1.0 if temp[2] > 1.0 else temp[2]
			temp[2] = 0 if temp[2] < 0 else temp[2]
			return temp
		def normalize(v):
			def magnitude(v):
				return sqrt(sum(v[i]*v[i] for i in range(len(v))))
			vmag = magnitude(v)
			return np.array([ v[i]/vmag  for i in range(len(v)) ])


		if dep > 3:
			return np.array([0,0,0])
		ls = []
		for item in self.ins:
			t = item.intersectRay(ray)
			if t != None:
				ls.append(t)

		if dep > 1 and ls != []:
			print ls
			
		try :
			temp = (min(ls, key = lambda t : t[0]))
		except :
			return np.array([0,0,0])
		if temp != None:
			temp1 = light.simpleRender(temp[1].ka, temp[1].kd, temp[1].ks, temp[4], temp[1].mat, temp[3], temp[2], ray.o)
#			temp1 = normColor(temp1)
			xp = temp[2]
			xp = np.array([xp[0], xp[1], xp[2]])
			w =  xp - ray.o
			w = -1.0 * w
			n = temp[1].getNormal(xp)
			r = -1.0 * w + 2 * np.dot(n, w) * n
			r = normalize(r)
			xp += r * 0.5
			ray1 = Ray(xp, r)
			temp2 = np.array([0,0,0])
			if temp[1].ref > 0.00000001:
				temp2 = self.ref(ray1, dep + 1, light)
#				temp2 = normColor(temp2)
#				print temp2
			if temp2[0] != 0: 
				print temp2

			temp1 = temp2 * temp[1].ref + temp1 * (1.0 - temp[1].ref)
#			print temp1
			temp1 = normColor(temp1)
			return temp1


