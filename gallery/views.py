from flask import Blueprint, render_template, request, redirect, url_for, current_app
import simplejson
from .models import Images
from .models_share import Images_share
import cv2
from PIL import Image
from resizeimage import resizeimage
import shutil

gallery = Blueprint('gallery', __name__, template_folder='templates', static_folder='static')
@gallery.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        print(request.form['username'])
        if request.form['username'] == '' or request.form['password'] == '':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(('gallery/user'))
    return render_template('login.html', error=error)
@gallery.route('/user', methods=['GET', 'POST',])
def show_gallery():
    images = Images.all(current_app.config['GALLERY_ROOT_DIR'])
    return render_template('index.html', images=images)

@gallery.route('/', methods=['GET', 'POST',])
def shareing():
    images = Images_share.all(current_app.config['GALLERY_ROOT_SHARE_DIR'])
    return render_template('share.html', images=images)

@gallery.route('/upload', methods=['POST',])
def upload():
    if request.method == 'POST' and 'image' in request.files:
        image = request.files['image']
        Images('', post=image, root=current_app.config['GALLERY_ROOT_DIR'])

        return redirect(('gallery/user'))

    return (simplejson.dumps({'error': 'you need to pass an image'}), 400)

@gallery.route('/edit_crop' ,methods=['GET', 'POST',])
def edit_crop():
    s = request.args.get('s')
    d = s.split('*')
    filename = request.args.get('filename')
    filename_crop = current_app.config['ROOT_DIR'] + filename[0:filename.rfind(".")] + '_crop' + \
                   filename[filename.rfind("."):]


    filename = current_app.config['ROOT_DIR'] + filename
    print(filename)
    print(filename_crop)
    if request.method == 'GET' and s != '':
        with open(filename, 'r+b') as f:
            with Image.open(f) as img:
                img = resizeimage.resize_crop(img, [int(d[0]), int(d[1])])
                img.save(filename_crop, img.format)


    return redirect(('gallery/user'))

@gallery.route('/edit_wb' ,methods=['GET', 'POST',])
def edit_wb():
    filename=request.args.get('filename')
    print(filename)
    if request.method == 'GET' and filename !='':

        filename_gray = current_app.config['ROOT_DIR'] +filename[0:filename.rfind(".")] +'_gray'+ filename[filename.rfind("."):]
        filename=current_app.config['ROOT_DIR']+filename

        print(filename)
        print(filename_gray)
        col = Image.open(filename)
        gray = col.convert('L')
        bw = gray.point(lambda x: 0 if x < 128 else 255, '1')
        bw.save(filename_gray)
    return redirect(('gallery/user'))
@gallery.route('/edit_resize' ,methods=['GET', 'POST',])
def edit_resize():
    s=request.args.get('s')
    d=s.split('*')
    filename = request.args.get('filename')
    filename_res = current_app.config['ROOT_DIR'] + filename[0:filename.rfind(".")] + '_resize' + \
                    filename[filename.rfind("."):]

    print(filename)
    filename=current_app.config['ROOT_DIR'] +filename
    print(filename_res)
    if request.method == 'GET' and s !='':
        with open(filename, 'r+b') as f:
            with Image.open(f) as image:
                cover = resizeimage.resize_cover(image, [int(d[0]), int(d[1])])
                cover.save(filename_res, image.format)
    return redirect(('gallery/user'))

@gallery.route('/edit_rotate' ,methods=['GET', 'POST',])
def edit_rotate():
    dg = request.args.get('dg')
    filename = request.args.get('filename')
    filename_rot = current_app.config['ROOT_DIR'] + filename[0:filename.rfind(".")] + '_rotate' + \
                    filename[filename.rfind("."):]

    print(filename)
    filename=current_app.config['ROOT_DIR'] +filename
    print(filename_rot)
    if request.method == 'GET' and dg !='':
        im = Image.open(filename)
        im.rotate(int(dg)).save(filename_rot, im.format)

    return redirect(('gallery/user'))

@gallery.route('/doshare' ,methods=['GET', 'POST',])
def share():
    filename = request.args.get('filename')

    print(filename)
    filename_share = current_app.config['ROOT_DIR'] + filename.replace('/static/gallery/', '/static/gallery_share/')
    filename=current_app.config['ROOT_DIR'] +filename

    if request.method == 'GET':
        shutil.copy(filename,filename_share)

    return redirect(('gallery/user'))

# FIXME: make more modular to avoid the import below
# this import is here to avoid circular hell import
import app
