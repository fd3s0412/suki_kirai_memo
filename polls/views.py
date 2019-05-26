from django.shortcuts import render
from django.conf import settings
from glob import glob
import re

def index(request) :
  base_dir = "../keras/Shigure-kabu/"
  back_num = int(request.GET.get(key="back", default=1))
  # 運用フォルダ一覧取得
  reg_dirs = glob(base_dir + "regression_v*")
  conv_dir_name(reg_dirs)
  # ファイル一覧取得
  files = []
  for dir_name in reg_dirs :
    forward_dirs = glob(base_dir + dir_name + "/" + "forward_*")
    conv_dir_name(forward_dirs)
    if back_num <= len(forward_dirs) :
      dir_map = {}
      file_list = []
      path_list = glob(base_dir + dir_name + "/" + forward_dirs[-1 * back_num] + "/" + "*.png")
      conv_dir_name(path_list)
      for path_index in range(len(path_list)) :
        file_map = {}
        file_map["file_name"] = path_list[path_index]
        file_map["path"] = settings.MEDIA_URL + dir_name + "/" + forward_dirs[-1 * back_num] + "/" + path_list[path_index]
        file_list.append(file_map)
      dir_map["dir_name"] = dir_name
      dir_map["file_list"] = file_list
      files.append(dir_map)
  datas = {"files": files}
  return render(request, 'index.html', datas)

def conv_dir_name(list) :
  for i in range(len(list)) :
    list[i] = re.match("^.*/(.*)$", list[i]).group(1)
  list.sort()
