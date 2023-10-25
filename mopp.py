# Module for MOPP protocol
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

        #print (m, " ENCODER") # FIXME

        res = ''
        for i in range (0, len(m), 8):
            #print (m[i:i+8], bytes(chr(int(m[i:i+8],2)),"latin_1"), i, " ENCODER")
            res += chr(int(m[i:i+8],2))

        self.serial += 1
        return bytes(res,'latin_1') # WATCH OUT: UNICODE MAKES MULTI-BYTES 

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
        if len(data_bytes) < 1:
            return {"Keepalive": True}
        
        speed = data_bytes[1] >> 2 

        # Convert symbols to string of 0 and 1 again
        n = ""
        for l in [data_bytes[i:i+1] for i in range(len(data_bytes))]:
            n += "{:08b}".format(ord(l))
        
        # list of bit pairs 01, 10, 11, 00
        sym = [n[i:i+2] for i in range(0, len(n), 2)] 
        protocol = sym[0]
        serial = int("".join(sym[1:4]),2)

        # Extract message in format ./-/EOC/EOW
        msg = ""
        for i in range (14, len(n), 2):
            s = n[i:i+2]
            msg += self._mopp2morse(s)

        return {"Protocol": protocol, "Serial": serial, "Speed": speed, "Message": msg}


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
            logging.debug ("This should not happen: symbol ", s)
        return s
    
    def _morse2txt(self, morse):
        return