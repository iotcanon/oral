# -*- coding: utf-8 -*-

from flask import Flask, request, Response, send_file, render_template
import json

_dir = './歯分割_IoU/'
_sumfile = '歯分割_IoU.csv'
_dic = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s']

app = Flask("helloapp")


def mk_dt(exp):
  data = []
  first = True
  with open(_sumfile, encoding='shift_jis') as f:
    while True:
      if first:
        f.readline()
        first = False
      l = f.readline().strip()
      if len(l) == 0:
        break
      csv = l.split(',')
      tmp = exp.lower()
      for i in range(len(_dic)):
        tmp = tmp.replace(_dic[i], csv[i], -1)
      dt = {
        'fname': csv[0][:5],
        'score': int(eval(tmp))
      }
      #print(l)
      data.append(dt)
  return data

@app.route("/")
def hello():
  exp = '0'
  if not ('QUERY_STRING' in request.headers.environ):
    return Response(response=json.dumps({'message': 'no query string'}), status=400)
  qs = request.headers.environ['QUERY_STRING'].split('&')
  exp = qs[0]
  if len(exp) == 0:
    exp = '0'
  dt = mk_dt(exp)
  return render_template('index.html', data=dt)

# 指定のimg_idの非公開画像を返す
@app.route("/image")
def iamge():
  print("** /iamge " + request.method)
  if not ('QUERY_STRING' in request.headers.environ):
    return Response(response=json.dumps({'message': 'no query string'}), status=400)
  qs = request.headers.environ['QUERY_STRING'].split('&')
  rid = '' if len(qs) == 0 else qs[0]
  print('/image?' + rid)
  if rid == '':
    return Response(response=json.dumps({'message': 'no id'}), status=400)
  imgFileName = _dir + rid + '.jpg'
  return send_file(imgFileName, mimetype='image/jpg')


if __name__ == '__main__':
  app.debug = True
  app.run(host='127.0.0.1')
'''

formula = 'b * k'

'''