import json
import pickle
from parser import args

from paths import graphdoc_pkl_paths, triple_path

for i, path in enumerate(graphdoc_pkl_paths):
    graph_documents = list()

    with open(path, "rb") as f:
        while 1:
            try:
                graph_documents.append(pickle.load(f))
            except EOFError:
                break

    if not args.saveinbetweenoutputs:
        rels = [
            (r, g.source.page_content) for g in graph_documents for r in g.relationships
        ]
        rel_triples = [[[r.source.id, r.type, r.target.id], p] for (r, p) in rels]
    else:
        rels = [[step.relationships for step in g] for g in graph_documents]
        rel_triples = list()
        for doc in rels:
            step_list = list()
            for step in doc:
                rel_list = list()
                for rel in step:
                    rel_list.append([rel.source.id, rel.type, rel.target.id])
                step_list.append(rel_list)
            rel_triples.append(step_list)

    triple_filename = "triples.json"
    if args.saveinbetweenoutputs:
        triple_filename = "triples_+_in_between.json"

    if args.target == "both":
        if i == 0:
            triple_filename = "ppi_triples.json"
        else:
            triple_filename = "tf_triples.json"

    if not args.dev:
        with open(triple_path / triple_filename, "w") as f:
            json.dump(rel_triples, f, indent=4)

        print(f"{triple_path / triple_filename}")
