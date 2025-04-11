# LLM_Relations

## Installation

Clone this project and install the requirements in a python environment of your choice.

```bash
git clone  https://github.com/dieterich-lab/LLM_Relations
cd LLM_Relations/llm_extractions
python3 -m venv ~/.venvs/llm  # or any other choice of directory # tested with Python 3.11.2
. ~/.venvs/llm/bin/activate # or your choice of directory
pip install -r requirements.txt
```

We also use the [BAML](https://www.boundaryml.com/) framework as structured output parser to extract triples from the LLM's response. The library will already get installed with the requirements and we also prepared the according [baml](./baml/baml_src/) files. All you need to do now is to trigger the initiation of the src code by running from the command line:

```bash
baml-cli generate
```

## Folder Structure

### Project Folders

```bash
.
├── add_names.py # script to query an LLM for alternative names for extracted triples
├── baml # we use boundary ml ("baml") to parse structured outputs (e.g. triples)
│   └── baml_src                      
│       ├── clients.baml # a dummy client, as all clients will be created live from a dictionary and added to the client registry (see clients.py)
│       ├── generators.baml # standard file for baml that declares the language and version of baml
│       ├── names.baml # function and classes for generating alt names for triples
│       └── rel.baml # function and classes for extracting triples from text
├── clients.py # here are aliases for the used models saved, ips for GPU nodes in our compute environment and the client registry for baml
├── converter.py # containing a function to convert pydantic triples to json and save them
├── data # containing the curated and pre-processed input data
├── documents.py # script to prepare the input documents
├── embed.py # function to embed the trainig and development set of regulatome in a vector store
├── extract.py # main script to extract triples from texts
├── finetune.py # main script to finetune a model
├── finetuning_tools.py # outsourced configurations used for finetuning a model
├── llama_parse.ipynb # notebook to parse papers via llama_parse
├── parser.py # argparser for CLI
├── paths.py # declaration of all the input and outpt pathes
├── prompts.py # declaration of the prompts for the different styles and regimes
├── README.md # this readme :-)
├── regu_names.py # script to query an LLM for alternative names for the entities in the RegulaTome test dataset
├── requirements.txt # installation requirements
```

### Output Folders

The project will save the outputs in a folder `outputs` in the same directoy as this code is located:

```bash
├── outputs            
│   ├── datasets # folder for the RegulaTome dataset saved as arrow files for fine-tuning
│   ├── docs # here we save the input data documents
│   ├── finetunedmodels # path for the finetuned models
│   ├── parsed_papers # a folder for your custom parsed papers
│   ├── regulatome_train_idx.bin # the train and development set of RegulaTome as vector store binary
│   ├── regu_test_names.json # the alternative names and abbreviations for the entities in the RegulaTome test set
│   └── triples # the actual extracted triples
```

### LLMs and Inference Server:

As we used [Ollama](ollama.com) for inference and [huggingface](huggingface.co)/[unsloth](https://unsloth.ai/) for fine-tuning. All models can be acquired from the following sources:


| model  | alias |huggingface  | ollama |
|---|---|---|---|
|llama3.1:8b   | llama31 | https://huggingface.co/unsloth/Meta-Llama-3.1-8B |https://ollama.com/library/llama3.1 |
|llama3.3:70b   | llama33 | https://huggingface.co/meta-llama/Llama-3.3-70B  |https://ollama.com/library/llama3.3:70b |
|llama3.1:8b (finetuned)  | llama31regu | _tbd_ | - |
|llama3.3:70b (finetuned)  | llama33regu | _tbd_ | - |


To set up the ip's and corresponding aliases for your Ollama server, customize the `ip_dict` in [clients.py](./clients.py) and don't forget to pull the models via `ollama pull [llama3.1 | llama3.3:70b]`.

### Data

We used the RegulaTome dataset for high throughput evaluation and cureated 5 cardiac research to analyze performance on real-world data.

The regulatome corpus can be found [here](https://zenodo.org/records/10808330) under the [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode) licencse.

The five curated papers are the following:

@Enio: citations here

We processed the corpus and the annotated papers to have easy access to the input texts and their according ground truths. They are automatically used by the scripts when choosing the option `--data [regulatome | 5curated]` and can be found here:

```bash
data/
├── 5curated # containing the 5 chosen papers in plaintext format (parsed with llama_parse)
├── regulatome # containing the regulatome texts in plaintext format
├── transformers_datasets # the regulatome data as transformers datasets
├── uniprot_lookup # a compiled list from the uniprot database containing related molecule information
└── vector_index # the train and development set saved as a HNSW vector index
```

### Relation Extraction

To extract relations, you can use [extract.py](./extract.py). To get all possible options, use the help of the argparser:

```bash
python extract.py -h
```

The most important parameters the following:

```bash
  --model {llama31,llama33,deepseek8b,gemma,gemmaregu,deepseek70b,llama31regu,llama33regu}
                        Aliases pointing back to model names of the local Ollama server or the provider. More specifically defined in `clients.py`.
  --extractionmode {direct,nerrel}
                        `nerrel`: Extract entities first, from these, extract corresponding relations. `direct`: Extract relations (triples) in a single step.
  --chattype {oneshot,stepwise,lookup}
                        `oneshot`: extract relations in a single step (don't ask for revising). `stepwise`: Let the LLM revise the prompts in two additional steps. `lookup`: Sets `extractionmode` to `nerrel` and queries information about the entities from our uniprot
                        database.
  --data {5curated,regulatome}
                        Aliases that point to the according txt/md files of the RegulaTome corpus or our 5 curated papaers.
```

### Fine-tuning

For finetuning, you can use the [finetune.py](./finetune.py) script with either the `--model llama31` or the `--model llama33` flag, depending what model you want to fine-tune.