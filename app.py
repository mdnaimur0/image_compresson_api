from flask import Flask, send_file, render_template, request
from PIL import Image
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        file = request.files["image"]
        maxsize = int(request.form['maxsize'])
        if file:
            image_data = file.read()
            image = Image.open(io.BytesIO(image_data))
            image_data = compress_image(image=image, maxsize=maxsize)
            return send_file(io.BytesIO(image_data), mimetype="image/jpeg", download_name=f'{file.filename}.jpg')
        else:
            return render_template("error.html", error="Image file not found!")

def compress_image(image: Image, maxsize):
    width, height = image.size
    aspect_ratio = width / height
    if width > height:
        new_width = maxsize
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = maxsize
        new_width = int(new_height * aspect_ratio)
    compressed_image = image.resize((new_width, new_height), Image.ANTIALIAS)

    # Convert the image to RGB mode if it has an alpha channel
    if compressed_image.mode in ("RGBA", "LA") or (
        compressed_image.mode == "P" and "transparency" in compressed_image.info
    ):
        compressed_image = compressed_image.convert("RGB")
    compressed_image_io = io.BytesIO()
    compressed_image.save(compressed_image_io, format="JPEG", quality=100)
    compressed_image_data = compressed_image_io.getvalue()
    compressed_image_io.close()

    return compressed_image_data

app.run(debug=True)