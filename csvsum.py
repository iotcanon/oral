# -*- coding: utf-8 -*-

_csv_dir = './csv/*.csv'
_sumfile = 'sum.csv'

import os
import glob

def read1line(fname):
  with open(fname) as f:
    return f.readline()

# メインの処理
with open(_sumfile, 'w') as f:
  csvfiles = glob.glob(_csv_dir)
  csvfiles.sort()
  #csvfiles.sort(reverse=True)
  for csvfile in csvfiles:
    path, fileext = os.path.split(csvfile)
    s = read1line(csvfile).strip()
    f.write(fileext + ',' + s + '\n')
