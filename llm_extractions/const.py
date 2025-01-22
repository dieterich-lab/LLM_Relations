from parser import args

if "ppi" in args.target or args.target == "biored":
    PROMPT_LOOKUP = "ppi"
elif "tf" in args.target:
    PROMPT_LOOKUP = "tf"
elif "lr" in args.target:
    PROMPT_LOOKUP = "lr"
else:
    PROMPT_LOOKUP = args.target

if args.target in ["ppi", "tf", "both"] and args.curated:
    PAPER_PATH = "ppi"
else:
    PAPER_PATH = args.target
