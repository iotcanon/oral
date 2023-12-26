# -*- coding: utf-8 -*-

# Python+Tkinterで作る画像ビューワ
# https://qiita.com/takimotoseiji/items/a70ae15e1d8dbd858d5c

import tkinter
import glob
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk


# 各種定数宣言
INT_COLUMN_COUNTS = 5
INT_PICTURE_SIZE = 200

# ボタンが押下された時の処理
def click_button_get(event):
    # ビューワで表示する画像のパスを取得
    # 今回はjpgファイルで固定
    pictures = glob.glob(file_edit.get() + "\\*.jpg")
    if len(pictures) == 0 :
        print("対象ディレクトリ、画像が存在しません")
        return 0 
    # リストの初期化
    picture_list = []
    for picture in pictures:
        picture_list.append(picture)
    show_pictures(scroll_canvas, picture_list)

# 取得した画像を表示
def show_pictures(canvas, picture_path):
    canvas.delete('all')

    for index, file_name in enumerate(picture_path):
        img = arrange_image(file_name)
        img = ImageTk.PhotoImage(image=img)
        row_no =  int(index / INT_COLUMN_COUNTS)
        column_no = int(index % INT_COLUMN_COUNTS)
        canvas.create_image(column_no * INT_PICTURE_SIZE , row_no * INT_PICTURE_SIZE, anchor='nw', image=img)
        # 画像を配置
        img_list.append(img)

# 指定のサイズにファイルを成形
def arrange_image(file_name):
    img = Image.open(file_name)
    img_width, img_height = img.size
    reducation_size =  img_width if img_width >= img_height else img_height
    return img.resize(( int( img_width * (INT_PICTURE_SIZE/reducation_size)), int(img_height * (INT_PICTURE_SIZE/reducation_size)) ))

# メインウインドウ
window = tkinter.Tk()
window.geometry("1100x600")     
window.title("PictureViewer")

# ガベコレに消されないようにイメージリストに画像を入れておく用のリスト
img_list = []

# メインフレーム
## input_frame
input_frame = tkinter.Frame(window, width=1100, height=100, bg='black')
input_frame.pack()

## output_frame
output_frame = tkinter.Frame(window, width=1100, height=500, bg='yellow')
output_frame.pack()

# 画像表示用のcanvasを作成
scroll_canvas = tkinter.Canvas(output_frame, width=1050, height=500, bg='red')
scroll_canvas.grid(column=0, row=0)
bar = tkinter.Scrollbar(output_frame, orient=tkinter.VERTICAL)
bar.grid(column=1, row=0, sticky='ns')
bar.config(command=scroll_canvas.yview)
scroll_canvas.config(yscrollcommand=bar.set)
# scroll_canvasの表示範囲
scroll_canvas.config(scrollregion=(0, 0, 1100, 1200))

# ウイジェット設定
## input_frame
file_label = ttk.Label(input_frame, text='パス')
file_edit = ttk.Entry(input_frame)
file_btn = ttk.Button(input_frame, text='取得')

# ボタンにイベントをバインド
file_btn.bind('<Button-1>', click_button_get)

# ウィジェット配置
## input_frame
file_label.grid(column=0, row=0, pady=10, padx=5)
file_edit.grid(column=1, row=0, sticky=tkinter.EW, padx=5)
file_btn.grid(column=2, row=0, padx=5)

window.mainloop()
