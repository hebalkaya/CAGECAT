from flask import Flask, url_for, render_template, request, flash, redirect, \
    send_from_directory
import os
from markupsafe import escape # to use strings in HTML : security

# https://flask.palletsprojects.com/en/1.1.x/quickstart/

# deployment: https://flask.palletsprojects.com/en/1.1.x/deploying/#deployment

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

print(UPLOAD_FOLDER)
@app.route("/") # <variable> to make it possible to use in function
def say_hi(): # by adding it as parameter, it can be used in the function
    return url_for("static", filename="styles.css")

@app.route("/starter")
def starting(name=None):
    add_count()
    # print(request.host)
    # print(request.host_url)
    name_list = ["Matthias", "Rosan", "Thijs", "Pim", "Aline"]
    return render_template("index.xhtml", name_list=name_list)

@app.route("/upload_file", methods=["POST", "GET"])
def upload_file():
    if request.method == "POST":
        if request.files:
            print(request.files)
            file = request.files["image"]
            filename = file.filename

            location = os.path.join(app.config["UPLOAD_FOLDER"], filename, )
            file.save(location)
        else:
            print("No files were uploaded")
    else:
        return redirect(url_for("starting"))
    # print(file)
    # print(filename)
    # print(location)
    return render_template("show_image.xhtml", image_title=filename,
                           link=location)

# @app.route("/<name>")
# def start(name):
#     return f"Hello {name}"

@app.errorhandler(404)
def page_not_found(error):
    #print(error)
    return render_template('page_not_found.xhtml'), 404


def add_count(filename="upload_page.txt"):
    with open(filename, "r+") as outf:
        new_number = str(int(outf.readline().strip()) + 1)
        outf.seek(0)
        outf.write(new_number)
        outf.truncate()
        #outf.write()
if __name__ == "__main__":
    app.run(debug=True)