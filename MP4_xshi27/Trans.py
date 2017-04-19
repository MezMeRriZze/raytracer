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

class Transparency:

    #tree should be an octree or equivalent
    def __init__(self, objarr, light, eye):
        self.tree = objarr
        self.light = light
        self.eye = eye

    #render the transmission
    def render(self, ray, depth, obj, hitPoint, inObj = False):
        def magnitude(v):
            return sqrt(sum(v[i]*v[i] for i in range(len(v))))
        def normalize(v):
            vmag = magnitude(v)
            return np.array([ v[i]/vmag  for i in range(len(v)) ])
        if obj == None or hitPoint == None :
            return np.array([0.0,0.0,0.0])
        if depth > 2:
            return obj.getColor(hitPoint)
        wi = -1.0 * ray.d
        n = obj.getNormal(hitPoint)
        costheta = np.dot(wi, n) / magnitude(wi) / magnitude(n)
        #total internal
        r = wi  + 2.0 * np.dot(n, ray.d) * n
        r = normalize(r * -1.0)
        rRay = Ray(hitPoint + 0.001 * r, r)
        objarr = self.tree.get(rRay)
        ls = []
        for item in objarr:
            t = item.intersectRay(rRay)
            if t != None:
                xp = ray.getPoint(t)
                ls.append((t, item, xp))
        try :
            (t, newObj, newHitPoint) = min(ls, key = lambda t : t[0])
        except:
            newObj = None
            newHitPoint = None
        if obj.trans == None:
            return (1.0 - obj.transDeg) * self.light.simpleRender(obj.ka, obj.kd, obj.ks, obj.getColor(hitPoint), obj.mat, obj.getNormal(hitPoint * -1.0), hitPoint, self.eye)
        if 1.0 - 1.0 / obj.trans / obj.trans * (1.0 - costheta ** 2.0) < 0:
            return (1.0 - obj.transDeg) * self.light.simpleRender(obj.ka, obj.kd, obj.ks, obj.getColor(hitPoint), obj.mat, obj.getNormal(hitPoint * -1.0), hitPoint, self.eye) + \
                    self.render(rRay, depth + 1, newObj, newHitPoint, inObj = inObj)
        if inObj:
            sintheta2 = obj.trans * sqrt(1.0 - costheta ** 2.0)
            t = obj.trans * ray.d + (costheta * obj.trans - sqrt(1.0 - sintheta2 ** 2.0)) * n
        else :
            sintheta2 = 1.0 / obj.trans * sqrt(1.0 - costheta ** 2.0)
            t = 1.0 / obj.trans * ray.d + (costheta * 1.0 / obj.trans - sqrt(1.0 - sintheta2 ** 2.0)) * n
        t = normalize(t)
        tRay = Ray(hitPoint + 0.001 * t, t)
        ls = []
        for item in objarr:
            time = item.intersectRay(tRay)
            if time != None:
                xp = ray.getPoint(time)
                ls.append((time, item, xp))
        try :
            (time, tObj, tHitPoint) = min(ls, key = lambda t : t[0])
        except:
            tObj = None
            tHitPoint = None
        return (1.0 - obj.transDeg) * 0.5 * self.light.simpleRender(obj.ka, obj.kd, obj.ks, obj.getColor(hitPoint), obj.mat, obj.getNormal(hitPoint * -1.0), hitPoint, self.eye) + \
                (1.0 - obj.transDeg) * 0.5 * self.render(rRay, depth + 1, newObj, newHitPoint, inObj = inObj) + \
                self.render(tRay, depth + 1, tObj, tHitPoint, inObj = not inObj)










