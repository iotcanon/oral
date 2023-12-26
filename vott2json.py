# -*- coding: utf-8 -*-

# vottファイルから-asset.jsonファイルを作成
# vottファイルは既にエントリができていること、
# 指定のディレクトリにある-asset.jsonファイルをコピーリネームする

_vott_dir = 'c:/vott/test200/'    # 最後に「/」を付けること
_vott_file = 'test200.vott'
_json_dir = 'd:/hack/oral/out2/'      # 最後に「/」を付けること
_img_dir = 'C:/vott/test200/img/'      # 最後に「/」を付けること

import os
import json

# -asset.jsonファイルをコピーして作成
def cp_json(src, id):
  with open(src) as f:
    d = json.load(f)
  d['asset']['id'] = id
  d['asset']['path'] = 'file:' + _img_dir + d['asset']['name']
  with open(_vott_dir + id + '-asset.json', 'w') as f:
    json.dump(d, f, indent=4)

# メインの処理
with open(_vott_dir + _vott_file) as f:
  d = json.load(f)
  for k, v in d['assets'].items(): 
    id = v['id']
    name = os.path.splitext(v['name'])[0]
    cp_json(_json_dir + name + '.json', id)
