# -*- coding: utf-8 -*-

#_csv_dir = './result_iou/*.csv'
#_sumfile = 'sum.csv'
_csv_dir = './歯分割_IoU/*.csv'
_sumfile = '歯分割_IoU.csv'

import os
import glob

def readcsv(fname, encoding='shift_jis'):
  with open(fname) as f:
    l1 = f.readline().strip()
    l2 = f.readline().strip()
    return [l1, l2]

# メインの処理
with open(_sumfile, 'w', encoding='shift_jis') as f:
  csvfiles = glob.glob(_csv_dir)
  csvfiles.sort()
  #csvfiles.sort(reverse=True)
  first = True
  for csvfile in csvfiles:
    path, fileext = os.path.split(csvfile)
    csv = readcsv(csvfile)
    if first:
      f.write('ファイル名,' + csv[0] + '\n')
      first = False
    f.write(fileext + ',' + csv[1] + '\n')
