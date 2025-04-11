import json
import os
import pickle
from parser import args
from pathlib import Path

from langchain_core.documents.base import Document
from paths import regulatome_eval_path

ending_dict = {"marker": "md", "llama_parse": "txt"}

paper_dict = dict()
all_ner_paths = None
true_ner_paths = None

if args.data == "regulatome":
    _paper_paths = Path("/prj/LINDA_LLM/scripts/data/regulatome/texts")
    _all_ner_paths = Path("/prj/LINDA_LLM/scripts/data/regulatome/all_entities")
    all_ner_paths = list(_all_ner_paths.glob(f"*"))
    _true_ner_paths = Path("/prj/LINDA_LLM/scripts/data/regulatome/true_entities")
    true_ner_paths = list(_true_ner_paths.glob(f"*"))
elif args.data == "5curated":
    _paper_paths = Path("data/5curated")

paper_paths = list(_paper_paths.glob(f"*.{ending_dict[args.parser]}"))

if args.data == "regulatome":
    with open(regulatome_eval_path, "r") as f:
        eval_data = [
            (x.split("\t")[0], x.split("\t")[1], x.split("\t")[2].strip())
            for x in f.readlines()[1:]
        ]

    eval_data = [
        {"file_stem": x[0], "relations": x[1], "split": x[2]} for x in eval_data
    ]
    test_data = [x["file_stem"] for x in eval_data if x["split"] == "Test"]
    test_paper_paths = [x for x in paper_paths if x.stem in test_data]
else:
    test_paper_paths = paper_paths


paper_pkl_path = Path(
    f"/beegfs/prj/LINDA_LLM/outputs/docs/{args.data}/{args.target}/{args.parser}/papers.pkl"
)
os.makedirs(paper_pkl_path.parent, exist_ok=True)

paper_dict_path = Path(
    f"/beegfs/prj/LINDA_LLM/outputs/paper_dicts/{args.data}/{args.target}/{args.parser}/paper_dict.pkl"
)
os.makedirs(Path(paper_dict_path).parent, exist_ok=True)

all_docs = list()
for i, x in enumerate(paper_paths):
    paper_dict[i] = str(x)
    text = open(x, "r").read().strip()
    if text:
        all_docs.append(Document(page_content=text, metadata={"file_path": x}))

wf = open(paper_pkl_path, "wb")
with open(paper_pkl_path, "wb") as doc_file:
    for i, x in enumerate(test_paper_paths):
        paper_dict[i] = str(x)
        text = open(x, "r").read().strip()
        if text:
            doc = Document(page_content=text, metadata={"file_path": x})
            pickle.dump((doc, i), doc_file)

with open(paper_dict_path, "w") as f:
    json.dump(paper_dict, f, indent=4)

test_chunks = list()

test_docs = list()
with open(paper_pkl_path, "rb") as f:
    while 1:
        try:
            test_docs.append(pickle.load(f))
        except EOFError:
            break

texts = test_docs

print(f"Len texts: {len(texts)}")
