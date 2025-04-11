import glob
import os
import subprocess
from parser import args
from pathlib import Path

from marker.convert import convert_single_pdf
from marker.models import load_all_models

os.environ["PAGINATE_OUTPUT"] = "1"
os.environ["EXTRACT_IMAGES "] = "0"

model_lst = load_all_models()

path_dict = {
    "ppi": [
        "/beegfs/prj/LINDA_LLM/PubMed_Resources/Papers_Human_Cardiac_Alternative_Splicing/pdf_separate",
        "/beegfs/prj/LINDA_LLM/PubMed_Resources/Papers_Human_Cardiac_Signaling/pdf_separate",
    ],
    "tf": ["/beegfs/prj/LINDA_LLM/PubMed_Resources/Papers_Human_TF_Genes/pdf_separate"],
    "ppi_eval": [
        "/beegfs/prj/LINDA_LLM/PubMed_Resources/Papers_PPI_Evaluation/separate_pdf"
    ],
    "tf_eval": [
        "/beegfs/prj/LINDA_LLM/PubMed_Resources/Papers_TF_Evaluation/pdf_separate"
    ],
    "lr_eval": [
        "/beegfs/prj/LINDA_LLM/PubMed_Resources/Papers_LR_Evaluation/separate_pdf"
    ],
}

paths = path_dict[args.target]
_raw_docs = [glob.glob(path + "/*.pdf") for path in paths]
raw_docs = [y for x in _raw_docs for y in x]
print(len(raw_docs))

parsed_papers_path = (
    f"/beegfs/prj/LINDA_LLM/outputs/parsed_papers/{args.target}/marker/"
)

os.makedirs(parsed_papers_path, exist_ok=True)


for i, doc in enumerate(raw_docs):
    print(i, doc)
    full_text, _, _ = convert_single_pdf(doc, model_lst)
    with open(Path(parsed_papers_path) / (str(Path(doc).stem) + ".md"), "w") as f:
        f.write(full_text)

print("Finished")

# paths = ["/home/pwiesenbach/LINDA_LLM/test"]
# for path in paths:
#     print(path)
#     result = subprocess.call(
#         ["marker", path, parsed_papers_path, "--workers", "4", "--min_length", "1000"],
#     )

# logger.info(result)
