import argparse
import glob

import sys,os
from dotenv import load_dotenv
from langchain_community.chat_models.openai import ChatOpenAI

load_dotenv()  # 加载.env文件

sys.path.append("..")
from objs.Paper import Paper
from objs.Report import Report
from utils.general_utils import is_valid_filepath
from utils.markdown_utils import markdown_convertion
from utils.general_utils import text2html
from utils.general_utils import result
from utils.general_utils import get_mermaid
from utils.img_utils import mermaid_txt_to_image

from flask import Blueprint, request, jsonify

api_report = Blueprint('api_report', __name__)

html = []

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
        for paper in paper_list:
            print("---------section_page_dict---------")
            print(paper.section_page_dict)
            print("---------section_text_dict---------")
            print(paper.section_text_dict)
        [print(paper_index, paper_name.path.split('\\')[-1]) for paper_index, paper_name in enumerate(paper_list)]
        # report_htmls = [[text2html(sublist)] for sublist in report.summary_paper(paper_list=paper_list)]

        report_htmls = [[markdown_convertion('\n'.join(sublist))] for sublist in report.summary_paper(paper_list=paper_list)]
        # report_htmls = [['<div class="markdown-body"><h2>Paper:1</h2>\n<ol>\n<li>标题: AutoKG: Efficient Automated Knowledge Graph (自动知识图谱:高效自动化知识图谱)</li>\n<li>Title: AutoKG: Efficient Automated Knowledge Graph</li>\n<li>Authors: Bohan Chen and Andrea L. Bertozzi</li>\n<li>Affiliation: Department of Mathematics, University of California, Los Angeles (加州大学洛杉矶分校数学系)</li>\n<li>Keywords: Large Language Models, Knowledge Graph, Graph Learning, Retrieval-augmented Generation</li>\n</ol>\n<h2>Summary:</h2>\n<ul>\n<li>(1): 本文的研究背景是传统方法在将大型语言模型（LLMs）与知识库链接时往往无法捕捉复杂的关系动态。</li>\n<li>(2): 过去的方法包括语义相似性搜索，存在问题是难以捕捉复杂的关系动态。本文的方法是有充分动机的，提出了一种轻量高效的自动化知识图谱构建方法。</li>\n<li>(3): 本文提出的研究方法是通过使用LLM提取关键词，然后通过图拉普拉斯学习评估每对关键词之间的关系权重。使用向量相似性和基于图的关联的混合搜索方案来丰富LLM响应。</li>\n<li>(4): 本文的方法在任务上取得了更全面和相互关联的知识检索机制，从而增强了LLMs在生成更具洞察力和相关性输出方面的能力。</li>\n</ul>\n<h2>Methods:</h2>\n<ul>\n<li>\n<p>(1): 使用大型语言模型（LLMs）提取关键词。</p>\n</li>\n<li>\n<p>(2): 通过图拉普拉斯学习评估每对关键词之间的关系权重。</p>\n</li>\n<li>\n<p>(3): 利用向量相似性和基于图的关联的混合搜索方案来丰富LLMs响应。</p>\n</li>\n<li>\n<p>(4): 通过构建更全面和相互关联的知识检索机制增强LLMs的生成能力。</p>\n</li>\n</ul>\n<h2>Conclusion:</h2>\n<ul>\n<li>\n<p>(1): 本研究的意义在于提出了一种轻量高效的自动化知识图谱构建方法，弥补了传统方法在捕捉复杂关系动态方面的不足。</p>\n</li>\n<li>\n<p>(2): 创新点: 提出了基于大型语言模型（LLMs）的关键词提取和图拉普拉斯学习的方法，增强了知识检索机制；表现: 在任务上取得更全面和相互关联的知识检索机制；工作量: 通过轻量高效的自动化方法减少了工作量。</p>\n</li>\n</ul></div>'],['<div class="markdown-body"><h2>Paper:1</h2>\n<ol>\n<li>标题: AutoKG: Efficient Automated Knowledge Graph (自动知识图谱:高效自动化知识图谱)</li>\n<li>Title: AutoKG: Efficient Automated Knowledge Graph</li>\n<li>Authors: Bohan Chen and Andrea L. Bertozzi</li>\n<li>Affiliation: Department of Mathematics, University of California, Los Angeles (加州大学洛杉矶分校数学系)</li>\n<li>Keywords: Large Language Models, Knowledge Graph, Graph Learning, Retrieval-augmented Generation</li>\n</ol>\n<h2>Summary:</h2>\n<ul>\n<li>(1): 本文的研究背景是传统方法在将大型语言模型（LLMs）与知识库链接时往往无法捕捉复杂的关系动态。</li>\n<li>(2): 过去的方法包括语义相似性搜索，存在问题是难以捕捉复杂的关系动态。本文的方法是有充分动机的，提出了一种轻量高效的自动化知识图谱构建方法。</li>\n<li>(3): 本文提出的研究方法是通过使用LLM提取关键词，然后通过图拉普拉斯学习评估每对关键词之间的关系权重。使用向量相似性和基于图的关联的混合搜索方案来丰富LLM响应。</li>\n<li>(4): 本文的方法在任务上取得了更全面和相互关联的知识检索机制，从而增强了LLMs在生成更具洞察力和相关性输出方面的能力。</li>\n</ul>\n<h2>Methods:</h2>\n<ul>\n<li>\n<p>(1): 使用大型语言模型（LLMs）提取关键词。</p>\n</li>\n<li>\n<p>(2): 通过图拉普拉斯学习评估每对关键词之间的关系权重。</p>\n</li>\n<li>\n<p>(3): 利用向量相似性和基于图的关联的混合搜索方案来丰富LLMs响应。</p>\n</li>\n<li>\n<p>(4): 通过构建更全面和相互关联的知识检索机制增强LLMs的生成能力。</p>\n</li>\n</ul>\n<h2>Conclusion:</h2>\n<ul>\n<li>\n<p>(1): 本研究的意义在于提出了一种轻量高效的自动化知识图谱构建方法，弥补了传统方法在捕捉复杂关系动态方面的不足。</p>\n</li>\n<li>\n<p>(2): 创新点: 提出了基于大型语言模型（LLMs）的关键词提取和图拉普拉斯学习的方法，增强了知识检索机制；表现: 在任务上取得更全面和相互关联的知识检索机制；工作量: 通过轻量高效的自动化方法减少了工作量。</p>\n</li>\n</ul></div>']]
        # for sublist in report.summary_paper(paper_list=paper_list):
        #     print('\n'.join(sublist))

        return report_htmls


@api_report.route('/paper_report', methods=['POST'])
def api_paper_report():
    filepath = request.form.get('file_path')  # 通过request对象获取filepath参数的值
    filepath = os.path.dirname(filepath)


    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE")
    model = os.getenv("OPENAI_API_NAME")#'gpt-3.5-turbo-0301'

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
    parser.add_argument("--api_base", type=str, default=api_base, help="the api base")
    parser.add_argument("--api_key", type=str, default=api_key,
                        help="the api key")
    parser.add_argument("--llm", type=str, default=model, help="language model name")

    import time

    start_time = time.time()
    report_html = paper_report_main(args=parser.parse_args())
    html = report_html
    # report_html = [
    #         '<div class="markdown-body"><h2>Paper:1</h2>\n<ol>\n<li>标题: AutoKG: Efficient Automated Knowledge Graph (自动知识图谱:高效自动化知识图谱)</li>\n<li>Title: AutoKG: Efficient Automated Knowledge Graph</li>\n<li>Authors: Bohan Chen and Andrea L. Bertozzi</li>\n<li>Affiliation: Department of Mathematics, University of California, Los Angeles (加州大学洛杉矶分校数学系)</li>\n<li>Keywords: Large Language Models, Knowledge Graph, Graph Learning, Retrieval-augmented Generation</li>\n</ol>\n<h2>Summary:</h2>\n<ul>\n<li>(1): 本文的研究背景是传统方法在将大型语言模型（LLMs）与知识库链接时往往无法捕捉复杂的关系动态。</li>\n<li>(2): 过去的方法包括语义相似性搜索，存在问题是难以捕捉复杂的关系动态。本文的方法是有充分动机的，提出了一种轻量高效的自动化知识图谱构建方法。</li>\n<li>(3): 本文提出的研究方法是通过使用LLM提取关键词，然后通过图拉普拉斯学习评估每对关键词之间的关系权重。使用向量相似性和基于图的关联的混合搜索方案来丰富LLM响应。</li>\n<li>(4): 本文的方法在任务上取得了更全面和相互关联的知识检索机制，从而增强了LLMs在生成更具洞察力和相关性输出方面的能力。</li>\n</ul>\n<h2>Methods:</h2>\n<ul>\n<li>\n<p>(1): 使用大型语言模型（LLMs）提取关键词。</p>\n</li>\n<li>\n<p>(2): 通过图拉普拉斯学习评估每对关键词之间的关系权重。</p>\n</li>\n<li>\n<p>(3): 利用向量相似性和基于图的关联的混合搜索方案来丰富LLMs响应。</p>\n</li>\n<li>\n<p>(4): 通过构建更全面和相互关联的知识检索机制增强LLMs的生成能力。</p>\n</li>\n</ul>\n<h2>Conclusion:</h2>\n<ul>\n<li>\n<p>(1): 本研究的意义在于提出了一种轻量高效的自动化知识图谱构建方法，弥补了传统方法在捕捉复杂关系动态方面的不足。</p>\n</li>\n<li>\n<p>(2): 创新点: 提出了基于大型语言模型（LLMs）的关键词提取和图拉普拉斯学习的方法，增强了知识检索机制；表现: 在任务上取得更全面和相互关联的知识检索机制；工作量: 通过轻量高效的自动化方法减少了工作量。</p>\n</li>\n</ul></div>\n<img src="/src/assets/mermaid_imgs/diagram1.png" width="500" alt="">',
    #         '<div class="markdown-body"><h2>Paper:1</h2>\n<ol>\n<li>标题: AutoKG: Efficient Automated Knowledge Graph (自动知识图谱:高效自动化知识图谱)</li>\n<li>Title: AutoKG: Efficient Automated Knowledge Graph</li>\n<li>Authors: Bohan Chen and Andrea L. Bertozzi</li>\n<li>Affiliation: Department of Mathematics, University of California, Los Angeles (加州大学洛杉矶分校数学系)</li>\n<li>Keywords: Large Language Models, Knowledge Graph, Graph Learning, Retrieval-augmented Generation</li>\n</ol>\n<h2>Summary:</h2>\n<ul>\n<li>(1): 本文的研究背景是传统方法在将大型语言模型（LLMs）与知识库链接时往往无法捕捉复杂的关系动态。</li>\n<li>(2): 过去的方法包括语义相似性搜索，存在问题是难以捕捉复杂的关系动态。本文的方法是有充分动机的，提出了一种轻量高效的自动化知识图谱构建方法。</li>\n<li>(3): 本文提出的研究方法是通过使用LLM提取关键词，然后通过图拉普拉斯学习评估每对关键词之间的关系权重。使用向量相似性和基于图的关联的混合搜索方案来丰富LLM响应。</li>\n<li>(4): 本文的方法在任务上取得了更全面和相互关联的知识检索机制，从而增强了LLMs在生成更具洞察力和相关性输出方面的能力。</li>\n</ul>\n<h2>Methods:</h2>\n<ul>\n<li>\n<p>(1): 使用大型语言模型（LLMs）提取关键词。</p>\n</li>\n<li>\n<p>(2): 通过图拉普拉斯学习评估每对关键词之间的关系权重。</p>\n</li>\n<li>\n<p>(3): 利用向量相似性和基于图的关联的混合搜索方案来丰富LLMs响应。</p>\n</li>\n<li>\n<p>(4): 通过构建更全面和相互关联的知识检索机制增强LLMs的生成能力。</p>\n</li>\n</ul>\n<h2>Conclusion:</h2>\n<ul>\n<li>\n<p>(1): 本研究的意义在于提出了一种轻量高效的自动化知识图谱构建方法，弥补了传统方法在捕捉复杂关系动态方面的不足。</p>\n</li>\n<li>\n<p>(2): 创新点: 提出了基于大型语言模型（LLMs）的关键词提取和图拉普拉斯学习的方法，增强了知识检索机制；表现: 在任务上取得更全面和相互关联的知识检索机制；工作量: 通过轻量高效的自动化方法减少了工作量。</p>\n</li>\n</ul></div>\n<img src="/src/assets/mermaid_imgs/diagram2.png" width="500" alt="">']

    # print(report_html)
    print("summary time:", time.time() - start_time)

    return result(200, '报告生成完成，请查收~',{'report_html':report_html})

@api_report.route('/generate_img', methods=['GET'])
def generate_img():
    try:
        print("MERMAIDING______")
        for index, report_html in enumerate(html):
            # 在这里处理每个索引和对应的报告HTML内容
            print("Index:", index)
            print("Report HTML:", report_html)
            from dotenv import load_dotenv
            load_dotenv()
            llm = ChatOpenAI()
            mermaid_text = get_mermaid(report_html, llm)

            def replace_code_blocks(string):
                string = string.replace("```mermaid", "")
                string = string.replace("```", "")
                return string

            mermaid_text = replace_code_blocks(mermaid_text)
            print("mermaid_text:", mermaid_text)

            mermaid_txt_to_image(mermaid_text, "diagram{}.png".format(index + 1))

            # img_path = '<img src="/src/assets/mermaid_imgs/diagram{}.png" width="500" alt="">'.format(index + 1)

            # report_htmls_final.append(
            #     report_html[0] + "\n" + img_path)

            # print(report_htmls_final)
            return result(200, '成功生成思维图')

    except Exception as e:
        # 异常处理代码
        print("发生异常:", str(e))
        return result(400, '无法生成思维图')


# if __name__ == '__main__':
#     report_htmls = ["ss","ss"]
#     for index, report_html in enumerate(report_htmls):
#         mermaid_text = """graph TD
#             A(介绍BADAM研究)
#             A --> B(内存高效的全参数训练方法)
#             B --> C(解决大型语言模型在GPU内存有限的训练挑战)
#             B --> D(结合了Adam作为内部求解器的块坐标优化框架)
#             D --> E(通过参数分组和动态学习率调整策略)
#             E --> F(减少存储和计算成本)
#             A --> G(实验结果在Alpaca-GPT4数据集上的表现优于LoRA和LOMO方法)
#             G --> H(性能优于其他对比方法)
#             A --> I(提出新思路)
#             I --> J(为大型语言模型的优化训练提供有益探索)
#         """
#         print("mermaid_text:", mermaid_text)
#
#         mermaid_txt_to_image(mermaid_text, "diagram{}.png".format(index + 1))