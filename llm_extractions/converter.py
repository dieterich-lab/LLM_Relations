import json
import pickle

import baml


def convert_and_save_triples_to_json(triple_pkl_path, triple_json_path):
    json_triples = list()
    with open(triple_pkl_path, "rb") as triple_pkl_file:
        while 1:
            try:
                tuple = pickle.load(triple_pkl_file)
                steps = tuple[0]
                text = tuple[1]
                file_name = str(tuple[2])
                step_list = list()
                for triple_objs in steps:
                    triple_list = list()
                    if isinstance(triple_objs, baml.baml_client.types.Entities):
                        triple_list = triple_objs.entities
                    elif isinstance(triple_objs, list):
                        triple_list = triple_objs
                    else:
                        for triple_obj in triple_objs.triples:
                            if hasattr(triple_obj, "confidence"):
                                triple_list.append(
                                    {
                                        "head": triple_obj.head,
                                        "relation": triple_obj.relation,
                                        "tail": triple_obj.tail,
                                        "confidence": triple_obj.confidence,
                                    }
                                )
                            else:
                                triple_list.append(
                                    {
                                        "head": triple_obj.head,
                                        "relation": triple_obj.relation,
                                        "tail": triple_obj.tail,
                                    }
                                )
                    step_list.append(triple_list)
                json_triples.append(
                    {"triples": step_list, "text": text, "filename": file_name}
                )
            except EOFError:
                break

    with open(triple_json_path, "w") as triple_json_file:
        json.dump(json_triples, triple_json_file, indent=4)
        print(f"Saved json to {triple_json_path}")


if __name__ == "__main__":
    from paths import triple_json_path, triple_pkl_path

    convert_and_save_triples_to_json(triple_pkl_path, triple_json_path)
