import asyncio
import json
import pathlib
import re
from typing import Any
from evaluate import load
import pandas as pd
import requests
from langchain_openai import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
    SystemMessage
)

from utils.markdown_utils import markdown_convertion
from utils.general_utils import result
def load_json(path: str) -> Any:
    """
    This function opens and JSON file path
    and loads in the JSON file.

    :param path: Path to JSON file
    :type path: str
    :return: the loaded JSON file
    :rtype: dict
    """
    with open(path, "r",  encoding="utf-8") as file:
        json_object = json.load(file)
    return json_object

def load_all_prompts(file_path: str = None) -> str:
    """
    Loads the api key from json file path

    :param file_path:
    :return:
    """
    cur_dir = pathlib.Path(__file__).parent.resolve()
    # Load prompts from file
    if not file_path:
        # Default file path
        # file_path = f"{cur_dir}/utils/prompts.json"
        file_path = r"D:\Pycharm_Projects\report-generate-webui\web-backend\utils\prompts.json"
    prompts = load_json(file_path)

    return prompts


class RelatedWork:
    def __init__(self,args=None):
        self.base_paper_url = args.base_paper_url
        self.sort_by = args.sort_by
        self.num_papers = args.num_papers
        self.s2_api_key = args.s2_api_key
        self.rerank = args.rerank
        self.keyword = args.keyword
        self.base_abstract = args.base_abstract
        self.cite_format = args.cite_format
        self.limit_words = args.limit_words
        self.llm =  ChatOpenAI(
                model_name=args.model,
                openai_api_base=args.api_base,
                openai_api_key=args.api_key,
                streaming=False,
            )
        # self.llm = ChatOpenAI(
        #         model_name="chatglm",
        #         openai_api_base="http://localhost:8000/v1",
        #         openai_api_key="EMPTY",
        #         streaming=False,
        #     )
        self.prompts = load_all_prompts()
        self.role_template = self.prompts["role_template"]
        self.plan_prompt = self.prompts["plan_template"]
        self.vanilla_prompt = self.prompts["vanilla_template"]
        self.sample_plan = self.prompts["plan"]
        self.summarization_prompt = self.prompts["summarization_template"]
        self.ranking_prompt = self.prompts["ranking_template"]
        self.wer = load("wer")

    def sort_papers(self,papers):
        """
        sort by categories: "Relevance", "Citations", "Year
        """
        df = pd.DataFrame(papers)
        if self.sort_by == "Citations":
            df = df.sort_values(by="citationCount", ascending=False)
        elif self.sort_by == "Year":
            df = df.sort_values(by="year", ascending=False)
        papers_list = df.to_dict(orient='records')
        return papers_list

    def parse_arxiv_id_from_paper_url(self,url):
        arxiv_id = url.split("/")[-1]
        if arxiv_id[-4:] == ".pdf":
            arxiv_id = arxiv_id[:-4]
        return arxiv_id

    def get_recommendations_from_semantic_scholar(self,num_papers_api=20):
        """
        https://www.semanticscholar.org/product/api/tutorial
        """
        fields = 'title,url,abstract,citationCount,journal,isOpenAccess,fieldsOfStudy,year,journal'
        arxiv_id = self.parse_arxiv_id_from_paper_url(self.base_paper_url)
        query_id = f"ArXiv:{arxiv_id}"

        rsp = requests.post(
            "https://api.semanticscholar.org/recommendations/v1/papers/",
            json={
                "positivePaperIds": [query_id],
            },
            params={"fields": fields, "limit": num_papers_api},
        )

        results = rsp.json()
        papers = results['recommendedPapers']
        return papers

    def format_abstracts_as_references(self,papers):
        # cite_list = ["@cite_1", "@cite_2", "@cite_3"]
        cite_text = ""
        for index, paper in enumerate(papers):
            # citation = f"@cite_{index+1}"
            citation = f"{index + 1}"
            cite_text = f"{cite_text}[{citation}]: {paper['abstract']}\n"
        return cite_text

    def format_results_into_markdown(self,recommendations):
        comment = "The following papers were found by the Semantic Scholar API \n\n"
        for index, r in enumerate(recommendations):
            # hub_paper_url = f"https://huggingface.co/papers/{r['externalIds']['ArXiv']}"
            # comment += f"* [{r['title']}]({hub_paper_url}) ({r['year']})\n"
            comment += f"[{index + 1}] [{r['title']}]({r['url']}) ({r['year']}) Cited by {r['citationCount']} <br>"
        return comment

    def get_markdown_query_text(self,papers):
        reference_markdown = self.format_results_into_markdown(papers)
        cite_text = self.format_abstracts_as_references(papers)
        return reference_markdown, cite_text

    def get_complete_prompt_for_summarization(self,base_prompt, data):
        """
        This prompt helps in getting keywords to be used by S2 API
        """
        complete_prompt = f"{base_prompt}\n```Abstract: {data}```"
        return complete_prompt

    def format_prompt(self,base_prompt, cite_text, plan=""):
        if plan:
            data = f"Abstract: {self.base_abstract} \n {cite_text} \n Plan: {plan}"
        else:
            data = f"Abstract: {self.base_abstract} \n {cite_text}"
        complete_prompt = f"{base_prompt}\n```{data}```"
        return complete_prompt

    def get_paper_data(self):
        """
        Retrieves data of one paper based on URL
        """
        fields = 'title,url,abstract,citationCount,journal,isOpenAccess,fieldsOfStudy,year,journal'
        rsp = requests.get(f"https://api.semanticscholar.org/graph/v1/paper/URL:{self.base_paper_url}",
                           headers={'X-API-KEY': self.s2_api_key},
                           params={'fields': fields})
        results = rsp.json()
        return results

    def find_basis_paper(self,query, num_papers_api=20):
        fields = 'title,url,abstract,citationCount,journal,isOpenAccess,fieldsOfStudy,year,journal'
        rsp = requests.get('https://api.semanticscholar.org/graph/v1/paper/search',
                           headers={'X-API-KEY': self.s2_api_key},
                           params={'query': query, 'limit': num_papers_api, 'fields': fields})
        rsp.raise_for_status()
        results = rsp.json()
        total = results["total"]
        if not total:
            print('No matches found. Please try another query.')

        print(f'Found {total} results. Showing up to {num_papers_api}.')
        papers = results['data']
        # df = pd.DataFrame(papers)
        return papers  # [:result_limit]

    def check_matching_paper(self, papers, check_papers: int = 3, wer_threshold=0.12):
        """
        Check if the user put the abstract of already existing paper and it is in the retrieved papers.
        Using Word error rate as the metric on the top check_papers
        """
        references = [self.base_abstract]
        for i in range(check_papers):
            predictions = [papers[i]['abstract']]
            wer_score = self.wer.compute(predictions=predictions, references=references)
            if wer_score < wer_threshold:
                papers.pop(i)
                return papers
        return papers


    def run_open_ai_api(self,json_data) -> str:
        """
        This function actually calls the OpenAI API
        Models such as gpt-4-32k, gpt-4-1106-preview
        :param json_data:
        :return:
        """
        messages = [
            SystemMessage(role='system',
                          content="You are a helpful assistant"),
            HumanMessage(role='user', content="{}".format(json_data['prompt']))
        ]
        llm = self.llm
        response = llm(messages)
        # result = response.content
        return response.content

    async def run_open_ai_api_stream(self,json_data):
        messages = [
            SystemMessage(role='system',
                          content="You are a helpful assistant."),
            HumanMessage(role='user', content="{}".format(json_data['prompt']))
        ]

        chunks = []
        async for chunk in self.llm.astream(messages):
            chunks.append(chunk)
            print(chunk.content, end="", flush=True)

        # Call the async function to execute the code

    def generate_reference(self):
        print("Generating")
        try:
            if self.base_paper_url:
                hist_response = f"Finding recommendations from S2 API based on the paper \n {self.base_paper_url}"
                papers = self.get_recommendations_from_semantic_scholar()
            else:
                if self.keyword:
                    query = self.keyword
                else:
                    # query = "multi document summarization"
                    prompt = self.get_complete_prompt_for_summarization(self.summarization_prompt,self.base_abstract)
                    json_data = {"prompt": prompt}
                    query = self.run_open_ai_api(json_data)
                # print(query)
                hist_response = f"LLM summarized keyword query to be used for S2 API: \n {query}"
                papers = self.find_basis_paper(query)
        except:
            print("Exception: 使用S2没有搜索到相关的文章，请尝试修改查询条件~")
            return  "Exception: 使用S2没有搜索到相关的文章，请尝试修改查询条件~"
        if not papers:
            print("Exception:使用S2没有搜索到相关的文章，请尝试修改查询条件~")
            return "使用S2没有搜索到相关的文章，请尝试修改查询条件~"
        papers = self.sort_papers(papers)
        # try:
        #     papers = self.check_matching_paper(papers)
        # except:
        #     print("WER failed")
        papers = self.sort_papers(papers)
        reference_markdown, cite_text = self.get_markdown_query_text(papers)
        if self.rerank == "True":
            # print(f"{self.role_template}{self.ranking_prompt}")
            try:
                complete_prompt = self.format_prompt(base_prompt=f"{self.role_template} {self.ranking_prompt}", cite_text=cite_text)
                json_data = {"prompt": complete_prompt}
                response = self.run_open_ai_api(json_data)
                # print(response)
                # [1] > [2] > [4] > [3] > [6] > [5]
                new_order = [int(s) for s in re.findall(r'\d+', response)]
                # print(new_order)
                papers = [papers[i-1] for i in new_order]
            except:
                print("LLM not able to rerank!")
        # if self.base_paper_url:
        #     try:
        #         base_paper_data = self.get_paper_data()
        #         papers.insert(0, base_paper_data)
        #     except:
        #         print("Cant retrieve data for base paper!")
        papers = papers[:self.num_papers]
        reference_markdown, cite_text = self.get_markdown_query_text(papers)
        print("cite_text----------",cite_text)
        return reference_markdown, cite_text

    def generate_relatedwork(self):
        reference_markdown, cite_text = self.generate_reference()

        if cite_text =="":
            return "How may I help?"

        if self.cite_format:
            complete_prompt = self.format_prompt(base_prompt=self.plan_prompt, cite_text=cite_text, plan=self.cite_format)
        else:
            self.vanilla_prompt = self.vanilla_prompt.format(max_tokens=self.limit_words)
            # print(self.vanilla_prompt)
            complete_prompt = self.format_prompt(base_prompt=self.vanilla_prompt, cite_text=cite_text, plan="")
        json_data = {"prompt": complete_prompt}
        response = self.run_open_ai_api(json_data)
        print({'relatedwork':response,'reference':reference_markdown})
        return result(200,'OK',{'relatedwork':markdown_convertion(response),'reference':reference_markdown})
    def generate_relatedwork_stream(self):
        reference_markdown, cite_text = self.generate_reference()
        print(reference_markdown)
        print('----------------------------------')
        if cite_text =="":
            return "How may I help?"

        if self.cite_format:
            complete_prompt = self.format_prompt(base_prompt=self.plan_prompt, cite_text=cite_text, plan=self.cite_format)
        else:
            self.vanilla_prompt = self.vanilla_prompt.format(max_tokens=self.limit_words)
            # print(self.vanilla_prompt)
            complete_prompt = self.format_prompt(base_prompt=self.vanilla_prompt, cite_text=cite_text, plan="")
        json_data = {"prompt": complete_prompt}

        asyncio.run(self.run_open_ai_api_stream(json_data))
