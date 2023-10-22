from flask import (
    Flask,
    render_template,
    request,
    make_response,
    send_from_directory,
    redirect,
    url_for,
)
from flask_cors import CORS
import os
from static.RemoveVFX import *
from wsgiref.simple_server import make_server
from random import randint
import json

# 获取运行时路径
basedir = os.path.abspath(os.path.dirname(__file__))

# 可删除列表
options = {
    "A": "MoveTrack",
    "B": "ColorTrack",
    "C": "RecolorTrack",
    "D": "SetFilter",
    "E": "HallOfMirrors",
    "F": "ShakeScreen",
    "G": "Bloom",
    "H": "MoveCamera",
    "I": "MoveDecorations",
    "J": "AddDecoration",
    "K": "Flash",
    "L": "CustomBackground",
}

# 实例化,开启跨域
app = Flask(__name__)
CORS(app, resources=r"/*")
# 定义上传文件夹名
upload_folder_name = "upload"
modify_folder_name = "modify"
# 设置环境变量"UPLOAD_FOLDER"为所定义文件夹名
app.config["UPLOAD_FOLDER"] = upload_folder_name
app.config["MODIFY_FOLDER"] = modify_folder_name
app.secret_key = "uEIlR7Jdg9vrkeutV23u6rFj+ggtTQW8FTtL/7TKeXA9qkZSPXljk5NgRocjAjEiY5fr2pMegjDsSmapVkiSTeMxb4doaf2NXpqm/BIMOaciJ7QS1wI4ZaMiCW1SYxd3IBcmKFqbOdDgd2Yck3yJRM+Tyo94GrMs0Emwlue7/Ee1RSKIO1L7/Pin1RELHc+aF0JKD5Cm0niovKvU4A4pWywlcbdEJm8IFzMiM1fsv8kPlxclP4WRnXDbViVmR/OMZzZXXNwFT2o="

# 检测是否存在upload和modify文件夹
file_dir = os.path.join(basedir, app.config["UPLOAD_FOLDER"])
if not os.path.exists(file_dir):
    os.makedirs(file_dir)

file_dir_modify = os.path.join(basedir, app.config["MODIFY_FOLDER"])
if not os.path.exists(file_dir_modify):
    os.makedirs(file_dir_modify)


# 装饰器以及视图函数
@app.route("/", methods=["GET", "POST"])
@app.route("/upload/", methods=["GET", "POST"])
def uphtml():
    # 若为GET请求，渲染上传界面html
    if request.method == "GET":
        return render_template("upload.html")
    # 若为POST请求，上传adofai文件
    elif request.method == "POST":
        f = request.files["adofaifile"]
        file_name = os.path.splitext(f.filename)[0]
        file_extension = ".adofai"
        new_filename = f"{file_name}{file_extension}"
        new_filepath = os.path.join(file_dir, new_filename)
        temp = ""
        while True:
            if os.path.exists(new_filepath):
                temp = randint(1, 9999)
                new_filename = f"{file_name}{temp}{file_extension}"
                new_filepath = os.path.join(file_dir, new_filename)
                continue
            else:
                break

        f.save(new_filepath)

        filename = f"{file_name}{temp}"

        file_redirect = f"/modify?nm={filename}.adofai"

        response = {
            "filename": filename,
            "file_extension": ".adofai",
            "file_redirect": file_redirect,
        }

        return json.dumps(response)


@app.route("/modify/", methods=["GET", "POST"])
def modify():
    if request.method == "GET":
        response = make_response(render_template("modify.html"))
        file_name = request.args.get("nm")
        print(file_name)
        name, extension = os.path.splitext(file_name)
        response.set_cookie("FileName", name)
        response.set_cookie("FileExtension", extension)
        return response
    elif request.method == "POST":
        checkbox_values = request.form.getlist("box")
        filename = request.cookies.get("FileName")
        file_extension = request.cookies.get("FileExtension")
        fullname = f"{filename}{file_extension}"
        newfullname = f"{filename}(Without VFX){file_extension}"
        fullpath = os.path.join("upload", fullname)
        adofai = Encoder(fullpath, checkbox_values, newfullname)
        adofai.fix_json()
        adofai.remove_event()
        adofai.encode_and_dump()
        return redirect(url_for("done", filename=newfullname))


@app.route("/done/<filename>/", methods=["GET"])
def done(filename):
    return render_template("done.html", filename=filename)


@app.route("/download/<filename>/", methods=["GET"])
def Download(filename):
    new_filename = "%s" % filename
    return send_from_directory("modify", new_filename, as_attachment=True)



# 启动flask服务
if __name__ == "__main__":
    website = make_server("0.0.0.0", 5123, app)
    website.serve_forever()