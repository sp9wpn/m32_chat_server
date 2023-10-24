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

        m = '01'				# protocol
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

        res = ''
        for i in range (0, len(m), 8):
            res += chr(int(m[i:i+8],2))

        self.serial += 1
        return bytes(res,'utf-8')

    def _stripheader(self, msg):
        res = bytes(0x00) + bytes(msg[1] & 3) + msg[2:]
        return res
