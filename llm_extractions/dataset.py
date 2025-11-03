import json

from datasets import Dataset, load_from_disk
from pydantic.json import pydantic_encoder

from baml.baml_client.types import Triple, Triples

# from documents import all_docs
from paths import finetune_data_path, regulatome_ppi_eval_path, regulatome_tf_eval_path
from prompts import OUTPUT_FORMAT, prompts, rel_system_prompt


def get_dataset(target, data, tokenizer=None, force_new=False):
    if tokenizer and (
        not (finetune_data_path / f"{data}_{target}_train_dataset").exists()
        or force_new
    ):
        raise

        def chat_conversion(test=False):
            def _chat_conversion(data):
                doc = [
                    x
                    for x in all_docs
                    if x.metadata["file_path"].stem == data["file_stem"]
                ][0].page_content
                relations = [x.strip() for x in data["relations"].split(";")]
                relations = [(x.split("=")[0], x.split("=")[1]) for x in relations]
                triples = [
                    Triple(head=x[0], relation="INTERACTS_WITH", tail=x[1])
                    for x in relations
                ]

                triples = Triples(triples=triples)
                formatted_triples = f"```json\n{json.dumps(triples.model_dump(), default=pydantic_encoder, indent=2)}\n```"

                conversations = [
                    {"role": "system", "content": rel_system_prompt},
                    {"role": "system", "content": f"TEXT: {doc}"},
                    {
                        "role": "system",
                        "content": f"Use the following OUTPUT FORMAT:\n{OUTPUT_FORMAT}",
                    },
                    {"role": "user", "content": f"USER QUESTION {prompts[0]}"},
                ]
                assistant_msg = {"role": "assistant", "content": formatted_triples}
                if not test:
                    conversations.append(assistant_msg)
                    texts = tokenizer.apply_chat_template(
                        conversations, tokenize=False, add_generation_prompt=False
                    )
                else:
                    texts = tokenizer.apply_chat_template(
                        conversations, tokenize=False, add_generation_prompt=True
                    )
                return (
                    {"text": texts, "doc": doc, "triples": formatted_triples}
                    if not test
                    else {
                        "text": texts,
                        "assistant": assistant_msg,
                        "doc": doc,
                        "triples": formatted_triples,
                    }
                )

            return _chat_conversion

        # if data == "regulatome":
        eval_path = (
            regulatome_ppi_eval_path if target == "ppi" else regulatome_tf_eval_path
        )
        # elif data == "biored":
        #     eval_path = biored_eval_path
        with open(eval_path, "r") as f:
            eval_data = [
                (x.split("\t")[0], x.split("\t")[1], x.split("\t")[2].strip())
                for x in f.readlines()[1:]
            ]

        eval_data = [
            {"file_stem": x[0], "relations": x[1], "split": x[2]} for x in eval_data
        ]
        train_data = [x for x in eval_data if x["split"] == "Train"]
        dev_data = [x for x in eval_data if x["split"] == "Devel"]
        test_data = [x for x in eval_data if x["split"] == "Test"]
        train_dataset = Dataset.from_list(train_data)
        dev_dataset = Dataset.from_list(dev_data)
        test_dataset = Dataset.from_list(test_data)
        train_dataset = train_dataset.map(chat_conversion(), batched=False)
        dev_dataset = dev_dataset.map(chat_conversion(), batched=False)
        test_dataset = test_dataset.map(chat_conversion(test=True), batched=False)
        train_dataset.save_to_disk(
            finetune_data_path / f"{data}_{target}_train_dataset"
        )
        dev_dataset.save_to_disk(finetune_data_path / f"{data}_{target}_dev_dataset")
        test_dataset.save_to_disk(finetune_data_path / f"{data}_{target}_test_dataset")
    else:
        train_dataset = load_from_disk(
            finetune_data_path / f"{data}_{target}_train_dataset"
        )
        dev_dataset = load_from_disk(
            finetune_data_path / f"{data}_{target}_dev_dataset"
        )
        test_dataset = load_from_disk(
            finetune_data_path / f"{data}_{target}_test_dataset"
        )

    return train_dataset, dev_dataset, test_dataset
