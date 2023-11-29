# 汚れのjson＋元画像 ⇒ 汚れの付いた画像
# 予想結果のjsonを読み、画像にオーバーレイする

# 新しい色を指定 (BGR フォーマット)
#new_color = (0, 255, 0)  # 緑
#new_color = (255, 0, 0)  # 青
new_color = (0, 0, 255)  # 赤

import os
import json
import glob
import cv2
#import numpy as np

def stain(json_path, image_path, out_image_path):
  image = cv2.imread(image_path)

  with open(json_path) as f:
    d = json.load(f)
  for p in d['confidence_points']:
    class_list = p['class_list']
    confidence = list(filter(lambda item : item['class'] == 'plaque', class_list))[0]['confidence']
    print(p['x'], p['y'], confidence)
    if confidence >= 50:
      image[p['y'], p['x']] = new_color

  # 変更した画像を保存
  cv2.imwrite(out_image_path, image)

# メインの処理
jsonfiles = glob.glob("./out/*.json")
for jsonfile in jsonfiles:
  path, fileext = os.path.split(jsonfile)
  file = fileext[:fileext.rfind('.')]
  imagefile = os.path.join(path, file + '.jpg')
  outimagefile = os.path.join(path, 'o_' + file + '.jpg')
  stain(jsonfile, imagefile, outimagefile)
