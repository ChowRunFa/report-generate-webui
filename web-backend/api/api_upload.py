from flask import Flask, request
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# 设置允许上传的文件类型和文件大小限制
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'zip', 'rar'}
# MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 16MB

# 检查文件类型是否允许上传
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from flask import Blueprint
api_upload = Blueprint('api_delete', __name__)


# 处理文件上传的路由处理函数
@app.route('/upload', methods=['POST'])
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
    filename = secure_filename(file.filename)
    file.save('../uploads/paper/' + filename)

    return 'File uploaded successfully'


