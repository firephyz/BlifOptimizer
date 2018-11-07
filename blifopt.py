#!/usr/bin/env python3

import sys
import parseblif

def removeDuplicates(implicants):
  removals = []
  for i in range(len(implicants)):
    for j in range(i + 1, len(implicants)):
      if implicants[i] == implicants[j]:
        if implicants[i] not in removals: removals.append(implicants[i])
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
  """Combines two implicants."""
  hasDiff = False
  diffIndex = -1
  doesCover = False
  primaryImplicant = None
  secondaryImplicant = None
  if countDontCares(impA) >= countDontCares(impB):
    primaryImplicant = impA
    secondaryImplicant = impB
  elif countDontCares(impA) < countDontCares(impB):
    primaryImplicant = impB
    secondaryImplicant = impA
  
  for i in range(len(impA)):
    if impA[i] != impB[i]:
      if secondaryImplicant[i] == '-':
        return None
      elif primaryImplicant[i] == '-':
        if hasDiff:
          return None
        else:
          doesCover = True
      else:
        if hasDiff:
          return None
        elif primaryImplicant[i] != '-':
          if doesCover:
            return None
          else:
            diffIndex = i
            hasDiff = True
  if hasDiff:
    return primaryImplicant[:diffIndex] + '-' + primaryImplicant[diffIndex + 1:]
  else:
    return primaryImplicant

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
      # Combine in the current group
      for j in range(i + 1, len(group)):
        result = combineImplicants(group[i], group[j])
        if result != None:
          if not didChange: didChange = True
          if result == group[i]:
            if group[i] not in removals:
              removals.append(group[i])
              print('REMOVED:')
              print('{0} {1}'.format(groupIndex, group[i]))
          else:
            if group[i] not in removals:
              removals.append(group[i])
            if group[j] not in removals:
              removals.append(group[j])
            
            # Add new implicant to the groups
            if groupIndex + 1 == len(groups):
              groups.append([])
            
            groups[groupIndex + 1].append(result)
            print('REMOVED:')
            print('{0} {1}'.format(groupIndex, group[i]))
            print('{0} {1}'.format(groupIndex, group[j]))
            print('ADDED:')
            print('{0} {1}'.format(groupIndex + 1, result))
      # Combine with the group above
      for j in range(1, len(groups) - groupIndex):
        nextRemovals = []
        for imp in groups[groupIndex + j]:
          result = combineImplicants(group[i], imp)
          if result != None:
            if result == imp:
              if group[i] not in removals:
                removals.append(group[i])
                print('REMOVED:')
                print('{0} {1}'.format(groupIndex, group[i]))
            else:
              if not didChange: didChange = True
              if group[i] not in removals:
                removals.append(group[i])
              if imp not in nextRemovals:
                nextRemovals.append(imp)

              if groupIndex + 1 + j == len(groups):
                groups.append([])

              groups[groupIndex + 1 + j].append(result)
              print('REMOVED:')
              print('{0} {1}'.format(groupIndex, group[i]))
              print('{0} {1}'.format(groupIndex + j, imp))
              print('ADDED:')
              print('{0} {1}'.format(groupIndex + 1 + j, result))
        for elem in nextRemovals:
          groups[groupIndex + j].remove(elem)
    for elem in removals:
      group.remove(elem)
    removals = []
  if not didChange: shouldRunReduceCycle = False

def printGroups():
  print('RESULTS:')
  for group in groupedImplicants:
    print("Don't cares: {0}".format(len(group)))
    print(group)

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
  for group in groupedImplicants:
    removeDuplicates(group)
  removeRedundantImplicants(groupedImplicants)
  findLargerImplicants(groupedImplicants)

printGroups()