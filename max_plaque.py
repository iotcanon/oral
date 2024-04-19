# -*- coding: utf-8 -*-

# 点数をつけるのにどのようにするか？
# 「歯分割_IoU」に解析後の画像、IoUなどがあるのでそれを使って確認する

import glob
import json

_dir = './歯分割_IoU/'    # 最後に「/」を付けること

# CSVの集計は、csvsum.pyで行っている。

# jsonファイル中で一番高いplaqueを算出
jsonfiles = glob.glob(_dir + "*.json")
for jsonfile in jsonfiles:
  with open(jsonfile) as f:
    d = json.load(f)
    max_p = 0
  for p in d['confidence_points']:
    class_list = p['class_list']
    background = list(filter(lambda item : item['class'] == 'background', class_list))[0]['confidence']
    plaque = list(filter(lambda item : item['class'] == 'plaque', class_list))[0]['confidence']
    print('background', background, 'plaque', plaque)
    max_p = plaque if max_p < plaque else max_p
  print(jsonfile, max_p)
