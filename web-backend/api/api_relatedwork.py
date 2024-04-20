import argparse
import sys

# 设置OpenAI API密钥
from dotenv import load_dotenv
load_dotenv()

from flask import Blueprint, request, jsonify

sys.path.append("..")

from objs.RelatedWork import RelatedWork
from utils.general_utils import result


def related_work_main(args):
    # print(RelatedWork(args).generate_reference())
    return RelatedWork(args).generate_relatedwork()

api_relatedwork = Blueprint('api_relatedwork', __name__)
@api_relatedwork.route('/related_work', methods=['POST'])
def api_related_work():
    # 通过request对象获取参数的值
    sort_by = request.get_json()['_value'].get('sort_by')
    api_base = request.get_json()['_value'].get('api_base')
    api_key = request.get_json()['_value'].get('api_key')
    model = request.get_json()['_value'].get('model')
    s2_api_key = request.get_json()['_value'].get('s2_api_key')
    base_paper_url = request.get_json()['_value'].get('base_paper_url')
    num_papers = request.get_json()['_value'].get('num_papers')
    rerank = request.get_json()['_value'].get('rerank')
    keyword = request.get_json()['_value'].get('keyword')
    base_abstract = request.get_json()['_value'].get('base_abstract')
    cite_format = request.get_json()['_value'].get('cite_format')
    limit_words = request.get_json()['_value'].get('limit_words')
    # sort_by = ''
    # api_base = ''
    # api_key = ''
    # model = ''
    # s2_api_key = ''
    # base_paper_url = ''
    # num_papers = ''
    # rerank = ''
    # keyword = ''
    # base_abstract = ''
    # cite_format = ''
    # limit_words = ''

    parser = argparse.ArgumentParser()
    api_key = "sk-CjN80YJ5SE9pHUdfxuN88pXsrBaIHIxIlFjOSPnzf6ahO362"
    api_base = "https://api.openai-proxy.org/v1"
    model = "gpt-3.5"
    parser.add_argument("--api_base", type=str, default=api_base, help="the api base")
    parser.add_argument("--api_key", type=str, default=api_key,help="the api key")
    parser.add_argument("--model", type=str, default=model, help="name of the  llm")
    parser.add_argument("--s2_api_key", type=str, default=s2_api_key, help="api key for search paper")
    parser.add_argument("--base_paper_url", type=str, default=base_paper_url, help="the base paper input by user")
    parser.add_argument("--num_papers", type=str, default=num_papers, help="the used nums of cited paper")
    parser.add_argument("--sort_by", type=str,default=sort_by,help="sort references by which values")
    parser.add_argument("--rerank", type=str,default=rerank,help="LLM Re-rank true or false")
    parser.add_argument("--keyword", type=str,default=keyword,help="user input optional keywords for querying")
    parser.add_argument("--base_abstract", type=str,default=base_abstract,help="user input base abstract for querying")
    parser.add_argument("--cite_format", type=str,default=cite_format,help="the user input cited format for citation")
    parser.add_argument("--limit_words", type=str,default=limit_words,help="the words limit of generated related work")
    args = parser.parse_args()

    for arg in vars(args):
        print(f"{arg}: {getattr(args, arg)}")

    # return related_work_main(args=parser.parse_args())
    return result(200,"hello",{"related_work":"this <br>"})


# if __name__ == "__main__":
#     api_relatedwork()