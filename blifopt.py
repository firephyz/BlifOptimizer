#!/usr/bin/env python3

import sys
import parseblif

if len(sys.argv) != 2:
  print('Usage: blifopt.py <blif_file>')
  sys.exit()

parser = parseblif.BlifParser(sys.argv[1])
blif = parser.parse()