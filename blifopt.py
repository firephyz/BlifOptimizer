#!/usr/bin/env python3

import sys

class BlifObject:
  pass

class BlifParser:
  def __init__(self, fileName):
    self.inputFile = open(inputFileName, 'r')self.moduleName = moduleName

  def parse():
    """Parse the input file into a BlifObject"""
    modelName = self.parseModelName()
    inputList = self.parseInputList()
    outputList = self.parseOutputList()
    nameList = self.parseNameDecls()
    return BlifObject(modelName, inputList, outputList, nameList)

  def parseModelName():
    """Get the model name from the blif file"""

  def parseInputList():
    """Get the input list from the blif file"""

if len(sys.argv) != 2:
  print('Usage: blifopt.py <blif_file>')
  sys.exit()

parser = BlifParser(sys.argv[1])
blif = parser.parse()