import os
from parser import args
from pathlib import Path

from llm import model

graph_doc_filename = "graph_documents.pkl"
if args.saveinbetweenoutputs:
    graph_doc_filename = "graph_documents_+_in_between.pkl"

graphdoc_pkl_path = f"/beegfs/prj/LINDA_LLM/outputs/graph_docs/{args.target}/{args.parser}/{model}/graph_documents.pkl"

if args.curated:
    graphdoc_pkl_path = Path(graphdoc_pkl_path).parent / "5curated" / graph_doc_filename

if args.level == "docs":
    graphdoc_pkl_path = Path(graphdoc_pkl_path).parent / "docs" / graph_doc_filename
else:
    graphdoc_pkl_path = Path(graphdoc_pkl_path).parent / "chunks" / graph_doc_filename

if args.style:
    graphdoc_pkl_path = (
        Path(graphdoc_pkl_path).parent / f"style{args.style}" / graph_doc_filename
    )

if args.simple:
    graphdoc_pkl_path = Path(graphdoc_pkl_path).parent / "simple" / graph_doc_filename
else:
    graphdoc_pkl_path = Path(graphdoc_pkl_path).parent / "complex" / graph_doc_filename

ner_json_path = None
if args.nerrel:
    graphdoc_pkl_path = (
        Path(graphdoc_pkl_path).parent / f"nerrel_{args.nerrel}" / graph_doc_filename
    )
    # if args.toolcall:
    #     graphdoc_pkl_path = (
    #         Path(graphdoc_pkl_path).parent / f"toolcall" / graph_doc_filename
    #     )
    ner_json_path = Path(graphdoc_pkl_path).parent / "ner.json"

if args.relgiventrueners:
    graphdoc_pkl_path = (
        Path(graphdoc_pkl_path).parent / "relgiventrueners" / graph_doc_filename
    )
if args.relgivenallners:
    graphdoc_pkl_path = (
        Path(graphdoc_pkl_path).parent / "relgivenallners" / graph_doc_filename
    )

os.makedirs(Path(graphdoc_pkl_path).parent, exist_ok=True)

ppi_graphdoc_pkl_path = Path(graphdoc_pkl_path).parent / "ppi_graph_documents.pkl"
tf_graphdoc_pkl_path = Path(graphdoc_pkl_path).parent / "tf_graph_documents.pkl"
os.makedirs(Path(ppi_graphdoc_pkl_path).parent, exist_ok=True)
os.makedirs(Path(tf_graphdoc_pkl_path).parent, exist_ok=True)

graph_documents = list()

if args.target != "both":
    graphdoc_pkl_paths = [graphdoc_pkl_path]
else:
    ppi_graphdoc_pkl_path = Path(graphdoc_pkl_path).parent / "ppi_graph_documents.pkl"
    tf_graphdoc_pkl_path = Path(graphdoc_pkl_path).parent / "tf_graph_documents.pkl"
    graphdoc_pkl_paths = [ppi_graphdoc_pkl_path, tf_graphdoc_pkl_path]

triple_path = Path(
    f"/beegfs/prj/LINDA_LLM/outputs/graph_triples/{args.target}/{args.parser}/{model}"
)

if args.curated:
    triple_path = Path(triple_path) / "5curated"

if args.level == "docs":
    triple_path = Path(triple_path) / "docs"
else:
    triple_path = Path(triple_path) / "chunks"
if args.style:
    triple_path = Path(triple_path) / f"style{args.style}"
if args.simple:
    triple_path = Path(triple_path) / "simple"
else:
    triple_path = Path(triple_path) / "complex"
if args.nerrel:
    triple_path = Path(triple_path) / f"nerrel_{args.nerrel}"
# if args.toolcall:
#     triple_path = Path(triple_path) / f"toolcall"
if args.relgiventrueners:
    triple_path = Path(triple_path) / f"relgiventrueners"
if args.relgivenallners:
    triple_path = Path(triple_path) / f"relgivenallners"

os.makedirs(Path(triple_path), exist_ok=True)
