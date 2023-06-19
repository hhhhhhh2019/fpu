import ctypes


# return 1/d
def get_fractional(d: int) -> int:
	s = bin(d)[2:]

	fp = len(s) - len(s.rstrip('0'))

	# 1 2 4 8 16...
	if s.count('1') == 1:
		return (1, fp)

	res = "1"

	for i in range(63):
		m = bin(d * int(res, 2))[2:]

		fst = len(m)-len(res)-fp

		res = m[fst-1] + res

	return (int(res,2), fp)



class Number:
	def __init__(self, val = None):
		self.number = 0
		self.float_point = 0

		if type(val) == str:
			snums = val.split('.') + [""]
			nums = [0,0]

			if len(snums[0]) > 0:
				nums[0] = int(snums[0])

			if len(snums[1]) > 0:
				nums[1] = int(snums[1])

			f_div = 0
			f_mul = nums[1]
			i_num = nums[0]

			f_div,self.float_point = get_fractional(10 ** len(snums[1]))

			self.number = f_div * f_mul + int(bin(i_num)[2:] + "0" * self.float_point, 2)

			self.normalize()


	def normalize(self):
		if self.float_point < 0:
			self.number = int(bin(self.number)[2:] + "0" * (-self.float_point), 2)
			self.float_point = 0
		else:
			s = bin(self.number)[2:]
			sf = 0

			for i in range(self.float_point):
				if s[-1] == '0':
					sf += 1
					s = s[:-1]

			self.number = int(s, 2)
			self.float_point -= sf

		self.number = ctypes.c_uint64(~self.number).value
		self.number = ctypes.c_uint64(~self.number).value


	def __add__(self, other):
		n1 = int(bin(self.number)[2:] + "0" * other.float_point, 2)
		n2 = int(bin(other.number)[2:] + "0" * self.float_point, 2)

		r = n1 + n2
		fst = self.float_point + other.float_point

		rn = Number()
		rn.number = r
		rn.float_point = fst

		rn.normalize()

		return rn


	def __sub__(self, other):
		self.number = ctypes.c_uint64(~self.number).value
		res = self + other
		res.number = ctypes.c_uint64(~res.number).value
		res.normalize()
		self.number = ctypes.c_uint64(~self.number).value
		return res


	def __mul__(self, other):
		r = self.number * other.number
		fst = self.float_point + other.float_point

		rn = Number()
		rn.number = r
		rn.float_point = fst

		rn.normalize()

		return rn

	def __truediv__(self, other):
		#r = int(self.number / other.number)
		#fst = self.float_point + other.float_point

		#rn = Number()
		#rn.number = r
		#rn.float_point = fst

		#rn.normalize()

		#return rn

		n = Number()
		n.number, n.float_point = get_fractional(other.number)
		n.normalize()

		res = self * n
		res.float_point -= other.float_point
		res.normalize()

		return res


	def __str__(self):
		s = bin(self.number)[2:].zfill(64)
		s = s[::-1]
		s = s[:self.float_point] + '.' + s[self.float_point:]
		s = s[::-1]
		return s


a = Number("0.6")
b = Number("0.3")
c = a / b

print(a,b,c)
