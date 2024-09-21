import os
from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# 设置上传文件夹
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 允许上传的文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 存储上传的文件信息（日期和文件路径）
uploaded_files = []


# 检查文件类型是否允许
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 主页：展示上传文件的表单
@app.route('/')
def index():
    # 渲染主页，并传递已上传文件的信息
    return render_template('index.html', files=uploaded_files)


# 文件上传逻辑
@app.route('/upload', methods=['POST'])
def upload_file():
    # 检查是否有文件上传
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    # 如果用户没有选择文件
    if file.filename == '':
        return redirect(request.url)

    # 文件合法并且允许上传
    if file and allowed_file(file.filename):
        filename = file.filename
        # 保存文件到指定目录
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # 获取当前时间
        upload_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 将上传日期和文件路径存储到 uploaded_files 列表中
        uploaded_files.append({
            'date': upload_date,
            'url': f'/{file_path}'  # 生成文件的访问链接
        })

        return redirect(url_for('index'))

    return '上传失败，文件类型不被允许！'


if __name__ == '__main__':
    # 启动 Flask 应用
    app.run(debug=True)
