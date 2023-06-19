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

		#print("{:>64} {:>64}".format(res, m))

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


	def __str__(self):
		s = bin(self.number)[2:]
		s = s[::-1]
		s = s[:self.float_point] + ',' + s[self.float_point:]
		s = s[::-1]
		return s


a = Number("1.5")
print(a)
