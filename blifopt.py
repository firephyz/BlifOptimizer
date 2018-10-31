#!/usr/bin/env python3

import sys
import parseblif

def removeDuplicates(implicants):
  removals = []
  for i in range(len(implicants)):
    for j in range(i + 1, len(implicants)):
      if implicants[i] == implicants[j]:
        removals.append(implicants[i])
  for elem in removals:
    implicants.remove(elem)

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
      else:
        break
    
def groupImplicants(implicants):
  groups = []
  for i in range(len(implicants)):
    groupIndex = countDontCares(implicants[i])
    if groupIndex > len(groups) - 1:
      for j in range(len(groups) - 1, groupIndex):
        groups.append([])
    
    insertImplicant(implicants[i], groups[groupIndex])
  return groups

def implicantCovers(first, second):
  """Tests if the second implicant is covered by the first.
  If so, the second is unnecessary. Drop it."""
  for index in range(len(first)):
    if first[index] == '-':
      continue
    else:
      if second[index] == '-':
        return False
      elif first[index] != second[index]:
        return False
  return True

def removeRedundantImplicants(groups):
  """Removes more specific implicants if a more general one
  can cover it."""
  for i in range(len(groups) - 1, -1, -1):
    for j in range(i):
      mainGroup = groups[i]
      otherGroup = groups[j]
      for coverImp in mainGroup:
        for testImp in otherGroup:
          if implicantCovers(coverImp, testImp):
            otherGroup.remove(testImp)

def combineImplicants(impA, impB):
  """Combines two implicants. We assume they have
  the same number of dashes (dontCares)"""
  hasDiff = False
  diffIndex = -1
  for i in range(len(impA)):
    if impA[i] != impB[i]:
      if impA[i] == '-' or impB[i] == '-':
        return None
      else:
        if hasDiff:
          return None
        else:
          diffIndex = i
          hasDiff = True
  return impA[:diffIndex] + '-' + impA[diffIndex + 1:]

def findLargerImplicants(groups):
  """Assumes traversal always occurs from lowest indexed group
  to highest index group"""
  didChange = False
  global shouldRunReduceCycle
  removals = []
  for groupIndex in range(len(groups)):
    group = groups[groupIndex]
    i = 0
    for i in range(len(group)):
      for j in range(i + 1, len(group)):
        result = combineImplicants(group[i], group[j])
        if result != None:
          if not didChange: didChange = True
          if group[i] not in removals:
            removals.append(group[i])
          if group[j] not in removals:
            removals.append(group[j])
          
          # Add new implicant to the groups
          if groupIndex + 1 == len(groups):
            groups.append([])
          
          groups[groupIndex + 1].append(result)
    for elem in removals:
      group.remove(elem)
    removals = []
  if not didChange: shouldRunReduceCycle = False

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
for group in groupedImplicants:
  print("Don't cares: {0}".format(len(group)))
print("\n")

shouldRunReduceCycle = True
while shouldRunReduceCycle:
  for group in groupedImplicants:
    removeDuplicates(group)
  removeRedundantImplicants(groupedImplicants)
  findLargerImplicants(groupedImplicants)

for group in groupedImplicants:
  print("Don't cares: {0}".format(len(group)))
  #print("\n")
  #print(group)
  #print("\n")
print('Done')