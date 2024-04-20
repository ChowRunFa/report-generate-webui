import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import openai
import yaml
sys.path.append("..")

from utils import *
from objs.KG import KG_Class

with open("config.yaml", 'r') as stream:
    try:
        params = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


COMPLETIONS_MODEL = params["OPENAI_API_MODEL"]
EMBEDDING_MODEL = params["EMBEDDING_MODEL"]
my_api_key = params["OPENAI_API_KEY"]
my_api_base = params["OPENAI_API_BASE"]
openai.api_key = my_api_key
openai.api_base = my_api_base
os.environ['OPENAI_API_KEY'] = my_api_key
os.environ['OPENAI_API_BASE'] = my_api_base
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_API_BASE = os.environ["OPENAI_API_BASE"]

print(OPENAI_API_BASE)