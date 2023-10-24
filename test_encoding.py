#!/usr/local/bin/python3
from mopp import * 
from math import ceil

data="4c:52:c2:a5:45:51:49:57"
msg1 = "ho"

mopp = Mopp()

data1 = mopp.mopp(20,msg1)

print (data1, mopp._str2hex(data1), mopp._str2bin(data1))


print ("Manual encoding: ho")
serial = 1
speed = 20
m = '01'				# protocol
print (m, "protocol")
m += bin(serial)[2:].zfill(6)
print (m, "serial")
m += bin(speed)[2:].zfill(6)
print (m, "speed", speed, bin(speed)[2:], bin(speed)[2:].zfill(6))

# h = ....
m += '01'
m += '01'
m += '01'
m += '01'
m += '00'				# EOC
print (m, "h")

# o = ---
m += '10'
m += '10'
m += '10'
m += '00'				# EOC

print (m,"o")
    
m = m[0:-2] + '11'			# final EOW

print (m, "eow")
        
m = m.ljust(int(8*ceil(len(m)/8.0)),'0')
print ("Length", len(m))
print (m, "final")

print ("Construct string")
res = ''
for i in range (0, len(m), 8):
    res += chr(int(m[i:i+8],2))
    print (bytes(res,'latin1'), chr(int(m[i:i+8],2)), int(m[i:i+8],2), m[i:i+8])

rr=bytes(res,'latin1')
print (rr, "Encoding complete")


print (mopp.decode_message(res))