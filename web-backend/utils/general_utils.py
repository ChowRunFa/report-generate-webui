import json
import os

import markdown


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

txt = ['## Paper:1', '\n\n\n',
             '1. 标题: 智源开源新一代多模态基础模型 Emu2\n2. Title: New Generation Multi-modal Base Model Emu2 Released by Zhivian Open Source\n3. Authors: Zhivian Research Institute\n4. 发布单位及发布时间: 智源研究院于2023年12月21日发布\n5. Summary:\n   - (1) 研究背景：本文介绍了智源研究院发布的新一代多模态基础模型 Emu2，旨在提升多模态上下文学习能力。\n   - (2) 过去方法及问题：本文提到 Flamingo-80B、IDEFICS-80B等主流多模态预训练大模型在少样本多模态理解任务上存在一些问题。因此，本文的方法是有很好的动机性。\n   - (3) 研究方法：Emu2采用了大规模自回归生成式多模态预训练，并在编码器语义空间重建图像的解码器上进行训练。\n   - (4) 研究成果：Emu2在多项少样本理解、视觉问答、主体驱动图像生成等任务中表现出最佳性能，超越了Flamingo-80B、IDEFICS-80B等主流多模态预训练大模型。因此，该模型的性能支持了他们的目标。',
             '\n\n\n\n',
             '8. Conclusion:\n\n- (1): 本文介绍了智源研究院发布的新一代多模态基础模型 Emu2，该模型的研发意义在于提升多模态上下文学习能力，解决了过去主流多模态预训练大模型在少样本多模态理解任务上存在的问题。\n\n- (2): 创新点：Emu2采用了大规模自回归生成式多模态预训练，并在编码器语义空间重建图像的解码器上进行训练，这一方法在多模态任务中取得了显著的性能提升。性能：Emu2在多项少样本理解、视觉问答、主体驱动图像生成等任务中展现出最佳性能，超越了过去的主流多模态预训练大模型，证明了其在多模态学习领域的优越性。工作量：本文提出的Emu2模型展示了智源研究院在多模态学习领域的技术实力，为研究者提供了一个高效且强大的基础模型，减少了他们在模型构建上的工作量。\n\n请确保使用中文回答（专有名词需要用英文标记），陈述要简洁、学术化，并且不要重复前面的<summary>内容，使用原始数字的价值，严格按照格式进行，将相应的内容输出为xxx，换行符按照要求填写，如果没有，则可以不写。',
             '\n\n\n\n']
test_text = [txt,txt]
report_htmls = [[text2html(sublist)]  for sublist in test_text]

print(report_htmls)