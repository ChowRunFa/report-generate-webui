import argparse
import os
import sys
import time

import numpy as np
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, Blueprint
load_dotenv()  # 加载.env文件
from tqdm import tqdm

sys.path.append("..")
from utils.kg_utils import *
from utils.general_utils import *
from objs.KG import KG_Class
from utils.general_utils import result
from utils.markdown_utils import markdown_convertion
# Create a Blueprint for the API
api_autokg = Blueprint('api_autokg', __name__)

@api_autokg.route('/autokg', methods=['POST'])
def api_kg():
    # time.sleep(2)
    # return result(200, "图谱报告生成完毕", {
    #     'keywords': ['financial tasks', ' metaphor', ' language models', ' causal reasoning',
    #                  ' community detection', ' legal domain', ' extraction', ' fine-tuning', ' graph indexing',
    #                  ' evaluation benchmarks', ' logistic reasoning'],
    #     'kg_report': markdown_convertion(
    #         "**Survey on Enhancing Information Extraction with METORIE**\n\nIn recent years, the advancement of large language models (LLMs) like GPT-3.5, GPT-4, LLaMA3, and GLM4 has significantly improved natural language processing tasks. However, these models still face challenges in vertical domain information extraction (IE) tasks. To address this issue, researchers have been exploring fine-tuning strategies to enhance the performance of LLMs in specific domains.\n\nOne such innovative approach is the METORIE dataset, which focuses on improving information extraction through the use of logical traps and metaphors. Unlike traditional IE datasets, METORIE incorporates elements like logical traps to break conventional thinking patterns and metaphors to enhance the model's understanding of complex contexts and indirect expressions. By training LLMs on METORIE, researchers have observed significant improvements in reasoning abilities and IE efficiency.\n\nThe METORIE dataset consists of approximately 4,000 bilingual instructions in English and Chinese, designed to challenge LLMs with brain teasers that require logical reasoning and metaphor comprehension. Through multidimensional analysis of each question, METORIE helps LLMs progress in their reasoning abilities by deconstructing semantics in complex contexts. This approach has proven to be effective in enhancing the accuracy and generalization of LLMs in IE tasks.\n\nExperimental results have shown that fine-tuning LLMs with METORIE leads to substantial improvements in IE tasks, particularly in event extraction (EE) tasks. By comparing the performance of LLMs fine-tuned with METORIE against vertical domain LLMs, researchers have verified the dataset's effectiveness in vertical IE tasks without specific domain data.\n\nMoreover, the METORIE dataset has demonstrated exceptional performance in legal and medical verticals, highlighting the importance of enhanced metaphor understanding and logical deduction in improving LLMs' adaptability and efficiency across different domains. The balanced use of metaphor complexity has been identified as a key factor in optimizing model reasoning and enhancing performance, especially for smaller language models (SLMs).\n\nIn conclusion, the METORIE dataset represents a significant advancement in enhancing information extraction capabilities in LLMs. By leveraging logical traps and metaphors, researchers have been able to improve reasoning abilities, accuracy, and generalization in IE tasks across various domains. The success of METORIE underscores the importance of innovative approaches in fine-tuning LLMs for specific tasks and domains.\n\n**METORIE提高信息提取的调查**\n\n近年来，大型语言模型（LLMs）如GPT-3.5、GPT-4、LLaMA3和GLM4在自然语言处理任务中取得了显著进展。然而，这些模型在垂直领域信息提取（IE）任务中仍然面临挑战。为了解决这一问题，研究人员一直在探索精细调整策略，以提高LLMs在特定领域的性能。\n\nMETORIE数据集是一种创新方法，旨在通过使用逻辑陷阱和隐喻来提高信息提取。与传统的IE数据集不同，METORIE包含了逻辑陷阱等元素，以打破传统思维模式，并通过隐喻来增强模型对复杂语境和间接表达的理解。通过在METORIE上对LLMs进行训练，研究人员观察到了推理能力和IE效率的显著提高。\n\nMETORIE数据集包含大约4000条英语和中文的双语指令，旨在挑战LLMs，要求其进行逻辑推理和隐喻理解。通过对每个问题进行多维分析，METORIE帮助LLMs在复杂语境中逐步解构语义，从而提高了在IE任务中的准确性和泛化能力。\n\n实验结果显示，通过使用METORIE对LLMs进行精细调整，可以显著改善IE任务的表现，特别是在事件提取（EE）任务中。通过比较使用METORIE进行精细调整的LLMs与垂直领域LLMs的性能，研究人员验证了该数据集在没有特定领域数据的情况下在垂直IE任务中的有效性。\n\n此外，METORIE数据"),
    #     'kg_fig_path': 'related_work_ref_KG.png'})
    DEBUG = False
    if DEBUG:
        try:
            # 从表单中获取数据
            main_topic = request.form.get('main_topic', "knowledge graph, automatic generation")
            kg_name = request.form.get('kg_name', "related_work_ref_KG")
            usr_query = request.form.get('usr_query',
                                         "Please write a survey about {}in both English and 中文. more than 500 words".format(main_topic))

            # 从环境变量中获取API配置
            api_key = os.getenv("OPENAI_API_KEY")
            api_base = os.getenv("OPENAI_API_BASE")
            model = os.getenv("OPENAI_API_NAME")

            # 创建一个字典来存储所有参数
            args = {
                "api_base": api_base,
                "api_key": api_key,
                "model": model,
                "main_topic": main_topic,
                "kg_name": kg_name,
                "usr_query": usr_query
            }

            # Load the latest folder and process files
            directory = get_latest_folder()
            print("using directory is :",directory)
            texts, sources = load_and_process_files(directory, chunk_size=200, separator=None)

            # Initialize KG_Class
            KG_class = KG_Class(texts=texts, source=sources, main_topic=args['main_topic'], embedding=True, args=args)

            # Create a list of steps to monitor progress
            steps = [
                ("Removing duplicates", lambda: KG_class.remove_same_text(use_nn=True, n_neighbors=25, thresh=1e-6, update=True)),
                ("First keyword extraction", lambda: KG_class.cluster(15, clustering_method='NgJordanWeiss', max_texts=15, select_mtd='similarity', prompt_language='English', num_topics=10, max_length=3, post_process=True, add_keywords=False, verbose=False)),
                ("Second keyword extraction", lambda: KG_class.cluster(15, clustering_method='k_means', max_texts=15, select_mtd='similarity', prompt_language='English', num_topics=10, max_length=3, post_process=True, add_keywords=True)),
                ("Sub-entry filtering", lambda: KG_class.sub_entry_filter()),
                ("Final keyword filtering", lambda: KG_class.final_keywords_filter()),
                ("Building knowledge graph", lambda: KG_class.make_graph(30)),
                ("Segmenting coretexts", lambda: KG_class.coretexts_seg_individual(k=30, trust_num=5, negative_multiplier=7, seg_mtd='laplace', return_mat=True, connect_threshold=0.2)),
                ("Getting distance matrix", lambda: KG_class.get_dist_mat()),
                ("Saving data", lambda: KG_class.save_data(os.path.join('KG_data', args['kg_name'] + '.npy'), include_texts=True))
            ]

            # Initialize the progress bar
            with tqdm(total=len(steps), desc="Knowledge Graph Generation Progress", ncols=100) as pbar:
                for step_name, step_action in steps:
                    pbar.set_description(f"Processing: {step_name}")
                    step_action()  # Execute the step action
                    pbar.update(1)  # Update the progress bar

            # Completion check
            completion_status = KG_class.check_completion()

            # Generate final knowledge graph report
            Chat_KG_class = KG_Class(texts=None, source=None, main_topic=None, embedding=False, args=args)
            Chat_KG_class.load_data(os.path.join('KG_data', args['kg_name'] + '.npy'), include_texts=True)

            record = Chat_KG_class.KG_prompt(args['usr_query'], search_nums=(15, 7, 3, 4, 2), search_mtd='pair_dist', use_u=False)
            response, keywords_info, ref_info, all_tokens = Chat_KG_class.completion_from_record(record, output_tokens=1024, prompt_language='English', show_prompt=False, prompt_keywords=False, include_source=False)

            # Generate knowledge graph image
            Chat_KG_class.draw_graph_from_record(
                record,
                node_colors=([0, 1, 1], [0, 1, 0.5], [1, 0.7, 0.75]),
                node_shape='o',
                edge_color='black',
                edge_widths=(2, 0.5),
                node_sizes=(500, 150, 50),
                font_color='black',
                font_size=6,
                show_text=False,
                save_fig=True,
                save_path='../src/assets/kg_imgs/{}.png'.format(args['kg_name'])
            )
            print({
                'keywords': KG_class.keywords,
                'kg_report': response,
                'kg_fig_path': '{}.png'.format(args['kg_name'])
            })
            return result(200, "图谱报告生成完毕", {
                'keywords': KG_class.keywords,
                'kg_report': markdown_convertion(response),
                'kg_fig_path': '{}.png'.format(args['kg_name'])
            })

        except Exception as e:
            return jsonify(result(500, "An error occurred during knowledge graph generation.", str(e)))
    else:
        try:
            # 从表单中获取数据
            main_topic = request.form.get('main_topic', "knowledge graph, automatic generation")
            kg_name = request.form.get('kg_name', "related_work_ref_KG")
            usr_query = request.form.get('usr_query',
                                         "Please write a survey based on what you  in both English and 中文. more than 500 words")

            # 从环境变量中获取API配置
            api_key = os.getenv("OPENAI_API_KEY")
            api_base = os.getenv("OPENAI_API_BASE")
            model = os.getenv("OPENAI_API_NAME")

            # 创建一个字典来存储所有参数
            args = {
                "api_base": api_base,
                "api_key": api_key,
                "model": model,
                "main_topic": main_topic,
                "kg_name": kg_name,
                "usr_query": usr_query
            }

            # Load the latest folder and process files
            directory = get_latest_folder()
            print("Using directory:", directory)
            texts, sources = load_and_process_files(directory, chunk_size=200, separator=None)

            # Initialize KG_Class
            KG_class = KG_Class(texts=texts, source=sources, main_topic=args['main_topic'], embedding=True,
                                args=args)



            # Create a list of steps to monitor progress
            steps = [
                ("Removing duplicates",
                 lambda: KG_class.remove_same_text(use_nn=True, n_neighbors=25, thresh=1e-6, update=True)),
                ("First keyword extraction",
                 lambda: KG_class.cluster(15, clustering_method='NgJordanWeiss', max_texts=15,
                                          select_mtd='similarity', prompt_language='English', num_topics=10,
                                          max_length=3, post_process=True, add_keywords=False, verbose=False)),
                ("Second keyword extraction",
                 lambda: KG_class.cluster(15, clustering_method='k_means', max_texts=15, select_mtd='similarity',
                                          prompt_language='English', num_topics=10, max_length=3, post_process=True,
                                          add_keywords=True)),
                ("Sub-entry filtering", lambda: KG_class.sub_entry_filter()),
                ("Final keyword filtering", lambda: KG_class.final_keywords_filter()),
                ("Building knowledge graph", lambda: KG_class.make_graph(30)),
                ("Segmenting coretexts",
                 lambda: KG_class.coretexts_seg_individual(k=30, trust_num=5, negative_multiplier=7,
                                                           seg_mtd='laplace', return_mat=True,
                                                           connect_threshold=0.2)),
                ("Getting distance matrix", lambda: KG_class.get_dist_mat()),
                ("Saving data",
                 lambda: KG_class.save_data(os.path.join('KG_data', args['kg_name'] + '.npy'), include_texts=True))
            ]

            # Progress tracking without tqdm
            for step_name, step_action in steps:
                print(f"Processing: {step_name}")
                step_action()  # Execute the step action
                print(f"Completed: {step_name}")


            # Completion check
            completion_status = KG_class.check_completion()

            # Generate final knowledge graph report
            Chat_KG_class = KG_Class(texts=None, source=None, main_topic=None, embedding=False, args=args)
            Chat_KG_class.load_data(os.path.join('KG_data', args['kg_name'] + '.npy'), include_texts=True)



            record = Chat_KG_class.KG_prompt(args['usr_query'], search_nums=(15, 7, 3, 4, 2),
                                             search_mtd='pair_dist', use_u=False)
            response, keywords_info, ref_info, all_tokens = Chat_KG_class.completion_from_record(record,
                                                                                                 output_tokens=1024,
                                                                                                 prompt_language='English',
                                                                                                 show_prompt=False,
                                                                                                 prompt_keywords=False,
                                                                                                 include_source=False)

            print({
                'keywords': KG_class.keywords,
                'kg_report': markdown_convertion(response),
                'kg_fig_path': 'related_work_ref_KG.png'
            })

            return result(200, "图谱报告生成完毕", {
                'keywords': KG_class.keywords,
                'kg_report': markdown_convertion(response + '\n\n' + ref_info),
                'kg_fig_path': 'related_work_ref_KG.png'
            })

            # Generate knowledge graph image
            # Chat_KG_class.draw_graph_from_record(
            #     record,
            #     node_colors=([0, 1, 1], [0, 1, 0.5], [1, 0.7, 0.75]),
            #     node_shape='o',
            #     edge_color='black',
            #     edge_widths=(2, 0.5),
            #     node_sizes=(500, 150, 50),
            #     font_color='black',
            #     font_size=6,
            #     show_text=False,
            #     save_fig=True,
            #     # save_path='../src/assets/kg_imgs/{}.png'.format(args['kg_name'])
            #     save_path='../src/assets/kg_imgs/{}.png'.format(args['kg_name'])
            # )


        except Exception as e:
            return jsonify(result(500, "An error occurred during knowledge graph generation.", str(e)))

@api_autokg.route('/update_kg', methods=['GET'])
def update_kg():
    kg_name = request.form.get('kg_name', "related_work_ref_KG")
    main_topic = request.form.get('main_topic', "knowledge graph, automatic generation")

    # 从环境变量中获取API配置
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE")
    model = os.getenv("OPENAI_API_NAME")

    # 创建一个字典来存储所有参数
    args = {
        "api_base": api_base,
        "api_key": api_key,
        "main_topic": main_topic,
        "model": model,
        "kg_name": kg_name
    }
    Chat_KG_class = KG_Class(texts=None, source=None, main_topic=None, embedding=False, args=args)
    Chat_KG_class.load_data(os.path.join('KG_data', args['kg_name'] + '.npy'), include_texts=True)

    record = Chat_KG_class.KG_prompt(args['main_topic'], search_nums=(15, 7, 3, 4, 2),
                                     search_mtd='pair_dist', use_u=False)


    # Generate knowledge graph image
    Chat_KG_class.draw_graph_from_record(
        record,
        node_colors=([0, 1, 1], [0, 1, 0.5], [1, 0.7, 0.75]),
        node_shape='o',
        edge_color='black',
        edge_widths=(2, 0.5),
        node_sizes=(500, 150, 50),
        font_color='black',
        font_size=6,
        show_text=False,
        save_fig=True,
        # save_path='../src/assets/kg_imgs/{}.png'.format(args['kg_name'])
        save_path='../src/assets/kg_imgs/{}.png'.format(args['kg_name'])
    )

    return result(200, "图谱更新完成", {
        'kg_fig_path': 'related_work_ref_KG.png'
    })