import argparse

import sys,os

sys.path.append("..")
from objs.Paper import Paper
from objs.Report import Report
from utils.general_utils import is_valid_filepath
from utils.general_utils import text2html
from utils.general_utils import result

from flask import Blueprint, request, jsonify

api_report = Blueprint('api_report', __name__)


def paper_report_main(args):
    if args.pdf_path:
        report = Report(key_word=args.key_word,
                        api_base=args.api_base,
                        api_key=args.api_key,
                        llm=args.llm,
                        args=args
                        )
        # 开始判断是路径还是文件：
        paper_list = []
        if args.pdf_path.endswith(".pdf"):
            paper_list.append(Paper(path=args.pdf_path))
        else:
            for root, dirs, files in os.walk(args.pdf_path):
                print("root:", root, "dirs:", dirs, 'files:', files)  # 当前目录路径
                for filename in files:
                    # 如果找到PDF文件，则将其复制到目标文件夹中
                    if filename.endswith(".pdf"):
                        paper_list.append(Paper(path=os.path.join(root, filename)))
        print("------------------paper_num: {}------------------".format(len(paper_list)))
        [print(paper_index, paper_name.path.split('\\')[-1]) for paper_index, paper_name in enumerate(paper_list)]
        report_htmls = [[text2html(sublist)] for sublist in report.summary_paper(paper_list=paper_list)]
        return report_htmls

@api_report.route('/paper_report', methods=['POST'])
def api_paper_report():
    filepath = request.form.get('file_path')  # 通过request对象获取filepath参数的值
    filepath = os.path.dirname(filepath)

    # print(request.form)

    # 检查 filepath 参数的有效性
    # if not is_valid_filepath(filepath):
    #     return result(400,'无效的 filepath 参数')
    # filepath = r'D:\Pycharm_Projects\report-generate-webui\web-backend\uploads\paper\1712644670\19_20240105.pdf'
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf_path", type=str,
                        default=filepath,
                        help="if none, the bot will download from arxiv with query")
    parser.add_argument("--key_word", type=str, default='reinforcement learning',
                        help="the key word of user research fields")
    parser.add_argument("--language", type=str, default='zh', help="The other output lauguage is English, is en")
    parser.add_argument("--api_base", type=str, default='https://api.openai-proxy.org/v1', help="the api base")
    parser.add_argument("--api_key", type=str, default='sk-CjN80YJ5SE9pHUdfxuN88pXsrBaIHIxIlFjOSPnzf6ahO362',
                        help="the api key")
    parser.add_argument("--llm", type=str, default='gpt-3.5-turbo-0301', help="language model name")

    import time

    start_time = time.time()
    report_html = paper_report_main(args=parser.parse_args())
    print(report_html)
    print("summary time:", time.time() - start_time)

    return result(200, '报告生成完成，请查收~',{'report_html':report_html})

