import argparse
import configparser
import datetime
import io
import re
import sys

import fitz
import openai
import os

import tenacity
import tiktoken
from PIL import Image
from langchain.chains.llm import LLMChain
from langchain_community.chat_models.openai import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.schema import (
    HumanMessage,
    SystemMessage
)

class Report:
    # 初始化方法，设置属性

    def __init__(self,key_word,api_base,api_key,llm,args=None):
        if args.language == 'en':
            self.language = 'English'
        elif args.language == 'zh':
            self.language = 'Chinese'
        # 获取某个键对应的值
        self.api_base = api_base
        self.api_key = api_key
        self.llm =  ChatOpenAI(
                model_name=llm,
                openai_api_base=self.api_base,
                openai_api_key=self.api_key,
                streaming=False,
            )
        # llm = ChatOpenAI(
        #         model_name="chatglm",
        #         openai_api_base="http://localhost:8000/v1",
        #         openai_api_key="EMPTY",
        #         streaming=False,
        #     )
        self.key_word = key_word  # 读者感兴趣的关键词

        self.file_format = 'md'
        self.max_token_num = 4096
        self.encoding = tiktoken.get_encoding("gpt2")

    def validateTitle(self, title):
        # 将论文的乱七八糟的路径格式修正
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title)  # 替换为下划线
        return new_title

    def summary_paper(self, paper_list):
        result_htmls = []
        htmls = []
        # for paper_index, paper in enumerate(paper_list):
        #     # 第一步先用title，abs，和introduction进行总结。
        #     text = ''
        #     text += 'Title:' + paper.title
        #     text += 'Url:' + paper.url
        #     text += 'Abstract:' + paper.abs
        #     print('-----paper.abs:---', text, '-----paper.abs:---')
        #     text += 'Paper_info:' + paper.section_text_dict['paper_info']
        #     print('-----text:---', text, '-----text:---')
        #     # intro
        #     text += list(paper.section_text_dict.values())[0]
        #     chat_summary_text = ""
        #     try:
        #         chat_summary_text = self.final_summary(text=text)
        #     except Exception as e:
        #         print("summary_error:", e)
        #         import sys
        #         exc_type, exc_obj, exc_tb = sys.exc_info()
        #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #         print(exc_type, fname, exc_tb.tb_lineno)
        #         if "maximum context" in str(e):
        #             current_tokens_index = str(e).find("your messages resulted in") + len(
        #                 "your messages resulted in") + 1
        #             offset = int(str(e)[current_tokens_index:current_tokens_index + 4])
        #             summary_prompt_token = offset + 1000 + 150
        #             chat_summary_text = self.final_summary(text=text, summary_prompt_token=summary_prompt_token)
        #
        #     htmls.append('## Paper:' + str(paper_index + 1))
        #     htmls.append('\n\n')
        #     htmls.append(chat_summary_text)
        #
        #     # 第二步总结方法：
        #     # TODO，由于有些文章的方法章节名是算法名，所以简单的通过关键词来筛选，很难获取，后面需要用其他的方案去优化。
        #     method_key = ''
        #     for parse_key in paper.section_text_dict.keys():
        #         if 'method' in parse_key.lower() or 'approach' in parse_key.lower():
        #             method_key = parse_key
        #             break
        #
        #     if method_key != '':
        #         text = ''
        #         method_text = ''
        #         summary_text = ''
        #         summary_text += "<summary>" + chat_summary_text
        #         # methods
        #         method_text += paper.section_text_dict[method_key]
        #         text = summary_text + "\n\n<Methods>:\n\n" + method_text
        #         chat_method_text = ""
        #         try:
        #             chat_method_text = self.chat_method(text=text)
        #         except Exception as e:
        #             print("method_error:", e)
        #             import sys
        #             exc_type, exc_obj, exc_tb = sys.exc_info()
        #             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #             print(exc_type, fname, exc_tb.tb_lineno)
        #             if "maximum context" in str(e):
        #                 current_tokens_index = str(e).find("your messages resulted in") + len(
        #                     "your messages resulted in") + 1
        #                 offset = int(str(e)[current_tokens_index:current_tokens_index + 4])
        #                 method_prompt_token = offset + 800 + 150
        #                 chat_method_text = self.chat_method(text=text, method_prompt_token=method_prompt_token)
        #         htmls.append(chat_method_text)
        #     else:
        #         chat_method_text = ''
        #     htmls.append("\n" * 4)
        #
        #     # 第三步总结全文，并打分：
        #     conclusion_key = ''
        #     for parse_key in paper.section_text_dict.keys():
        #         if 'conclu' in parse_key.lower():
        #             conclusion_key = parse_key
        #             break
        #
        #     text = ''
        #     conclusion_text = ''
        #     summary_text = ''
        #     summary_text += "<summary>" + chat_summary_text + "\n <Method summary>:\n" + chat_method_text
        #     if conclusion_key != '':
        #         # conclusion
        #         conclusion_text += paper.section_text_dict[conclusion_key]
        #         text = summary_text + "\n\n<Conclusion>:\n\n" + conclusion_text
        #     else:
        #         text = summary_text
        #     chat_conclusion_text = ""
        #     try:
        #         chat_conclusion_text = self.chat_conclusion(text=text)
        #     except Exception as e:
        #         print("conclusion_error:", e)
        #         import sys
        #         exc_type, exc_obj, exc_tb = sys.exc_info()
        #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #         print(exc_type, fname, exc_tb.tb_lineno)
        #         if "maximum context" in str(e):
        #             current_tokens_index = str(e).find("your messages resulted in") + len(
        #                 "your messages resulted in") + 1
        #             offset = int(str(e)[current_tokens_index:current_tokens_index + 4])
        #             conclusion_prompt_token = offset + 800 + 150
        #             chat_conclusion_text = self.chat_conclusion(text=text,
        #                                                         conclusion_prompt_token=conclusion_prompt_token)
        #
        #     htmls.append(chat_conclusion_text)
        #     htmls.append("\n" * 4)
        #
        #     result_htmls.append(htmls)
        #     # return htmls
        #     # # # 整合成一个文件，打包保存下来。
        #     # date_str = str(datetime.datetime.now())[:13].replace(' ', '-')
        #     # export_path = os.path.join(self.root_path, 'export')
        #     # if not os.path.exists(export_path):
        #     #     os.makedirs(export_path)
        #     # mode = 'w' if paper_index == 0 else 'a'
        #     # file_name = os.path.join(export_path,
        #     #                          date_str + '-' + self.validateTitle(paper.title[:80]) + "." + self.file_format)
        #     # self.export_to_markdown("\n".join(htmls), file_name=file_name, mode=mode)
        #     #
        #     # # file_name = os.path.join(export_path, date_str+'-'+self.validateTitle(paper.title)+".md")
        #     # # self.export_to_markdown("\n".join(htmls), file_name=file_name, mode=mode)
        #     # htmls = []
        test_text = ['## Paper:1', '\n\n\n',
                     '1. 标题: 智源开源新一代多模态基础模型 Emu2\n2. Title: New Generation Multi-modal Base Model Emu2 Released by Zhivian Open Source\n3. Authors: Zhivian Research Institute\n4. 发布单位及发布时间: 智源研究院于2023年12月21日发布\n5. Summary:\n   - (1) 研究背景：本文介绍了智源研究院发布的新一代多模态基础模型 Emu2，旨在提升多模态上下文学习能力。\n   - (2) 过去方法及问题：本文提到 Flamingo-80B、IDEFICS-80B等主流多模态预训练大模型在少样本多模态理解任务上存在一些问题。因此，本文的方法是有很好的动机性。\n   - (3) 研究方法：Emu2采用了大规模自回归生成式多模态预训练，并在编码器语义空间重建图像的解码器上进行训练。\n   - (4) 研究成果：Emu2在多项少样本理解、视觉问答、主体驱动图像生成等任务中表现出最佳性能，超越了Flamingo-80B、IDEFICS-80B等主流多模态预训练大模型。因此，该模型的性能支持了他们的目标。',
                     '\n\n\n\n',
                     '8. Conclusion:\n\n- (1): 本文介绍了智源研究院发布的新一代多模态基础模型 Emu2，该模型的研发意义在于提升多模态上下文学习能力，解决了过去主流多模态预训练大模型在少样本多模态理解任务上存在的问题。\n\n- (2): 创新点：Emu2采用了大规模自回归生成式多模态预训练，并在编码器语义空间重建图像的解码器上进行训练，这一方法在多模态任务中取得了显著的性能提升。性能：Emu2在多项少样本理解、视觉问答、主体驱动图像生成等任务中展现出最佳性能，超越了过去的主流多模态预训练大模型，证明了其在多模态学习领域的优越性。工作量：本文提出的Emu2模型展示了智源研究院在多模态学习领域的技术实力，为研究者提供了一个高效且强大的基础模型，减少了他们在模型构建上的工作量。\n\n请确保使用中文回答（专有名词需要用英文标记），陈述要简洁、学术化，并且不要重复前面的<summary>内容，使用原始数字的价值，严格按照格式进行，将相应的内容输出为xxx，换行符按照要求填写，如果没有，则可以不写。',
                     '\n\n\n\n']
        for paper_index, paper in enumerate(paper_list):
            result_htmls.append(test_text)
        return result_htmls
    # @tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
    #                 stop=tenacity.stop_after_attempt(5),
    #                 reraise=True)
    def chat_method(self, text, method_prompt_token=800):
        text_token = len(self.encoding.encode(text))
        clip_text_index = int(len(text) * (self.max_token_num - method_prompt_token) / text_token)
        clip_text = text[:clip_text_index]


        messages = [
            SystemMessage(role='system', content="You are a researcher in the field of [" + self.key_word + "] who is good at summarizing papers using concise statements"),
            SystemMessage(role='assistant', content="This is the <summary> and <Method> part of an English document, where <summary> you have summarized, but the <Methods> part, I need your help to read and summarize the following questions." + clip_text),
            HumanMessage(role = 'user', content="""                 
                 7. Describe in detail the methodological idea of this article. Be sure to use {} answers (proper nouns need to be marked in English). For example, its steps are.
                    - (1):...
                    - (2):...
                    - (3):...
                    - .......
                 Be sure to use {} answers (proper nouns need to be marked in English), statements as concise and academic as possible, do not repeat the content of the previous <summary>, the value of the use of the original numbers, be sure to strictly follow the format, the corresponding content output to xxx, in accordance with \n line feed, ....... means fill in according to the actual requirements, if not, you can not write.                 
                 Follow the format of the output that follows: 
                 ## Methods: \n\n
                    - (1):xxx;\n 
                    - (2):xxx;\n 
                    - (3):xxx;\n  
                    ....... \n\n     
                """.format(self.language, self.language))
        ]
        llm = self.llm
        response = llm(messages)
        print("method_result:\n", response.content)
        # print("prompt_token_used:", response.prompt_tokens,
        #       "completion_token_used:", response.completion_tokens,
        #       "total_token_used:", response.total_tokens)
        return response.content

    # @tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
    #                 stop=tenacity.stop_after_attempt(5),
    #                 reraise=True)
    def chat_conclusion(self, text, conclusion_prompt_token=800):
        text_token = len(self.encoding.encode(text))
        clip_text_index = int(len(text) * (self.max_token_num - conclusion_prompt_token) / text_token)
        clip_text = text[:clip_text_index]

        messages = [
            SystemMessage(role='system',
                          content="You are a reviewer in the field of [" + self.key_word + "] and you need to critically review this article"),
            SystemMessage(role='assistant',
                          content="This is the <summary> and <conclusion> part of an English literature, where <summary> you have already summarized, but <conclusion> part, I need your help to summarize the following questions:" + clip_text),
            HumanMessage(role='user', content="""                 
                 8. Make the following summary.Be sure to use {} answers (proper nouns need to be marked in English).
                    - (1):What is the significance of this piece of work?
                    - (2):Summarize the strengths and weaknesses of this article in three dimensions: innovation point, performance, and workload.                   
                    .......
                Be sure to use {} answers (proper nouns need to be marked in English), statements as concise and academic as possible, do not repeat the content of the previous <summary>, the value of the use of the original numbers, be sure to strictly follow the format, the corresponding content output to xxx, in accordance with \n line feed, ....... means fill in according to the actual requirements, if not, you can not write.                 
                Follow the format of the output later:
                 ## Conclusion: \n\n
                    - (1):xxx;\n                     
                    - (2):Innovation point: xxx; Performance: xxx; Workload: xxx;\n                      
                 """.format(self.language, self.language))
        ]

        llm = self.llm
        response = llm(messages)
        # result = response.content
        print("conclusion_result:\n", response.content)
        # print("prompt_token_used:", response.prompt_tokens,
        #       "completion_token_used:", response.completion_tokens,
        #       "total_token_used:", response.total_tokens)
        return response.content

    # @tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
    #                 stop=tenacity.stop_after_attempt(5),
    #                 reraise=True)
    def final_summary(self, text, summary_prompt_token=1100):
        openai.api_key = self.api_key
        text_token = len(self.encoding.encode(text))
        clip_text_index = int(len(text) * (self.max_token_num - summary_prompt_token) / text_token)
        clip_text = text[:clip_text_index]

        # 设定 AI 的角色和目标
        system_template = "You are a reviewer in the field of {keyword} and you need to critically review this article"
        system_prompt = SystemMessagePromptTemplate.from_template(system_template)
        assistant_template = ("This is the <summary> and <conclusion> part of an English literature,"
                              " where <summary> you have already summarized, but <conclusion> part, I need your help to summarize the following questions: {clip_text}")
        assistant_prompt = SystemMessagePromptTemplate.from_template(assistant_template)

        human_template = """                 
                 1. Mark the title of the paper (with Chinese translation)
                 2. Mark the title of the paper (use English)
                 3. list all the authors' names (use English)
                 4. mark the first author's affiliation (总结这篇文章的发布单位和发布时间)     
                 5. summarize according to the following four points.Be sure to use {language} answers (proper nouns need to be marked in English)
                    - (1):What is the research background of this article?
                    - (2):What are the past methods? What are the problems with them? Is the approach well motivated?
                    - (3):What is the research methodology proposed in this paper?
                    - (4):On what task and what performance is achieved by the methods in this paper? Can the performance support their goals?
                 Be sure to use {language} answers (proper nouns need to be marked in English), statements as concise and academic as possible, do not have too much repetitive information, numerical values using the original numbers, be sure to strictly follow the format, the corresponding content output to xxx, in accordance with \n line feed.  
                 Follow the format of the output that follows:                  
                 # 标题 : xxx\n\n
                 # Title : xxx\n\n
                 ## xxxx年xx月，由xxxx等在xxxx上发表\n\n                       
                 ## Summary: \n\n               
                 """

        human_prompt = HumanMessagePromptTemplate.from_template(human_template)

        # 将以上所有信息结合为一个聊天提示
        chat_prompt = ChatPromptTemplate.from_messages([system_prompt, assistant_prompt, human_prompt])
        prompt = chat_prompt.format_prompt(keyword = self.key_word,clip_text = clip_text, language = self.language).to_messages()

        llm = self.llm

        result = llm(prompt).content
        print("summary_result:\n", result)
        return result
