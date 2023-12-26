# -*- coding: utf-8 -*-

# 汚れのjson＋元画像 ⇒ 汚れの付いた画像
# 予想結果のjsonを読み、画像にオーバーレイする

_result_dir = './result/*.json'
_org_img_dir = 'C:/vott/test200/img/'

# 新しい色を指定 (BGR フォーマット)
#new_color = (0, 255, 0)  # 緑
#new_color = (255, 0, 0)  # 青
new_color = (0, 0, 255)  # 赤

import os
import json
import glob
import cv2
#import numpy as np

def stain(json_path, image_path, org_image_path, out_image_path):
  image = cv2.imread(org_image_path)

  with open(json_path) as f:
    d = json.load(f)
  for p in d['confidence_points']:
    x = p['x'] - 1      # 1オリジン
    y = p['y'] - 1
    if x >= image.shape[1]:
      fileext = os.path.split(jsonfile)[1]
      print('error {} x={} y={}  {}x{}'.format(fileext, x, y, image.shape[1], image.shape[0]))
      continue
    if y >= image.shape[0]:
      fileext = os.path.split(jsonfile)[1]
      print('error {} x={} y={}  {}x{}'.format(fileext, x, y, image.shape[1], image.shape[0]))
      continue
    class_list = p['class_list']
    background = list(filter(lambda item : item['class'] == 'background', class_list))[0]['confidence']
    plaque = list(filter(lambda item : item['class'] == 'plaque', class_list))[0]['confidence']
    #print(x, y, background, plaque)
    #if confidence >= 50:
    if background < plaque:
      image[y, x] = new_color

  pdct = cv2.imread(image_path)
  mearged = cv2.hconcat([pdct, image])
  # 変更した画像を保存
  cv2.imwrite(out_image_path, mearged)

# メインの処理
jsonfiles = glob.glob(_result_dir)
for jsonfile in jsonfiles:
  print(jsonfile)
  path, fileext = os.path.split(jsonfile)
  file = fileext[:fileext.rfind('.')]
  org_img_file = os.path.join(_org_img_dir, file + '.jpg')
  img_file = os.path.join(path, file + '.jpg')
  out_img_file = os.path.join(path, 'o_' + file + '.jpg')
  stain(jsonfile, img_file, org_img_file, out_img_file)
