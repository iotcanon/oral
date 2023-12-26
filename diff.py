# Python, OpenCV, NumPyで画像を比較（完全一致か判定、差分取得など）
# https://note.nkmk.me/python-opencv-numpy-image-difference/

import cv2
import numpy as np

# 画像ファイルの比較、最大の違いを返す(0-255)
def diff(org, cur):
  im_org = cv2.imread(org)
  print(im_org.shape)

  im_cur = cv2.imread(cur)
  print(im_cur.shape)

  if im_org.shape[0] != im_cur.shape[0] or im_org.shape[1] != im_cur.shape[1] or im_org.shape[2] != im_cur.shape[2]:
    print('size error')
    return -1

  print(np.array_equal(im_org, im_cur))

  im_diff = im_org.astype(int) - im_cur.astype(int)
  ret = np.abs(im_diff).max()
  return ret

# 画像ファイルの比較、違いのファイルを出力して最大の違いを返す(0-255)
def diff2(org, cur, out):
  im_org = cv2.imread(org)
  print(im_org.shape)

  im_cur = cv2.imread(cur)
  print(im_cur.shape)

  if im_org.shape[0] != im_cur.shape[0] or im_org.shape[1] != im_cur.shape[1] or im_org.shape[2] != im_cur.shape[2]:
    print('size error')
    return -1
  
  print(np.array_equal(im_org, im_cur))

  im_diff = np.abs(im_org.astype(int) - im_cur.astype(int))
  ret = im_diff.max()

  im_diff_bin = (im_diff > 32) * 255
  cv2.imwrite(out, im_diff_bin)

  return ret


ret = diff('img/org.jpg', 'img/org.png')
print(ret)

ret = diff('img/org.jpg', 'img/png.jpg')
print(ret)

ret = diff2('img/IMG_0923.PNG', 'img/IMG_0924.PNG', 'img/IMG_092x.PNG')
print(ret)
