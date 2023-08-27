from flask import Flask, request, render_template, flash
from werkzeug.utils import secure_filename
import os
import cv2


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "uploads"
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'gif'}
app.secret_key = "riyanswat"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def processImage(filename, operation):
    print(f"The operation is {operation} and the filename is {filename}")

    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cg":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(f"static/{filename}", imgProcessed)
            return newFilename
        case "cpng":
            newFilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpg":
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cwebp":
            newFilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == 'POST':
        operation = request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return "No Selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            new = processImage(filename, operation)
            flash(
                f"Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
            return render_template("index.html")
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, port=5001)
