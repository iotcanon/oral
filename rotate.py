# 回転画像を作成
# vottプロジェクトごと変換するので、バックアップしておくこと

_vott_dir = './vott/'
_vott_file = 'iral-test.vott'

import json
import cv2

# 画像を回転
def rotate_img(fname):
  img = cv2.imread(fname)
  print(img.shape)
  img90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
  print(img90.shape)
  cv2.imwrite(fname, img90)

# asset.jsonファイルを回転
def rotate_asset(fname):
  with open(fname) as f:
    d = json.load(f)

  # 画像サイズ
  width = d['asset']['size']['width']
  height = d['asset']['size']['height']
  d['asset']['size']['width'] = height
  d['asset']['size']['height'] = width

  # 各リージョン
  for r in d['regions']:
    b_height = r['boundingBox']['height']
    b_width = r['boundingBox']['width']
    b_left = r['boundingBox']['left']
    b_top = r['boundingBox']['top']
    r['boundingBox']['height'] = b_width
    r['boundingBox']['width'] = b_height
    r['boundingBox']['left'] = height - b_top - b_height
    r['boundingBox']['top'] = b_left

    for p in r['points']:
      x = p['x']
      y = p['y']
      p['x'] = height - y
      p['y'] = x

  with open(fname, 'w') as f:
    json.dump(d, f, indent=4)

# メインの処理、vottファイルを読み処理する
with open(_vott_dir + _vott_file) as f:
  d = json.load(f)
  for k, v in d['assets'].items():
    # 画像ファイルを回転
    imgfile = v['path'][5:]
    rotate_img(imgfile)
    # asset.jsonを回転
    jsonfile = _vott_dir + k + '-asset.json'
    rotate_asset(jsonfile)
    width = v['size']['width']
    height = v['size']['height']
    v['size']['width'] = height
    v['size']['height'] = width

  with open(_vott_dir + _vott_file, 'w') as f:
    json.dump(d, f, indent=4)
