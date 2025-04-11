import json

import torch
from baml.baml_client.types import Triple, Triples
from clients import hf_model_id
from datasets import Dataset, load_from_disk
from documents import all_docs
from paths import finetune_data_path, regulatome_eval_path
from peft import LoraConfig, prepare_model_for_kbit_training
from prompts import OUTPUT_FORMAT, prompts, rel_system_prompt
from pydantic.json import pydantic_encoder
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


def get_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(
        hf_model_id, use_fast=True, trust_remote_code=True
    )

    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.pad_token_id = tokenizer.eos_token_id
    tokenizer.padding_side = "left"

    tokenizer.model_max_length = 120_000
    if hasattr(tokenizer, "chat_template") and tokenizer.chat_template is not None:
        tokenizer.chat_template = None  # Reset the chat template
    return tokenizer


def get_bnb_config():
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )
    return bnb_config


def get_model(bnb_config):
    device_map = (
        {"": torch.cuda.current_device()} if torch.cuda.is_available() else None
    )
    model = AutoModelForCausalLM.from_pretrained(
        hf_model_id,
        device_map=device_map,
        attn_implementation="flash_attention_2",
        quantization_config=bnb_config,
    )
    return model


def get_peft_config():
    peft_config = LoraConfig(
        lora_alpha=128,  # 32
        lora_dropout=0.05,
        r=256,  # 16
        bias="none",
        target_modules=[
            "q_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
            "k_proj",
            "v_proj",
        ],
        task_type="CAUSAL_LM",
    )
    return peft_config


def get_dataset(tokenizer=None, force_new=False):
    if tokenizer and (
        not (finetune_data_path / "regulatome_train_dataset").exists() or force_new
    ):

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
                if test:
                    assistant_msg = tokenizer.apply_chat_template(
                        [assistant_msg], tokenize=False, add_generation_prompt=False
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

        with open(regulatome_eval_path, "r") as f:
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
        train_dataset.save_to_disk(finetune_data_path / "regulatome_train_dataset")
        dev_dataset.save_to_disk(finetune_data_path / "regulatome_dev_dataset")
        test_dataset.save_to_disk(finetune_data_path / "regulatome_test_dataset")

    train_dataset = load_from_disk(finetune_data_path / "regulatome_train_dataset")
    dev_dataset = load_from_disk(finetune_data_path / "regulatome_dev_dataset")
    test_dataset = load_from_disk(finetune_data_path / "regulatome_test_dataset")
    return train_dataset, dev_dataset, test_dataset
