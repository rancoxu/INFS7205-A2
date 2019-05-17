# quadtree.py
# Implements a Node and QuadTree class that can be used as 
# base classes for more sophisticated implementations.
# Malcolm Kesson Dec 19 2012
import os


class Node:
    ROOT = 0
    BRANCH = 1
    LEAF = 2
    minsize = 1  # Set by QuadTree

    # _______________________________________________________
    # In the case of a root node "parent" will be None. The
    # "rect" lists the min-x,min-y,max-x,max-y of the rectangle
    # represented by the node.
    def __init__(self, parent, rect):
        self.parent = parent
        self.children = [None, None, None, None]
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1
        self.rect = rect
        x0, z0, x1, z1 = rect
        if self.parent is None:
            self.type = Node.ROOT
        elif (x1 - x0) <= Node.minsize:
            self.type = Node.LEAF
        else:
            self.type = Node.BRANCH

    # _______________________________________________________
    # Recursively subdivides a rectangle. Division occurs
    # ONLY if the rectangle spans a "feature of interest".
    def subdivide(self):
        if self.type == Node.LEAF:
            return
        x0, z0, x1, z1 = self.rect
        h = (x1 - x0) / 2
        rects = list()
        rects.append((x0, z0, x0 + h, z0 + h))
        rects.append((x0, z0 + h, x0 + h, z1))
        rects.append((x0 + h, z0 + h, x1, z1))
        rects.append((x0 + h, z0, x1, z0 + h))
        for n in range(len(rects)):
            span = self.spans_feature(rects[n])
            if span:
                self.children[n] = self.getinstance(rects[n])
                self.children[n].subdivide()  # << recursion

    # _______________________________________________________
    # A utility proc that returns True if the coordinates of
    # a point are within the bounding box of the node.
    def contains(self, x, z):
        x0, z0, x1, z1 = self.rect
        if x >= x0 and x <= x1 and z >= z0 and z <= z1:
            return True
        return False

    # _______________________________________________________
    # Sub-classes must override these two methods.
    def getinstance(self, rect):
        return Node(self, rect)

    def spans_feature(self, rect):
        return False


# ===========================================================
class QuadTree():
    maxdepth = 3  # the "depth" of the tree
    leaves = []
    allnodes = []

    # _______________________________________________________
    def __init__(self, rootnode, minrect):
        Node.minsize = minrect
        rootnode.subdivide()  # constructs the network of nodes
        self.prune(rootnode)
        self.traverse(rootnode)

    # _______________________________________________________
    # Sets children of 'node' to None if they do not have any
    # LEAF nodes.
    def prune(self, node):
        if node.type == Node.LEAF:
            return 1
        leafcount = 0
        removals = []
        for child in node.children:
            if child is not None:
                leafcount += self.prune(child)
                if leafcount == 0:
                    removals.append(child)
        for item in removals:
            n = node.children.index(item)
            node.children[n] = None
        return leafcount

    # _______________________________________________________
    # Appends all nodes to a "generic" list, but only LEAF
    # nodes are appended to the list of leaves.
    def traverse(self, node):
        QuadTree.allnodes.append(node)
        if node.type == Node.LEAF:
            QuadTree.leaves.append(node)
            if node.depth > QuadTree.maxdepth:
                QuadTree.maxdepth = node.depth
        for child in node.children:
            if child is not None:
                self.traverse(child)  # << recursion


# _______________________________________________________
# Returns a string containing the rib statement for a
# four sided polygon positioned at height "y".
def RiPolygon(rect, y):
    x0, z0, x1, z1 = rect
    verts = list()
    verts.append(' %1.3f %1.3f %1.3f' % (x0, y, z0))
    verts.append(' %1.3f %1.3f %1.3f' % (x0, y, z1))
    verts.append(' %1.3f %1.3f %1.3f' % (x1, y, z1))
    verts.append(' %1.3f %1.3f %1.3f' % (x1, y, z0))
    rib = '\tPolygon "P" ['
    rib += ''.join(verts)
    rib += ']\n'
    return rib


if __name__ == "__main__":
    rootrect = [-2.0, -2.0, 2.0, 2.0]
    resolution = 0.05
    rootnode = Node(None, rootrect)
    tree = QuadTree(rootnode, resolution)

    # rect = [-2.0, -2.0, 2.0, 2.0]
    # tree = QuadTree(rect, 0.05)
    print(f"QuadTree.leaves: {len(QuadTree.leaves)}")
    print(f"QuadTree.maxdepth: {QuadTree.maxdepth}")
    # ribspath = '/Users/mkesson/Documents/WebSite/FUNDZA_COM/algorithmic/quadtree/ribs'
    ribspath = '/Users/rancoxu/Desktop/INFS7205/A2/quadtree'
    count = 1
    rib = ''
    for node in QuadTree.leaves:
        fname = 'rect.%0*d.rib' % (4, count)
        path = os.path.join(ribspath, fname)
        f = open(path, 'w')
        height = float(node.depth) / QuadTree.maxdepth
        rib += RiPolygon(node.rect, height * 0.25)
        f.write(rib)
        f.close()
        count += 1
    print('---------' * 8)
