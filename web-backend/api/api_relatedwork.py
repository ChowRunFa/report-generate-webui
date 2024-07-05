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
    related_work = '''
Extracting hyper-relations from text to construct comprehensive knowledge graphs is a crucial task in natural language processing (NLP) [#1]. However, limited supervised methods exist for this task. To fill this gap, a zero-shot prompt-based method using OpenAI's GPT-3.5 model is introduced, achieving promising results with a recall of 0.77. Although the precision is currently lower, a detailed analysis of the model outputs suggests potential avenues for future research [#1].

Large Language Models (LLMs) have shown promise in text-generation tasks in NLP. However, their applications in educational scenarios, particularly for domain-specific queries, remain underexplored [#2]. To address this, LLMs are evaluated for their zero-shot performance in creating domain-specific concept graphs and answering questions. TutorQA, a new NLP-focused benchmark for scientific graph reasoning and QA, is introduced. Results indicate that LLMs' zero-shot concept graph recovery is competitive with supervised methods, and in TutorQA tasks, LLMs achieve up to a 26% F1 score enhancement. Moreover, human evaluation and analysis show that LLMs generate answers with more fine-grained concepts [#2].

Deploying LLMs in specific domains faces challenges like hallucination. Existing knowledge graph retrieval-based approaches offer partial solutions, but they are not well adapted to the political domain [#3]. To address this, the Political Experts through Knowledge Graph Integration (PEG) framework is proposed. PEG utilizes a multi-view political knowledge graph (MVPKG) that integrates U.S. legislative, election, diplomatic data, and conceptual knowledge from Wikidata. PEG enhances existing methods through knowledge acquisition, aggregation, and injection, yielding superior results in political modeling tasks [#3].

Knowledge infusion enhances LLMs for domain-specific NLP tasks by directly infusing knowledge from relevant documents rather than relying on structured knowledge graphs [#4]. A simple and generalizable approach is proposed, generating prompts from the context in the input text. Experimental results demonstrate the effectiveness of this approach, evaluated by probing fine-tuned LLMs [#4].

Automated methods for knowledge graph creation (KGC) from input text have gained attention, leveraging large language models (LLMs) [#5]. However, existing methods face challenges in scaling up to text common in real-world applications due to limitations in incorporating the KG schema in LLM prompts. To overcome this, an Extract-Define-Canonicalize (EDC) framework is proposed. EDC performs open information extraction, schema definition, and post-hoc canonicalization, allowing flexibility for both predefined and automatic schema construction. Additionally, a trained component is introduced to retrieve schema elements relevant to the input text, improving extraction performance. Experimental results on three KGC benchmarks demonstrate the effectiveness of EDC in extracting high-quality triplets with larger schemas compared to prior works [#5].

In summary, prior work has addressed various challenges in extracting hyper-relational knowledge, exploring LLMs' capabilities in educational scenarios, addressing domain-specific needs, infusing knowledge directly from documents, and improving knowledge graph creation from input text. However, there is still room for improvement, and this motivates the proposed approach in this paper.'''
    reference = '''
    [1] [Construction of Hyper-Relational Knowledge Graphs Using Pre-Trained Large Language Models](https://www.semanticscholar.org/paper/714937cf949dc2da51e160bad43746d35d8b706d) (2024.0) Cited by 0 <br>[2] [Leveraging Large Language Models for Concept Graph Recovery and Question Answering in NLP Education](https://www.semanticscholar.org/paper/2ee64b780d371c9b5f7ed51d1f7a9f9fca01042c) (2024.0) Cited by 0 <br>[3] [Unifying Local and Global Knowledge: Empowering Large Language Models as Political Experts with Knowledge Graphs](https://www.semanticscholar.org/paper/379e3ee9a6a92817bd0812848b409eafb9bf9550) (nan) Cited by 2 <br>[4] [Infusing Knowledge into Large Language Models with Contextual Prompts](https://www.semanticscholar.org/paper/407a9bb8aac47a37748a581e4e98ddd0156dac97) (2024.0) Cited by 1 <br>[5] [Extract, Define, Canonicalize: An LLM-based Framework for Knowledge Graph Construction](https://www.semanticscholar.org/paper/db96e019410006c3ee0ae0184800ab206f8704dd) (2024.0) Cited by 0 <br>
    '''
    related_work = markdown_convertion(related_work)
    # reference = markdown_convertion(reference)
    return RelatedWork(args=args).generate_relatedwork()
    # return related_work_main(args=args)
    # return result(200, 'OK', {'relatedwork': related_work, 'reference': reference})





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