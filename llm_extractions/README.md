# LINDA-LLM Extraction Toolkit

Production-ready scripts for extracting molecular interaction triples with large language models. This directory mirrors the `llm_extractions/` folder of the public [dieterich-lab/LLM_Relations](https://github.com/dieterich-lab/LLM_Relations) repository.

## Quick Start

Requires Python 3.11 and [Poetry](https://python-poetry.org/docs/) 1.7+. Install Poetry first if it is not already available:

```bash
command -v poetry >/dev/null || pipx install poetry  # or follow Poetry's official installer

git clone https://github.com/dieterich-lab/LLM_Relations.git
cd LLM_Relations/llm_extractions
poetry install
poetry run baml-cli generate
```

## Configure Paths

Runtime paths are now configurable through environment variables. Defaults point to the project-relative locations shown below, but you can override any value without editing the source code.

| Variable | Default | Purpose |
| --- | --- | --- |
| `LINDA_LLM_PROJECT_ROOT` | project root (this folder) | Base directory for relative defaults |
| `LINDA_LLM_OUTPUT_ROOT` | `outputs/` | Root for generated artefacts and checkpoints |
| `LINDA_LLM_TRIPLES_ROOT` | `outputs/triples/` | Base folder for extracted triples |
| `LINDA_LLM_REGULATOME_ROOT` | `../RegulaTome/` | Location of the RegulaTome evaluation corpus |
| `LINDA_LLM_RESOURCES_ROOT` | `../resources/` | Shared resources such as UniProt tables |

Create a `.env` (or export the variables manually) before running the scripts:

```bash
cp .env.example .env  # edit .env with your paths
source .env
```

All scripts import `paths.py`, which resolves these variables and creates any missing output folders on demand. If an environment variable is omitted, the default path is used.

## Repository Layout

- `add_names.py` – query LLMs for alternative entity names
- `baml/` – BoundaryML schema used for structured parsing of model outputs
- `clients.py` – client registry with model aliases and inference endpoints
- `converter.py` – transform Pydantic triples into JSON/JSONL artefacts
- `data/` – curated and pre-processed inputs (RegulaTome, 5 curated cardiac papers)
- `documents.py` – utilities to prepare inputs from parsed PDFs
- `embed.py` – build dense vector indices for retrieval-augmented extraction
- `extract.py` – main CLI entrypoint for extraction experiments
- `finetune.py` & `finetuning_tools.py` – supervised fine-tuning pipeline
- `parser.py` – centralised CLI argument definitions
- `paths.py` – single source of truth for runtime paths (now environment-aware)
- `prompts.py` – prompt templates, exemplars, and ToT strategies
- `regu_names.py` / `add_names.py` – generate synonym dictionaries for evaluation
- `requirements.txt` – Python dependencies

## Running Extractions

```bash
python extract.py \
  --model llama33 \
  --data regulatome \
  --target ppi \
  --extractionmode direct \
  --chattype oneshot
```

Useful flags:

- `--ensemble N` – enable self-consistency ensembles (default temperature 0.8)
- `--tot N` – activate Tree-of-Thoughts reasoning with `vote|best|merge` strategies
- `--lookup` – query STRING metadata before relation extraction (forces `nerrel` mode)
- `--force_new` – overwrite existing outputs under the resolved run directory

Outputs are stored beneath `${LINDA_LLM_TRIPLES_ROOT}/{data}/{target}/…` with JSON and JSONL artefacts for each run configuration.

## Fine-tuning

Fine-tune LoRA adapters with:

```bash
python finetune.py --model llama31 --data regulatome --save
```

Resulting checkpoints are written to `${LINDA_LLM_OUTPUT_ROOT}/finetunedmodels/` (configurable via environment variables).

## Model Hosting

The framework works with local Ollama deployments or external providers (Nebius, etc.). Update `clients.py` to map `--model` aliases to your chosen backends and ensure the models are available:

| Alias | Suggested model |
| --- | --- |
| llama31 | `ollama pull llama3.1` or corresponding HF ID |
| llama33 | `ollama pull llama3.3:70b` |

## Data

The RegulaTome corpus is available at [Zenodo](https://zenodo.org/records/10808330) under CC BY 4.0. Place the files under `${LINDA_LLM_REGULATOME_ROOT}` or point the environment variable to your copy. The repository also includes five manually curated cardiac signalling papers; see `data/5curated/` for plain-text inputs.

## Contributing / Publishing

1. Keep this directory in sync with the `llm_extractions/` folder in the public repository. See the project wiki (or internal runbook) for the release checklist.
2. Document any environment assumptions in this README and keep `.env.example` aligned with the code.
3. Run the evaluation scripts in `outputs/` (or your configured directory) to verify reproductions before tagging a release.