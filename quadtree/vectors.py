import math

def dot(v,w):
	x,y,z = v
	X,Y,Z = w
	return x*X + y*Y + z*Z

def length(v):
	x,y,z = v
	return math.sqrt(x*x + y*y + z*z)

def vector(b,e):
	x,y,z = b
	X,Y,Z = e
	return (X-x, Y-y, Z-z)

def unit(v):
	x,y,z = v
	mag = length(v)
	return (x/mag, y/mag, z/mag)

def distance(p0,p1):
	return length(vector(p0,p1))

def scale(v,sc):
	x,y,z = v
	return (x * sc, y * sc, z * sc)

def add(v,w):
	x,y,z = v
	X,Y,Z = w
	return (x+X, y+Y, z+Z)
	
#---------------------------------------------------	
if __name__=="__main__":	
	segn = [(0,0,0),(1.0,0,0)]
	pnt1 = (-0.4,0,-1)
	pnt2 = ( 2.0,0,-1)
	pnt3 = ( 1.5,0,-1)
	
	
	#print dot(segn[1],pnt1)
	#print dot(segn[1],pnt2)
	#print dot(segn[1],pnt3)
	
	seg = [(1,0,0),(2.9,0,0)]
	pnt2 = ( 1.9,0,-1)
	
	#print('vector segment %s' % str(vector(seg[0],seg[1])) )
	# convert segment to vector
	segvec = vector(seg[0],seg[1])
	print('segment vector %s' % str(segvec))
	
	seglen = length(segvec)
	print('length of segment %1.3f' % seglen)
	
	# convert to unit vector
	segunit = unit(segvec)
	
	# convert point P to a vector relative to segment
	pnt2v = vector(seg[0],pnt2)
	
	# make its length proportional to the segment unit vector
	pnt2u = (pnt2v[0]/seglen, pnt2v[1]/seglen, pnt2v[2]/seglen)
	
	# dot product of segment vector and point
	t = dot(segvec, pnt2u)/seglen
	
	print('t %1.3f' % t)
	if t < 0:
		t = 0
	elif t > 1:
		t = 1
		
	# use 't' to find intersection point on the segment vector
	#print('segvec x = %1.3f' % segvec[0])
	intersect = (segvec[0] * t, segvec[1] * t, segvec[2] * t) 
	
	print('intersect %s' % str(intersect))
	
	dist = distance(intersect, pnt2v)
	print('distance is %1.3f' % dist)
	
	# convert the point of intersection to its position on
	# the line segement
	intersect = (intersect[0] + seg[0][0],
				 intersect[1] + seg[0][1],
				 intersect[2] + seg[0][2])
	print('intersect %s' % str(intersect))
	
	# find the distance from point P to the intersect
	dist = distance(intersect, pnt2)
	print('distance is %1.3f' % dist)
	
	
	
	# convert to unit vector
	#segu = unit(segv)
	#print('segment as unit vector %s' % str(segu))
	#
	#print '---'
	#print('pnt2 as vector %s' % str(pnt2v))
	#print('length of vector %1.3f' % length(pnt2v))
	#pnt2u = unit(pnt2v)
	#print('pnt2 as unit vector %s' % str(pnt2u))
	#print('length of unit vector %1.3f' % length(pnt2u))
	#t = dot(segu, pnt2u)
	#print('dot product %1.3f' % t)
	#
	#d = t * pnt2u[0]
	#print('dt %1.3f pnt2v.x %1.3f' % (d,pnt2v[0]) )
	#
	#d = t * pnt2u[0]  + seg[0][0]
	#print('d %1.3f' % d)









