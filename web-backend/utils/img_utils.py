import subprocess
import tempfile
def mermaid_file_to_image(mermaid_name, output_name):
    mmdc_path = r'D:\Pycharm_Projects\report-generate-webui\node_modules\.bin\mmdc.CMD'
    mermaid_path = r'D:\Pycharm_Projects\report-generate-webui\web-backend\txt2charts\\'
    output_path = r'D:\Pycharm_Projects\report-generate-webui\web-backend\extracted_images\\'
    mermaid_file = mermaid_path + mermaid_name
    output_file = output_path + output_name
    subprocess.run([mmdc_path, "-i", mermaid_file, "-o", output_file], check=True)


def mermaid_txt_to_image(mermaid_text,output_name):
    mmdc_path = r'D:\Pycharm_Projects\report-generate-webui\node_modules\.bin\mmdc.CMD'
    # output_path = r'D:\Pycharm_Projects\report-generate-webui\web-backend\extracted_images\\'
    output_path = r'D:\Pycharm_Projects\report-generate-webui\src\assets\mermaid_imgs\\'
    output_file = output_path + output_name
    # 将 Mermaid 文本保存到临时文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(mermaid_text)
        temp_file_path = temp_file.name

    print(temp_file_path)

    # 定义命令
    command = [mmdc_path, '-i', temp_file_path, '-o', output_file]
    # 执行命令，并将文本作为输入传递
    subprocess.run(command, check=True)

    # 删除临时文件
    temp_file.close()

# mermaid_text = """
# sequenceDiagram
# 智源研究院->>Emu2: 发布新一代多模态基础模型
# Emu2->>Emu2: 采用大规模自回归生成式多模态预训练
# Emu2->>Emu2: 在编码器语义空间重建图像的解码器上进行训练
# Emu2->>Emu2: 在多项少样本理解、视觉问答、主体驱动图像生成等任务中表现出最佳性能
# Emu2->>Emu2: 超越过去的主流多模态预训练大模型
# Emu2->>Emu2: 解决了过去主流多模态预训练大模型在少样本多模态理解任务上存在的问题
# Emu2->>多模态学习领域: 带来了显著的性能提升
# """

# mermaid_text = """erDiagram
#
# ARTICLE{
#     string title
#     string authors
#     string institution
# }
# ARTICLE ||--|{ KEYWORDS : include
# KEYWORDS ||--o{ LLMs : use
# KEYWORDS ||--o{ Knowledge Graph : evaluate
# KEYWORDS ||--o{ Graph Learning : apply
# KEYWORDS ||--o{ Retrieval-augmented Generation : utilize
# """
#
# mermaid_txt_to_image(mermaid_text,"diagram1.png")


# mermaid_file_to_image("Emu2.md", "diagram.png")