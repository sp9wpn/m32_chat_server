#!/usr/local/bin/python3
from mopp import * 
from math import ceil

msg1 = "hello"
mopp = Mopp()

data1 = mopp.mopp(20,msg1)
d1 = mopp._stripheader(data1)
zo1 = mopp._str2bin(data1)
print (mopp._str2bin(data1), msg1, data1, mopp._str2hex(data1))
#print (d1, mopp._str2hex(d1), mopp._str2bin(d1))
#print (len(zo1))

data1_encoder_n = "01000001010100010101010001000110010100011001010010101011" # CORRECT
data1_mopp_n = "010000010101000101010100010001100101000111000010100101001100001010101011" # INCORRECT(!)
data_bytes = data1

# Convert symbols to string of 0 and 1 again
n = ""
for l in [data_bytes[i:i+1] for i in range(len(data_bytes))]:
    print (l, ord(l), "{:08b}".format(ord(l)))
    n += "{:08b}".format(ord(l))

print (zo1)
print (n) # OK

#print (mopp._mopp2morse ("01"))

#for i in range (14, len(data1_encoder_n), 2):
for i in range (14, len(n), 2):
    s = n[i:i+2]
    print (s, mopp._mopp2morse(s))





sym = [n[i:i+2] for i in range(8, len(n), 2)] # list of bit pairs 01, 10, 11, 00
#print (sym)

msg = ""
for i in range(8, len(sym), 1):
    s = ""

    msg += s
#print (msg)
