from flask import Flask, render_template, jsonify, send_from_directory, abort, request
from werkzeug.utils import secure_filename
from app import app
from models import Icon, Device
import os

@app.route('/')
def index():
    icons = Icon.query.all()
    return render_template('index.html', icons=icons)

@app.route('/api/devices')
def get_all_devices():
    devices = Device.query.all()
    device_list = [{'id': device.id, 'name': device.name, 'icon_id': device.icon_id} for device in devices]
    return jsonify(devices=device_list)

@app.route('/api/icons')
def get_all_icons():
    icons = Icon.query.all()
    icon_list = [{'id': icon.id, 'name': icon.name, 'path': icon.path} for icon in icons]
    return jsonify(icons=icon_list)

def save_icon_file(icon_file):
    filename = secure_filename(icon_file.filename)
    icon_path = os.path.join(app.root_path, 'static', 'icons', filename)
    icon_file.save(icon_path)
    return os.path.join('static', 'icons', filename)

@app.route('/static/icons/<int:icon_id>', methods=['GET'])
def get_icon(icon_id):
    icon = Icon.query.get_or_404(icon_id)
    if not icon.path:
        abort(404, description="Icon not found")
    icon_path = icon.path
    return jsonify({"icon": icon_path})

@app.route('/static/icons/<path:filename>')
def serve_icon(filename):
    if '..' in filename or filename.startswith('/'):
        abort(404)
    return send_from_directory(os.path.join(app.root_path, 'static', 'icons'), filename)
