#!/usr/bin/python
#code to generate the wave files for all the examples
#version 1
import os
import sys
def getInputFiles():
  for path,dirs,files in os.walk('../../examples'):
    pass
  inputs = []
#print files
  for f in files:
    if f.endswith('.xhtml'):
      inputs.append(f)
  inputs.sort()
  return inputs
   
def generateSable(inputs):
  for file in inputs:
    print file
    cmd = 'python 4.py  ../../examples/'+file
    os.system(cmd)
    sableCmd = 'mv equation.sable ../sable/'+file.split('.')[0]+'.sable'
    #print ' enter to continue\n'
    #raw_input()
    os.system(sableCmd)
    print 'moved sable file to sable directory using\n',sableCmd
    #print 'press enter to continue\n'
    #raw_input()
  return

def main():
  inputs = getInputFiles()
  print 'Inputs done'
  generateSable(inputs)
if __name__=='__main__':
  main()
