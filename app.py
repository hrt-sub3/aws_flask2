from flask import Flask, request
import subprocess
import base64
import data_source

app = Flask(__name__)

@app.route("/")
def index():
  return "hrt_sub3"

@app.route("/programs", methods=['GET', 'POST'])
def programs():
  if request.method == 'POST':
    src = base64.b64encode(request.form["text"].encode())
    return str(data_source.insert_program("python", src, None))

  elif request.method == 'GET':
    return ','.join(map(lambda x: str(x), data_source.get_id_list()))


@app.route("/src", methods=['POST'])
def show_src():
  enc_src = data_source.get_src(request.form["text"].encode())
  src = base64.b64decode(enc_src).decode('UTF-8', 'replace')

  return src

@app.route("/exec", methods=['POST'])
def show_exec():
  enc_src = data_source.get_src(request.form["text"].encode())
  src = base64.b64decode(enc_src).decode('UTF-8', 'replace')
  with open("/tmp/tmp.py", "w") as f:
    f.write(src)
  return subprocess.Popen("python /tmp/tmp.py", shell=True, stdout=subprocess.PIPE).communicate()

@app.route("/delete", methods=['POST'])
def delete():
  data_source.delete_program(request.form["text"].encode())
  return "delete ok"

if __name__ == "__main__":
  data_source.init_cursor()
  app.run()
