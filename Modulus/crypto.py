import sys
from secret import encryptionKey, flag

if len(encryptionKey) % 2 == 1:
    print("Key Length Error")
    sys.exit(1)

n = len(encryptionKey) / 2
encrypted = ''
for c in flag:
    c = ord(c)
    for a, b in zip(encryptionKey[0:n], encryptionKey[n:2*n]):
        c = (ord(a) * c + ord(b)) % 251
    encrypted += '%02x' % c

print encrypted

# find flag with encrypted = e491a9c1d86d1925fa246b1783538f54d75f543b0c6b17545fd7a783b30c54d70054178f4754bf9b8f2fe2

