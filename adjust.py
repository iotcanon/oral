# -*- coding: utf-8 -*-

# vottをディレクトリ毎コピーした場合、vottファイルと-asset.jsonの関連が外れるので修正する
# vottファイルは既にエントリができていること、
# 

_vott_dir = 'c:/vott/test200r/'    # 最後に「/」を付けること
_img_dir = 'C:/vott/test200r/img/'      # 最後に「/」を付けること
_vott_file = 'test200r.vott'

import os
import json
import glob

tbl = {}

# メインの処理
with open(_vott_dir + _vott_file) as f:
  d = json.load(f)
  for k, v in d['assets'].items(): 
    id = v['id']
    name = v['name']
    tbl[name] = id
 
jsonfiles = glob.glob(_vott_dir + "*.json")
for jsonfile in jsonfiles:
  with open(jsonfile) as f:
    d = json.load(f)
    name = d['asset']['name']
    d['asset']['id'] = tbl[name]
    d['asset']['path'] = 'file:' + _img_dir + name
  os.remove(jsonfile)
  jsonfile = _vott_dir + d['asset']['id'] + '-asset.json'
  with open(jsonfile, 'w') as f:
    json.dump(d, f, indent=4)


