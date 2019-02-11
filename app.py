# encoding:utf-8
import os

from flask import Flask, redirect, url_for
from gallery.views import gallery



ROOT_DIR = os.path.dirname(__file__)
GALLERY_ROOT_DIR = os.path.join(os.path.dirname(__file__), 'static', 'gallery')
GALLERY_ROOT_SHARE_DIR = os.path.join(os.path.dirname(__file__), 'static', 'gallery_share')

UPLOAD_DIR = os.path.join(ROOT_DIR, GALLERY_ROOT_DIR)
UPLOAD_ALLOWED_EXTENSIONS = (
    'jpg',
    'jpeg',
    'png',
    'gif',
)


app = Flask(__name__)
app.register_blueprint(gallery, url_prefix='/gallery')
app.config['GALLERY_ROOT_DIR'] = GALLERY_ROOT_DIR
app.config['GALLERY_ROOT_SHARE_DIR'] = GALLERY_ROOT_SHARE_DIR
app.config['ROOT_DIR'] = ROOT_DIR

@app.route('/')
def index():
    return redirect(url_for('gallery.show_gallery'))

if __name__ == '__main__':
    app.logger.info('Listening on http://localhost:8000')
    app.run(port=8000, debug=True)
