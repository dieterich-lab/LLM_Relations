import json
import os
from parser import args
from pathlib import Path

from documents import all_docs
from paths import (
    finetune_data_path,
    regulatome_ppi_eval_path,
    regulatome_tf_eval_path,
    triple_json_path,
)

os.environ["BAML_LOG"] = args.loglevel  # isort:skip
from baml.baml_client.sync_client import b  # isort:skip
from clients import cr
from dataset import get_dataset

print(f"Getting triples from {triple_json_path.parent}")
with open(triple_json_path, "r") as f:
    all_triples = json.load(f)

d = dict()

print(len(all_triples))

for i, data in enumerate(all_triples):
    triples = data["triples"][0]
    print(i, triples)
    for triple in triples:
        if triple["head"] not in d:
            try:
                alt_names = b.CreateAltNames(
                    triple["head"],
                    {"client_registry": cr},
                ).alt_names
                d[triple["head"]] = alt_names
                print(alt_names)
            except:
                pass
        if triple["tail"] not in d:
            try:
                alt_names = b.CreateAltNames(
                    triple["tail"],
                    {"client_registry": cr},
                ).alt_names
                d[triple["tail"]] = alt_names
                print(alt_names)
            except:
                pass

with open(triple_json_path.parent / "synonyms.json", "w") as f:
    json.dump(d, f, indent=4)
    print(f"Saved json to {triple_json_path.parent}")
