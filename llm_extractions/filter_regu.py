import csv
from pathlib import Path

import regex

from paths import regulatome_ppi_eval_path

regu_paths = Path(
    "/beegfs/prj/LINDA_LLM/CardioPriorKnowledge/test_ppi_annotations/regulatome_extraction_13_12_2024/src/corpus"
)

ending_dict = {"marker": "md", "llama_parse": "txt"}
regu_paths = list(regu_paths.glob("*.txt"))

with open(regulatome_ppi_eval_path, "r") as f:
    eval_regu_data = [
        (x.split("\t")[0], x.split("\t")[1], x.split("\t")[2].strip())
        for x in f.readlines()[1:]
    ]

eval_regu_data = [
    {"file_stem": x[0], "relations": x[1], "split": x[2]} for x in eval_regu_data
]
test_regu_data = [x["file_stem"] for x in eval_regu_data if x["split"] == "Test"]
regu_paths = [x for x in regu_paths if x.stem in test_regu_data]

test_regu_paper_paths = Path("/prj/LINDA_LLM/outputs/parsed_papers/regu_test")
test_regu_paper_without_abstracts_paths = Path(
    "/prj/LINDA_LLM/outputs/parsed_papers/regu_test/without_abstracts"
)
test_regu_paper_without_abstracts_paths.mkdir(parents=True, exist_ok=True)
regu_paper_paths = list(test_regu_paper_paths.glob("*.md"))

csv_path = "/prj/LINDA_LLM/resources/pmid_to_pmcid_mapped_test.csv"

align_dict = dict()
with open(csv_path, mode="r") as file:
    reader = csv.reader(file)
    next(reader, None)
    for id, pmc in reader:
        if pmc:
            align_dict[pmc] = id

regu_paper_paths = [x for x in regu_paper_paths if align_dict[x.stem] in test_regu_data]

print(len(regu_paper_paths))

for j, rp in enumerate(regu_paper_paths):
    if j in [55, 79, 87]:
        continue
    else:
        p = [x for x in regu_paths if align_dict[rp.stem] in str(x)][0]
        rpt = rp.read_text()
        pt = p.read_text()
        for i in range(100, 20, -10):
            res = regex.search("(?e)(" + regex.escape(pt[-i:].strip()) + "){e<=7}", rpt)
            if res:
                break
        if not res:
            raise
        offset = res.span()[-1] + 1
        rpt_without_abstract = rpt[offset:]
        with open(test_regu_paper_without_abstracts_paths / rp.name, "w") as f:
            f.write(rpt_without_abstract)
