import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--model",
    choices=[
        "llama31",
        "llama33",
        "deepseek8b",
        "gemma",
        "gemmaregu",
        "deepseek70b",
        "llama31regu",
        "llama33regu",
    ],
    default="llama31",
    help="Aliases pointing back to model names of the local Ollama server. More specifically defined in `clients.py`.",
)
parser.add_argument(
    "--extractionmode",
    type=str,
    choices=[
        "direct",
        "nerrel",
    ],
    default="direct",
    help="`nerrel`: Extract entities first, from these, extract corresponding relations. `direct`: Extract relations (triples) in a single step.",
)
parser.add_argument(
    "--chattype",
    type=str,
    choices=["oneshot", "stepwise", "lookup"],
    default="stepwise",
    help="`oneshot`: extract relations in a single step (don't ask for revising). `stepwise`: Let the LLM revise the prompts in two additional steps. `lookup`: Sets `extractionmode` to `nerrel` and queries information about the entities from our uniprot database.",
)
parser.add_argument(
    "--data",
    type=str,
    choices=[
        "5curated",
        "regulatome",
    ],
    default="regulatome",
    help="Aliases that point to the according txt/md files of the RegulaTome corpus or our 5 curated papaers.",
)
parser.add_argument(
    "--target",
    type=str,
    choices=["ppi"],
    default="ppi",
    help="Aliases that point to different interaction types and therefore data files and prompt schemes. We solely used `ppi` (protein-protein interactions) for this project.",
)
parser.add_argument("--re_evaluate", choices=["judge", "corrector"])
parser.add_argument(
    "--dynex", action="store_true", help="If to use dynamically generated examples."
)
parser.add_argument(
    "--all_ners_given",
    action="store_true",
    help="Option to start relation extraction from the named entities given (pre-annotated as ground truth) in the paper (all entities, not only the ones particpating in relations).",
)
parser.add_argument(
    "--examples",
    choices=["neg", "pos", "negpos"],
    help="Option to either give positive, negative or both examples.",
)
parser.add_argument(
    "--noconfidence",
    action="store_true",
    default="true",
    help="If the LLM should also annoate confidence levels for triples. Must not activated for fine-tuned models.",
)
parser.add_argument(
    "--force_cot",
    action="store_true",
    help="If to use chain-of-thought prompts that force LLMs other than DeepSeek to show their thinking process.",
)
parser.add_argument(
    "--port",
    type=int,
    choices=[32, 33, 34, 35],
    default=34,
    help="Port where the local Ollama server is running.",
)
parser.add_argument(
    "--node",
    type=str,
    choices=["g2", "g3", "g4", "g5", "mk22d"],
    default="g4",
    help="Node alias that defines the ip where the Ollama server is running.",
)
parser.add_argument(
    "--parser",
    nargs="?",
    const="llama_parse",
    type=str,
    default="llama_parse",
    help="These are aliases pointing back to the folder of parsed PDF files. Only `llama_parse` available for this project.",
)
parser.add_argument(
    "--loglevel",
    choices=["error", "warn", "info", "debug", "trace", "off"],
    default="info",
    help="How much output to show from the baml-py library. `info`: Show the thinking process/raw output. `off`: Don't show the thinking process/raw output.",
)
parser.add_argument(
    "--recall", action="store_true", help="If to use a special high-recall prompt."
)
parser.add_argument(
    "--dev",
    action="store_true",
    help="A debugging option that stops the scripts from actually saving/overwriting results.",
)
parser.add_argument(
    "--filelist",
    action="store_true",
    default=True,
    help="If true, we append the filename of the current processed file to the list of entities that are extracted. So be careful when ever analysing the 'ner.json' in the `graphdoc_pkl_path` that the last element in a list will then be the filenmae",
)

args = parser.parse_args()
