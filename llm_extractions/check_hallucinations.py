import json
import os
import pickle
from pathlib import Path

# from langchain_community.graphs import Neo4jGraph

samples = True

# task = "ppi"
task = "tf"
old = True

simple = False
# simple = True

# parser = "marker"
parser = "llama_parse"

# model = "llama3.1:70b"
model = "llama3.1:8b"

if old:
    _task = "tf"
    filename = "graph_documents_old.pkl"
else:
    filename = "graph_documents.pkl"
    _task = task

graphdoc_pkl_path = f"/beegfs/prj/LINDA_LLM/outputs/graph_docs/{_task}/{parser}/{model}/graph_documents.pkl"

if samples:
    graphdoc_pkl_path = Path(graphdoc_pkl_path).parent / "100samples" / filename

if simple:
    graphdoc_pkl_path = Path(graphdoc_pkl_path).parent / "simple" / filename

graph_documents = list()
print(f"loading from {graphdoc_pkl_path}")
with open(graphdoc_pkl_path, "rb") as f:
    while 1:
        try:
            graph_documents.append(pickle.load(f))
        except EOFError:
            break

match, rels = 0, 0
for doc in graph_documents:
    for rel in doc.relationships:
        rels += 1
        src, tgt = rel.source.id, rel.target.id
        if all([src in doc.source.page_content, tgt in doc.source.page_content]):
            match += 1

score = match / rels

print(score)
