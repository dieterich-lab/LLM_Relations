# LLM_Relations

## LLM_Extractions

This is the code to that was used to extract the desired structured information from the LLMs.

The folder structure is the following, import files being highlighted:

```bash
.
├── check_hallucinations.py
├── const.py
├── generate_graph.py <--- main script to run the extractions
├── get_documents.py
├── graphdocs2json.py <--- script that can be run afterwards to convert the exraction objects into parsable json format
├── graph_utils.py
├── langchain_path.py <--- a patch for langchain to be applied (see installation)
├── llama_parse.ipynb <--- notebook used to parse your PDF papers with llama_parse
├── llm.py
├── marker_parse.py
├── parser.py <--- the argparser the will ask for the type of data, type of llm, API information and so on.
├── paths.py
├── README.md
├── requirements.txt
├── structured_classes.py
├── style_templates.py
├── templates.py
└── utils.py
```

### Installation

You can install the requirements after cloning the project:

```
git clone  https://github.com/dieterich-lab/LLM_Relations
cd LLM_Relations/llm_extractions
python3 -m venv ~/.venvs/linda  # or any other choice of directory # tested with Python 3.11.2
. ~/.venvs/linda/bin/activate # or your choice of directory
pip install -r requirements.txt
```

As we wrote the manuscript, we had to implement minor changes in the langchain code directly as it was diffult to inherit and overwrite the low-leveled functino diretctly. Please replace the function `_convert_to_message` in `langchain_core/messages/utils.py` at line `284` with the following patch located in [langchain path](langchain_patch.py).


### Usage

1) Parse PDFs to Markdown

Use the notebook llama_parse.ipynb to parse your bunch of PDFs into markdown format. To use llama_parse, you have to create your own APi key [here](https://docs.cloud.llamaindex.ai/llamaparse/getting_started/get_an_api_key).

2) Extract Relations

To extract relations we will use the [generate graph](generate_graph.py) script that will output a collection of serialized [GraphDocuments](https://python.langchain.com/api_reference/community/graphs/langchain_community.graphs.graph_document.GraphDocument.html). To start the script with the correct information, we have to set up certain arguments and paths. The [parser](parser.py) will help here:

```bash
usage: parser.py [-h] [--target [{tf,ppi,both,ppi_eval,tf_eval,lr_eval,biored,ppi_regulatome,tf_regulatome}]] [--style {1,2,3,4,5,6}]
                 [--port {34,35,36}] [--gpu {g2,g3,g4,g5}] [--parser [{llama_parse,marker}]] [--startfromdoc [STARTFROMDOC]]
                 [--untildoc [UNTILDOC]] [--simple] [--onlyner] [--relgiventrueners] [--relgivenallners]
                 [--nerrel {conversational,individual}] [--printpaperpaths] [--nebius] [--doclevel] [--curated] [--dev]
                 [--saveinbetweenoutputs] [--nerlist] [--toolcall] [--filelist] [--noexamples]
                 [--model {8b,70b,405b,mixtral,biollm,nemo}] [--apikey APIKEY]

options:
  -h, --help            show this help message and exit
  --target [{tf,ppi,both,ppi_eval,tf_eval,lr_eval,biored,ppi_regulatome,tf_regulatome}]
  --style {1,2,3,4,5,6}
  --port {34,35,36}
  --gpu {g2,g3,g4,g5}
  --parser [{llama_parse,marker}]
  --startfromdoc [STARTFROMDOC]
  --untildoc [UNTILDOC]
  --simple
  --onlyner
  --relgiventrueners
  --relgivenallners
  --nerrel {conversational,individual}
  --printpaperpaths
  --nebius
  --doclevel
  --curated
  --dev
  --saveinbetweenoutputs
  --nerlist
  --toolcall
  --filelist
  --noexamples
  --model {8b,70b,405b,mixtral,biollm,nemo}
  --apikey APIKEY
```

3) JSON Conversation