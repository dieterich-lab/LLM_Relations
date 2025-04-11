import json
import os
from parser import args

from paths import triple_json_path

os.environ["BAML_LOG"] = args.loglevel  # isort:skip
from baml.baml_client.sync_client import b  # isort:skip
from clients import cr

with open(triple_json_path, "r") as f:
    all_triples = json.load(f)

d = dict()

for i, data in enumerate(all_triples):
    print(i)
    triples = data["triples"][0]
    for triple in triples:
        if triple["head"] not in d:
            try:
                alt_names = b.CreateAltNames(
                    triple["head"],
                    {"client_registry": cr},
                ).alt_names
                d[triple["head"]] = alt_names
            except:
                pass
        if triple["tail"] not in d:
            try:
                alt_names = b.CreateAltNames(
                    triple["tail"],
                    {"client_registry": cr},
                ).alt_names
                d[triple["tail"]] = alt_names
            except:
                pass

with open(triple_json_path.parent / "names.json", "w") as f:
    json.dump(d, f, indent=4)
    print(f"Saved json to {triple_json_path.parent / 'names.json'}")
