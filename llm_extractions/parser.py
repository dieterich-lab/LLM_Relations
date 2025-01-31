import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--target",
    type=str,
    choices=[
        "tf",
        "ppi",
        "both",
        "ppi_eval",
        "tf_eval",
        "lr_eval",
        "biored",
        "ppi_regulatome",
        "tf_regulatome",
    ],
    help="These are pre-defined aliases for certain task and entity combinations. You have to set those up for your own data and pathing and change loading and processing rules in 'const.py', 'generate_graph.py', 'get_documents.py', 'graph_docs2json.py'. "
    " and 'paths.py'",
)
parser.add_argument(
    "--style",
    type=int,
    choices=list(range(1, 7)),
    default=1,
    help="Declare which of our predefined styles you want to chose (see `style_dict` in 'style_templates.py' for the individual prompts.)",
)
parser.add_argument(
    "--port",
    type=int,
    choices=[34, 35, 36],
    default=34,
    help="Port where the local Ollama server is running.",
)
parser.add_argument(
    "--node",
    type=str,
    choices=["g2", "g3", "g4", "g5", "mk22d"],
    default="g4",
    help="Node alias that defines the ip where the Ollama server is running (see 'llm.py').",
)
parser.add_argument(
    "--parser",
    nargs="?",
    const="llama_parse",
    type=str,
    default="marker",
    choices=["llama_parse", "marker"],
    help="These are aliases pointing back to the folder of parsed PDF files (paths configured in 'get_documents.py' and 'paths.py')",
)
parser.add_argument(
    "--startfromdoc",
    nargs="?",
    const=0,
    type=int,
    default=0,
    help="To exclude the first n documents/chunks from the extraction.",
)
parser.add_argument(
    "--untildoc",
    nargs="?",
    const=0,
    type=int,
    default=0,
    help="To only parse untnil the nth document/chunk.",
)
parser.add_argument(
    "--simple",
    action="store_true",
    default=True,
    help="If true, the simpler prompt if chosen from the `style_dict` in 'style_templates.py' for the current style. Otherwise we use the style denoted `complex`, which is a more elaborate variant of the prompt.",
)
parser.add_argument(
    "--onlyner",
    action="store_true",
    help="If true, only named entitiy recognition is carried out and the named entities are saved to 'ner.json' in the `graphdoc_pkl_path`.",
)
parser.add_argument(
    "--relgiventrueners",
    action="store_true",
    help="An option to only do RE. This sets `nerrel` automatically to `individual`. A list of the ground truth entities THAT PARTICIPATE IN RELATIONS is given to the chat model to let it classify relations between those. If you have those pre-annotations then "
    "you can add the path to in 'get_documents.py' to the variable `_true_ner_paths`. The path must containt txt-files for each document with the same filename as the document with newline separated entities.",
)
parser.add_argument(
    "--relgivenallners",
    action="store_true",
    help="An option to only do RE. This sets `nerrel` automatically to `individual`. A list of ALL the ground truth entities is given to the chat model to let it classify relations between those. If you have those pre-annotations then "
    "you can add the path to in 'get_documents.py' to the variable `_all_ner_paths`. The path must containt txt-files for each document with the same filename as the document with newline separated entities.",
)
parser.add_argument(
    "--nerrel",
    type=str,
    choices=["conversational", "individual"],
    default="individual",
    help="This is the option for doing NER first (extracting the entities) and then RE (classifying relations between those detected entities). "
    "'conversational' means that the same model is used for NER and RE (such that the conversation starts with the NER) whereas 'individual' means that a dedicated chat is used to extract the entities and the actual chat is started by "
    "giving those entities to the chat model and ask for RE.",
)
parser.add_argument(
    "--printpaperpaths",
    action="store_true",
    help="Debugging option to print the paper paths while processing.",
)
parser.add_argument(
    "--nebius",
    action="store_true",
    help="We used Nebius (nebius.com) as provider to run external computations. This changes the Chat Wrapper API (see 'llm.py').",
)
parser.add_argument(
    "--level",
    choices=["docs", "chunks"],
    default="docs",
    help="Either, whole documents are given as input to the llm instead or chunks. The the `text_splitter` in get_documents.py for information how documents are chunked.",
)
parser.add_argument(
    "--curated",
    action="store_true",
    help="An extra alias that points to a local subset of data in our environment.",
)
parser.add_argument(
    "--dev",
    action="store_true",
    help="A developing options that stops the scripts from actually saving/overwriting results.",
)
parser.add_argument(
    "--saveinbetweenoutputs",
    action="store_true",
    default=True,
    help="If true, we save outputs for each step in multi-step conversational prompts. So for each document/chunk a list of lists is saved, the order of the outer list representing the order of the steps.",
)
parser.add_argument(
    "--filelist",
    action="store_true",
    default=True,
    help="If true, we append the filename of the current processed file to the list of entities that are extracted. So be careful when ever analysing the 'ner.json' in the `graphdoc_pkl_path` that the last element in a list will then be the filenmae",
)
parser.add_argument(
    "--noexamples",
    action="store_true",
    help="Not yet implemented. Option for future experiments without giving examples to the model (exemplifying zero-shot inference.)",
)
parser.add_argument(
    "--model",
    choices=["8b", "70b", "405b", "deepseek", "70b3.3"],
    default="70b",
    help="Alias pointing back to model names of the local Ollama server or the provider.",
)
parser.add_argument(
    "--apikey",
    type=str,
    default="NEBIUS_API_KEY_PRP",
    help="If you use an external model provider, this is the API key that is used for it and read out from `os.env`.",
)

args = parser.parse_args()
