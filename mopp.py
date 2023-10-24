import logging
from math import ceil

class Mopp:
    serial = 1

    def __init__(self, speed = 20):
        self.speed = speed
        return

    def _str2hex(self, bytes):
        hex = ":".join("{:02x}".format(c) for c in bytes)
        return hex

    def _str2bin(self, bytes):
        bincode = "".join("{:08b}".format(c) for c in bytes)
        return bincode

    def mopp(self, speed, msg):
        logging.debug("Encoding message with "+str(speed)+" wpm :"+str(msg))

        morse = {
            "0" : "-----", "1" : ".----", "2" : "..---", "3" : "...--", "4" : "....-", "5" : ".....",
            "6" : "-....", "7" : "--...", "8" : "---..", "9" : "----.",
            "a" : ".-", "b" : "-...", "c" : "-.-.", "d" : "-..", "e" : ".", "f" : "..-.", "g" : "--.",
            "h" : "....", "i" : "..", "j" : ".---", "k" : "-.-", "l" : ".-..", "m" : "--", "n" : "-.",
            "o" : "---", "p" : ".--.", "q" : "--.-", "r" : ".-.", "s" : "...", "t" : "-", "u" : "..-",
            "v" : "...-", "w" : ".--", "x" : "-..-", "y" : "-.--", "z" : "--..", "=" : "-...-",
            "/" : "-..-.", "+" : ".-.-.", "-" : "-....-", "." : ".-.-.-", "," : "--..--", "?" : "..--..",
            ":" : "---...", "!" : "-.-.--", "'" : ".----."
        }

        m = '01'				# protocol version
        m += bin(self.serial)[2:].zfill(6)
        m += bin(speed)[2:].zfill(6)

        for c in msg:
            if c == " ":
                continue				# spaces not supported by morserino!

            for b in morse[c.lower()]:
                if b == '.':
                    m += '01'
                else:
                    m += '10'

            m += '00'				# EOC

        m = m[0:-2] + '11'			# final EOW
        m = m.ljust(int(8*ceil(len(m)/8.0)),'0')

        print (m, " ENCODER") # FIXME

        res = ''
        for i in range (0, len(m), 8):
            res += chr(int(m[i:i+8],2))

        self.serial += 1
        return bytes(res,'utf-8')

    def _stripheader(self, msg):
        res = bytes(0x00) + bytes(msg[1] & 3) + msg[2:]
        return res

    def msg_strcmp (self, data_bytes, speed, msg):
        if self._stripheader(data_bytes) == self._stripheader(self.mopp(speed, msg)):
            return True
        else:
            return False
        
    def received_speed (self, data_bytes): # FIXME
        speed = data_bytes[1] >> 2 
        return speed

    def received_serial (self, data_bytes): # FIXME
        #myserial = data_bytes[0] >> 2 
        myserial = 0 # FIXME
        return myserial

    def received_data (self, data_bytes): # TODO
        return self._str2hex(data_bytes)

    def decode_message (self, data_bytes):
        speed = data_bytes[1] >> 2 

        # Split symbols in an array
        L = [data_bytes[i:i+1] for i in range(len(data_bytes))]
        n = ""
        for l in L:
            #print (l, ord(l), "{:08b}".format(ord(l)))
            n += "{:08b}".format(ord(l))
        
        sym = [n[i:i+2] for i in range(0, len(n), 2)] # list of bit pairs 01, 10, 11, 00
        protocol = sym[0]
        serial = int("".join(sym[1:4]),2)
        msg = ""
        for i in range(8, len(sym), 1):
            s = ""
            if sym[i] == '01':
                s = '.'
            elif sym[i] == '10':
                s = '-'
            elif sym[i] == '00':
                s = 'EOC'
            elif sym[i] == '11':
                s = 'EOW'
            else:
                logging.debug ("This should not happen: symbol ", sym[i])
            msg += s
        print ("Decoded: ", "Protocol ", protocol, "Speed", speed, "Serial ", serial, sym, "Msg:", msg, "<EOM>")

        return (protocol, serial, msg)


    def _mopp2morse(self, sym):
        s = ""
        if sym == '01':
            s = '.'
        elif sym == '10':
            s = '-'
        elif sym == '00':
            s = 'EOC'
        elif sym == '11':
            s = 'EOW'
        else:
            logging.debug ("This should not happen: symbol ", sym[i])
        return s