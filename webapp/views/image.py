import base64
import io
import os
from PIL import Image
from flask import Blueprint, send_file, abort

image_bp = Blueprint('image', __name__)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))


@image_bp.route('/images/<string:isbn>', methods=['GET'])
def get_image(isbn):
    # image = Image.open("./images/" + isbn + ".png")
    # data = io.BytesIO()
    # image.save(data, "PNG")
    # encoded_img_data = base64.b64encode(data.getvalue())
    # print(encoded_img_data)
    image_path = os.path.join(BASE_DIR, 'images', f'{isbn}.png')
    if not os.path.exists(image_path):
        abort(404)
    return send_file(image_path, mimetype='image/png')
