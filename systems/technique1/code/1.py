
# -*- coding: utf-8 -*-
from lxml import etree as et
import sys
import os
# for TTS(default system TTS)
#import pyttsx
#coding: utf-8


#function that reads the xhtml file and returns the root of the document

def getData(fname):
  with open(fname) as f:
    parser = et.XMLParser(load_dtd=True, no_network=False,resolve_entities=False)
    data = f.read()
    data = data.replace('\t','')
    data = data.replace('\n','')
    doc = et.fromstring(data, parser=parser)
    return doc


#function to generate a basic sable root and append the version and other info at the end to a file "equation.sable"
def generateSable(node=None,flag=None):
  ##print 'in function generateSable'
  ##print flag
  documentInfo = '<?xml version="1.0"?><!DOCTYPE SABLE PUBLIC "-//SABLE//DTD SABLE speech mark up//EN" "Sable.v0_2.dtd" []>'
  if flag:
    sable = ''
    sable = documentInfo+et.tostring(node)
    ##print 'writing sable to file'
    f = open('equation.sable','w')
    f.write(sable)
    f.close()
    return
  return  et.Element('SABLE')

def operatorParse(op):
  if op == '+':
    return 'plus'
  if op == '&plus;':
    return 'plus'
  if op == '&int;':
    return 'integral'
  if op == '&sum;':
    return ' summation'
  if op == '&prod;':
    return ' product '
  if op == '-':
    return 'minus'
  if op == '&minus;':
    return 'minus'
  if op == '&plusmn;':
    return 'plus or minus '
  if op == '...':
    return 'so on till,'
  if op == '=':
    return 'is equal to'
  if op == '&ne;':
    return 'is not equal to'
  if op == '&asymp;':
    return ' is almost equal to '
  if op == '&prop;':
    return 'is proportional to '
  if op == '&le;':
    return 'is less than or equal to'
  if op == '&ge;':
    return 'is greater than or equal to'
  if op == '&lt;':
    return ' is less than'
  if op == '&gt;':
    return 'is greater than '
  if op == '&lt;':
    return ' is less than'
  if op == '(':
    return '('
  if op == ')':
    return ')'
  if op == 'sin':
    return 'sine'
  if op == 'cos':
    return 'cos'
  if op == 'tan':
    return 'tan'
  if op == 'log':
    return 'log'
  if op == '*':
    return 'times'
  if op == '&times;':
    return ' multiplied by'
  if op == '/':
    return 'divided by'
  if op == '&divide;':
    return 'divided by'
  if op == '%':
    return 'modulo divided by'
  if op == '&prime;':
    return 'first order derivative '
  if op == '&Prime;':
    return ' second derivative '
  if op == '&tprime;':
    return 'third derivative '
  if op == '&qprime;':
    return 'forth derivative '
  if op == '&part;':
    return ' parcial differential'
  if op == '∮':
    return ' contour integral of'
  if op == '∯':
    return ' surface integral of'
  if op == '∰':
    return ' volume integral of'
  if op == '∱':
    return ' clockwise integral of'
  if op == '∂':
    return 'partial derivative of'
  if op == '∠':
    return ' angle of'
  # alternative way for an integral, using the direct symbol should also work
  if op == '&dd;':
    return 'D'
  if op == '&int;':
    return 'integral'
  if op == '.':
    return '.'
  if op == '&infin;':
    return 'infinity'
  if op == 'lim':
    return 'limit'
  if op == '&rarr;':
    return 'tends to'
  if op == ',':
    return ','
  return op
#fill in operators


# if op == the operator:
#return a text form of the operator

def getEntityValue(node):
  if node.tag.split('}')[1] == 'mi':
    if node[0].text == '&alpha;':
      node.text = 'alpha'
    if node[0].text == '&beta;':
      node.text = 'beta'
    if node[0].text == '&gama;':
      node. text = 'gama'
    if node[0].text == '&theta;':
      node.text = 'theta'
    if node[0].text == '&pi;':
      node.text='pi'
  else:
    node.text = node[0].text
  deleteElement = node[0]
  node.remove(deleteElement)
  return node

#function to parse the mathML
def mathparse(element,snode,exp = []):
  ##print 'testing element'
  ##print 'text:'
  ##print element.text
  ##print 'tag:',element.tag
  mtag = element.tag.split('}')[1]
  #mtag = element.tag
  ##print 'modified tag:',mtag
  ##print 'expression string:', exp
  # numbers and variables
  if mtag == 'mi' or mtag == 'mn':
    if len(element) > 0:
      element = getEntityValue(element)
    exp.append(element.text)
  # operators
  if mtag == 'mo':
    if len(element) > 0:
      element = getEntityValue(element)
      #print element.text
    ##print 'this is'
    ##print operatorParse(element.text)
    exp.append(operatorParse(element.text))

# fractions
  if mtag == 'mfrac':
    exp.append('fraction')
    exp = mathparse(element[0],snode,exp)
    exp.append('over')
    exp = mathparse(element[1],snode,exp)
    return exp
# superscript
  if mtag == 'msup':
    exp = mathparse(element[0],snode,exp)
    
    exp.append('superscript')
    exp = mathparse(element[1],snode,exp)
    return exp
#subscript
  if mtag == 'msub':
    exp = mathparse(element[0],snode,exp)
    exp.append('subscript')
    exp = mathparse(element[1],snode,exp)
    return exp
#subscript-superscript pairs
  if mtag == 'msubsup':
    mathparse(element[0],snode,exp)
    exp.append('subscript')
    mathparse(element[1],snode,exp)
    exp.append('superscript')
    mathparse(element[2],snode,exp)
    return exp
#fence

# over script
  if mtag == 'mover':
    exp = mathparse(element[0],snode,exp)
    exp.append('overscript')
    exp = mathparse(element[1],snode,exp)
    return exp
#underscript
  if mtag == 'munder':
    exp = mathparse(element[0],snode,exp)
    exp.append('underscript')
    exp = mathparse(element[1],snode,exp)
    return exp
# underscript-overscript pair
  if mtag == 'munderover':
    exp = mathparse(element[0],snode,exp)
    exp.append('from')
    exp = mathparse(element[1],snode,exp)
    exp.append('to')
    exp=mathparse(element[2],snode,exp)
    return exp

# square root
  if mtag == 'msqrt':
    exp.append('square root')
    if len(element) == 1 and len(element[0]) > 1:
      exp.append('of')
    for c in element:
      exp=mathparse(c,snode,exp)
    return exp
# general root
  if mtag == 'mroot':
    exp=mathparse(element[-1],snode,exp)
    exp.append('root of')
    for c in element[:-1]:
      exp=mathparse(c,snode,exp)
    return exp
##print 'list:',len(exp)
##print 'items in the list:\n',exp
  #print 'sable markup:\n',et.tostring(snode)
  for e in element:
    exp=mathparse(e,snode,exp)
  if len(snode) > 0:
    if snode[-1].tail:
      snode[-1].tail = snode[-1].tail+' '.join(exp)
    else:
      snode[-1].tail = ' '.join(exp)
#exp = []
  else:
    if snode.text:
      snode.text = snode.text + ' '.join(exp)
    else:
      snode.text = ' '.join(exp)

  #print 'sable just before exiting:\n',et.tostring(snode)
  return exp


def main():
  args = sys.argv
  if len(args) < 2:
    #print 'usage:\nbasicSable.py inputFile.xhtml'
    exit(1)
  fileName = str(sys.argv[1])
  xmlroot = getData(fileName)  #'example1.xhtml' contains the xhtml code given above
  sableroot=generateSable()
  expList = mathparse(xmlroot,sableroot)
  if len(sableroot) > 0:
    sableroot[-1].tail = ' '.join(expList)
  else:
    sableroot.text = ' '.join(expList)
  generateSable(sableroot,1)
##print 'list in the main function:\n',expList
##print len(expList)
  expression = ' '.join(expList)
  ##print the resulting string
  #print 'result:',expression
#speak the expression
#speek(expression)
#speak the expression using festival
  cmd = 'echo "'+expression+'" | festival --tts'
  festCmd = 'festival --tts equation.sable'
  #os.system(festCmd)


if __name__ == '__main__':
  main()
