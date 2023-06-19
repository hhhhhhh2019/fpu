# return 1/d
def get_fractional(d: int) -> int:
	s = bin(d)[2:]

	fp = len(s) - len(s.rstrip('0'))

	res = "1"

	for i in range(10):
		m = bin(d * int(res, 2))[2:]

		print("{:>15} {:>15}".format(res, m))

		fst = len(m)-len(res)

		res = m[fst-1] + res

	return (res, fp)



class Number:
	def __init__(self, val = None):
		self.number = 0
		self.float_point = 0

		if type(val) == str:
			i,f = [int(i) for i in val.split('.')]




	def __str__(self):
		return bin(self.number)[2:]


print(get_fractional(3))
