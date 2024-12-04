import os
import time
from datetime import datetime

import PyPDF2
from docx import Document
import openai
from dotenv import load_dotenv
import faiss
import numpy as np
from tqdm import tqdm
from werkzeug.utils import secure_filename

openai_pricing = {
    "gpt-4o-mini": {
        "input_tokens": {
            "standard": 0.150,  # $0.150 per 1M input tokens
            "batch_api": 0.075,  # $0.075 per 1M input tokens (Batch API)
            "cached": 0.075  # $0.075 per 1M cached input tokens
        },
        "output_tokens": {
            "standard": 0.600,  # $0.600 per 1M output tokens
            "batch_api": 0.300  # $0.300 per 1M output tokens (Batch API)
        }
    },
    "gpt-4o-mini-2024-07-18": {
        "input_tokens": {
            "standard": 0.150,  # $0.150 per 1M input tokens
            "batch_api": 0.075,  # $0.075 per 1M input tokens (Batch API)
            "cached": 0.075  # $0.075 per 1M cached input tokens
        },
        "output_tokens": {
            "standard": 0.600,  # $0.600 per 1M output tokens
            "batch_api": 0.300  # $0.300 per 1M output tokens (Batch API)
        }
    },
    "text-embedding-3-small": {
        "input_tokens": {
            "standard": 0.020,  # $0.020 per 1M input tokens
            "batch_api": 0.010  # $0.010 per 1M input tokens (Batch API)
        },
        "output_tokens": {
            "standard": 0.600,  # $0.600 per 1M output tokens
            "batch_api": 0.300  # $0.300 per 1M output tokens (Batch API)
        }
    },
    "text-embedding-3-large": {
        "input_tokens": {
            "standard": 0.130,  # $0.130 per 1M input tokens
            "batch_api": 0.065  # $0.065 per 1M input tokens (Batch API)
        },
        "output_tokens": {
            "standard": 0.600,  # $0.600 per 1M output tokens
            "batch_api": 0.300  # $0.300 per 1M output tokens (Batch API)
        }
    },
    "ada v2": {
        "input_tokens": {
            "standard": 0.100,  # $0.100 per 1M input tokens
            "batch_api": 0.050  # $0.050 per 1M input tokens (Batch API)
        },
        "output_tokens": {
            "standard": 0.600,  # $0.600 per 1M output tokens
            "batch_api": 0.300  # $0.300 per 1M output tokens (Batch API)
        }
    }
}



class FrameworkReport:
    def __init__(self, api_key=None, api_base=None, embedding_model="text-embedding-3-small",llm_model=None):
        # 加载环境变量
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.api_base = api_base or os.getenv("OPENAI_API_BASE")
        openai.api_key = self.api_key
        openai.api_base = self.api_base
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.api_base
        )
        self.embedding_model = embedding_model
        self.model = llm_model or os.getenv("OPENAI_API_NAME","gpt-4o-mini")

        # 定价信息（美元）
        self.cost_per_1m_input_tokens = openai_pricing[self.model]["input_tokens"]["standard"]
        self.cost_per_1m_output_tokens = openai_pricing[self.model]["output_tokens"]["standard"]
        self.cost_per_1m_input_embedding_tokens = openai_pricing[self.embedding_model]["input_tokens"]["standard"]
        self.cost_per_1m_output_embedding_tokens = openai_pricing[self.embedding_model]["output_tokens"]["standard"]

    def read_pdf(self, file_path):
        content = []
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    content.append({"page": page_num + 1, "text": text})
        return content

    def read_word(self, file_path):
        document = Document(file_path)
        content = [para.text.strip() for para in document.paragraphs if para.text.strip()]
        return content

    def split_content(self, content, max_length=2048):
        blocks = []
        current_block = ""
        for segment in content:
            if len(current_block) + len(segment) < max_length:
                current_block += f"{segment}\n"
            else:
                blocks.append(current_block.strip())
                current_block = segment
        if current_block:
            blocks.append(current_block.strip())
        return blocks

    def get_embeddings(self, texts):
        embeddings = []
        total_input_tokens = 0
        for text in tqdm(texts, desc="生成嵌入向量"):
            response = self.client.embeddings.create(
                input=text,
                model=self.embedding_model
            )
            embeddings.append(response.data[0].embedding)
            total_input_tokens += response.usage.total_tokens
        return embeddings, total_input_tokens

    def build_faiss_index(self, embeddings):
        dimension = len(embeddings[0])
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings).astype('float32'))
        return index

    def retrieve_relevant_blocks(self, query, index, blocks, top_k=5):
        response = self.client.embeddings.create(
            input=query,
            model=self.embedding_model
        )
        query_embedding = response.data[0].embedding
        D, I = index.search(np.array([query_embedding]).astype('float32'), top_k)
        return [blocks[i] for i in I[0] if i < len(blocks)], response.usage.total_tokens

    def generate_report_with_feedback(self, framework, index, blocks):
        """基于 RAG 和 LLM 生成报告内容，并记录时间和 token 消耗"""
        report = []
        total_input_tokens = 0
        total_output_tokens = 0
        total_input_embedding_tokens = 0
        total_output_embedding_tokens = 0
        start_time = time.time()

        for section_title, prompt in tqdm(framework.items(),
                                          desc="初始化章节处理...",
                                          leave=True,
                                          ncols=100):
            tqdm.write(f"正在处理章节: {section_title}")

            section_content = f"# {section_title}\n\n"
            print(f"标题：{section_content}，prompts为：{prompt}")
            # 检索与提示相关的内容块
            relevant_blocks, embedding_tokens = self.retrieve_relevant_blocks(prompt, index, blocks, top_k=2)
            total_input_embedding_tokens += embedding_tokens
            context = "\n\n".join(relevant_blocks)
            full_prompt = f"请严格控制字数，你的回答不能超过100个字！{prompt}\n\n基于以下内容生成详细报告：\n{context}"

            # 使用 GPT 生成报告内容
            response = self.client.chat.completions.create(
                model=os.getenv('OPENAI_API_NAME', 'gpt-4o-mini'),
                messages=[
                    {"role": "system", "content": "你是一个善于生成精简报告的人工智能，所有回答请使用中文，精炼不重复。"},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.7,
                max_tokens=2048
            )

            content = response.choices[0].message.content
            section_content += f"{content}\n\n"

            usage = response.usage
            total_input_tokens += usage.prompt_tokens
            total_output_tokens += usage.completion_tokens


            # 生成反馈问题
            question_prompt = f"基于以下报告内容，提出2个问题，以帮助进一步深化理解或明确下一个分析方向：\n{section_content}"

            feedback_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system",
                     "content": "你是一个能够从报告内容中提问的智能助手，提出的问题应具有挑战性，能帮助进一步拓展分析。"},
                    {"role": "user", "content": question_prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )

            feedback_content = feedback_response.choices[0].message.content
            print("提问内容：", feedback_content)



            # 记录反馈问题的token消耗
            feedback_usage = feedback_response.usage
            total_input_tokens += feedback_usage.prompt_tokens
            total_output_tokens += feedback_usage.completion_tokens

            question_reference, embedding_tokens = self.retrieve_relevant_blocks(feedback_content, index, blocks, top_k=2)
            print("检索出的与问题最相关的 top 2 文本：", question_reference)
            total_input_embedding_tokens += embedding_tokens

            # 根据反馈问题生成新的报告内容
            question_based_prompt = f"请严格控制字数，你的回答不能超过100个字！根据以下问题，继续生成详细报告：\n{feedback_content}\n\n基于以下内容继续扩展报告：\n{question_reference}！"

            next_response = self.client.chat.completions.create(
                model=os.getenv('OPENAI_API_NAME', 'gpt-4o-mini'),
                messages=[
                    {"role": "system",
                     "content": "你是一个基于提供问题继续生成详细报告的人工智能，所有回答请使用中文，精炼不重复。"},
                    {"role": "user", "content": question_based_prompt}
                ],
                temperature=0.7,
                max_tokens=2048
            )

            next_content = next_response.choices[0].message.content
            section_content += f"\n\n- 相关讨论：{feedback_content}"
            section_content += f"\n\n- 相关解答：{next_content}"

            next_usage = next_response.usage
            total_input_tokens += next_usage.prompt_tokens
            total_output_tokens += next_usage.completion_tokens
            report.append(section_content)

        end_time = time.time()
        total_time = end_time - start_time

        # 调用 _log_costs 方法
        self._log_costs(
            total_input_tokens,
            total_output_tokens,
            total_input_embedding_tokens,
            total_output_embedding_tokens,
            total_time
        )

        return "\n\n".join(report)

    def _log_costs(self, input_tokens, output_tokens, input_embedding_tokens, output_embedding_tokens, total_time):
        # 计算总输入成本（包括嵌入输入令牌）
        total_input_cost = (input_tokens / 1_000_000 * self.cost_per_1m_input_tokens) + \
                           (input_embedding_tokens / 1_000_000 * self.cost_per_1m_input_embedding_tokens)

        # 计算总输出成本（包括嵌入输出令牌）
        total_output_cost = (output_tokens / 1_000_000 * self.cost_per_1m_output_tokens) + \
                            (output_embedding_tokens / 1_000_000 * self.cost_per_1m_output_embedding_tokens)

        # 总成本
        total_cost = total_input_cost + total_output_cost

        # 打印成本和时间信息
        print(f"生成报告总用时: {total_time:.2f} 秒")
        print(f"总输入 tokens (包括嵌入): {input_tokens + input_embedding_tokens}")
        print(f"总输出 tokens (包括嵌入): {output_tokens + output_embedding_tokens}")
        print(f"总费用: ${total_cost:.4f}")

    def generate_main(self, file_path, framework=None):
        if file_path.endswith('.pdf'):
            raw_content = self.read_pdf(file_path)
            content = [block['text'] for block in raw_content if block['text']]
        elif file_path.endswith('.docx'):
            content = self.read_word(file_path)
        else:
            raise ValueError("Unsupported file type. Please use a PDF or Word document.")

        if not framework:
            framework = {
                "引言": ["提供对主题的介绍，包括其重要性和背景。"],
                "方法论": ["描述用于分析的方法。"],
                "结果": ["总结分析的主要发现。"],
                "结论": ["总结关键点并为未来的工作提供建议。"]
            }

        blocks = self.split_content(content)
        embeddings, embedding_tokens = self.get_embeddings(blocks)
        index = self.build_faiss_index(embeddings)
        report = self.generate_report_with_feedback(framework, index, blocks)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        folder_path = './uploads/FM-Report/' + timestamp

        report_filename = f"framework_report_{timestamp}.md"
        os.makedirs(folder_path, exist_ok=True)
        written_file = os.path.join(folder_path, report_filename)

        with open(written_file, "w", encoding="utf-8") as file:
            file.write(report)

        print(f"报告生成完毕，已保存为 {report_filename}")

        return report
