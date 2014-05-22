#!/usr/bin/python

# read and unpack the IBM sample TLOG file - this should be fun!

import fileinput
import string
import re
import csv
import sys

def unpack(self):
   if self == 0xfd: # padded minus sign, only case where - sign will be in low nible
       return '-'
   highNibble = self >>4 # high nibble is right-bit-shift-4
   if highNibble == 0xf:
       highNibble = ''
   elif highNibble == 0xd: # the minus sign
       highNibble = '-'
   lowNibble=self & 0x0f # AND the number with 0F to blank the high bits
   return '{0[0]}{0[1]}'.format((highNibble,lowNibble))

def decodeFields(self):
    output = []
    eventType = ord(self[0])
    for field in self:
        if ( eventType == 0x20 ) & ( reSignedInt.match(field) != None ): # if contents of type 20 events are purely ints with optional leading -sign 
            output.append(field) # treat as a number and don't unpack. Can further restrict this to columns 9-13
        elif len(field) == 0: # empty field (very common)
            output.append('')
        else: # otherwise treat as packed BCD and unpack, see http://www.ogf.org/pipermail/dfdl-wg/2012-September/001987.html
            bArrayString = ''
            for b in bytearray(field): # loop over the bytes in the field
                bArrayString = bArrayString+unpack(b)
            output.append(bArrayString)
    return output

reSignedInt = re.compile('^-?[0-9]+$') # define regex for positive/negative integers
writer = csv.writer(sys.stdout)

for line in fileinput.input():
    c1 = ord(line[1])
    if c1 == 32: # short lines with ":" delimiters, in practice these can probably be ignored altogether
        line = ' ":"'+line[3:len(line)-3] # strip leading '" :' and trailing '"<cr><lf>' while replacing the first un-double-quoted : with ":"
        fields = string.split(line,'":"')
        decodedLine = decodeFields(fields)
        writer.writerows([decodedLine,])
    elif c1 == 0 : # long lines with double quoted blocks delimited by commas and fields in each block delimited by colons. First field is always x00 
        line = line[1:len(line)-3]
        blocks = string.split(line,'","')
        for block in blocks:
            fields = string.split(block,':')# decode each block stripping off the first and last char which will be double quotes
            decodedLine = decodeFields(fields)
            writer.writerows([decodedLine,])
    else:
        sys.stderr.write('Unexpected record:'+line)
