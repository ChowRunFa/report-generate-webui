import json
import os
import time
from datetime import datetime

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
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
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


@api_upload.route('/document_list', methods=['GET'])
def document_list():
    folder_path = './uploads/docs/'  # 文件夹路径

    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        return jsonify({"error": "Folder does not exist"}), 404

    # 获取文件夹中的文件信息
    documents = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):  # 只处理文件
            file_info = {
                    "date": datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),  # 最后修改时间
                    "title": file_name,  # 文件名作为标题
                    "abstract": f"File located at: {file_path}",  # 简介信息，文件路径
                    "size": round(os.path.getsize(file_path) / (1024*1024), 2)  # 文件大小（KB），保留两位小数
            }
            documents.append(file_info)

    # 按修改时间排序（可选）
    documents.sort(key=lambda x: x["date"], reverse=True)

    # 返回文件信息
    return jsonify(documents)

SAVE_FOLDER = './uploads/prompts/'  # 保存文件的文件夹路径
os.makedirs(SAVE_FOLDER, exist_ok=True)

# 保存 Prompt 和思维链为文件
@api_upload.route('/save_prompt', methods=['POST'])
def save_prompt():
    try:
        # 获取前端传递的数据
        data = request.json
        prompt = data.get('prompt', '')
        chain = data.get('chain', '')

        if not prompt or not chain:
            return jsonify({'error': 'Prompt 和思维链不能为空'}), 400

        # 时间戳作为文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 保存为 TXT 文件
        txt_filename = f"prompt_chain_{timestamp}.txt"
        txt_file_path = os.path.join(SAVE_FOLDER, txt_filename)
        with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(f"提示词:\n{prompt}\n\n思维链:\n{chain}")

        # 保存为 JSON 文件
        json_filename = f"prompt_chain_{timestamp}.json"
        json_file_path = os.path.join(SAVE_FOLDER, json_filename)
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump({'prompt': prompt, 'chain': chain}, json_file, ensure_ascii=False, indent=4)

        return jsonify({
            'message': '数据保存成功',
            'txt_file_path': txt_file_path,
            'json_file_path': json_file_path
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_upload.route('/load_prompts', methods=['GET'])
def load_prompts():
    try:
        # 获取文件夹中的所有文本文件
        files = [f for f in os.listdir(SAVE_FOLDER) if f.endswith('.txt')]

        # 读取每个文件的内容
        results = []
        for file_name in files:
            file_path = os.path.join(SAVE_FOLDER, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            results.append({
                'file_name': file_name,
                'content': content,
                'date': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
            })

        # 按文件日期排序
        results.sort(key=lambda x: x['date'], reverse=True)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_upload.route('/load_json_prompts', methods=['GET'])
def load_json_prompts():
    try:
        # 获取文件夹中的所有 JSON 文件
        files = [f for f in os.listdir(SAVE_FOLDER) if f.endswith('.json')]

        # 读取每个 JSON 文件的内容
        results = []
        for file_name in files:
            file_path = os.path.join(SAVE_FOLDER, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = json.load(file)
            results.append({
                'file_name': file_name,
                'prompt': content.get('prompt', ''),
                'chain': content.get('chain', ''),
                'date': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
            })

        # 按文件日期排序
        results.sort(key=lambda x: x['date'], reverse=True)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

from dotenv import load_dotenv
import openai
from openai import OpenAI
# 加载环境变量
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")  # 默认值

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

# 定义保存文件的目录
SAVE_FRAMEWORK_FOLDER = './uploads/saved_frameworks'
os.makedirs(SAVE_FRAMEWORK_FOLDER, exist_ok=True)
@api_upload.route('/generate_framework', methods=['POST'])
def generate_framework():

    # return jsonify({
    #         'message': '报告框架生成并保存成功',
    #         'json_file_path': 'json_file_path',
    #         'framework_preview':  {
    #             "topic": 'topic',
    #             "field": 'field',
    #             "keywords": 'keywords',
    #             "framework": 'framework'
    #         }
    #     })
    try:
        # 获取前端传递的数据
        data = request.json
        topic = data.get('topic', '')
        field = data.get('field', '')
        keywords = data.get('keywords', [])
        max_retries = data.get('max_retries', 3)  # 默认最大重试次数为3

        if not topic or not field or not keywords:
            return jsonify({'error': '主题、领域和关键词不能为空'}), 400

        # 构建提示词
        full_prompt = construct_prompt_for_framework(topic, field, keywords)

        base_answer = ''

        # 调用大模型生成报告框架（带重试逻辑）
        framework_json = None
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model=os.getenv('OPENAI_API_NAME', 'gpt-4o-mini'),
                    messages=[
                        {"role": "system", "content": "你是一个专业的分析报告框架设计助手。"},
                        {"role": "user", "content": full_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1024,
                )
                # 获取模型返回内容
                framework = response.choices[0].message.content
                base_answer = framework
                framework_json = json.loads(framework)  # 验证返回是否为合法JSON
                break  # 如果成功解析JSON，则退出重试循环
            except json.JSONDecodeError:
                if attempt < max_retries - 1:
                    time.sleep(1)  # 等待1秒后重试
                    continue
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(1)  # 等待1秒后重试
                    continue
                else:
                    print(f"模型调用失败: {str(e)}")

        # 如果超过最大重试次数仍未成功，创建默认的 JSON 数据
        if framework_json is None:
            framework_json = {
                "topic": topic,
                "field": field,
                "keywords": keywords,
                "framework": base_answer
            }

        framework_json = convert_top_level_values_to_str(framework_json)

        # 时间戳作为文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_filename = f"framework_{timestamp}.json"
        json_file_path = os.path.join(SAVE_FRAMEWORK_FOLDER, json_filename)


        # 保存框架为 JSON 文件
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(framework_json, json_file, ensure_ascii=False, indent=4)

        return jsonify({
            'message': '报告框架生成并保存成功',
            'json_file_path': json_file_path,
            'framework_preview': framework_json
        })
    except Exception as e:
        print(f"未捕获的错误: {str(e)}")
        return jsonify({'error': str(e)}), 500

def convert_top_level_values_to_str(data):
    if isinstance(data, dict):  # 确保输入是字典
        return {str(k): str(v) for k, v in data.items()}
    else:
        raise ValueError("Input data must be a dictionary.")

def construct_prompt_for_framework(topic, field, keywords):
    """
    构建大模型的中文提示词，用于生成报告框架
    """
    keywords_str = '，'.join(keywords)
    model_name = os.getenv('OPENAI_API_NAME', 'gpt-4o-mini')
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    return (
        f"请严格按照以下要求生成一份中文的报告框架，并只返回纯JSON格式数据：\n"
        f"主题: \"{topic}\"\n"
        f"领域: \"{field}\"\n"
        f"关键词: \"{keywords_str}\"\n"
        f"\n"
        f"JSON格式结构如下（请严格遵循JSON格式，但各个章节的名称和内容描述根据上述提供的：**主题**、**领域**、**关键词**进行个性化生成）：\n"
        f"{{\n"
        f"  \"主题\": \"{topic}\",\n"
        f"  \"领域\": \"{field}\",\n"
        f"  \"关键词\": [\"关键词1\", \"关键词2\", \"关键词3\"],\n"
        f"  \"报告框架\": {{\n"
        f"    \"引言\": \"引言内容，简要描述报告主题和背景。\",\n"
        f"    \"章节\": [\n"
        f"      {{\"标题\": \"章节名称1\", \"内容\": \"章节描述1\"}},\n"
        f"      {{\"标题\": \"章节名称2\", \"内容\": \"章节描述2\"}},\n"
        f"      {{\"标题\": \"章节名称3\", \"内容\": \"章节描述3\"}}\n"
        f"    ],\n"
        f"    \"总结\": \"总结内容，概述报告的核心观点和未来展望。\"\n"
        f"  }},\n"
        f"  \"元信息\": {{\n"
        f"    \"生成时间\": \"{current_time}\",\n"
        f"    \"生成工具\": \"{model_name}\"\n"
        f"  }}\n"
        f"}}\n"
        f"\n"
        f"请根据提供的主题、领域和关键词，结合您的专业能力，自主设计每个章节的标题，并仅返回上述结构的纯JSON格式数据。不得包含任何多余的解释性文字。"
    )


@api_upload.route('/load_framework', methods=['GET'])
def load_framework_reports():
    try:
        # 获取文件夹中的所有 JSON 文件
        files = [f for f in os.listdir(SAVE_FRAMEWORK_FOLDER) if f.endswith('.json')]

        # 读取每个 JSON 文件的内容
        results = []
        for file_name in files:
            file_path = os.path.join(SAVE_FRAMEWORK_FOLDER, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = json.load(file)

            # 提取文件内容和元数据
            results.append({
                'file_name': file_name,
                'topic': content.get('主题', ''),
                'field': content.get('领域', ''),
                'keywords': content.get('关键词', []),
                'framework': content.get('报告框架', {}),
                'date': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
            })

        # 按文件日期排序
        results.sort(key=lambda x: x['date'], reverse=True)

        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

