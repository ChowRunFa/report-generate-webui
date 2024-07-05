import json
import os
import sys

from langchain_community.chat_models.openai import ChatOpenAI

sys.path.append("..")

from utils.split_utils import split_text_to_satisfy_token_limit
import markdown
from langchain.schema import SystemMessage, HumanMessage

#以下是每类图表的PROMPT
SELECT_PROMPT = """
“{subject}”
=============
以上是从文章中提取的摘要,将会使用这些摘要绘制图表。请你选择一个合适的图表类型:
1 流程图
2 序列图
3 类图
4 饼图
5 甘特图
6 状态图
7 实体关系图
8 象限提示图
不需要解释原因，仅需要输出单个不带任何标点符号的数字。
"""
#没有思维导图!!!测试发现模型始终会优先选择思维导图
#流程图
PROMPT_1 = """
请你给出围绕“{subject}”的逻辑关系图，使用mermaid语法，mermaid语法举例：
```mermaid
graph TD
    P(编程) --> L1(Python)
    P(编程) --> L2(C)
    P(编程) --> L3(C++)
    P(编程) --> L4(Javascipt)
    P(编程) --> L5(PHP)
```
"""
#序列图
PROMPT_2 = """
请你给出围绕“{subject}”的序列图，使用mermaid语法，mermaid语法举例：
```mermaid
sequenceDiagram
    participant A as 用户
    participant B as 系统
    A->>B: 登录请求
    B->>A: 登录成功
    A->>B: 获取数据
    B->>A: 返回数据
```
"""
#类图
PROMPT_3 = """
请你给出围绕“{subject}”的类图，使用mermaid语法，mermaid语法举例：
```mermaid
classDiagram
    Class01 <|-- AveryLongClass : Cool
    Class03 *-- Class04
    Class05 o-- Class06
    Class07 .. Class08
    Class09 --> C2 : Where am i?
    Class09 --* C3
    Class09 --|> Class07
    Class07 : equals()
    Class07 : Object[] elementData
    Class01 : size()
    Class01 : int chimp
    Class01 : int gorilla
    Class08 <--> C2: Cool label
```
"""
#饼图
PROMPT_4 = """
请你给出围绕“{subject}”的饼图，使用mermaid语法，mermaid语法举例：
```mermaid
pie title Pets adopted by volunteers
    "狗" : 386
    "猫" : 85
    "兔子" : 15
```
"""
#甘特图
PROMPT_5 = """
请你给出围绕“{subject}”的甘特图，使用mermaid语法，mermaid语法举例：
```mermaid
gantt
    title 项目开发流程
    dateFormat  YYYY-MM-DD
    section 设计
    需求分析 :done, des1, 2024-01-06,2024-01-08
    原型设计 :active, des2, 2024-01-09, 3d
    UI设计 : des3, after des2, 5d
    section 开发
    前端开发 :2024-01-20, 10d
    后端开发 :2024-01-20, 10d
```
"""
#状态图
PROMPT_6 = """
请你给出围绕“{subject}”的状态图，使用mermaid语法，mermaid语法举例：
```mermaid
stateDiagram-v2
   [*] --> Still
    Still --> [*]
    Still --> Moving
    Moving --> Still
    Moving --> Crash
    Crash --> [*]
```
"""
#实体关系图
PROMPT_7 = """
请你给出围绕“{subject}”的实体关系图，使用mermaid语法，mermaid语法举例：
```mermaid
graph LR
    A[Hard skill] --> B(Programming)
    A[Hard skill] --> C(Design)
    D[Soft skill] --> E(Coordination)
    D[Soft skill] --> F(Communication)
```
"""
#象限提示图
PROMPT_8 = """
请你给出围绕“{subject}”的象限图，使用mermaid语法，mermaid语法举例：
```mermaid
graph LR
    A[Hard skill] --> B(Programming)
    A[Hard skill] --> C(Design)
    D[Soft skill] --> E(Coordination)
    D[Soft skill] --> F(Communication)
```
"""
#思维导图
PROMPT_9 = """
{subject}
==========
请给出上方内容的思维导图，充分考虑其之间的逻辑，使用mermaid语法，mermaid语法举例：
```mermaid
mindmap
  root((mindmap))
    Origins
      Long history
      ::icon(fa fa-book)
      Popularisation
        British popular psychology author Tony Buzan
    Research
      On effectiveness<br/>and features
      On Automatic creation
        Uses
            Creative techniques
            Strategic planning
            Argument mapping
    Tools
      Pen and paper
      Mermaid
```
"""



def text2html(text):
    markdown_text = '\n'.join(text)
    html_output = markdown.markdown(markdown_text)
    return html_output

def is_valid_filepath(filepath):
    # 检查 filepath 参数的有效性，例如检查文件是否存在、路径是否合法等
    # 示例：检查文件是否存在
    return os.path.isfile(filepath)

def result(code=200, msg = 'success',d={}):
    data = dict()#object.__dict__
    data['code'] = code
    data['msg'] = msg
    data['data'] = d
    return json.dumps(data,ensure_ascii=False)

def get_mermaid(content,llm):
    # 设置OpenAI API密钥
    from dotenv import load_dotenv
    load_dotenv()
    # llm = ChatOpenAI()
    ############################## <第 0 步，切割输入> ##################################
    # 借用PDF切割中的函数对文本进行切割
    TOKEN_LIMIT_PER_FRAGMENT = 2500
    txt = str(content).encode('utf-8', 'ignore').decode()  # avoid reading non-utf8 chars
    txt = split_text_to_satisfy_token_limit(txt=txt, limit=TOKEN_LIMIT_PER_FRAGMENT)
    ############################## <第 1 步，迭代地历遍整个文章，提取精炼信息> ##################################
    results = []
    MAX_WORD_TOTAL = 4096
    n_txt = len(txt)
    last_iteration_result = "从以下文本中提取摘要。"
    if n_txt >= 20: print('文章极长，不能达到预期效果')
    for i in range(n_txt):
        NUM_OF_WORD = MAX_WORD_TOTAL // n_txt
        i_say = f"Read this section, recapitulate the content of this section with less than {NUM_OF_WORD} words in Chinese: {txt[i]}"
        sys_prompt = "Extracts the main content from the text section where it is located for graphing purposes, answer me with Chinese."
        # llm = ChatOpenAI(
        #     model_name="chatglm",
        #     openai_api_base="http://localhost:8000/v1",
        #     openai_api_key="EMPTY",
        #     streaming=False,
        # )
        # llm = ChatOpenAI()
        messages = [
            SystemMessage(content=sys_prompt),
            HumanMessage(content=i_say)
        ]
        # gpt_say = llm(messages)
        gpt_say = llm(messages).content
        results.append(gpt_say)
    ############################## <第 2 步，根据整理的摘要选择图表类型> ##################################
    results_txt = '\n'.join(results)  # 合并摘要
    # if gpt_say not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:  # 如插件参数不正确则使用对话模型判断
    #     i_say_show_user = f'接下来将判断适合的图表类型,如连续3次判断失败将会使用流程图进行绘制';
    gpt_say = "[Local Message] 收到。"  # 用户提示
    i_say = SELECT_PROMPT.format(subject=results_txt)
    i_say_show_user = f'请判断适合使用的流程图类型,其中数字对应关系为:1-流程图,2-序列图,3-类图,4-饼图,5-甘特图,6-状态图,7-实体关系图,8-象限提示图。由于不管提供文本是什么,模型大概率认为"思维导图"最合适,因此思维导图仅能通过参数调用。'
    # llm = ChatOpenAI(
    #     model_name="chatglm",
    #     openai_api_base="http://localhost:8000/v1",
    #     openai_api_key="EMPTY",
    #     streaming=False,
    # )

    for i in range(3):
        gpt_say = llm([HumanMessage(content=i_say)]).content
        if gpt_say in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:  # 判断返回是否正确
            break
    if gpt_say not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        gpt_say = '1'
    ############################## <第 3 步，根据选择的图表类型绘制图表> ##################################
    if gpt_say == '1':
        i_say = PROMPT_1.format(subject=results_txt)
    elif gpt_say == '2':
        i_say = PROMPT_2.format(subject=results_txt)
    elif gpt_say == '3':
        i_say = PROMPT_3.format(subject=results_txt)
    elif gpt_say == '4':
        i_say = PROMPT_4.format(subject=results_txt)
    elif gpt_say == '5':
        i_say = PROMPT_5.format(subject=results_txt)
    elif gpt_say == '6':
        i_say = PROMPT_6.format(subject=results_txt)
    elif gpt_say == '7':
        i_say = PROMPT_7.replace("{subject}", results_txt)  # 由于实体关系图用到了{}符号
    elif gpt_say == '8':
        i_say = PROMPT_8.format(subject=results_txt)
    elif gpt_say == '9':
        i_say = PROMPT_9.format(subject=results_txt)
    i_say_show_user = f'请根据判断结果绘制相应的图表。如需绘制思维导图请使用参数调用,同时过大的图表可能需要复制到在线编辑器中进行渲染。'
    gpt_say = llm([HumanMessage(content=i_say)]).content
    return(gpt_say)

def get_latest_folder():
    directory = "../uploads/paper/"  # 指定文件夹路径
    folders = os.listdir(directory)  # 列出文件夹下的所有文件和文件夹
    folders_with_timestamp = [(folder, os.path.getmtime(directory + folder)) for folder in folders]
    folders_with_timestamp.sort(key=lambda x: x[1], reverse=True)  # 根据时间戳进行降序排序

    if folders_with_timestamp:
        latest_folder = folders_with_timestamp[0][0]  # 获取最新的文件夹名
        folder_path = directory + latest_folder  # 构建最新文件夹的完整路径
        return folder_path
    else:
        return None


#
# txt = ['## Paper:1', '\n\n\n',
#              '1. 标题: 智源开源新一代多模态基础模型 Emu2\n2. Title: New Generation Multi-modal Base Model Emu2 Released by Zhivian Open Source\n3. Authors: Zhivian Research Institute\n4. 发布单位及发布时间: 智源研究院于2023年12月21日发布\n5. Summary:\n   - (1) 研究背景：本文介绍了智源研究院发布的新一代多模态基础模型 Emu2，旨在提升多模态上下文学习能力。\n   - (2) 过去方法及问题：本文提到 Flamingo-80B、IDEFICS-80B等主流多模态预训练大模型在少样本多模态理解任务上存在一些问题。因此，本文的方法是有很好的动机性。\n   - (3) 研究方法：Emu2采用了大规模自回归生成式多模态预训练，并在编码器语义空间重建图像的解码器上进行训练。\n   - (4) 研究成果：Emu2在多项少样本理解、视觉问答、主体驱动图像生成等任务中表现出最佳性能，超越了Flamingo-80B、IDEFICS-80B等主流多模态预训练大模型。因此，该模型的性能支持了他们的目标。',
#              '\n\n\n\n',
#              '8. Conclusion:\n\n- (1): 本文介绍了智源研究院发布的新一代多模态基础模型 Emu2，该模型的研发意义在于提升多模态上下文学习能力，解决了过去主流多模态预训练大模型在少样本多模态理解任务上存在的问题。\n\n- (2): 创新点：Emu2采用了大规模自回归生成式多模态预训练，并在编码器语义空间重建图像的解码器上进行训练，这一方法在多模态任务中取得了显著的性能提升。性能：Emu2在多项少样本理解、视觉问答、主体驱动图像生成等任务中展现出最佳性能，超越了过去的主流多模态预训练大模型，证明了其在多模态学习领域的优越性。工作量：本文提出的Emu2模型展示了智源研究院在多模态学习领域的技术实力，为研究者提供了一个高效且强大的基础模型，减少了他们在模型构建上的工作量。\n\n请确保使用中文回答（专有名词需要用英文标记），陈述要简洁、学术化，并且不要重复前面的<summary>内容，使用原始数字的价值，严格按照格式进行，将相应的内容输出为xxx，换行符按照要求填写，如果没有，则可以不写。',
#              '\n\n\n\n']
# test_text = [txt,txt]
# report_htmls = [[text2html(sublist)]  for sublist in test_text]
# print(report_htmls[0])