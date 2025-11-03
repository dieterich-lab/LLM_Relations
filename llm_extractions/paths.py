import os
from parser import args
from pathlib import Path

from clients import hf_model_id


def _env_path(env_key: str, default: Path) -> Path:
    """Resolve a path from env or fall back to default."""
    value = os.environ.get(env_key)
    if value:
        return Path(value).expanduser().resolve()
    return default


# Resolve key project directories with sensible defaults that can be overridden.
PROJECT_ROOT = _env_path("LINDA_LLM_PROJECT_ROOT", Path(__file__).resolve().parents[1])
OUTPUT_ROOT = _env_path("LINDA_LLM_OUTPUT_ROOT", PROJECT_ROOT / "outputs")
TRIPLES_ROOT = _env_path("LINDA_LLM_TRIPLES_ROOT", OUTPUT_ROOT / "triples")
REGULATOME_ROOT = _env_path(
    "LINDA_LLM_REGULATOME_ROOT", PROJECT_ROOT.parent / "RegulaTome"
)
RESOURCES_ROOT = _env_path(
    "LINDA_LLM_RESOURCES_ROOT", PROJECT_ROOT.parent / "resources"
)


experiment_path = (
    TRIPLES_ROOT
    / args.data
    / args.target
    / args.model
    / args.extractionmode
    / args.chattype
    / args.doclevel
)
if args.doclevel == "chunks":
    experiment_path /= f"{args.chunksize}"
if args.examples:
    experiment_path /= f"{args.examples}_ex"
if args.recall:
    experiment_path /= "recall"
if args.tot:
    experiment_path /= f"tot_n{args.tot}_{args.tot_strategy}"
if args.ensemble:
    experiment_path /= f"ensemble_n{args.ensemble}_t{args.ensemble_temp}"
if args.dynex_k > 0:
    experiment_path /= f"dynex_k{args.dynex_k}"
if args.lookup:
    experiment_path /= f"lookup"

if args.all_nes_given:
    experiment_path /= "all_nes_given"
elif args.true_nes_given:
    experiment_path /= "true_nes_given"
elif args.spacy_nes_given:
    experiment_path /= "spacy_nes_given"
os.makedirs(experiment_path, exist_ok=True)

if not args.ext:
    triple_jsonl_path = experiment_path / "triples.jsonl"
    triple_json_path = experiment_path / "triples.json"
else:
    triple_jsonl_path = experiment_path / f"triples_{args.ext}.jsonl"
    triple_json_path = experiment_path / f"triples_{args.ext}.json"


# try:
#     fp_paths = {
#         "deepseek8b": {
#             "nerrel": "/beegfs/prj/LINDA_LLM/RegulaTome/test_ppi_annotations/FalsePositives_DeepSeek8b_Stepwise_NoEntities_Step1_AllRel.txt",
#             "all_ners_given": "/beegfs/prj/LINDA_LLM/RegulaTome/test_ppi_annotations/FalsePositives_DeepSeek8b_Stepwise_AllEntities_Step1_AllRel.txt",
#         }
#     }
# except:
#     pass

# lookup = "nerrel" if not args.all_ners_given else "all_ners_given"
# try:
#     fp_path = fp_paths[args.model][lookup]
# except:
#     pass

# mode = "direct" if not args.all_ners_given else "all_ners_given"
# alignment_json_path = Path(
#     f"/prj/LINDA_LLM/outputs/evaluations/FPs/{args.data}_{args.model}_{mode}_{args.chattype}_{args.doclevel}.json"
# )
# os.makedirs(alignment_json_path.parent, exist_ok=True)

# judge_path = Path("/prj/LINDA_LLM/outputs/evaluations/FPs_judged")
# os.makedirs(judge_path, exist_ok=True)
# judge_pkl_path = (
#     judge_path / f"{args.data}_{args.model}_{mode}_{args.chattype}_{args.doclevel}.pkl"
# )
# judge_json_path = (
#     judge_path / f"{args.data}_{args.model}_{mode}_{args.chattype}_{args.doclevel}.json"
# )

# corrector_path = Path("/prj/LINDA_LLM/outputs/evaluations/FPs_corrected")
# os.makedirs(corrector_path, exist_ok=True)
# corrector_pkl_path = (
#     corrector_path
#     / f"{args.data}_{args.model}_{mode}_{args.chattype}_{args.doclevel}.pkl"
# )
# corrector_json_path = (
#     corrector_path
#     / f"{args.data}_{args.model}_{mode}_{args.chattype}_{args.doclevel}.json"
# )

finetune_data_path = OUTPUT_ROOT / "datasets"
regulatome_ppi_eval_path = (
    REGULATOME_ROOT / "test_ppi_annotations" / "annotated_ppi_relations_dedup.txt"
)
regulatome_tf_eval_path = (
    REGULATOME_ROOT / "test_tf_annotations" / "annotated_tf_relations_dedup_new.txt"
)
try:
    sft_model_path = OUTPUT_ROOT / "finetunedmodels" / f"{hf_model_id}_regulatome"
except TypeError:
    pass

uniprot_path = RESOURCES_ROOT / "uniprot_description_and_interactors.txt"
