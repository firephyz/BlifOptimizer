#!/usr/bin/env python3

import sys

class BlifObject:
  def __init__(self, moduleName):
    self.moduleName = moduleName

  @staticmethod
  def parse(inputFileName):
    inputFile = open(inputFileName, 'r')
    result = inputFile.readline()
    print(result)
    return BlifObject('test')

if len(sys.argv) != 2:
  print('Usage: blifopt.py <blif_file>')
  sys.exit()

blif = BlifObject.parse(sys.argv[1])
print(blif.moduleName)