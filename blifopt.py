#!/usr/bin/env python3

import sys
import parseblif

def removeDuplicates(implicants):
  result = []
  for i in range(len(implicants)):
    if implicants[i] not in result:
      result.append(implicants[i])
  return result

def sortImplicant(impA, impB):
  """1 if impA > impB, 0 if equal, -1 if <"""
  for i in range(len(impA)):
    if impA[i] == '-':
      if impB[i] != '-':
        return 1
    elif impA[i] == '1':
      if impB[i] == '-':
        return -1
      elif impB[i] == '0':
        return 1
    else:
      if impB[i] != '0':
        return -1
  return 0

def countDontCares(implicant):
  count = 0
  for i in range(len(implicant)):
    if implicant[i] == '-':
      count += 1
  return count

def insertImplicant(implicant, group):
  index = 0
  while True:
    if index == len(group):
      group.insert(index, implicant)
      break
    else:
      value = sortImplicant(implicant, group[index])
      if value < 0:
        group.insert(index, implicant)
        break
      elif value > 0:
        index += 1
    
def groupImplicants(implicants):
  groups = []
  for i in range(len(implicants)):
    groupIndex = countDontCares(implicants[i])
    if groupIndex > len(groups) - 1:
      for j in range(len(groups) - 1, groupIndex):
        groups.append([])
    
    insertImplicant(implicants[i], groups[groupIndex])
  return groups

def removeRedundantImplicants(groups):
  for i in range(len(groups) - 1, -1, -1):
    gro
    for j in range(len)

def findLargerImplicants(groups):
  pass

if len(sys.argv) != 2:
  print('Usage: blifopt.py <blif_file>')
  sys.exit()

parser = parseblif.BlifParser(sys.argv[1])
blif = parser.parse()

# For this assignment, we only support one .names field
if len(blif.gates) != 1:
  print('Current implementation only supports one .names field; only one logic gate.')
  sys.exit()

# Get initial implicant list
implicants = []
for i in range(len(blif.gates[0].terms)):
  implicants.append(blif.gates[0].terms[i].term)

groupedImplicants = groupImplicants(implicants)

shouldRunReduceCycle = True
while shouldRunReduceCycle:
  removeRedundantImplicants(groupedImplicants)
  findLargerImplicants(groupedImplicants)

print('Done')