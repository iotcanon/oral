# -*- coding: utf-8 -*-

# テスト用のデータを抽出
# アノテーションファイルの名前を画像ファイル名と同じにします

_img_dir = 'd:/hack/oral/2022/img/'   # 最後に「/」を付けること
_json_dir = 'd:/hack/oral/2022/'      # 最後に「/」を付けること
_out_dir = 'd:/hack/oral/2022/out/'               # 最後に「/」を付けること

# 2022年の110件の予備のテストデーt
data = [
  "00003",
  "00005",
  "00010",
  "00016",
  "00017",
  "00030",
  "00037",
  "00038",
  "00040",
  "00046",
  "00062",
  "00064",
  "00066",
  "00067",
  "00068",
  "00070",
  "00078",
  "00085",
  "00094",
  "00095",
  "00097",
  "00100",
  "00101",
  "00103",
  "00104",
  "00107",
  "00112",
  "00113",
  "00115",
  "00118",
  "00130",
  "00132",
  "00136",
  "00139",
  "00140",
  "00145",
  "00146",
  "00147",
  "00148",
  "00149",
  "00150",
  "00156",
  "00159",
  "00164",
  "00167",
  "00169",
  "00170",
  "00176",
  "00179",
  "00181",
  "00186",
  "00190",
  "00191",
  "00192",
  "00193",
  "00194",
  "00195",
  "00196",
  "00197",
  "00198",
  "00200",
  "00202",
  "00203",
  "00205",
  "00206",
  "00207",
  "00209",
  "00211",
  "00212",
  "00214",
  "00216",
  "00217",
  "00220",
  "00221",
  "00222",
  "00223",
  "00224",
  "00227",
  "00229",
  "00232",
  "00235",
  "00237",
  "00240",
  "00241",
  "00243",
  "00245",
  "00252",
  "00255",
  "00259",
  "00260",
  "00265",
  "00266",
  "00268",
  "00269",
  "00278",
  "00279",
  "00280",
  "00281",
  "00282",
  "00285",
  "00288",
  "00289",
  "00290",
  "00291",
  "00292",
  "00301",
  "00302",
  "00308",
  "00315",
  "00316",
]

# ９３件の予備のテストデーt
__data = [
  "01411",
  "01412",
  "01413",
  "01414",
  "01415",
  "01418",
  "01419",
  "01420",
  "01421",
  "01422",
  "01423",
  "01424",
  "01426",
  "01427",
  "01428",
  "01429",
  "01430",
  "01431",
  "01432",
  "01433",
  "01434",
  "01435",
  "01436",
  "01437",
  "01438",
  "01439",
  "01441",
  "01442",
  "01443",
  "01444",
  "01445",
  "01446",
  "01447",
  "01448",
  "01449",
  "01451",
  "01453",
  "01454",
  "01455",
  "01456",
  "01457",
  "01458",
  "01459",
  "01460",
  "01461",
  "01462",
  "01463",
  "01464",
  "01465",
  "01466",
  "01467",
  "01468",
  "01469",
  "01470",
  "01471",
  "01472",
  "01473",
  "01474",
  "01475",
  "01476",
  "01477",
  "01479",
  "01480",
  "01481",
  "01483",
  "01485",
  "01486",
  "01487",
  "01488",
  "01489",
  "01491",
  "01492",
  "01493",
  "01494",
  "01495",
  "01496",
  "01497",
  "01498",
  "01499",
  "01500",
  "01701",
  "01702",
  "01703",
  "01706",
  "01708",
  "01711",
  "01712",
  "01714",
  "01715",
  "01716",
  "01718",
  "01719",
  "01720",
]

# ２００件のテストデータ
_data = [
  "00489",
  "00490",
  "00491",
  "00492",
  "00493",
  "00494",
  "00495",
  "00496",
  "00497",
  "00499",
  "00500",
  "01501",
  "01502",
  "01503",
  "01504",
  "01505",
  "01506",
  "01507",
  "01508",
  "01509",
  "01510",
  "01511",
  "01512",
  "01513",
  "01514",
  "01515",
  "01516",
  "01517",
  "01518",
  "01519",
  "01520",
  "01521",
  "01523",
  "01524",
  "01525",
  "01526",
  "01527",
  "01528",
  "01529",
  "01530",
  "01531",
  "01532",
  "01533",
  "01534",
  "01535",
  "01536",
  "01537",
  "01538",
  "01539",
  "01540",
  "01541",
  "01542",
  "01543",
  "01544",
  "01546",
  "01548",
  "01549",
  "01550",
  "01551",
  "01552",
  "01553",
  "01554",
  "01555",
  "01556",
  "01557",
  "01558",
  "01559",
  "01560",
  "01561",
  "01562",
  "01563",
  "01564",
  "01566",
  "01567",
  "01568",
  "01570",
  "01571",
  "01572",
  "01573",
  "01574",
  "01575",
  "01576",
  "01577",
  "01578",
  "01579",
  "01580",
  "01581",
  "01582",
  "01583",
  "01584",
  "01585",
  "01586",
  "01587",
  "01588",
  "01589",
  "01590",
  "01591",
  "01592",
  "01593",
  "01594",
  "01595",
  "01596",
  "01597",
  "01598",
  "01599",
  "01600",
  "01601",
  "01602",
  "01603",
  "01604",
  "01605",
  "01606",
  "01607",
  "01608",
  "01609",
  "01610",
  "01611",
  "01612",
  "01613",
  "01614",
  "01615",
  "01616",
  "01617",
  "01618",
  "01619",
  "01620",
  "01621",
  "01622",
  "01623",
  "01625",
  "01626",
  "01627",
  "01628",
  "01629",
  "01630",
  "01631",
  "01632",
  "01633",
  "01634",
  "01635",
  "01636",
  "01637",
  "01638",
  "01639",
  "01640",
  "01641",
  "01642",
  "01643",
  "01644",
  "01645",
  "01646",
  "01647",
  "01648",
  "01649",
  "01650",
  "01651",
  "01652",
  "01653",
  "01654",
  "01655",
  "01656",
  "01657",
  "01658",
  "01659",
  "01660",
  "01661",
  "01662",
  "01663",
  "01664",
  "01666",
  "01667",
  "01668",
  "01669",
  "01670",
  "01671",
  "01674",
  "01675",
  "01676",
  "01677",
  "01678",
  "01679",
  "01680",
  "01681",
  "01682",
  "01683",
  "01684",
  "01685",
  "01686",
  "01687",
  "01688",
  "01689",
  "01690",
  "01691",
  "01692",
  "01694",
  "01696",
  "01697",
  "01698",
  "01699",
  "01700",    
]

import os
import json
import glob
import shutil

# メインの処理
jsonfiles = glob.glob(_json_dir + "*.json")
for jsonfile in jsonfiles:
  with open(jsonfile) as f:
    d = json.load(f)
  fname = d['asset']['name']
  name = os.path.splitext(fname)[0]
  if name in data:
    # 画像ファイルをコピー
    shutil.copy(_img_dir + fname, _out_dir + fname)
    # JSONファイルをコピー
    d['asset']['size']['width'] = int(d['asset']['size']['width'] / 2)
    shutil.copy(jsonfile, _out_dir + name + '.json')
    with open(_out_dir + name + '.json', 'w') as f:
      json.dump(d, f, indent=4)
    # コピーリスのから削除
    data.remove(name)

# コピー漏れの確認
for d in data:
  print(d)