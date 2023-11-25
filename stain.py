# 汚れのjson＋元画像 ⇒ 汚れの付いた画像

# 予想結果のjsonを読み、画像にオーバーレイする

import cv2
#import numpy as np

# 画像の読み込み
image_path = 'para.jpg'
image = cv2.imread(image_path)

# 特定のピクセルの座標を指定
x, y = 100, 100

# 新しい色を指定 (BGR フォーマット)
#new_color = (0, 255, 0)  # 緑
#new_color = (255, 0, 0)  # 青
new_color = (0, 0, 255)  # 赤

for x in range(100, 100+ x ):
  # 特定のピクセルの色を変更
  image[y, x] = new_color

# 変更した画像を保存
cv2.imwrite('para-2.jpg', image)
