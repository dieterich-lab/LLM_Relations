import json
import os
import pickle
from parser import args
from pathlib import Path

from const import PAPER_PATH, PROMPT_LOOKUP
from langchain_core.documents.base import Document
from langchain_text_splitters import MarkdownTextSplitter

ending_dict = {"marker": "md", "llama_parse": "txt"}

text_splitter = MarkdownTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)
paper_dict = dict()

all_ner_paths = None
true_ner_paths = None

if args.target == "biored":
    _paper_paths = Path(
        "/beegfs/prj/LINDA_LLM/CardioPriorKnowledge/test_ppi_annotations/biored_26_11_2024/src/corpus"
    )
    paper_paths = list(_paper_paths.glob(f"*"))
elif "regulatome" in args.target:
    _paper_paths = Path(
        "/beegfs/prj/LINDA_LLM/CardioPriorKnowledge/test_ppi_annotations/regulatome_extraction_13_12_2024/src/corpus"
    )
    paper_paths = list(_paper_paths.glob(f"*"))
    if "ppi" in args.target:
        _all_ner_paths = Path(
            "/beegfs/prj/LINDA_LLM/CardioPriorKnowledge/test_ppi_annotations/regulatome_extraction_13_12_2024/src/entities"
        )
        all_ner_paths = list(_all_ner_paths.glob(f"*"))
        _true_ner_paths = Path(
            "/beegfs/prj/LINDA_LLM/CardioPriorKnowledge/test_ppi_annotations/regulatome_extraction_13_12_2024/src/entities_relations_ppi"
        )
        true_ner_paths = list(_true_ner_paths.glob(f"*"))
    elif "tf" in args.target:
        _all_ner_paths = Path(
            "/beegfs/prj/LINDA_LLM/CardioPriorKnowledge/test_ppi_annotations/regulatome_extraction_13_12_2024/src/entities"
        )
        all_ner_paths = list(_all_ner_paths.glob(f"*"))
        _true_ner_paths = Path(
            "/beegfs/prj/LINDA_LLM/CardioPriorKnowledge/test_ppi_annotations/regulatome_extraction_13_12_2024/src/entities_relations_tf"
        )
        true_ner_paths = list(_true_ner_paths.glob(f"*"))
else:
    _paper_paths = Path(
        f"/beegfs/prj/LINDA_LLM/outputs/parsed_papers/{PAPER_PATH}/{args.parser}"
    )
    if args.curated and "eval" not in args.target:
        _paper_paths = _paper_paths / "5curated"
    paper_paths = list(_paper_paths.glob(f"*.{ending_dict[args.parser]}"))


paper_pkl_path = Path(
    f"/beegfs/prj/LINDA_LLM/outputs/paper_chunks/{PAPER_PATH}/{args.parser}/paper_chunks.pkl"
)
if args.curated and "eval" not in args.target:
    paper_pkl_path = paper_pkl_path.parent / "5curated" / "paper_chunks.pkl"

paper_dict_path = Path(
    f"/beegfs/prj/LINDA_LLM/outputs/paper_dicts/{PAPER_PATH}/{args.parser}/paper_dict.pkl"
)
if args.curated and "eval" not in args.target:
    paper_dict_path = paper_dict_path.parent / "5curated" / "paper_chunks.pkl"

os.makedirs(paper_pkl_path.parent, exist_ok=True)

whole_paper_pkl_path = paper_pkl_path.parent / "whole_papers.pkl"
os.makedirs(whole_paper_pkl_path.parent, exist_ok=True)

f = open(paper_pkl_path, "wb")
wf = open(whole_paper_pkl_path, "wb")
for i, x in enumerate(paper_paths):
    if args.printpaperpaths:
        print(i, x)
    paper_dict[i] = str(x)
    text = open(x, "r").read().strip()
    if text:
        texts = text_splitter.create_documents([text])
        whole_text = Document(page_content=text, metadata={"file_path": x})
        for t in texts:
            pickle.dump((t, i), f)
        pickle.dump((whole_text, i), wf)
f.close()
wf.close()

os.makedirs(Path(paper_dict_path).parent, exist_ok=True)
with open(paper_dict_path, "w") as f:
    json.dump(paper_dict, f, indent=4)

with open(paper_dict_path, "r") as f:
    paper_dict = json.load(f)
    paper_dict = {int(k): v for k, v in paper_dict.items()}

documents = list()
with open(paper_pkl_path, "rb") as f:
    while 1:
        try:
            documents.append(pickle.load(f))
        except EOFError:
            break

whole_documents = list()
with open(whole_paper_pkl_path, "rb") as f:
    while 1:
        try:
            whole_documents.append(pickle.load(f))
        except EOFError:
            break

ner_list = None
if args.toolcall:
    if PROMPT_LOOKUP == "ppi":
        ner_path = "/beegfs/prj/LINDA_LLM/CardioPriorKnowledge/test_ppi_annotations/unique_gene_names.txt"
    elif PROMPT_LOOKUP == "tf":
        ner_path = "/beegfs/prj/LINDA_LLM/CardioPriorKnowledge/test_tf_annotations/unique_tf_names.txt"
    with open(ner_path, "r") as f:
        ner_list = [x.strip() for x in f.readlines()]
    ner_list = [x.replace(" ", "").lower() for x in ner_list]
