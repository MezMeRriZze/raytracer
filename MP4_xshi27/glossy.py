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
from random import uniform

class Glossy:

    #tree should be an octree or equivalent
    def __init__(self, objarr, light, eye, transp = None):
        self.transp = transp
        self.tree = objarr
        self.light = light
        self.eye = eye

    #return a sample of vectors
    def sample(self, obj, num = 10):
        def perpendicular_vector(v):
            if v[1] == 0 and v[2] == 0:
                if v[0] == 0:
                    return None
                else:
                    return np.cross(v, np.array([0, 1, 0]))
            return np.cross(v, [1, 0, 0])
        def magnitude(v):
            return sqrt(sum(v[i]*v[i] for i in range(len(v))))
        def normalize(v):
            vmag = magnitude(v)
            return np.array([ v[i]/vmag  for i in range(len(v)) ])
        temp = obj
        temp = normalize(temp)
        ran = perpendicular_vector(temp)
        ran = normalize(ran)
        thir = normalize(np.cross(ran, temp))
        ls = []
        for i in range(num):
            r1 = uniform(0.0, 0.1)
            r2 = uniform(0.0, 0.1)
            ls.append(normalize(temp + r1 * ran + r2 * thir))
        return ls
    

    #render an object with glossy reflection 
    def render(self, ray, depth, obj, hitPoint):
        def magnitude(v):
            return sqrt(sum(v[i]*v[i] for i in range(len(v))))
        def normalize(v):
            vmag = magnitude(v)
            return np.array([ v[i]/vmag  for i in range(len(v)) ])
        if obj == None or hitPoint == None :
            return np.array([0.0,0.0,0.0])
        if depth > 1:
            if obj.trans == None :
                return obj.getColor(hitPoint)
            else :
                return self.transp.render(ray, 1, obj, hitPoint) 
        wi = -1.0 * ray.d
        n = obj.getNormal(hitPoint)
        costheta = np.dot(wi, n) / magnitude(wi) / magnitude(n)
        #total internal
        glo = []
        r = wi  + 2.0 * np.dot(n, ray.d) * n
        r = normalize(r * -1.0)
        u = normalize(np.cross(np.array([0.0,1.0,0.0]), r))
        v = np.cross(u, r)

        gloPoints = self.sample(r)
        for item in gloPoints:
            rRay = r + item
            rRay /= 0.5
            if np.dot(n, rRay) < 0.0:
                rRay = -1.0 * rRay 
                rRay[2] = -1.0 * rRay[2]
            rRay = normalize(rRay)
            rRay = Ray(hitPoint + 0.001 * rRay, rRay)
            objarr = self.tree.get(rRay)
            ls = []
            for item1 in objarr:
                t = item1.intersectRay(rRay)
                if t != None:
                    xp = ray.getPoint(t)
                    ls.append((t, item1, xp))
            try :
                (t, newObj, newHitPoint) = min(ls, key = lambda t : t[0])
            except:
                newObj = None
                newHitPoint = None
            glo.append( (1.0 - obj.glossy) * self.light.simpleRender(obj.ka, obj.kd, obj.ks, obj.getColor(hitPoint), obj.mat, obj.getNormal(hitPoint * -1.0), hitPoint, self.eye) + \
                    self.render(rRay, depth + 1, newObj, newHitPoint))
        cum = np.array([0.0,0.0,0.0])
        for item in glo:
            cum += item
        cum /= len(glo)
        return cum
        

