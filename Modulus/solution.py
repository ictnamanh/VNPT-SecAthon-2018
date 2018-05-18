import string
from sympy import Matrix

encrypted = "e491a9c1d86d1925fa246b1783538f54d75f543b0c6b17545fd7a783b30c54d70054178f4754bf9b8f2fe2"

p = Matrix([[83, 1], [69, 1]])
c = Matrix([[228, 1], [145, 1]])

k = p.inv_mod(251) * c
inv_k = k.inv_mod(251)

flag = ''
for i in range(0, len(encrypted), 2):
	d = int(encrypted[i:i+2], 16)
	x = Matrix([[d, 1]]) * inv_k
	flag += chr(x[0, 0] % 251)
print flag