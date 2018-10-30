#!/usr/bin/env python3

import sys
import random

def binaryNumGen(maxNum):
    num = 0
    while num < maxNum:
        if random.random() > 0.8:
            yield num
        num += 1

def addDontCares(numString):
    numDontCares = int(0.5 * random.random() * numInputs)
    dontCareIndicies = random.sample(range(numInputs), numDontCares)
    dontCareIndicies.sort()
    dontCareIndex = 0
    result = []
    for i in range(len(numString)):
        if len(dontCareIndicies) != 0 and dontCareIndex < numDontCares and i == dontCareIndicies[dontCareIndex]:
            result.append('-')
            dontCareIndex += 1
        else:
            result.append(numString[i])
    return ''.join(result)

def genOutputTable():
    result = ''
    numGenerator = binaryNumGen(2**numInputs)
    for i in numGenerator:
        result += addDontCares(format(i, f'0{numInputs}b'))
        result += ' 1\n'
    return result

if len(sys.argv) == 1:
    print("Usage: gen-blif.py <input_size> (optional)<seed>")
    sys.exit()

numInputs = int(sys.argv[1])
seed = None
if len(sys.argv) == 3:
    seed = int(sys.argv[2])

random.seed(seed)

outputFile = open('output.blif', 'w+')

# Generate input declaration line
inputDeclLine = ''
for i in range(0, numInputs):
    inputDeclLine += ' in{0}'.format(i)

# Write the blif file header
outputFile.write(f"""\
.model test
.inputs{inputDeclLine}
.outputs out

.names{inputDeclLine} out
""")

# Generate output table
blifOutTable = genOutputTable()
outputFile.write(blifOutTable)
outputFile.write("\n.end")
    
outputFile.close()
