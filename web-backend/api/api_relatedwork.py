import argparse
import sys,os

import markdown
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()  # 加载.env文件


from flask import Blueprint, request, jsonify

sys.path.append("..")
from utils.markdown_utils import markdown_convertion
from objs.RelatedWork import RelatedWork
from utils.general_utils import result


def related_work_main(args):
    return RelatedWork(args).generate_relatedwork()

api_relatedwork = Blueprint('api_relatedwork', __name__)
@api_relatedwork.route('/related_work', methods=['POST'])
def api_related_work():
#     related_work = '''
# **Related Work**\n\nIn the realm of large language models (LLMs), handling long contexts is vital for tasks like multi-round dialogues and document summarization[#2]. Previous works have highlighted the challenges posed by long-context processing, with attention mechanisms' quadratic complexity and memory consumption during generation being significant obstacles[#4]. MemLong introduced a memory-augmented retrieval approach to address these issues, outperforming other LLMs and extending context length substantially[#4].\n\nQuery rewriting in retrieval-augmented generation (RAG) systems is crucial for enhancing user information needs understanding[#1]. Existing approaches, such as reinforcement learning with generation feedback, have limitations due to sparse rewards and unstable training[#1]. MaFeRw proposes a novel query rewriting method that integrates multi-aspect dense rewards from retrieval processes and generated results to achieve stable and satisfactory responses[#1]. This contrasts with prior works that focus solely on context-based rewriting without leveraging dense rewards from retrieved documents and ground truth[#1].\n\nMulti-hop question answering (QA) systems require complex reasoning and integration of multiple information pieces[#3]. HiRAG presents a hierarchical retrieval-augmented generation model that effectively combines sparse and dense retrieval strategies to handle outdated information and accuracy-quantity trade-offs[#3]. HiRAG outperforms existing models and introduces new corpora to address outdated and insufficient knowledge issues[#3].\n\nPrompt optimization methods have shown success in enhancing LLM performance, but often overlook query-preferred prompts leading to suboptimal performances[#5]. QPO introduces a query-dependent prompt optimization approach using offline reinforcement learning to iteratively fine-tune prompts tailored to input queries, improving prompting effects significantly[#5]. The method efficiently utilizes existing prompting data and continuously augments the dataset to generate optimal prompts[#5].\n\n综合以上相关工作可见，现有大型语言模型在处理长文本上面临挑战，而MemLong通过使用外部检索器来增强长文本语言建模的能力，有效地解决了这一问题[#4]。另一方面，查询重写在检索增强生成系统中起着关键作用，MaFeRw提出了一种集成了多方面奖励的新型查询重写方法，从而实现了更稳定和令人满意的响应[#1]。此外，多跳问答系统需要复杂推理，HiRAG提出了一个层次化的检索增强生成模型，有效地结合了稀疏和密集检索策略，处理了过时信息和准确性-数量折衷问题[#3]。最后，对于优化提示方法，QPO引入了一种依赖于查询的提示优化方法，通过离线强化学习迭代地调整与输入查询相关的最佳提示，显著提高了大型目标语言模型的提示效果[#5]。'''
#     reference = '''
# The following papers were found by the Semantic Scholar API \n\n[1] [MaFeRw: Query Rewriting with Multi-Aspect Feedbacks for Retrieval-Augmented Large Language Models](https://www.semanticscholar.org/paper/66cbace0db91e9648e439d1530c021ae3199eb2e) (2024.0) Cited by 0 <br>[2] [E2LLM: Encoder Elongated Large Language Models for Long-Context Understanding and Reasoning](https://www.semanticscholar.org/paper/3b2ae15f7c640cbb0438e92c31b3fe02b3367ac0) (2024.0) Cited by 0 <br>[3] [Hierarchical Retrieval-Augmented Generation Model with Rethink for Multi-hop Question Answering](https://www.semanticscholar.org/paper/68acf42708fd3bfad548872d04330ed089019d45) (2024.0) Cited by 0 <br>[4] [MemLong: Memory-Augmented Retrieval for Long Text Modeling](https://www.semanticscholar.org/paper/d71c5684f85a3b732e2e6403b605a67f72bb1699) (2024.0) Cited by 0 <br>[5] [QPO: Query-dependent Prompt Optimization via Multi-Loop Offline Reinforcement Learning](https://www.semanticscholar.org/paper/5ffa572d5126166a04b21ebb4e462016192297f3) (2024.0) Cited by 0 <br>'''
#     related_work = markdown_convertion(related_work)
#     reference = markdown_convertion(reference)
#     return result(200, 'OK', {'relatedwork': related_work, 'reference': reference})


    # 通过request对象获取参数的值
    sort_by = request.get_json()['_value'].get('sort_by')
    s2_api_key = request.get_json()['_value'].get('s2_api_key')
    base_paper_url = request.get_json()['_value'].get('base_paper_url')
    num_papers = request.get_json()['_value'].get('num_papers')
    rerank = request.get_json()['_value'].get('rerank')
    keyword = request.get_json()['_value'].get('keyword')
    base_abstract = request.get_json()['_value'].get('base_abstract')
    cite_format = request.get_json()['_value'].get('cite_format')
    limit_words = request.get_json()['_value'].get('limit_words')
    # sort_by = ''
    # s2_api_key = ''
    # base_paper_url = ''
    # num_papers = ''
    # rerank = ''
    # keyword = ''
    # base_abstract = ''
    # cite_format = ''
    # limit_words = ''

    parser = argparse.ArgumentParser()

    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE")
    model = os.getenv("OPENAI_API_NAME")

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
#

    return RelatedWork(args=args).generate_relatedwork()
    # return related_work_main(args=args)






# if __name__ == "__main__":
#     api_key = os.getenv("OPENAI_API_KEY")
#     api_base = os.getenv("OPENAI_API_BASE")
#     model = os.getenv("OPENAI_API_NAME")
#     client = ChatOpenAI(
#         openai_api_key=api_key,
#         openai_api_base=api_base,
#         model_name=model
#     )
#
#     messages = [
#         SystemMessage(role='system',
#                       content="You are a helpful assistant."),
#         HumanMessage(role='user', content="你是谁？")
#     ]
#
#     response = client(messages)
#     # result = response.content
#     print(response.content)