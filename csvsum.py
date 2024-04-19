# -*- coding: utf-8 -*-

#_csv_dir = './result_iou/*.csv'
#_sumfile = 'sum.csv'
_csv_dir = './歯分割_IoU/*.csv'
_sumfile = '歯分割_IoU.csv'

import os
import glob
import json

def get_plaque(fname):
  with open(fname) as f:
    d = json.load(f)
    ret = 0
  for p in d['confidence_points']:
    class_list = p['class_list']
    background = list(filter(lambda item : item['class'] == 'background', class_list))[0]['confidence']
    plaque = list(filter(lambda item : item['class'] == 'plaque', class_list))[0]['confidence']
    #print('background', background, 'plaque', plaque)
    ret = plaque if ret < plaque else ret
  return ret

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
    base_name, extension = os.path.splitext(fileext)
    plaque = get_plaque(path + '/' + base_name + '.json');
    csv = readcsv(csvfile)
    if first:
      f.write('ファイル名,最大プラーク値,' + csv[0] + '\n')
      first = False
    f.write(fileext + ',' + str(plaque) + ',' + csv[1] + '\n')
