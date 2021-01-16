

def inner_points(p: set):
	r = []
	for a in p:
		for b in (q for q in p if q != a):
			r.append( ( (a[0]+b[0] )/2,(a[1]+b[1] )/2,(a[2]+b[2] )/2 ) )
	return set(r)

k = [_ for _ in range(4)]

l = {(0,0,1) , (1,0,0) , (0,1,0),(1,1,0) , (0,1,1) , (1,0,1)}

while len(l) < len(k):
	l.update(inner_points(l))
	print(len(l))

t = zip(k,l)

print(dict(t))