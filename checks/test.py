class MyClass(object):
	class_var = 1

	def __init__(self, i_var, ob):
		self.i_var = i_var
		self.ob = ob

class test(object):
	def __init__(self,D):
		self.__dict__.update(D)

class poop:
	def __init__(self):
		self.P = 56

K = MyClass(4,poop())
k = K.__dict__

print(K.__dict__)

A = test(k)

print(A.i_var)
print(A.__dict__)
print(A.ob.P)