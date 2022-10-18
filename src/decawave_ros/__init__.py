#!/usr/bin/env python3

from collections import namedtuple

DecaMsg = namedtuple('DecaMsg', 'typ anc tag r0 r1 r2 r3')


class DecaParser:
    def __init__(self,stream):
        self.stream = stream


    def receive(self):

        data = self.stream.readline().decode('utf-8').split()
        #print(data)
        try:
            if (data[0] == 'mc'):
                if(data[9][0] == "a"):
                    typ = 'Anchor'
                else:
                    typ = 'Tag'
                anc = int(data[9][3])
                tag = int(data[9][1])
                r0  = int(data[2],16)/1000.0
                r1  = int(data[3],16)/1000.0
                r2  = int(data[4],16)/1000.0
                r3  = int(data[5],16)/1000.0

                return DecaMsg(typ, anc, tag, r0, r1, r2, r3)
        except:
            return