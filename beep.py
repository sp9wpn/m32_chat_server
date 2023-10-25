import pygame, numpy, pygame.sndarray

class Beep:
    def __init__(self, speed = 20):

        # Ref timings: https://morsecode.world/international/timing.html#:~:text=It's%20clear%20that%20this%20makes,%22)%20which%20also%20makes%20sense.
        speed_wpm = speed
        self.dit_duration = int(60 / (50*speed_wpm)*1000)
        self.dah_duration = 3*self.dit_duration
        self.eoc_duration = 3*self.dit_duration
        self.eow_duration = 7*self.dit_duration

        # Ref for sound: https://gist.github.com/nekozing/5774628
        sampleRate = 44100
        # 44.1kHz, 16-bit signed, mono
        pygame.mixer.pre_init(sampleRate, -16, 1) 
        pygame.init()
        # 4096 : the peak ; volume ; loudness
        # 440 : the frequency in hz
        # ?not so sure? if astype int16 not specified sound will get very noisy, because we have defined it as 16 bit mixer at mixer.pre_init()
        # ( probably due to int overflow resulting in non continuous sound data)
        arr = numpy.array([4096 * numpy.sin(2.0 * numpy.pi * 440 * x / sampleRate) for x in range(0, sampleRate)]).astype(numpy.int16)
        self.sound = pygame.sndarray.make_sound(arr)

    def _beep(self, symbol):
        if symbol == ".":
            self.sound.play(-1)
            pygame.time.delay(self.dit_duration)
            self.sound.stop()
            pygame.time.delay(self.dit_duration)
        elif symbol == "-":
            self.sound.play(-1)
            pygame.time.delay(self.dah_duration)
            self.sound.stop()
            pygame.time.delay(self.dit_duration)
        elif symbol == "C": # EOC
            pygame.time.delay(self.eoc_duration)
        elif symbol == "W": # EOW
            pygame.time.delay(self.eow_duration)

    def beep_message(self, message):
        for s in message:
            self._beep (s)

