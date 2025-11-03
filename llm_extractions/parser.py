import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--model",
    choices=[
        "llama31",
        "llama33",
        "llama31regu",
        "llama33regu",
        "llama31regutf",
        "llama33regutf",
        "qwen3",
        "qwen314",
        "qwen330",
        "qwen332",
    ],
    default="llama31",
    help="Alias pointing back to model names of the local Ollama server or the provider.",
)
parser.add_argument(
    "--extractionmode",
    type=str,
    choices=[
        "direct",
        "nerrel",
    ],
    default="direct",
)
parser.add_argument(
    "--chattype",
    type=str,
    choices=["oneshot", "stepwise"],
    default="oneshot",
)
parser.add_argument(
    "--data",
    type=str,
    choices=[
        "cardio",
        "5curated",
        "eval",
        "biored",
        "regulatome",
        "regulatomepapers",
    ],
    default="regulatome",
    help="Which data to extract from.",
)
parser.add_argument(
    "--target",
    type=str,
    choices=["ppi", "tf", "lr", "ppitf"],
    default="ppi",
    help="Which entity type you want to extract.",
)
parser.add_argument("--re_evaluate", choices=["judge", "corrector"])
parser.add_argument(
    "--doclevel",
    type=str,
    choices=["chunks", "docs"],
    default="docs",
)
parser.add_argument(
    "--dynex_k",
    type=int,
    default=0,
    help="Number of diverse examples to retrieve for dynex (0 to disable).",
)
parser.add_argument(
    "--lookup",
    action="store_true",
    help="Enable lookup for additional context in the STRING database.",
)
parser.add_argument(
    "--chunksize",
    type=int,
    default=2_000,
)
parser.add_argument(
    "--all_nes_given",
    action="store_true",
)
parser.add_argument(
    "--true_nes_given",
    action="store_true",
)
parser.add_argument(
    "--spacy_nes_given",
    action="store_true",
)
parser.add_argument(
    "--noconfidence",
    action="store_true",
    # default="true",
)
parser.add_argument(
    "--force_new",
    action="store_true",
    help="If set, the script will overwrite existing extraction files.",
)
parser.add_argument(
    "--force_cot",
    action="store_true",
)
parser.add_argument(
    "--node",
    type=str,
    choices=["g2", "g3", "g4", "g5", "mk22d"],
    default="g4",
    help="Node alias that defines the ip where the Ollama server is running (see 'llm.py').",
)
parser.add_argument(
    "--port",
    type=int,
    help="Port, if deviating from the standards defined in the `port_dict` of clients.py.",
)
parser.add_argument(
    "--parser",
    nargs="?",
    const="pymupdf4llm",
    type=str,
    default="pymupdf4llm",
    choices=["pymupdf4llm", "docling"],
    help="These are aliases pointing back to the folder of parsed PDF files (paths configured in 'get_documents.py' and 'paths.py')",
)
parser.add_argument(
    "--loglevel",
    choices=["error", "warn", "info", "debug", "trace", "off"],
    default="off",
)
parser.add_argument(
    "--recall",
    action="store_true",
)
parser.add_argument(
    "--ensemble",
    nargs="?",
    const=5,
    type=int,
    default=0,
    help="Enable self-consistency ensemble with n samples (default=5). Set to 0 to disable.",
)
parser.add_argument(
    "--ensemble_temp",
    type=float,
    default=0.8,
    help="Temperature for ensemble sampling (default=0.8). Only used when --ensemble is enabled.",
)
parser.add_argument(
    "--tot",
    nargs="?",
    const=3,
    type=int,
    default=0,
    help="Enable Tree-of-Thoughts with n reasoning paths (default=3). Set to 0 to disable.",
)
parser.add_argument(
    "--tot_strategy",
    type=str,
    choices=["vote", "best", "merge"],
    default="vote",
    help="Strategy for combining ToT paths: 'vote' (majority voting), 'best' (highest scored path), 'merge' (union of high-confidence).",
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
    "--dev",
    action="store_true",
    help="A developing options that stops the scripts from actually saving/overwriting results.",
)
parser.add_argument(
    "--ext",
    type=str,
    default="",
    help="An extension to the saved filename as a special denominator.",
)
parser.add_argument(
    "--filelist",
    action="store_true",
    default=True,
    help="If true, we append the filename of the current processed file to the list of entities that are extracted. So be careful when ever analysing the 'ner.json' in the `graphdoc_pkl_path` that the last element in a list will then be the filenmae",
)
parser.add_argument(
    "--examples",
    choices=["neg", "pos", "negpos"],
    help="Not yet implemented. Option for future experiments without giving examples to the model (exemplifying zero-shot inference.)",
)
parser.add_argument(
    "--apikey",
    type=str,
    default="NEBIUS_API_KEY_PRP",
    help="If you use an external model provider, this is the API key that is used for it and read out from `os.env`.",
)
parser.add_argument(
    "--train",
    action="store_true",
)
parser.add_argument(
    "--save",
    action="store_true",
)
parser.add_argument(
    "--push",
    action="store_true",
)
parser.add_argument(
    "--load",
    action="store_true",
)

args = parser.parse_args()

# Force extractionmode to nerrel when chattype is lookup or when lookup is enabled
if (
    args.lookup
    or args.all_nes_given
    or args.true_nes_given
    or args.spacy_nes_given
    or args.lookup
):
    args.extractionmode = "nerrel"
