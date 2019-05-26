from django.shortcuts import render
from django.conf import settings
from glob import glob
import re
import pandas

def index(request) :
  base_dir = "../keras/Shigure-kabu/"
  # 運用フォルダ一覧取得
  reg_dirs = glob(base_dir + "regression_20*")
  conv_dir_name(reg_dirs)
  result_list = []
  for dir_name in reg_dirs :
    reg_dir = base_dir + dir_name + "/"
    inner = {}
    try :
      # ----------------------------------------------------------------------
      # フォルダ名
      # ----------------------------------------------------------------------
      inner["dir_name"] = dir_name
      # ----------------------------------------------------------------------
      # サマリ ファイル名
      # ----------------------------------------------------------------------
      file_list = glob(reg_dir + "summary_*png")
      conv_dir_name(file_list)
      inner["file_name"] = file_list[0]
      # ----------------------------------------------------------------------
      # サマリ パス
      # ----------------------------------------------------------------------
      inner["path"] = settings.MEDIA_URL + dir_name + "/" + inner["file_name"]
      # ----------------------------------------------------------------------
      # 利益推移 パス
      # ----------------------------------------------------------------------
      file_list = glob(reg_dir + "summary_*csv")
      conv_dir_name(file_list)
      df = pandas.read_csv(reg_dir + file_list[0])
      train_index = df.sort_values("rieki")["train_index"].iloc[-1]
      inner["train_index"] = train_index
      train_dir = dir_name + "/train/" + str(train_index) + "/"
      file_list = glob(base_dir + train_dir + "f_img_rieki_*png")
      conv_dir_name(file_list)
      inner["rieki_path"] = settings.MEDIA_URL + train_dir + file_list[0]
    except :
      pass
    # ----------------------------------------------------------------------
    # 設定情報
    # ----------------------------------------------------------------------
    with open(reg_dir + "settings.txt") as f:
      inner["lines"] = f.readlines()

    result_list.append(inner)
  datas = {"result_list": result_list}
  return render(request, 'forward_summary_list.html', datas)

def conv_dir_name(list) :
  for i in range(len(list)) :
    list[i] = re.match("^.*/(.*)$", list[i]).group(1)
  list.sort()
