import numpy as np
from BoundBox import BoundBox

class Onode:
	#initialization for the tree node
    def __init__(self, x, y, z, length, height):
        self.center = np.array([x,y,z])
        self.length = length
        self.maxSize = 6
        self.height = height
        hl = length  /2
        print hl
        self.box = BoundBox(x + hl, x - hl, y + hl, y - hl, z + hl, z - hl)
        self.children = []
        self.shapes = []

	#this is simply for testing printing out the tree
    def printt(self):
        count = 0
        if len(self.children) == 0 :
            for item in self.shapes :
                count += 1
                print item
        else :
            for child in self.children :
                count += child.printt()
        return count


	#this is generating 8 children of the octree
    def createChildren(self):
        hl = self.length / 2
        ql = self.length / 4
        midx = self.center[0]
        midy = self.center[1]
        midz = self.center[2]
        h = self.height
        self.children.append(Onode(midx - ql, midy - ql, midz + ql, hl, h + 1))
        self.children.append(Onode(midx + ql, midy - ql, midz + ql, hl, h + 1))
        self.children.append(Onode(midx - ql, midy + ql, midz + ql, hl, h + 1))
        self.children.append(Onode(midx + ql, midy + ql, midz + ql, hl, h + 1))
        self.children.append(Onode(midx - ql, midy - ql, midz - ql, hl, h + 1))
        self.children.append(Onode(midx + ql, midy - ql, midz - ql, hl, h + 1))
        self.children.append(Onode(midx - ql, midy + ql, midz - ql, hl, h + 1))
        self.children.append(Onode(midx + ql, midy + ql, midz - ql, hl, h + 1))

	#add obj to the treenode
    def add(self, obj):
        if len(self.children) == 0:
            self.shapes.append(obj)

            if len(self.shapes) > self.maxSize and self.height < 6 :
                self.createChildren()
                for item in self.shapes :
                    for child in self.children :
                        if child.box.overlap(item.box):
                            child.add(item)
                self.shapes = []
        else :
            for child in self.children:
                if child.box.overlap(obj.box) :
                    child.add(obj)

    def getObj(self, ray):
        ret = []
        if not self.box.hitTime(ray):
            return ret
        if len(self.children) == 0 :
            for item in self.shapes :
                ret.append(item)
        else :
            for child in self.children :
                if child.box.hitTime(ray) :
                    ret += child.getObj(ray)
        return ret


#all calls to octree should go for class octree instead of ocnode
class Octree:

	#tree init
    def __init__(self):
        self.root = Onode(0.0,0.0,-10.0, 40.0,0)

	#insert obj to the tree. 
    def insert(self, obj):
        if self.root.box.overlap(obj.box) :
            self.root.add(obj)

	#this is returning all the hit objs for a particular ray.
    def get(self, ray):
        return self.root.getObj(ray)

