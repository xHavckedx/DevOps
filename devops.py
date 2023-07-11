import sys
import os

if len(sys.argv) >= 2:
  arg1 = sys.argv[1]
  if arg1 == 'restart':
    if len(sys.argv) >= 3:
      if sys.argv[2] in  ['stg', 'prod', 'mstg', 'mpro']:
        arg2 = sys.argv[2]
        os.system(f"restart {arg2}")
    else:
      print(f"Agrega un entorno: [stg | pro | mstg | mpro]")
exit()
