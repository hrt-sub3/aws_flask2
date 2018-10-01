from flask import Flask, request
import subprocess
import base64
import data_source
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/")
def index():
  return "hrt_sub3"

@app.route("/programs", methods=['GET', 'POST'])
def programs():
  if request.method == 'POST':
    text = request.form["text"].split('\r\n')
    lang, src = text[0], "\r\n".join(text[1:])
    if lang == 'python':
      return str(data_source.insert_program(lang, src, None))
    if lang == 'c':
      exe, error = compile_c_lang(src)
      if error:
        return "compile error"
      else:
        return str(data_source.insert_program(lang, src, exe))
    else:
      return 'invalid language'

  elif request.method == 'GET':
    return ','.join(map(lambda x: str(x), data_source.get_id_list()))


@app.route("/src", methods=['POST'])
def show_src():
  return data_source.get_src(request.form["text"])

@app.route("/exec", methods=['POST'])
def show_exec():
  exe = data_source.get_exec(request.form["text"])
  if exe == None:
    src = data_source.get_src(request.form["text"])
    dt = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = "/tmp/{}.py".format(dt)
    with open(path, "w") as f:
      f.write(src)
    result = subprocess.Popen("python {}".format(path), shell=True, stdout=subprocess.PIPE).communicate()
  else:
    dt = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = "/tmp/{}".format(dt)
    with open(path, "wb") as f:
      f.write(base64.b64decode(exe))
    subprocess.Popen("chmod 777 {}".format(path), shell=True).wait()
    result = subprocess.Popen(path, shell=True, stdout=subprocess.PIPE).communicate()

  os.remove(path)
  return result

@app.route("/delete", methods=['POST'])
def delete():
  data_source.delete_program(request.form["text"])
  return "delete ok"

def compile_c_lang(src):
  dt = datetime.now().strftime('%Y%m%d_%H%M%S')
  src_path = "/tmp/{}.c".format(dt)
  exe_path = "/tmp/{}".format(dt)

  with open(src_path, "w") as f:
    f.write(src)
  # 0が返ればコンパイルが正常終了
  return_code = subprocess.Popen("gcc -o {} {}".format(exe_path, src_path), shell=True).wait()
  os.remove(src_path)
  if return_code != 0:
    return "", True

  with open(exe_path, "rb") as f:
    encoded = base64.b64encode(f.read())

  os.remove(exe_path)
  return encoded, False

if __name__ == "__main__":
  data_source.init_cursor()
  app.run()
