import os
import pickle
import sys
import tempfile

sys.path.append("..")  # isort:skip
from parser import args

os.environ["BAML_LOG"] = args.loglevel  # isort:skip
from baml.baml_client.sync_client import b  # isort:skip
from baml.baml_client.types import Entities, Message, Triples  # isort:skip
from baml.baml_client.type_builder import TypeBuilder
from clients import cr
from converter import convert_and_save_triples_to_json
from documents import all_ner_paths, texts
from paths import triple_json_path, triple_pkl_path, uniprot_path
from prompts import prompts, rel_system_prompt

tb = TypeBuilder()
if not args.noconfidence:
    tb.Triple.add_property(
        "confidence", tb.union([tb.literal_string("high"), tb.literal_string("low")])
    ).description("if this relation was extracted with high confidence or not")

if args.chattype == "lookup":
    with open(uniprot_path, "r") as lookupfile:
        lookup_table = {
            line.split("\t")[0]: (line.split("\t")[1], line.split("\t")[2])
            for line in lookupfile.readlines()[1:]
        }

if args.dynex:
    from datasets import concatenate_datasets
    from embed import client, embed_model, load_index
    from finetuning_tools import get_dataset

    index = load_index()
    train_dataset, dev_dataset, _ = get_dataset()
    lookup_dataset = concatenate_datasets([train_dataset, dev_dataset])

print(f"New run: {triple_pkl_path.parent}")


def extract_ners(messages, responses, text, doc, prompts):
    ner_prompt = prompts.pop(0)
    message = Message(role="user", content=ner_prompt)
    messages.append(message)
    try:
        if not args.all_ners_given:
            response = b.ExtractNEs(
                rel_system_prompt,
                text,
                message,
                {"client_registry": cr, "tb": tb},
            )
        else:
            ner_path = [
                x for x in all_ner_paths if doc[0].metadata["file_path"].stem == x.stem
            ][0]
            if ner_path:
                ners = open(ner_path, "r").readlines()
                ners = [x.strip() for x in ners]
            else:
                ners = []
            response = Entities(entities=ners)
    except:
        print(f"Exception at Entity extraction")
        response = Entities(entities=[])
    responses.append(response)
    messages.append(Message(role="assistant", content=f"{str(response)}"))
    return prompts


def extract_rels(messages, responses, text, prompts):
    for i, prompt in enumerate(prompts):
        messages.append(Message(role="user", content=f"\nUSER QUESTION: {prompt}"))
        try:
            response = b.GeneralChatExtractRelationships(
                rel_system_prompt, text, messages, {"client_registry": cr, "tb": tb}
            )
        except Exception as e:
            print(f"Exception at step {i}")
            response = Triples(triples=[])
        responses.append(response)
        messages.append(Message(role="assistant", content=str(response)))


def lookup_infos(messages, responses):
    infos = dict()
    ent_set = set()
    for nes in responses[-1]:
        for ne in nes[1]:
            if ne in ent_set:
                continue
            ent_set.add(ne)
            if ne.lower() in lookup_table:
                infos[ne] = f"Function: {lookup_table[ne.lower()][0].strip()}"
    messages.append(Message(role="user", content=f"BACKGROUND KNOWLEDGE: {infos}\n"))


def get_dynex(messages, text):
    embed = client.embed(
        model=embed_model,
        input=text,
    ).embeddings
    labels, _ = index.knn_query(embed, k=1)
    example = lookup_dataset[labels[0]]
    example_text = "\n".join([example["doc"][0], example["triples"][0]])
    messages.append(Message(role="user", content=f"EXAMPLE: {example_text}\n"))


def main():
    file = triple_pkl_path if not args.dev else tempfile.NamedTemporaryFile().name
    with open(file, "wb") as triple_pkl_file:
        for i, doc in enumerate(texts):
            _prompts = prompts.copy()
            print(f"Doc {i}")
            text = doc[0].page_content
            messages = list()
            responses = list()
            if args.extractionmode == "nerrel":
                _prompts = extract_ners(messages, responses, text, doc, _prompts)
            if args.all_ners_given:
                _prompts.pop(0)
            if args.chattype == "lookup":
                lookup_infos(messages, responses)
            if args.dynex:
                get_dynex(messages, text)
            extract_rels(messages, responses, text, _prompts)
            if not args.dev:
                pickle.dump(
                    (responses, doc[0].page_content, doc[0].metadata["file_path"]),
                    triple_pkl_file,
                )

    if not args.dev:
        convert_and_save_triples_to_json(triple_pkl_path, triple_json_path)


if __name__ == "__main__":
    main()
