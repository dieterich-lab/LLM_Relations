import os
from parser import args
from pathlib import Path

from clients import hf_model_id

experiment_path = Path(
    f"/beegfs/prj/LINDA_LLM/outputs/triples/{args.data}/{args.target}/{args.model}/{args.extractionmode}/{args.chattype}"
)
if args.examples:
    experiment_path /= f"{args.examples}_ex"
if args.recall:
    experiment_path /= "recall"
if args.dynex:
    experiment_path /= "dynex"

all_ners_given = "all_ners_given" if args.all_ners_given else ""

if args.all_ners_given:
    experiment_path /= "all_ners_given"
os.makedirs(experiment_path, exist_ok=True)

triple_pkl_path = experiment_path / "triples.pkl"
triple_json_path = experiment_path / "triples.json"

mode = "direct" if not args.all_ners_given else "all_ners_givenFalsFalsee"
alignment_json_path = Path(
    f"/prj/LINDA_LLM/outputs/evaluations/FPs/{args.data}_{args.model}_{mode}_{args.chattype}.json"
)
os.makedirs(alignment_json_path.parent, exist_ok=True)

finetune_data_path = Path("data/transformers_datasets")
regulatome_eval_path = "/beegfs/prj/LINDA_LLM/CardioPriorKnowledge/test_ppi_annotations/annotated_ppi_relations.txt"
sft_model_path = Path("/prj/LINDA_LLM/outputs") / "finetunedmodels" / hf_model_id
uniprot_path = "/prj/LINDA_LLM/resources/uniprot_description_and_interactors.txt"
