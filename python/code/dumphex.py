import sys

import hashlib
import binascii

strs = "dafadfsaasdfasdfsdfsdafasdfasf"
FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])

def dump2(src, length=8):
    result=[]
    for i in range(0, len(src), length):
        s = src[i:i+length]
        hexa = ' '.join(["%02X"%ord(x) for x in s])
        printable = s.translate(FILTER)
        result.append("%04X   %-*s   %s\n" % (i, length*3, hexa, printable))
    return ''.join(result)
print (dump2(strs))


 
