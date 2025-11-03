import json
import os
from parser import args
from pathlib import Path

os.environ["BAML_LOG"] = args.loglevel  # isort:skip
from baml.baml_client.sync_client import b  # isort:skip
from finetuning_tools import get_dataset

from clients import cr

_, _, test_dataset = get_dataset()

d = dict()

for i, data in enumerate(test_dataset):
    print(i)
    triples = data["relations"].split(";")
    for triple in triples:
        head = triple.split("=")[0]
        tail = triple.split("=")[1]
        if head not in d:
            try:
                alt_names = b.CreateAltNames(
                    head,
                    {"client_registry": cr},
                ).alt_names
                d[head] = alt_names
            except:
                pass
        if tail not in d:
            try:
                alt_names = b.CreateAltNames(
                    tail,
                    {"client_registry": cr},
                ).alt_names
                d[tail] = alt_names
            except:
                pass

path = Path("/prj/LINDA_LLM/outputs") / "regu_test_names.json"
with open(path, "w") as f:
    json.dump(d, f, indent=4)
    print(f"Saved json to {path}")
