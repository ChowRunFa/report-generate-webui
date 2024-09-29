from flask import Flask, request, jsonify
from flask_cors import CORS
from rouge import Rouge
from nltk.translate.bleu_score import corpus_bleu, sentence_bleu
from nltk.tokenize import word_tokenize
import sys,os
import nltk
sys.path.append("..")
from utils.general_utils import result
# 下载nltk数据
nltk.download('punkt')

app = Flask(__name__)
CORS(app)

rouge = Rouge()

# 创建一个蓝图对象
api = Flask(__name__)
from flask import Blueprint
api_text_evaluate = Blueprint('api_text_evaluate', __name__)


@api_text_evaluate.route('/text_evaluate', methods=['POST'])
def text_evaluate():
    data = request.get_json(silent=True)  # 使用 silent=True 避免抛出异常

    candidate = data.get('candidateText', '')
    reference = data.get('referenceText', '')

    # BLEU-4 Calculation
    candidate_tokens = candidate.split()
    reference_tokens = [reference.split()]
    bleu_score = sentence_bleu(reference_tokens, candidate_tokens, weights=(0.25, 0.25, 0.25, 0.25))

    # ROUGE Calculation
    rouge = Rouge()
    rouge_scores = rouge.get_scores(candidate, reference, avg=True)

    # Extract ROUGE-1, ROUGE-2, and ROUGE-L F1 scores
    rouge_1_f1 = rouge_scores['rouge-1']['f']
    rouge_2_f1 = rouge_scores['rouge-2']['f']
    rouge_l_f1 = rouge_scores['rouge-l']['f']

    return result(200, "分数计算完毕",{
        "BLEU-4": bleu_score,
        "ROUGE-1": rouge_1_f1,
        "ROUGE-2": rouge_2_f1,
        "ROUGE-L": rouge_l_f1
    })


