from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect
from glob import glob
from datetime import datetime
import re
import pandas

def index(request) :
  datas = {}
  try :
    target = request.GET.get(key="target")
    if target is None :
      target = request.POST.get(key="target")
    print(target)
    df = pandas.DataFrame()
    try :
      df = pandas.read_csv(target + ".csv", encoding="shift-jis")
    except :
      print("target none.")
    datas = {
      "target": target,
      "result_list": df
    }
  except :
    pass
  return render(request, 'suki_kirai_memo.html', datas)

def edit(request) :
  target = request.POST.get(key="target", default="rie")
  item = request.POST.get(key="item")
  level = request.POST.get(key="level")
  df = pandas.DataFrame({"item": [], "level": [], "regist_time":[]})
  try :
    df = pandas.read_csv(target + ".csv")
  except :
    print("target none.")
  df.loc[len(df)] = [item, level, get_now()]
  df.to_csv(target + ".csv", index=None, encoding="shift-jis")

  url = reverse("index")
  return HttpResponseRedirect(url)

# ------------------------------------------------------------
# 現在日時取得.
# ------------------------------------------------------------
def get_now() :
  return datetime.now().strftime("%Y%m%d_%H%M%S")
