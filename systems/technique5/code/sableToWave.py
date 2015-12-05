#!/usr/bin/python
#code to generate the wave files for all the examples
#version 1
import os
import sys
from subprocess import check_call

def getInputFiles():
  for path,dirs,files in os.walk('.'):
    pass
  inputs = []
  #print files
  for f in files:
    if f.endswith('.sable'):
      inputs.append(f)
  inputs.sort()
  return inputs

def generateWave(inputs):
  print 'In Fn'
  for file in inputs:
    print file
    print os.getcwd()
    orig=file
    new= file.split('.')[0]+'.wav'
    #waveCmd='text2wave '+file+' -o '+file.split('.')[0]+'.wav'
    #os.system(waveCmd)
    check_call(['text2wave',orig,'-o',new])
    #print 'generated wave using command\n',waveCmd
  print 'moving wavefiles'
  #os.system('mv *.wave ../outputs/')
  return

def main():
  inputs = getInputFiles()
  print 'Inputs done'
  generateWave(inputs)
if __name__=='__main__':
  main()
