# LLM_Relations

## LLM_Extractions

This is the code that was used to extract the desired structured information from the LLMs.

The folder structure is the following, import files being highlighted:

```bash
.
├── check_hallucinations.py
├── const.py
├── generate_graph.py <--- main script to run the extractions
├── get_documents.py
├── graphdocs2json.py <--- script that can be run afterwards to convert the exraction objects into parsable json format
├── graph_utils.py
├── langchain_patch.py <--- a patch for langchain to be applied (see installation)
├── llama_parse.ipynb <--- notebook used to parse your PDF papers with llama_parse
├── llm.py
├── parser.py <--- the argparser the will ask for the type of data, type of llm, API information and so on.
├── paths.py
├── README.md
├── requirements.txt <--- requirements file to for the Pyhton environemnt (see installation)
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

As we wrote in the manuscript, we had to implement minor changes in the langchain code directly as it was diffult to inherit and overwrite the low-leveled functino diretctly. Please replace the function `_convert_to_message` in `langchain_core/messages/utils.py` at line `284` with the following patch located in [langchain_patch](langchain_patch.py).

### Usage

0) Output folder structure

The outputs are saved in a folder `outputs` in the same directoy as this code is located.

```
.
├── graph_docs <-- here are the triples directly after extracting with generate_graph.py (as langchain_community.graphs.GraphDocument)
├── graph_triples <-- here are the triples saved in json format after using graphdocs2json.py to convert them from the GraphDocument format
├── paper_chunks <-- here are the papers saved together with their id, both as chunks and as whole documents (as langchain_core.documents.base.Document)
├── paper_dicts <-- (for debugging purposes) a mapping from the number of the paper in read-in order to their parsed paper path
└── parsed papers <-- here we save the papers after parsed with llama_parse
```

You can change the naming of the output folder and most of the subpaths to your desired needs in [paths](paths.py).

1) Parse PDFs to Markdown

Use the notebook llama_parse.ipynb to parse your bunch of PDFs into markdown format. To use llama_parse, you have to create your own APi key [here](https://docs.cloud.llamaindex.ai/llamaparse/getting_started/get_an_api_key).

2) Extract Relations

To extract relations we will use the [generate_graph](generate_graph.py) script that will output a collection of serialized [GraphDocuments](https://python.langchain.com/api_reference/community/graphs/langchain_community.graphs.graph_document.GraphDocument.html). To start the script with the correct information, we have to set up certain arguments and paths. The [parser](parser.py) was designed to our environment (paths and data names). 

We first list those options that are essential for the algorithm and are valid in any environment:

```
  --style {1,2,3,4,5,6}
                        Declare which of our predefined styles you want to chose (see `style_dict` in 'style_templates.py' for the individual prompts.)
  --parser [{llama_parse,marker}]
                        These are aliases pointing back to the folder of parsed PDF files (paths configured in 'get_documents.py' and 'paths.py')
  --simple              If true, the simpler prompt if chosen from the `style_dict` in 'style_templates.py' for the current style. Otherwise we use the style denoted `complex`, which is a more elaborate variant of the prompt.
  --onlyner             If true, only named entitiy recognition is carried out and the named entities are saved to 'ner.json' in the `graphdoc_pkl_path`.
  --relgiventrueners    An option to only do RE. This sets `nerrel` automatically to `individual`. A list of the ground truth entities THAT PARTICIPATE IN RELATIONS is given to the chat model to let it classify relations between those. If you have those pre-annotations then
                        you can add the path to in 'get_documents.py' to the variable `_true_ner_paths`. The path must containt txt-files for each document with the same filename as the document with newline separated entities.
  --relgivenallners     An option to only do RE. This sets `nerrel` automatically to `individual`. A list of ALL the ground truth entities is given to the chat model to let it classify relations between those. If you have those pre-annotations then you can add the path to in
                        'get_documents.py' to the variable `_all_ner_paths`. The path must containt txt-files for each document with the same filename as the document with newline separated entities.
  --nerrel {conversational,individual}
                        This is the option for doing NER first (extracting the entities) and then RE (classifying relations between those detected entities). 'conversational' means that the same model is used for NER and RE (such that the conversation starts with the NER)
                        whereas 'individual' means that a dedicated chat is used to extract the entities and the actual chat is started by giving those entities to the chat model and ask for RE.
  --doclevel            If true, whole documents are given as input to the llm instead of chunks. The the `text_splitter` in get_documents.py for information how documents are chunked.
  --saveinbetweenoutputs
                        If true, we save outputs for each step in multi-step conversational prompts. So for each document/chunk a list of lists is saved, the order of the outer list representing the order of the steps.
  --filelist            If true, we append the filename of the current processed file to the list of entities that are extracted. So be careful when ever analysing the 'ner.json' in the `graphdoc_pkl_path` that the last element in a list will then be the filenmae
```

These are flags that you have to change in the code to suit your environment:

```
  --target [{tf,ppi,both,ppi_eval,tf_eval,lr_eval,biored,ppi_regulatome,tf_regulatome}]
                        These are pre-defined aliases for certain task and entity combinations. You have to set those up for your own data and pathing and change loading and processing rules in 'const.py', 'generate_graph.py', 'get_documents.py', 'graph_docs2json.py'. and
                        'paths.py'
  --port {34,35,36}     Port where the local Ollama server is running.
  --node {g2,g3,g4,g5,mk22d}
                        Node alias that defines the ip where the Ollama server is running (see 'llm.py').
  --nebius              We used Nebius (nebius.com) as provider to run external computations. This changes the Chat Wrapper API (see 'llm.py').
  --curated             An extra alias that points to a local subset of data in our environment.
  --model {8b,70b,405b}
                        Alias pointing back to model names of the local Ollama server or the provider.
  --apikey APIKEY       If you use an external model provider, this is the API key that is used for it and read out from `os.env`.
```

And finally debugging/experimental settings:

```
  --startfromdoc [STARTFROMDOC]
                        To exclude the first n documents/chunks from the extraction.
  --untildoc [UNTILDOC]
                        To only parse untnil the nth document/chunk.
  --printpaperpaths     Debugging option to print the paper paths while processing.
  --dev                 A developing options that stops the scripts from actually saving/overwriting results.
  --noexamples          Not yet implemented. Option for future experiments without giving examples to the model (exemplifying zero-shot inference.)
```

After having made yourself familiar with the options and have changed aliases in the code to point to your own data, you can then run the script with:

```bash
python generate_graph.py --target ... [...]
```

3) Conversation to json format

The relations are saved in the GraphDocument format (in our environment under `outputs/graph_docs`) and can now be converted to json format for easier analysis. To do so, you can use the script [`graphdocs2json](graphdocs2json.py). When you use the same flags as for extraction and have set your aliases correctly in the code, the script will load them and write them back in the correct subfolder (`outputs/graph_triples` in our environment).

