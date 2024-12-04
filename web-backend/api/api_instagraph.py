import argparse
import json
import logging
import os,sys
import re

from openai import OpenAI
from pydantic import BaseModel

sys.path.append("..")

import instructor
import openai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request,Blueprint
from graphviz import Digraph
from typing import Optional

from instagraph_drivers.driver import Driver
from instagraph_drivers.falkordb import FalkorDB
from instagraph_drivers.neo4j import Neo4j
from objs.InstaGraph import InstaGraph

# instructor.patch()

load_dotenv()

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
response_data = ""

# If a Graph database set, then driver is used to store information
# 使用 Optional 来注解可以为 None 的类型
driver: Optional[Driver] = None

# Function to scrape text from a website
api_instagraph = Blueprint('api_instagraph', __name__)

def scrape_text_from_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        return "Error: Could not retrieve content from URL."
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    text = " ".join([p.get_text() for p in paragraphs])
    logging.info("web scrape done")
    return text


# Function to check user plan


def check_if_free_plan():
    """
    receive USER_PLAN from .env.
    Added default None, as this project won't be in free plan in production mode.

    Returns:
        bool: _description_
    """
    return os.environ.get("USER_PLAN", None) == "free"


# Rate limiting


@api_instagraph.after_request
def add_header(response):
    """
    add response header if free plan.

    Args:
        response (_type_): _description_

    Returns:
        _type_: _description_
    """
    if check_if_free_plan():
        response.headers["Retry-After"] = 20
    return response


def correct_json(json_str):
    """
    Corrects the JSON response from OpenAI to be valid JSON by removing trailing commas
    """
    while ",\s*}" in json_str or ",\s*]" in json_str:  # noqa: W605
        json_str = re.sub(r",\s*}", "}", json_str)
        json_str = re.sub(r",\s*]", "]", json_str)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logging.error(
            "SanitizationError: %s for JSON: %s", str(e), json_str, exc_info=True
        )
        return None


@api_instagraph.route("/get_response_data", methods=["POST"])
def get_response_data():
    global response_data
    # response_data =  {'metadata': {'createdDate': '2022-10-10', 'lastUpdated': '2022-10-10', 'description': 'A knowledge graph describing the paper on improving argument retrieval in Retrieval-Augmented Generation (RAG) systems.'}, 'nodes': [{'id': '1', 'label': '论文简要', 'type': 'summary', 'color': '#FFC947', 'properties': {}}, {'id': '2', 'label': '无块上下文检索', 'type': 'method', 'color': '#FF8F40', 'properties': {}}, {'id': '3', 'label': 'Retrieval-Augmented Generation (RAG) 系统', 'type': 'system', 'color': '#FF5733', 'properties': {}}, {'id': '4', 'label': '论据检索', 'type': 'task', 'color': '#C70039', 'properties': {}}, {'id': '5', 'label': '优化检索过程', 'type': 'improvement', 'color': '#900C3F', 'properties': {}}, {'id': '6', 'label': '信息的相关性和准确性', 'type': 'improvement', 'color': '#581845', 'properties': {}}, {'id': '7', 'label': '改进', 'type': 'improvement', 'color': '#C266C2', 'properties': {}}], 'edges': [{'from_': '1', 'to': '2', 'relationship': '使用', 'direction': 'none', 'color': '#000000', 'properties': {}, 'from': '1'}, {'from_': '1', 'to': '3', 'relationship': '解决', 'direction': 'none', 'color': '#000000', 'properties': {}, 'from': '1'}, {'from_': '1', 'to': '4', 'relationship': '困难', 'direction': 'none', 'color': '#000000', 'properties': {}, 'from': '1'}, {'from_': '1', 'to': '5', 'relationship': '通过', 'direction': 'none', 'color': '#000000', 'properties': {}, 'from': '1'}, {'from_': '1', 'to': '6', 'relationship': '提高', 'direction': 'none', 'color': '#000000', 'properties': {}, 'from': '1'}, {'from_': '5', 'to': '3', 'relationship': '优化', 'direction': 'none', 'color': '#000000', 'properties': {}, 'from': '5'}, {'from_': '5', 'to': '4', 'relationship': '过程', 'direction': 'none', 'color': '#000000', 'properties': {}, 'from': '5'}, {'from_': '6', 'to': '3', 'relationship': '相关性', 'direction': 'none', 'color': '#000000', 'properties': {}, 'from': '6'}, {'from_': '6', 'to': '3', 'relationship': '准确性', 'direction': 'none', 'color': '#000000', 'properties': {}, 'from': '6'}, {'from_': '7', 'to': '4', 'relationship': '显著的改进', 'direction': 'none', 'color': '#000000', 'properties': {}, 'from': '7'}]}
    # return response_data
    user_input = request.json.get("user_input", "")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    if user_input.startswith("http"):
        user_input = scrape_text_from_url(user_input)

    if user_input.startswith("+"):
        prompt = "\n".join(
            [
                "请根据说明更新知识图谱:.",
                json.dumps(
                    dict(instruction=user_input[1:], knowledge_graph=response_data)
                ),
            ]
        )
    else:
        prompt = f"通过详细的知识图描述来帮助我理解以下内容: {user_input}"

    logging.info("starting openai call: %s", prompt)
    try:

        client = OpenAI(
            # This is the default and can be omitted
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )

        response = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            response_format=InstaGraph

        )

        # Its now a dict, no need to worry about json loading so many times
        response_data = response.choices[0].message.parsed.model_dump()
        # response_data = response.choices[0].message.content

        # try:
        #     response_data = json.loads(response_data)
        # except json.JSONDecodeError:
        #     print("给定的字符串不是有效的JSON格式。")

        # response_data = response.model_dump()

        # response_data = response.model_dump()
        # copy "from_" prop to "from" prop on all edges
        # Parse the response into the KnowledgeGraph model
        # response_data = KnowledgeGraph.parse_raw(response.choices[0].message['content'])
        # edges = response_data['edges']
        edges = response_data['edges']

        def _restore(e):
            e["from"] = e["from_"]
            return e

        response_data['edges'] = [_restore(e) for e in edges]

    # except openai.error.RateLimitError as e:
    except openai.RateLimitError as e:
        # request limit exceeded or something.
        logging.warning("%s", e)
        return jsonify({"error": "rate limitation"}), 429
    except Exception as e:
        # general exception handling
        logging.error("%s", e)
        return jsonify({"error": "unknown error"}), 400

    try:
        if driver:
            results = driver.get_response_data(response_data)
            logging.info("Results from Graph:", results)

    except Exception as e:
        logging.error("An error occurred during the Graph operation: %s", e)
        return (
            jsonify(
                {"error": "An error occurred during the Graph operation: {}".format(e)}
            ),
            500,
        )

    return response_data, 200


# Function to visualize the knowledge graph using Graphviz
@api_instagraph.route("/graphviz", methods=["POST"])
def visualize_knowledge_graph_with_graphviz():
    global response_data
    dot = Digraph(comment="Knowledge Graph")
    response_dict = response_data
    # Add nodes to the graph
    for node in response_dict.get("nodes", []):
        dot.node(node["id"], f"{node['label']} ({node['type']})")

    # Add edges to the graph
    for edge in response_dict.get("edges", []):
        dot.edge(edge["from"], edge["to"], label=edge["relationship"])

    # Render and visualize
    dot.render("knowledge_graph.gv", view=False)
    # Render to PNG format and save it
    dot.format = "png"
    dot.render("static/knowledge_graph", view=False)

    # Construct the URL pointing to the generated PNG
    png_url = f"{request.url_root}static/knowledge_graph.png"

    return jsonify({"png_url": png_url}), 200


@api_instagraph.route("/get_graph_data", methods=["POST"])
def get_graph_data():
    # return {'elements': {'nodes': [{'data': {'id': 'n1', 'label': 'Long Text Processing in LLMs', 'color': '#f5c0c0'}}, {'data': {'id': 'n2', 'label': 'Landmark Embedding', 'color': '#d0e1f9'}}, {'data': {'id': 'n3', 'label': 'Retrieval-Augmented Generation (RAG)', 'color': '#f9e79f'}}, {'data': {'id': 'n4', 'label': 'FaviComp', 'color': '#c0f2c5'}}, {'data': {'id': 'n5', 'label': 'AdaComp', 'color': '#ffe6e6'}}, {'data': {'id': 'n6', 'label': 'E2LLM', 'color': '#e0d1b1'}}, {'data': {'id': 'n7', 'label': 'Challenges', 'color': '#e6cfb3'}}, {'data': {'id': 'n8', 'label': 'Incomplete Retrieval', 'color': '#ffefc1'}}, {'data': {'id': 'n9', 'label': 'Semantic Representation', 'color': '#c1d9ff'}}, {'data': {'id': 'n10', 'label': 'Context Window Limitations', 'color': '#f9d6d1'}}, {'data': {'id': 'n11', 'label': 'Processing Overhead', 'color': '#c4f2e4'}}, {'data': {'id': 'n12', 'label': 'Balancing Performance', 'color': '#ffecc1'}}, {'data': {'id': 'n13', 'label': 'Improving Consistency', 'color': '#e1f7d5'}}, {'data': {'id': 'n14', 'label': 'External Database', 'color': '#d1ebeb'}}, {'data': {'id': 'n15', 'label': 'Open-Domain QA Performance', 'color': '#d0f0c0'}}, {'data': {'id': 'n16', 'label': 'Query Complexity', 'color': '#c9d9ff'}}, {'data': {'id': 'n17', 'label': 'Retrieval Quality', 'color': '#f9d0e1'}}], 'edges': [{'data': {'source': 'n1', 'target': 'n7', 'label': 'associated_with', 'color': '#d0d8e8'}}, {'data': {'source': 'n2', 'target': 'n1', 'label': 'enhances', 'color': '#adafda'}}, {'data': {'source': 'n2', 'target': 'n8', 'label': 'faces_challenge', 'color': '#7a84cd'}}, {'data': {'source': 'n3', 'target': 'n13', 'label': 'aims_to_improve', 'color': '#f0c27b'}}, {'data': {'source': 'n3', 'target': 'n14', 'label': 'utilizes', 'color': '#f2b34d'}}, {'data': {'source': 'n4', 'target': 'n3', 'label': 'enhances', 'color': '#84d4b2'}}, {'data': {'source': 'n4', 'target': 'n15', 'label': 'boosts', 'color': '#94dae8'}}, {'data': {'source': 'n5', 'target': 'n16', 'label': 'adapt_based_on', 'color': '#f7e9e4'}}, {'data': {'source': 'n5', 'target': 'n17', 'label': 'considers', 'color': '#d6bbeb'}}, {'data': {'source': 'n6', 'target': 'n1', 'label': 'proposed_solution_for', 'color': '#e0bc7c'}}, {'data': {'source': 'n6', 'target': 'n12', 'label': 'balances', 'color': '#b29eb1'}}, {'data': {'source': 'n6', 'target': 'n11', 'label': 'reduces', 'color': '#c0ccd9'}}, {'data': {'source': 'n6', 'target': 'n9', 'label': 'improves', 'color': '#d2b2ab'}}, {'data': {'source': 'n7', 'target': 'n8', 'label': 'includes', 'color': '#e5c1c2'}}, {'data': {'source': 'n7', 'target': 'n9', 'label': 'includes', 'color': '#d1e9f7'}}, {'data': {'source': 'n7', 'target': 'n10', 'label': 'includes', 'color': '#f8d1b4'}}, {'data': {'source': 'n7', 'target': 'n11', 'label': 'includes', 'color': '#aad8d3'}}, {'data': {'source': 'n7', 'target': 'n12', 'label': 'includes', 'color': '#f2dec4'}}]}}
    try:
        if driver:
            (nodes, edges) = driver.get_graph_data()
        else:
            global response_data
            response_dict = response_data
            # Assume response_data is global or passed appropriately
            nodes = [
                {
                    "data": {
                        "id": node["id"],
                        "label": node["label"],
                        "color": node.get("color", "defaultColor"),
                    }
                }
                for node in response_dict["nodes"]
            ]
            edges = [
                {
                    "data": {
                        "source": edge["from"],
                        "target": edge["to"],
                        "label": edge["relationship"],
                        "color": edge.get("color", "defaultColor"),
                    }
                }
                for edge in response_dict["edges"]
            ]
        print({"elements": {"nodes": nodes, "edges": edges}})
        return jsonify({"elements": {"nodes": nodes, "edges": edges}})
    except Exception:
        return jsonify({"elements": {"nodes": [], "edges": []}})


@api_instagraph.route("/get_graph_history", methods=["GET"])
def get_graph_history():
    try:
        page = request.args.get("page", default=1, type=int)
        per_page = 10
        skip = (page - 1) * per_page

        result = (
            driver.get_graph_history(skip, per_page)
            if driver
            else {
                "graph_history": [],
                "error": "Graph driver not initialized",
                "graph": False,
            }
        )
        return jsonify(result)
    except Exception as e:
        logging.error("%s", e)
        return jsonify({"error": str(e), "graph": driver is not None}), 500


# @api_instagraph.route("/")
# def index():
#     return render_template("index.html")



# @api_instagraph.route('/instagraph', methods=['POST'])
# def api_instagraph():
#     parser = argparse.ArgumentParser(description="InstaGraph")
#     parser.add_argument("--debug", action="store_true")
#     parser.add_argument("--port", type=int, dest="port_num", default=8080)
#     parser.add_argument("--graph", type=str, dest="graph_db", default="neo4j")
#
#     args = parser.parse_args()
#     port = args.port_num
#     graph = args.graph_db
#
#     if graph.lower() == "neo4j":
#         driver = Neo4j()
#     elif graph.lower() == "falkordb":
#         driver = FalkorDB()
#     else:
#         # Default try to connect to Neo4j for backward compatibility
#         try:
#             driver = Neo4j()
#         except Exception:
#             driver = None
#
#     if args.debug:
#         app.run(debug=True, host="0.0.0.0", port=port)
#     else:
#         app.run(host="0.0.0.0", port=port)
