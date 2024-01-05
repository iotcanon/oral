# -*- coding: utf-8 -*-

# PythonのGUIライブラリ「Tkinter」を使って簡単な画像編集ツールを作ってみた
# https://iatom.hatenablog.com/entry/2020/11/01/151945

import os
import sys
import json
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import subprocess
import numpy as np
import shutil

color_purple = (128, 0, 128)  # 紫
color_red = (0, 0, 255)  # 赤
color_orange = (0, 165, 255)  # 橙
color_yellow = (0, 255, 255)  # 黄

IN_IMG_FILE = "./$output_image.png"
OUT_IMG_FILE = "./$input_image.png"
CANVAS_W = 320
CANVAS_H = 440

class image_gui():
    # 変数
    #cdir = os.path.abspath(os.path.dirname(__file__))
    cdir = os.path.dirname(os.path.abspath(sys.argv[0]))
    jsondir = None
    filepath = None
    purple = None
    red = None
    orange = None
    yellow = None
    input_canvas = None
    output_canvas = None
    #chg_out = None

    # imreadが日本語のパスに未対応の為
    def imread(self, filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
        try:
            n = np.fromfile(filename, dtype)
            img = cv2.imdecode(n, flags)
            return img
        except Exception as e:
            print(e)
            return None
        
    # 初期設定
    def __init__(self, main):
        # ファイル削除処理
        self.file_del()
        # 参照ボタン配置
        button1 = Button(root, text = 'JSONファイルのディレクトリ選択', command = self.dir_button_clicked)
        button1.grid(row=0, column=1)
        button1.place(x = 570, y = 3)

        button2 = Button(root, text = 'JPEGファイル選択', command=self.file_button_clicked)
        button2.grid(row=0, column = 1)
        button2.place(x = 570, y = 32)

        # 閉じるボタン
        close1 = Button(root, text= '閉じる', command = self.close_clicked)
        close1.grid(row = 0, column = 3)
        close1.place(x = 790, y = 3)

        # 描画ボタン
        paint1 = Button(root, text = '汚れ描画', command = self.repaint)
        paint1.grid(row = 0, column = 3)
        paint1.place(x = 780, y = 32)

        # 参照ファイルパス表示ラベルの作成
        self.dir1 = StringVar()
        self.dir1_entry = ttk.Entry(root, textvariable = self.dir1, width = 70)
        self.dir1_entry.grid(row = 0, column = 2)
        self.dir1_entry.place(x = 12, y = 10)
        self.file1 = StringVar()
        self.file1_entry = ttk.Entry(root, textvariable=self.file1, width = 90)
        self.file1_entry.grid(row=0, column = 2)
        self.file1_entry.place(x = 12,y = 35)

    # ファイルを削除
    def file_del(self):
        if os.path.exists(IN_IMG_FILE) == True:
            os.remove(IN_IMG_FILE)        
        if os.path.exists(OUT_IMG_FILE) == True:
            os.remove(OUT_IMG_FILE)

    # フォームを閉じる
    def close_clicked(self):
        # メッセージ出力
        res = messagebox.askokcancel("確認", "フォームを閉じますか？")
        #　フォームを閉じない場合
        if res != True:
            # 処理終了
            return        

        #不要ファイル削除
        self.file_del()
        #処理終了
        sys.exit()

    # ディレクトリ参照ボタンクリック時に起動するメソッド
    def dir_button_clicked(self):
        # 選択したディレクトリを取得
        jsondir = filedialog.askdirectory(initialdir = self.cdir)
        # ファイル選択指定なし？
        if jsondir == "":
            messagebox.showinfo('エラー', '選択されていません')
            return
        self.jsondir = jsondir
        self.cdir = self.jsondir
        # 選択したパス情報を設定    
        self.dir1.set(self.jsondir)
        if self.filepath:
            self.image_changed()

    # ファイル参照ボタンクリック時に起動するメソッド
    def file_button_clicked(self):
        # ファイル種類のフィルタ指定とファイルパス取得と表示（今回はjpeg)
        fTyp = [("画像ファイル","*.jpeg"),("画像ファイル","*.jpg")]
        # 選択したファイルのパスを取得
        filepath = filedialog.askopenfilename(filetypes = fTyp,initialdir = self.cdir)
        # ファイル選択指定なし？
        if filepath == "":
            messagebox.showinfo('エラー', '選択されていません')
            return
        self.filepath = filepath
        self.cdir = os.path.dirname(self.filepath)
        # 選択したパス情報を設定    
        self.file1.set(self.filepath)
        if self.jsondir:
            self.image_changed()

    # 参照ボタンクリック時に起動するメソッド
    def image_changed(self):
        # 紫のスケールバーの設定
        self.purple = Scale(root, label = '紫', orient = 'h',
                         from_ = 0, to = 100, length = 195, command=self.onSlider, resolution = 1)
        self.purple.set(80)
        self.purple.place(x=335,y=60)
        # 赤のスケールバーの設定
        self.red = Scale(root, label = '赤', orient = 'h',
                         from_ = 0, to = 100, length = 195, command = self.onSlider, resolution = 1)
        self.red.set(60)
        self.red.place(x = 335, y = 130)
        # 橙のスケールバーの設定
        self.orange = Scale(root, label = '橙', orient = 'h',
                         from_ = 0, to = 100, length = 195, command = self.onSlider, resolution = 1)
        self.orange.set(40)
        self.orange.place(x = 335, y = 200)
        # 黄のスケールバーの設定
        self.yellow = Scale(root, label = '黄', orient = 'h',
                         from_ = 0, to = 100, length = 195, command = self.onSlider, resolution = 1)
        self.yellow.set(20)
        self.yellow.place(x = 335, y = 270)
        # チェックボックス
        self.checkvar = BooleanVar()
        self.check = Checkbutton(text = '背景比較しない', variable = self.checkvar)
        self.check.place(x = 335, y = 400)
 
        # 画像ファイル読み込みと表示用画像サイズに変更と保存
        img = self.imread(self.filepath)
        img2 = self.resize(img, CANVAS_W, CANVAS_H)
        cv2.imwrite(OUT_IMG_FILE, img2)
    
        # 入力画像を画面に表示
        self.input_image = ImageTk.PhotoImage(file = OUT_IMG_FILE)
        print('input shape', self.input_image.width(), self.input_image.height())
        input_canvas.create_image(0, 0, image = self.input_image, anchor="nw")

    def onSlider(self, args):
        pass

    # 汚れを描画
    def repaint(self):
        if not self.filepath or not self.jsondir:
            return
        # JSONファイル名の作成
        name = os.path.splitext(os.path.basename(self.filepath))[0]
        jsonpath = os.path.join(self.jsondir, name + '.json')
        if not os.path.exists(jsonpath):
            messagebox.showinfo('エラー', '指定のディレクトリにJSONファイルがありません')
            return
        # 汚れを書く
        i_out = self.stain(jsonpath, self.filepath)

        # 表示用に画像サイズを小さくする
        img2 = self.resize(i_out, CANVAS_W, CANVAS_H)
        # 出力画像を保存
        cv2.imwrite(IN_IMG_FILE, img2)
        # 画像をセット
        self.out_image = ImageTk.PhotoImage(file = IN_IMG_FILE)
        print('output shape', self.out_image.width(), self.out_image.height())
        output_canvas.create_image(0, 0, image = self.out_image, anchor="nw")

    def stain(self, json_path, image_path):
        image = self.imread(image_path)
        with open(json_path) as f:
            d = json.load(f)
        for p in d['confidence_points']:
            x = p['x'] - 1      # 1オリジン
            y = p['y'] - 1
            if x >= image.shape[1]:
                continue
            if y >= image.shape[0]:
                continue
            class_list = p['class_list']
            background = list(filter(lambda item : item['class'] == 'background', class_list))[0]['confidence']
            plaque = list(filter(lambda item : item['class'] == 'plaque', class_list))[0]['confidence']
            #print(x, y, background, plaque)
            if background < plaque or self.checkvar.get():
                if self.purple.get() < plaque:
                    image[y, x] = color_purple
                elif self.red.get() < plaque:
                    image[y, x] = color_red
                elif self.orange.get() < plaque:
                    image[y, x] = color_orange
                elif self.yellow.get() < plaque:
                    image[y, x] = color_yellow
                else:
                    pass
        return image

    def resize(self, img, width, height):
        h, w = img.shape[:2]
        aspect = w / h
        if width / height >= aspect:
            nh = height
            nw = round(nh * aspect)
        else:
            nw = width
            nh = round(nw / aspect)
        dst = cv2.resize(img, dsize=(nw, nh))
        print('resize', nw, nh)
        return dst

if __name__ == '__main__':
    root = Tk()
    root.title("汚れシミュレーション")
    # GUI全体のフレームサイズ
    root.geometry("870x550")
    # 出力ファイル画像表示の場所指定とサイズ指定
    output_canvas = Canvas(root, width = CANVAS_W, height = CANVAS_H, bg='#DDD')
    output_canvas.place(x = 540, y = 90)
    #　入力ファイル画像表示の場所指定とサイズ指定
    input_canvas = Canvas(root, width = CANVAS_W, height = CANVAS_H, bg='#DDD')
    input_canvas.place(x = 5, y = 90)
    # GUI表示
    image_gui(root)
    root.mainloop()
