"""Parses .blif files"""

import sys

class BlifObject:
  """A representation of a .blif file"""
  def __init__(self, modelName, inputList, outputList, gateList):
    self.name = modelName
    self.inputs = inputList
    self.outputs = outputList
    self.gates = gateList

class BlifLogicGate:
  """A single .names instance from a .blif file. This
  is effectively a large sum of products 'logic gate'."""
  def __init__(self, wireList, logicTermList):
    if len(wireList) == 1:
      self.inputs = None
    else:
      self.inputs = wireList[:len(wireList) - 1]

    self.output = wireList[len(wireList) - 1]
    self.terms = logicTermList

class BlifLogicTerm:
  """A single logical term under a BlifLogicGate. Corresponds to a
  single term in the sum of products form of the logic gate."""
  def __init__(self, string):
    parts = string.split(' ')
    if len(parts) == 1: # No ' ' delimiter exists.
      self.term = None
      self.result = parts[0]
    else:
      self.term = parts[0]
      self.result = parts[1]
    
    if self.result == '0':
      print("Doesn't currently support a logic term with '0' as output.")
      sys.exit()
  
  def __repr__(self):
    return self.term + ": " + self.result

class BlifParser:
  """Parses a .blif file into a BlifObject"""
  def __init__(self, fileName):
    self.inputFile = open(fileName, 'r')

  def parse(self):
    """Parse the input file into a BlifObject"""
    modelName = self.parseModelName()
    inputList = self.parseInputList()
    outputList = self.parseOutputList()
    gateList = self.parseNameDecls()
    return BlifObject(modelName, inputList, outputList, gateList)

  def parseModelName(self):
    """Get the model name from the blif file"""
    line = self.inputFile.readline().strip()
    while True:
      parts = line.partition('.model')
      if len(parts[1]) != 0:
        return parts[2].strip()
      else:
        line = self.inputFile.readline().strip()

  def parseInputList(self):
    """Get the input list from the blif file"""
    line = self.inputFile.readline().strip()
    while True:
      parts = line.partition('.inputs')
      if len(parts[1]) != 0:
        inputString = parts[2].strip()
        break
      else:
        line = self.inputFile.readline().strip()
    return inputString.split(' ')

  def parseOutputList(self):
    """Get the output list from the blif file"""
    line = self.inputFile.readline().strip()
    while True:
      parts = line.partition('.outputs')
      if len(parts[1]) != 0:
        inputString = parts[2].strip()
        break
      else:
        line = self.inputFile.readline().strip()
    return inputString.split(' ')

  def parseNameDecls(self):
    """Get the list of logic function blocks"""
    result = []
    while self.isEmptyLine(): self.inputFile.readline()
    while not self.isEndField():
      line = self.inputFile.readline().strip()
      if line == '.names top^LOGICAL_OR~39^LOGICAL_OR~41 top^out':
        print('here')
      parts = line.partition('.names')
      result.append(self.parseSingleNameDecl(parts[2].strip().split(' ')))
      while self.isEmptyLine(): self.inputFile.readline()
    return result
  
  def parseSingleNameDecl(self, wireList):
    return BlifLogicGate(wireList, self.parseSingleOutputCover())

  def parseSingleOutputCover(self):
    result = []
    while (not self.isNamesField()) and (not self.isEndField()) and (not self.isEmptyLine()):
      result.append(BlifLogicTerm(self.inputFile.readline().strip()))
    return result

  def isNamesField(self):
    filePos = self.inputFile.tell()
    nameField = self.inputFile.readline().strip().partition('.name')[1]
    # Reset the file back before the readline. We are only checking if
    # the next line is a .names field
    self.inputFile.seek(filePos, 0)
    return len(nameField) != 0
  
  def isEndField(self):
    filePos = self.inputFile.tell()
    nameField = self.inputFile.readline().strip().partition('.end')[1]
    # Reset the file back before the readline. We are only checking if
    # the next line is a .names field
    self.inputFile.seek(filePos, 0)
    return len(nameField) != 0

  def isEmptyLine(self):
    filePos = self.inputFile.tell()
    line = self.inputFile.readline().strip()
    self.inputFile.seek(filePos, 0)
    return len(line) == 0