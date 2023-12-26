# -*- coding: utf-8 -*-

# テスト
# 指定のフォルダにファイルをコピーする

_vott_dir = './test200/'    # 最後に「/」を付けること
_img_dir = './test200/img/'      # 最後に「/」を付けること
_vott_file = 'test200.vott'
#_out_dir = '../plaque_detect/in_out_folder/watchdog/test_watchdog/'               # 最後に「/」を付けること
_out_dir = '../plaque_detect/in_out_folder/watchdog/test_watchdog_whole_iou/'               # 最後に「/」を付けること
#_out_dir = '../plaque_detect/in_out_folder/watchdog/test_watchdog_whole/'               # 最後に「/」を付けること
#_json_copy = False
_json_copy = True

'''
# 歯全体画像推論格納フォルダ
IMAGE_PATH = "in_out_folder/watchdog/test_watchdog/"
# 歯全体画像推論格納フォルダの出力先
SAVE_PATH = "in_out_folder/watchdog_output/result"
# 歯全体画像IoU算出格納フォルダ
IMAGE_IOU_PATH = "in_out_folder/watchdog/test_watchdog_iou/"
# 歯全体画像IoU算出格納フォルダの出力先
SAVE_IOU_PATH = "in_out_folder/watchdog_output/result_iou"
# 歯分割画像推論格納フォルダ
IMAGE_WHOLE_PATH = "in_out_folder/watchdog/test_watchdog_whole/"
# 歯分割画像推論格納フォルダの出力先
SAVE_WHOLE_PATH = "in_out_folder/watchdog_output/result_whole"
# 歯分割画像IoU算出格納フォルダ
IMAGE_WHOLE_IOU_PATH = "in_out_folder/watchdog/test_watchdog_whole_iou/"
# 歯分割画像IoU算出格納フォルダの出力先
SAVE_WHOLE_IOU_PATH = "in_out_folder/watchdog_output/result_whole_iou"
# 歯茎除去画像推論格納フォルダ
IMAGE_GUM_PATH = "in_out_folder/watchdog/test_watchdog_gum/"
# 歯茎除去画像推論格納フォルダの出力先
SAVE_GUM_PATH = "in_out_folder/watchdog_output/result_gum"
# 歯茎除去画像IoU算出格納フォルダ
IMAGE_GUM_IOU_PATH = "in_out_folder/watchdog/test_watchdog_gum_iou/"
# 歯茎除去画像IoU算出格納フォルダの出力先
SAVE_GUM_IOU_PATH = "in_out_folder/watchdog_output/result_gum_iou"
'''

import os
import time
import json
import shutil

# メインの処理、vottファイルを読み処理する
with open(_vott_dir + _vott_file) as f:
  d = json.load(f)
  for k, v in d['assets'].items():
    imgfile = v['name']
    # 画像ファイルをコピー
    shutil.copy(_img_dir + imgfile, _out_dir + imgfile)
    print('copy ', _img_dir + imgfile, _out_dir + imgfile)
    if _json_copy:
      # JSONファイルをコピー
      jsonfile = v['id'] + '-asset.json'
      path = os.path.splitext(imgfile)[0]
      shutil.copy(_vott_dir + jsonfile, _out_dir + path + '.json')
      print('copy ', _vott_dir + jsonfile, _out_dir + path + '.json')
    time.sleep(9)
    #input('Hit Enter > ')

