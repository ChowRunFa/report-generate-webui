import os
import time

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS

# 设置允许上传的文件类型和文件大小限制
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'zip', 'rar'}
# MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 16MB

# 检查文件类型是否允许上传
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from flask import Blueprint
api_upload = Blueprint('api_upload', __name__)


# 处理文件上传的路由处理函数
@api_upload.route('/upload', methods=['POST'])
def upload_file():
    # 检查是否有文件被上传
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']

    # 检查文件名是否为空
    if file.filename == '':
        return 'Empty filename', 400

    # 检查文件类型是否允许上传
    if not allowed_file(file.filename):
        return 'Invalid file type', 400

    # 将文件保存到指定的位置
    # 生成当前时间戳
    timestamp = str(int(time.time()))
    # 创建以时间戳为名称的文件夹
    folder_path = './uploads/paper/' + timestamp
    os.makedirs(folder_path, exist_ok=True)
    filename = secure_filename(file.filename)
    file_path = os.path.join(folder_path, filename)
    file.save(file_path)

    # 构建文件路径的响应
    response_data = {
        'file_path': file_path
    }

    return jsonify(response_data)






# 处理文件上传的路由处理函数
@api_upload.route('/upload_local', methods=['POST'])
def upload_file_local():
    # 检查是否有文件被上传
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']

    # 检查文件名是否为空
    if file.filename == '':
        return 'Empty filename', 400

    # 检查文件类型是否允许上传
    if not allowed_file(file.filename):
        return 'Invalid file type', 400

    # 将文件保存到指定的位置
    # 生成当前时间戳
    timestamp = str(int(time.time()))
    # 创建以时间戳为名称的文件夹
    folder_path = './uploads/paper/local/' + timestamp
    os.makedirs(folder_path, exist_ok=True)
    filename = secure_filename(file.filename)
    file_path = os.path.join(folder_path, filename)
    file.save(file_path)

    # 构建文件路径的响应
    response_data = {
        'file_path': file_path
    }

    return jsonify(response_data)
