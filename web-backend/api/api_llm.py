
import sys

sys.path.append("..")

from db.models import *
from utils.general_utils import result
from flask import Blueprint, request, jsonify

api_llm = Blueprint('api_llm', __name__)

@api_llm.route('/set_llm', methods=['POST'])
def set_llm():
    llm_name = request.get_json().get('llm_name')
    api_key = request.get_json().get('api_key')
    api_base = request.get_json().get('api_base')
    using = request.get_json().get('using')
    # 检查是否已存在
    existing_llm = llm_set.query.filter_by(llm_name=llm_name, api_key=api_key, api_base=api_base).first()
    if existing_llm:
        return result(code=400, msg="配置已存在，请选择其他配置")

    new_llm = llm_set(llm_name=llm_name, api_key=api_key, api_base=api_base, using=using)
    db.session.add(new_llm)
    db.session.commit()
    return result(code=200, msg="配置设置成功！")

    return result(code=200, msg = "配置设置成功！")