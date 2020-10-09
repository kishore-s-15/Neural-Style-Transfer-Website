# Importing the required libraries and modules
import os
from flask import Flask, render_template, request, redirect, url_for

from model import NST

# Global Variables
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'JPG']
UPLOAD_FOLDER = os.path.join('static', 'Imgs')
CONTENT_IMAGE_PATH = ''
STYLE_IMAGE_PATH = ''
STYLIZED_IMAGE_PATH = ''

app = Flask(__name__)

@app.after_request
def add_header(r):
    """
    Function which prevents Chrome from caching the static resources
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def index():
    """
    Function which renders the home page
    """

    if os.path.isfile(CONTENT_IMAGE_PATH):
        os.remove(CONTENT_IMAGE_PATH)
    
    if os.path.isfile(STYLE_IMAGE_PATH):
        os.remove(STYLE_IMAGE_PATH)

    if os.path.isfile(STYLIZED_IMAGE_PATH):
        os.remove(STYLIZED_IMAGE_PATH)
        
    return render_template('index.html')

@app.route('/img_upload/<image>', methods=['GET', 'POST'])
def img_upload(image):
    """
    Function which is used for uploading images from our local file system
    """

    render_image, paths = {}, {}
    if image == 'content':
        img_name = "content_img"
    else:
        img_name = "style_img"

    if request.method == 'POST':
        if img_name not in request.files:
            print('No File Part')
            return render_template('index.html')

        img = request.files[img_name]

        if img.filename == '':
            print('No File Selected')
            return render_template('index.html')
        
        file_extension = img.filename.split('.')[-1]
        if img and file_extension in ALLOWED_EXTENSIONS:

            if not os.path.isdir(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)

            if image == 'content':
                global CONTENT_IMAGE_PATH
                CONTENT_IMAGE_PATH = os.path.join(UPLOAD_FOLDER, f"{img_name}.{file_extension}")
                img.save(CONTENT_IMAGE_PATH)

            elif image == 'style':
                global STYLE_IMAGE_PATH
                STYLE_IMAGE_PATH = os.path.join(UPLOAD_FOLDER, f"{img_name}.{file_extension}")
                img.save(STYLE_IMAGE_PATH)

            print(f"File Uploaded Successfully - {img_name}")

            render_image = {'content_image': os.path.isfile(CONTENT_IMAGE_PATH),
                            'style_image': os.path.isfile(STYLE_IMAGE_PATH)}

            paths = {'content_image': CONTENT_IMAGE_PATH,
                     'style_image': STYLE_IMAGE_PATH,
                     'stylized_image': STYLIZED_IMAGE_PATH}

    return render_template('index.html', render_image = render_image, paths=paths)

@app.route('/result', methods=["POST"])
def transfer_style():
    """
    Function which applies the style to the content image
    """

    render_image, paths = {}, {}
    if os.path.isfile(CONTENT_IMAGE_PATH) and os.path.isfile(STYLE_IMAGE_PATH):     
        stylized_image = NST(CONTENT_IMAGE_PATH, STYLE_IMAGE_PATH)

        global STYLIZED_IMAGE_PATH
        STYLIZED_IMAGE_PATH = os.path.join(UPLOAD_FOLDER, 'stylized_image.png')
        stylized_image.save(STYLIZED_IMAGE_PATH)

        render_image = {'content_image': os.path.isfile(CONTENT_IMAGE_PATH),
                        'style_image': os.path.isfile(STYLE_IMAGE_PATH),
                        'stylized_image': os.path.isfile(STYLIZED_IMAGE_PATH)}

        paths = {'content_image': CONTENT_IMAGE_PATH,
                 'style_image': STYLE_IMAGE_PATH,
                 'stylized_image': STYLIZED_IMAGE_PATH}

    return render_template('index.html', render_image=render_image, paths=paths)

if __name__ == "__main__":
    app.run(debug=True)