import argparse
import os
import sys

import numpy as np
from dotenv import load_dotenv
import matplotlib.pyplot as plt

load_dotenv()  # 加载.env文件


sys.path.append("..")
from utils.kg_utils import *
from utils.general_utils import *
from objs.KG import KG_Class

def api_kg():

    main_topic = "related work, automatic generation"


    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE")
    model = os.getenv("OPENAI_API_NAME")

    parser = argparse.ArgumentParser()
    parser.add_argument("--api_base", type=str, default=api_base, help="the api base")
    parser.add_argument("--api_key", type=str, default=api_key,help="the api key")
    parser.add_argument("--model", type=str, default=model, help="name of the  llm")
    args = parser.parse_args()

    # directory = r"D:\Pycharm_Projects\AutoKG\related_work"
    directory = get_latest_folder()
    texts, sources = load_and_process_files(directory,
                                            chunk_size=200,
                                            separator=None)
    print('len(texts):',len(texts))

    KG_class = KG_Class(texts=texts,
                          source=sources,
                        main_topic=main_topic,
                          embedding=True,
                               args=args)

    print('KG_class.vectors:',KG_class.vectors)

    # step one: remove duplicates
    to_keep, to_delete, remains = KG_class.remove_same_text(use_nn=True, n_neighbors=25, thresh=1e-6, update=True)
    print('len(to_keep):',len(to_keep))

    # step two: extract keywords with two methods
    core_list_1, all_tokens = KG_class.cluster(15,
                                               clustering_method='NgJordanWeiss',
                                               max_texts=15,
                                               select_mtd='similarity',
                                               prompt_language='English',
                                               num_topics=10,
                                               max_length=3,
                                               post_process=True,
                                               add_keywords=False,
                                               verbose=False)
    print("Number of keywords selected:", len(core_list_1))
    print("Token used:", all_tokens)

    core_list_2, all_tokens = KG_class.cluster(15,
                                               clustering_method='k_means',
                                               max_texts=15,
                                               select_mtd='similarity',
                                               prompt_language='English',
                                               num_topics=10,
                                               max_length=3,
                                               post_process=True,
                                               add_keywords=True)
    print("Number of keywords selected:", len(core_list_2))
    print("Token used:", all_tokens)

    print("Number of keywords:", len(KG_class.keywords))

    _ = KG_class.sub_entry_filter()
    print("Number of keywords:", len(KG_class.keywords))

    _, all_tokens = KG_class.final_keywords_filter()
    print("Token used:", all_tokens)
    print("Number of keywords:", len(KG_class.keywords))

    KG_class.make_graph(30)
    pred_mat, U_mat, A = KG_class.coretexts_seg_individual(k=30, trust_num=5, negative_multiplier=7, seg_mtd='laplace',
                                                           return_mat=True, connect_threshold=0.2)

    KG_class.get_dist_mat()
    print(KG_class.check_completion())

    deg_mat = np.sum(np.array(A.todense()) > 0, axis=0)
    plt.hist(deg_mat)
    plt.show()

    KG_class.save_data(os.path.join('KG_data', 'realted_work_ref_KG.npy'), include_texts=True)

