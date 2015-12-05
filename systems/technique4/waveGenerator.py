#!/usr/bin/python
#code to generate the wave files for all the examples
#version 1
import os
import sys
def getInputFiles():
  for path,dirs,files in os.walk('./examples'):
    pass
  inputs = []
  for f in files:
    fileExtension = f.split('.')[1]
    if fileExtension == '.xhtml':
      inputs.append(f)
  return inputs

def generateWaveAudio(inputs):
  for file in inputs:
    cmd = 'python 1.py '+file
    os.system(cmd)
    waveCmd= 'text2wave equation.sable -o '+file.split('.')[0]+'.wave'
    os.system(waveCmd)
  os.system('mv *.wave ../outputs/')
  return

def main():
  inputs = getInputFiles()
  generateWaveAudio(inputs)
if __name__=='__main__':
  main()