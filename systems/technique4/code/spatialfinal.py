#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
from scipy.signal import lfilter
from subprocess import check_call
import sys
import os

def readHRTF(name):
    '''Read the hrtf data from compact format files'''
    r = np.fromfile(file(name, 'rb'), np.dtype('>i2'), 256)
    r.shape = (128,2)
    # half the rate to 22050 and scale to 0 -> 1
    r = r.astype(float)
    # should use a better filter here, this is a box lowering the sample rate from 44100 to 22050
    r = (r[0::2,:] + r[1::2,:]) / 65536
    return r

# run as python hrtf.py infile outdir
if len(sys.argv) < 1:
    print 'usage: python hrtf.py inputfile '
    sys.exit(1)
print sys.argv
fname = sys.argv[1]


# recode the sound to mono and 22050
check_call(['sox','-G', fname, '-r', '16000', '-c1', '-b', '16', 'inp.wav'])

# read the input
rate, mono_sound = wavfile.read(file('inp.wav', 'rb'))

# remove that tmp file
#os.remove('inp.wav')

# scan azimuth generating sounds
elev = 30
az=18
try:
    hrtf = readHRTF(os.path.join('compact', 'elev%d'%elev, 'H%d'%elev +'e%03da.dat' % az))
except IOError:
    print 'Sorry File not found !!'
   
    
    #print hrtf
    # apply the filter
left = lfilter(hrtf[:,0], 1.0, mono_sound)
right = lfilter(hrtf[:,1], 1.0, mono_sound)

    # combine the channels
result = np.array([left, right]).T.astype(np.int16)

    # save as a wav    
#wavfile.write('result1.wav',rate,result)
    # swap the left and right channels for the negative angle
result = result[:,(1,0)]
wavfile.write('result2.wav',rate,result)







# Generating the varied signal

# Determining the pitch variations

f=open('timestamp.txt')
start_array=[]
end_array=[]



for line in f:
    start_array.append(float(line.split()[0]))
    end_array.append(float(line.split()[1]))

start=0

print start_array
print end_array

# Split the original wave from start till the first occurence of the variation


for i in range(0, len(start_array)):
    #print 'start is ' + str(start) 
    #begin=str(start)
    #print 'begin is ' + str(begin)   
    #duration1=str(start_array[i] )
    #print 'duration1 is '+ str(duration1)
    #init_time=str(start_array[i])
    #print 'init_time is '+str(init_time)
    #final_time=str(end_array[i])
    #print 'final_time is ' + str(final_time)
    #duration = str(float(final_time) - float(init_time))
    
   # print 'duration is ' + str(duration) 
    #start+=end_array[i]

    if (i%2) == 0 :
        print 'Normal Wave'
        start = str(start_array[i])
        end= str(end_array[i])
        print start
        print end
        duration=str(float(end)-float(start))
        print duration
        fname=str(i)+'.wav'
        check_call(['sox','inp.wav', fname, 'trim', start, duration])
        print '\n\n\n'
    else:
        print 'Spatial Wave'
        start = str(start_array[i])
        end= str(end_array[i])
        print start
        print end
        duration=str(float(end)-float(start))
        print duration
        fname=str(i)+'.wav'
        check_call(['sox','result2.wav', fname , 'trim', start,duration])
        print '\n\n\n'



    
    
#    check_call(['sox','inp.wav', 'array[i].wav', 'trim', 'start', 'duration1'])
#    check_call(['sox','result2.wav', 'array[i+1].wav', 'trim', 'array[i]','duration'])
#    start=int(final_time)
































def frange(start, end=None, inc=None):
    "A range function, that does accept float increments..."

    if end == None:
        end = start + 0.0
        start = 0.0

    if inc == None:
        inc = 1.0

    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)
        
    return L


