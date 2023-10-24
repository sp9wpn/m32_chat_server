#!/usr/local/bin/python3
from mopp import * 
data="4c:52:c2:a5:45:51:49:57"
msg1 = "hho"

mopp = Mopp()

#print (m.serial)
data1 = mopp.mopp(20,msg1)
#print (m.serial)
data1a = mopp.mopp(20,msg1)
#print (m.serial)

print (data1, mopp._str2hex(data1), mopp._str2bin(data1))
print (data1a, mopp._str2hex(data1a), mopp._str2bin(data1a))


# print (m._str2bin(m._stripheader(data1)))
# print (m._str2bin(m._stripheader(data1a)))

# print ( m.received_speed(data1) )
# print ( m.received_serial(data1) )
# print ( int( data1[0] >>2 ))

print ("Manual encoding: ho")
serial = 55
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
    print (bytes(res,'utf-8'), chr(int(m[i:i+8],2)), int(m[i:i+8],2), m[i:i+8])

rr=bytes(res,'utf-8')
print (rr, "Encoding complete")

print ("Decoding")
L = [rr[i:i+1] for i in range(len(rr))]
print (L)
n = ""
for l in L:
    print (l, ord(l), "{:08b}".format(ord(l)))
    n += "{:08b}".format(ord(l))
print(n)
print ("Length", len(n)) # FIXME

#n="01000001010100010101010010101011"
#n="01000001010100010101010001010101001010101100001110000000"

sym = [n[i:i+2] for i in range(0, len(n), 2)]
print (sym)
protocol = sym[0]
print (protocol, "Protocol")
serial = int("".join(sym[1:4]),2)
print (serial, "Serial", "".join(sym[1:4]))
speed = rr[1] >> 2  #"".join(sym[5:8])
print (speed, "Speed")
for i in range(0, len(sym), 1):
    
    s = ""
    if sym[i] == '01':
        s = '.'
    elif sym[i] == '10':
        s = '-'
    elif sym[i] == '00':
        s = 'EOC'
    elif sym[i] == '11':
        s = 'EOW'
    
    print (i, sym[i], s)

print (mopp.decode_message(rr))