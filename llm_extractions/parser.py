import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--target",
    nargs="?",
    const="tf",
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
)
parser.add_argument(
    "--style",
    type=int,
    choices=list(range(1, 7)),
    default=1,
)
parser.add_argument("--port", type=int, choices=[34, 35, 36], default=34)
parser.add_argument("--gpu", type=str, choices=["g2", "g3", "g4", "g5"], default="g4")
parser.add_argument(
    "--parser",
    nargs="?",
    const="llama_parse",
    type=str,
    default="marker",
    choices=["llama_parse", "marker"],
)
parser.add_argument(
    "--startfromdoc",
    nargs="?",
    const=0,
    type=int,
    default=0,
)
parser.add_argument(
    "--untildoc",
    nargs="?",
    const=0,
    type=int,
    default=0,
)
parser.add_argument(
    "--simple",
    action="store_true",
    default=True,
)
parser.add_argument(
    "--onlyner",
    action="store_true",
)
parser.add_argument(
    "--relgiventrueners",
    action="store_true",
)
parser.add_argument(
    "--relgivenallners",
    action="store_true",
)
parser.add_argument(
    "--nerrel", type=str, choices=["conversational", "individual"], default="individual"
)
parser.add_argument(
    "--printpaperpaths",
    action="store_true",
)
parser.add_argument(
    "--nebius",
    action="store_true",
)
parser.add_argument(
    "--doclevel",
    action="store_true",
    default=True,
)
parser.add_argument(
    "--curated",
    action="store_true",
)
parser.add_argument(
    "--dev",
    action="store_true",
)
parser.add_argument(
    "--saveinbetweenoutputs",
    action="store_true",
    default=True,
)
parser.add_argument(
    "--nerlist",
    action="store_true",
)
parser.add_argument(
    "--toolcall",
    action="store_true",
)
parser.add_argument(
    "--filelist",
    action="store_true",
    default=True,
)
parser.add_argument(
    "--noexamples",
    action="store_true",
)
parser.add_argument(
    "--model", choices=["8b", "70b", "405b", "mixtral", "biollm", "nemo"], default="70b"
)
parser.add_argument("--apikey", type=str, default="NEBIUS_API_KEY_PRP")

args = parser.parse_args()
