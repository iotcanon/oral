# -*- coding: utf-8 -*-

# PythonのGUIライブラリ「Tkinter」を使って簡単な画像編集ツールを作ってみた
# https://iatom.hatenablog.com/entry/2020/11/01/151945

import os,sys
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

class image_gui():
    # 変数
    cdir = os.path.abspath(os.path.dirname(__file__))
    jsondir = None
    filepath = None
    purple = None
    red = None
    orange = None
    yellow = None
    input_canvas = None
    output_canvas = None
    #chg_out = None

    # 初期設定
    def __init__(self, main):
        # ファイル削除処理
        self.file_del()
        # 参照ボタン配置
        button1 = Button(root, text=u'JSONファイルのディレクトリ選択', command=self.dir_button_clicked)
        button1.grid(row=0, column=1)
        button1.place(x=470, y=3)

        button2 = Button(root, text=u'JPEGファイル選択', command=self.file_button_clicked)
        button2.grid(row=0, column=1)
        button2.place(x=470, y=32)

        # 閉じるボタン
        close1 = Button(root,text=u'閉じる',command=self.close_clicked)
        close1.grid(row=0,column=3)
        close1.place(x=690,y=3)

        # 描画ボタン
        paint1 = Button(root,text=u'汚れ描画',command=self.repaint)
        paint1.grid(row=0,column=3)
        paint1.place(x=680,y=32)

        # 参照ファイルパス表示ラベルの作成
        self.dir1 = StringVar()
        self.dir1_entry = ttk.Entry(root,textvariable=self.dir1, width=50)
        self.dir1_entry.grid(row=0, column=2)
        self.dir1_entry.place(x=12,y=10)
        self.file1 = StringVar()
        self.file1_entry = ttk.Entry(root,textvariable=self.file1, width=70)
        self.file1_entry.grid(row=0, column=2)
        self.file1_entry.place(x=12,y=35)

    # ファイルを削除
    def file_del(self):
        if os.path.exists("./output_image_small.png") == True:
            os.remove("./output_image_small.png")        
        if os.path.exists("./input_image.png") == True:
            os.remove("./input_image.png")

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
        # ガンマ補正用のスケールバーの設定
        self.purple = Scale(root, label='紫', orient='h',
                         from_=0, to=100,length=95, command=self.onSlider,resolution=1)
        self.purple.set(80)
        self.purple.place(x=335,y=60)
        # 彩度変更用のスケールバーの設定
        self.red = Scale(root, label='赤', orient='h',
                         from_=0, to=100,length=95, command=self.onSlider,resolution=1)
        self.red.set(60)
        self.red.place(x=335,y=130)
        # 明度変更用のスケールバーの設定
        self.orange = Scale(root, label='橙', orient='h',
                         from_=0, to=100,length=95, command=self.onSlider,resolution=1)
        self.orange.set(40)
        self.orange.place(x=335,y=200)
        #　ぼかしのスケールバーの設定
        self.yellow = Scale(root, label='黄', orient='h',
                         from_=0, to=100,length=95, command=self.onSlider,resolution=1)
        self.yellow.set(20)
        self.yellow.place(x=335,y=270)        
 
        # 画像ファイル読み込みと表示用画像サイズに変更と保存
        img = cv2.imread(self.filepath)
        #cv2.imwrite("input_image_file.jpeg",img)
        img2 = cv2.resize(img,dsize=(320,240))
        cv2.imwrite("input_image.png",img2)
    
        # 入力画像を画面に表示
        self.out_image = ImageTk.PhotoImage(file="input_image.png")
        input_canvas.create_image(163, 122, image=self.out_image)

    def onSlider(self,args):
        pass

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
        img2 = cv2.resize(i_out,dsize=(320,240))
        # 出力画像を保存
        cv2.imwrite("output_image_small.png",img2)
        # 画像をセット
        self.out_image2 = ImageTk.PhotoImage(file="output_image_small.png")
        output_canvas.create_image(160, 120, image=self.out_image2)

    def stain(self, json_path, image_path):
        image = cv2.imread(image_path)
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
            #if confidence >= 50:
            if background < plaque:
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

if __name__ == '__main__':
    root = Tk()
    root.title("Image Viewer")
    # GUI全体のフレームサイズ
    root.geometry("770x400")
    # 出力ファイル画像表示の場所指定とサイズ指定
    output_canvas = Canvas(root, width=320, height=240)
    output_canvas.place(x=440, y=90)
    #　入力ファイル画像表示の場所指定とサイズ指定
    input_canvas = Canvas(root, width=320, height=240)
    input_canvas.place(x=5, y=90)
    # GUI表示
    image_gui(root)
    root.mainloop()
