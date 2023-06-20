import ctypes


# return 1/d
def get_fractional(d: int) -> int:
	s = bin(d)[2:]

	fp = len(s) - len(s.rstrip('0'))

	# 1 2 4 8 16...
	if s.count('1') == 1:
		return (1, fp)

	res = "1"

	for i in range(64-11):
		m = bin(d * int(res, 2))[2:]

		fst = len(m)-len(res)-fp

		res = m[fst-1] + res

	return (int(res,2), fp)


def f(s, p):
	count = 0

	while len(s) >= len(p):
		if s[0:len(p)] != p:
			break

		s = s[len(p):]
		count += 1

	return count



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
		elif type(val) == int:
			self.number = val
		elif type(val) == float:
			snums = str(val).split('.') + [""]
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
		elif type(val) == tuple:
			self.number,self.float_point = get_fractional(val[1])
			self.number = val[0] * int(bin(self.number)[2:], 2)

		self.normalize()


	def normalize(self):
		if self.float_point < 0:
			self.number = int(bin(self.number)[2:] + "0" * (-self.float_point), 2)
			self.float_point = 0
		else:
			s = bin(self.number)[2:]
			sf = 0

			for i in range(self.float_point):
				if len(s) == 0:
					break

				if s[-1] == '0':
					sf += 1
					s = s[:-1]

			if len(s) == 0:
				s = '0'

			self.number = int(s, 2)
			self.float_point -= sf

		self.number &= (1<<(64-11))-1
		self.float_point &= (2<<11)-1
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
		n = Number()
		n.number, n.float_point = get_fractional(other.number)
		n.normalize()

		res = self * n
		res.float_point -= other.float_point
		res.normalize()

		return res


	def __neg__(self):
		return Number(0) - self


	def __str__(self):
		period = "0"
		number = 0

		s = bin(self.number)[2:].zfill(64-11)
		d = {}

		#return bin(self.float_point)[2:] + s

		for i in range(1,len(s)):
			d[s[0:i]] = f(s, s[0:i])

		if len(d) != 0:
			mk = max(d, key=d.get)
			mv = d[mk]

			period = "{} / {}".format(int(mk, 2), (1<<len(mk))-1)

			if len(mk)*mv < len(s):
				number = int(s[len(mk)*mv:], 2)

			period += " * " + str(1<<len(s[len(mk)*mv:]))
		else:
			number = int(s, 2)

		float = "1/" + str(1<<self.float_point)
		s = "({} - {}) * {}".format(number, period, float)
		return s + " ~= " + str(eval(s))


	def debug(self):
		print("-"*50)
		print(bin(self.number)[2:].zfill(64-11))
		print(self.float_point)
		print("-"*50)


a = Number((123412232138121,9007199254740991))
print(a*Number(9007199254740991))
