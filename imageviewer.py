# -*- coding: utf-8 -*-

# PythonのGUIライブラリ「Tkinter」を使って簡単な画像編集ツールを作ってみた
# https://iatom.hatenablog.com/entry/2020/11/01/151945

import os,sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import subprocess
import numpy as np
import shutil

# 顔検出インスタンス生成
cascadePath = '/Users/local/source/opencv/face_recognition/data_xml/haarcascade_frontalface_alt2.xml'
faceCascade = cv2.CascadeClassifier(cascadePath)

# 目検出インスタンス生成
eye_cascadePath = '/Users/local/source/opencv/face_recognition/data_xml/haarcascade_eye.xml'
eye_cascade = cv2.CascadeClassifier(eye_cascadePath)

class image_gui():

    # 変数
    filepath = None
    gamma = None
    Brightness = None
    Saturation= None
    Gaussian = None
    input_canvas = None
    output_canvas = None
    chg_out = None

    ##############
    #   初期設定  #
    ##############
    def __init__(self, main):
        # ファイル削除処理
        self.file_del()
        # 参照ボタン配置
        button1 = Button(root, text=u'参照', command=self.button1_clicked)
        button1.grid(row=0, column=1)
        button1.place(x=670, y=12)

        # 閉じるボタン
        close1 = Button(root,text=u'閉じる',command=self.close_clicked)
        close1.grid(row=0,column=3)
        close1.place(x=715,y=12)

        # 参照ファイルパス表示ラベルの作成
        self.file1 = StringVar()
        self.file1_entry = ttk.Entry(root,textvariable=self.file1, width=70)
        self.file1_entry.grid(row=0, column=2)
        self.file1_entry.place(x=12,y=10)

    ##########################
    # ファイルを削除するメソッド #
    ##########################
    def file_del(self):
        if os.path.exists("./output_image_small.png") == True:
            os.remove("./output_image_small.png")        
        if os.path.exists("./output_image.jpeg") == True:
            os.remove("./output_image.jpeg")        
        if os.path.exists("./output_object_image.jpeg") == True:
            os.remove("./output_object_image.jpeg")
        if os.path.exists("./input_image.png") == True:
            os.remove("./input_image.png")
        if os.path.exists("./input_image_file.jpeg") == True:
            os.remove("./input_image_file.jpeg") 

    ########################
    # フォームを閉じるメソッド #
    ########################
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

    ####################################
    # 参照ボタンクリック時に起動するメソッド #
    ####################################
    def button1_clicked(self):
        # ファイル種類のフィルタ指定とファイルパス取得と表示（今回はjpeg)
        fTyp = [("画像ファイル","*.jpeg"),("画像ファイル","*.jpg")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        # 選択したファイルのパスを取得
        self.filepath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        # ファイル選択指定なし？
        if self.filepath == "":
            return
        # 選択したパス情報を設定    
        self.file1.set(self.filepath)

        # 顔モザイク実施するボタンの生成と配置
        self.button2 = Button(root,text=u"顔モザイク ON", command=self.mosaic_clicked,width=10)
        self.button2.grid(row=0, column=3)
        self.button2.place(x=340, y=45)

        # 顔検出を実施するボタンの生成と配置
        self.button3 = Button(root, text=u"顔検出 ON", command=self.face_clicked,width=10)
        self.button3.grid(row=0, column=3)
        self.button3.place(x=340, y=75)

       # 顔検出を実施するボタンの生成と配置
        self.button4 = Button(root, text=u"目検出 ON", command=self.eye_clicked,width=10)
        self.button4.grid(row=0, column=3)
        self.button4.place(x=340, y=105)

        # 物体検知を実施するボタンの生成と配置
        self.button5 = Button(root,text=u"物体検知 ON", command=self.object_detection_clicked,width=10)
        self.button5.grid(row=0, column=3)
        self.button5.place(x=340, y=135)
 
        # 画像を保存を実施するボタンの生成と配置
        self.button6 = Button(root,text=u"画像保存", command=self.save_clicked,width=10)
        self.button6.grid(row=0, column=3)
        self.button6.place(x=665, y=45)

        # ガンマ補正用のスケールバーの設定
        self.gamma = Scale(root, label='ガンマ補正', orient='h',
                         from_=1.0, to=3.0,length=95, command=self.onSlider,resolution=0.1)
        self.gamma.place(x=340,y=160)
        # 彩度変更用のスケールバーの設定
        self.Saturation = Scale(root, label='彩度倍率', orient='h',
                         from_=0.0, to=1.0,length=95, command=self.onSlider,resolution=0.1)
        self.Saturation.set(1.0)  
        self.Saturation.place(x=340,y=215)
        # 明度変更用のスケールバーの設定
        self.Brightness = Scale(root, label='明度倍率', orient='h',
                         from_=0.0, to=1.0,length=95, command=self.onSlider,resolution=0.1)
        self.Brightness.set(1.0)  
        self.Brightness.place(x=340,y=270)
        #　ぼかしのスケールバーの設定
        self.Gaussian = Scale(root, label='ぼかし', orient='h',
                         from_=0, to=10,length=95, command=self.onSlider,resolution=1)
        # Gaussianfilterのカーネル値は奇数値のみだが、どうもresolution=2刻みにすると
        # 初期値が2で、2刻みになってしまう。したがってスケール上は1刻みで表示で
        # 奇数値になるように計算で行うことにする。
        self.Gaussian.set(0)  
        self.Gaussian.place(x=340,y=325)        
 
        # 画像ファイル読み込みと表示用画像サイズに変更と保存
        img = cv2.imread(self.filepath)
        cv2.imwrite("input_image_file.jpeg",img)
        img2 = cv2.resize(img,dsize=(320,240))
        cv2.imwrite("input_image.png",img2)
    
        # 入力画像を画面に表示
        self.out_image = ImageTk.PhotoImage(file="input_image.png")
        input_canvas.create_image(163, 122, image=self.out_image)

    ##################################
    # 画像保存ボタンクリック時のメソッド #
    ##################################
    def save_clicked(self):
        # ファイル種類
        f_type = [('画像ファイル', '*.jpeg'), ('画像ファイル', '*.jpg')]
        # 実行中のフォルダパス取得
        ini_dir = os.getcwd()
        # ファイル保存のダイアログ出力
        filepath = filedialog.asksaveasfilename(filetypes=f_type , initialdir=ini_dir, title='名前をつけて保存')
        # ファイル名を取得
        filename = os.path.basename(filepath)
        # ファイルを保存
        if filepath:
            # ファイルを書き込みで開く
            with open(filepath, "w", encoding="utf_8") as f:
                len = f.write(filename)
        else:
            return

        # 編集した画像ファイルがあるか確認する
        if os.path.exists("./output_image.jpeg") == True:            
            # 編集した画像ファイルを、ダイアログで指定したファイルへコピーする
            shutil.copyfile("./output_image.jpeg", filepath)
        else:
            # 編集画像が無いので、入力した画像ファイルで保存する。
            shutil.copyfile("./input_image_file.jpeg", filepath)

    ##################################
    # 顔モザイクONのボタンクリック時の処理 #
    ##################################
    def mosaic_clicked(self):
        # 出力ファイルなし
        if os.path.exists("./output_image.jpeg") == False:
            # 入力ファイルの読み出し
            img = cv2.imread(self.filepath)
        else:
            # 作成済みの出力ファイル
            img = cv2.imread("./output_image.jpeg")

        img = self.face_detect_mosaic(img)
        # 表示用に画像サイズを小さくする
        img2 = cv2.resize(img,dsize=(320,240))
        # 出力画像を保存
        cv2.imwrite("output_mosaic_image.png",img2)
        # 画像をセット
        self.out_image2 = ImageTk.PhotoImage(file="output_mosaic_image.png")
        output_canvas.create_image(160, 120, image=self.out_image2)
        # ファイル削除
        os.remove("./output_mosaic_image.png")

    ##############################
    # 顔検出ONボタンクリック時の処理 #
    ##############################
    def face_clicked(self):
        # 出力ファイルなし
        if os.path.exists("./output_image.jpeg") == False:
            # 入力ファイルの読み出し
            img = cv2.imread(self.filepath)
        else:
            # 作成済みの出力ファイル
            img = cv2.imread("./output_image.jpeg")
        # 顔検出と描画する
        img = self.face_detect(img)            
        # 表示用に画像サイズを小さくする
        img2 = cv2.resize(img,dsize=(320,240))
        # 出力画像を保存
        cv2.imwrite("output_facerectangle_image.png",img2)
        # 画像をセット
        self.out_image3 = ImageTk.PhotoImage(file="output_facerectangle_image.png")
        output_canvas.create_image(160, 120, image=self.out_image3)
        os.remove("./output_facerectangle_image.png")

    ##################################
    ## 目検出ONボタンクリック時メソッド ###
    ##################################
    def eye_clicked(self):
        # 出力ファイルなし
        if os.path.exists("./output_image.jpeg") == False:
            # 入力ファイルの読み出し
            img = cv2.imread(self.filepath)
        else:
            # 作成済みの出力ファイル
            img = cv2.imread("./output_image.jpeg")
        # 目検出し描画する
        img = self.eye_detect(img)
        # 表示用に画像サイズを小さくする
        img2 = cv2.resize(img,dsize=(320,240))
        # 出力画像を保存
        cv2.imwrite("output_eyerectangle_image.png",img2)
        # 画像をセット
        self.out_image4 = ImageTk.PhotoImage(file="output_eyerectangle_image.png")
        output_canvas.create_image(160, 120, image=self.out_image4)
        os.remove("./output_eyerectangle_image.png")

    ##########################
    # 目検出した箇所を矩型で描画 #
    ##########################
    def eye_detect(self,img):
        # グレースケールに変換
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # 顔検出
        faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 3,
                minSize = (10, 10)
            )
        # 顔検出箇所に矩型描画のためのループ
        for(x,y,w,h) in faces:
        # 顔の上半分を検出対象範囲とする
            eyes_gray = gray[y : y + int(h/2), x : x + w]
            ################
            # 目検出        #
            ################
            eyes = eye_cascade.detectMultiScale(
                eyes_gray, 
                scaleFactor=1.11, 
                minNeighbors=3, 
                minSize=(4, 4))

            # 目検出した箇所を四角で描画
            for ex, ey, ew, eh in eyes:
                cv2.rectangle(img, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 255, 0),2)

        return img

    ##########################
    # 顔検出した箇所を矩型で描画 #
    ##########################
    def face_detect(self,img):
        # グレースケールに変換
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # 顔検出
        faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 3,
                minSize = (10, 10)
            )
        # 顔検出箇所に矩型描画のためのループ
        for(x,y,w,h) in faces:
            # 顔箇所を四角で描画
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        return img

    ######################
    # 顔検出とモザイク加工  #
    ######################
    def face_detect_mosaic(self,img):
        # グレースケールに変換
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # 顔検出
        faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 3,
                minSize = (10, 10)
            )
        # 顔検出箇所にモザイクをかけるためのループ
        for(x,y,w,h) in faces:
            # モザイクをかける
            img = self.mosaic(img,(x,y,x+w,y+h),10)

        return img

    #################
    # モザイクをかける #
    #################
    def mosaic(self,img,rect,size):
        # モザイクをかける領域を取得
        (x1,y1,x2,y2)=rect
        w=x2-x1
        h=y2-y1
        i_rect = img[y1:y2,x1:x2]
        # 一度縮小して拡大する
        i_small = cv2.resize(i_rect,(size,size))
        i_mos = cv2.resize(i_small,(w,h),interpolation=cv2.INTER_AREA)
        # モザイクに画像を重ねる
        img2=img.copy()
        img2[y1:y2,x1:x2]=i_mos
        return img2

    ###################
    # γ補正メソッド     #
    ###################
    def gamma_correction(self,image,gamma):
        # 整数型で2次元配列を作成[256,1]
        lookup_table = np.zeros((256, 1), dtype = 'uint8')
        for loop in range(256):
            # γテーブルを作成
            lookup_table[loop][0] = 255 * pow(float(loop)/255, 1.0/gamma)
        # lookup Tableを用いて配列を変換        
        image_gamma = cv2.LUT(image, lookup_table)
        return image_gamma

    #####################
    # 彩度/明度変更メソッド #
    #####################
    def saturation_brightness_chg(self,image,saturation,brightness):
        # 色空間をBGRからHSVに変換
        img_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)  
        # 彩度の計算
        img_hsv[:,:,(1)] = img_hsv[:,:,(1)]*saturation
        # 明度の計算
        img_hsv[:,:,(2)] = img_hsv[:,:,(2)]*brightness
        # 色空間をHSVからBGRに変換
        image_sat_bri = cv2.cvtColor(img_hsv,cv2.COLOR_HSV2BGR)
        return image_sat_bri

    ####################
    # ぼかし変更メソッド  #
    ####################
    def Gaussian_chg(self,image,kernel):
        #　Gaussianフィルタ制御
        gaussian_img = cv2.GaussianBlur(image,(kernel,kernel),5)
        return gaussian_img

    ###############################################
    # 物体検知(YOLO3)                               #
    # 物体検知したい時は、このpythonファイル直下にYOLOを # 
    # ダウンロードしておくこと。                       #
    # （YOLO3の学習済みデータで物体検出してみた）を参考に #   
    ################################################
    def object_detection_clicked(self):
        
        # メッセージBox出力
        res = messagebox.askokcancel("確認", "検出時間が20秒くらいかかります。実行しますか？")
        #　物体検知を実施しない場合
        if res != True:
            # 処理終了
            return
        # 出力ファイルなし
        if os.path.exists("./output_image.jpeg") == False:
            # 入力ファイルを物体検知用のフォルダにコピーする
            shutil.copyfile("./input_image_file.jpeg","./YOLO/pic/input_image_file.jpeg")
        else:
           # 入力ファイルを物体検知用のフォルダにコピーする
            shutil.copyfile("./output_image.jpeg","./YOLO/pic/input_image_file.jpeg")
        # 物体検知のコマンドを作成
        args = ['./darknet', 'detect', 'cfg/yolov3.cfg','yolov3.weights','pic/input_image_file.jpeg']
        # ディレクトリをYOLOへ移動
        os.chdir('YOLO/')
        print(os.getcwd())
        # YOLO3 の物体検知コマンドを実行
        subprocess.run(args)
        # ディレクトリを戻す
        os.chdir('../')
        shutil.copyfile("./YOLO/predictions.jpg", "./output_object_image.jpeg")
        # YOLO3の物体検知画像を読み出し
        img = cv2.imread("./output_object_image.jpeg")
        # 表示用に画像サイズを小さくする
        img2 = cv2.resize(img,dsize=(320,240))
        # 出力画像を保存
        cv2.imwrite("output_image_small.png",img2)
        # 画像をセット
        self.out_image2 = ImageTk.PhotoImage(file="output_image_small.png")
        output_canvas.create_image(160, 120, image=self.out_image2)

    def onSlider(self,args):
        # 入力ファイルの読み出し
        img = cv2.imread(self.filepath)
        # ガンマ補正
        i_out = self.gamma_correction(img,float(self.gamma.get()))
        # 彩度、明度変更
        i_out = self.saturation_brightness_chg(i_out,self.Saturation.get(),self.Brightness.get())
        #ガウシアンフィルタのカーネル値を計算
        kernel_val = self.Gaussian.get()*2+1
        #ガウシアンフィルタによるモザイク変更
        i_out=self.Gaussian_chg(i_out,kernel_val)
        # GUIに表示する用の画像ファイルを作成
        cv2.imwrite("output_image.jpeg",i_out)
        self.chg_out = i_out
        # 表示用に画像サイズを小さくする
        img2 = cv2.resize(i_out,dsize=(320,240))
        # 出力画像を保存
        cv2.imwrite("output_image_small.png",img2)
        # 画像をセット
        self.out_image2 = ImageTk.PhotoImage(file="output_image_small.png")
        output_canvas.create_image(160, 120, image=self.out_image2)
            

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
