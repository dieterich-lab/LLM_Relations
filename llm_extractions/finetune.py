import os
import sys

import torch

from clients import hf_model_id

from unsloth import FastLanguageModel  # isort:skip
from unsloth import is_bfloat16_supported  # isort:skip
from unsloth.chat_templates import get_chat_template  # isort:skip

from paths import sft_model_path  # isort:skip
from transformers import TrainingArguments  # isort:skip
from transformers import TextStreamer  # isort:skip
from trl import SFTTrainer  # isort:skip

sys.path.append("..")  # isort:skip
from parser import args

args.noconfidence = True

from huggingface_hub import login
from transformers import TrainingArguments
from trl import SFTTrainer
from unsloth.chat_templates import train_on_responses_only

from dataset import get_dataset

hf_key = os.getenv("HF_ACCESS_TOKEN")
login(token=hf_key, add_to_git_credential=True)

max_seq_length = 120_000
dtype = None
load_in_4bit = True


model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=hf_model_id,
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit,
    token=hf_key,
)

# Available templates:
# ['unsloth', 'zephyr', 'chatml', 'mistral', 'llama', 'vicuna', 'vicuna_old', 'vicuna old', 'alpaca', 'gemma', 'gemma_chatml', 'gemma2', 'gemma2_chatml', 'llama-3', 'llama3', 'phi-3', 'phi-35', 'phi-3.5', 'llama-3.1', 'llama-31', 'llama-3.2', 'llama-3.3', 'llama-32', 'llama-33', 'qwen-2.5', 'qwen-25', 'qwen25', 'qwen2.5', 'phi-4', 'gemma-3', 'gemma3']

chat_dict = {
    "llama33": "llama-33",
    "llama31": "llama-31",
    "gemma": "gemma-3",
}

tokenizer = get_chat_template(
    tokenizer,
    chat_template="chatml",
    # chat_template=chat_dict[args.model],
    map_eos_token=True,
)

train_dataset, dev_dataset, test_dataset = get_dataset(
    target=args.target, data=args.data, tokenizer=tokenizer, force_new=True
)

print(f"Len train set: {len(train_dataset)}, len dev set: {len(dev_dataset)}")


# Training
if args.train:
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ],
        lora_alpha=16,
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=3407,
        use_rslora=False,
        loftq_config=None,
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=dev_dataset,
        dataset_text_field="text",
        max_seq_length=max_seq_length,
        dataset_num_proc=2,
        packing=False,
        args=TrainingArguments(
            disable_tqdm=True,
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            warmup_steps=5,
            # eval_strategy="epoch",
            do_eval=False,
            num_train_epochs=2,
            learning_rate=2e-4,
            fp16=not is_bfloat16_supported(),
            bf16=is_bfloat16_supported(),
            logging_steps=1,
            optim="adamw_8bit",
            weight_decay=0.01,
            lr_scheduler_type="linear",
            seed=3407,
            output_dir=sft_model_path,
            report_to="none",
        ),
    )

    trainer = train_on_responses_only(
        trainer,
        instruction_part="<|im_start|>system\n",
        response_part="<|im_start|>assistant\n",
    )

    t1 = trainer.train_dataset[0]["input_ids"]
    d1 = tokenizer.decode(t1)
    print(d1)

    t2 = trainer.train_dataset[0]["labels"]
    d2 = tokenizer.decode(
        [tokenizer.pad_token_id if x == -100 else x for x in t2]
    ).replace(tokenizer.pad_token, " ")
    print(d2)

    print(d1 == d2)

    gpu_stats = torch.cuda.get_device_properties(0)
    start_gpu_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
    max_memory = round(gpu_stats.total_memory / 1024 / 1024 / 1024, 3)
    print(f"GPU = {gpu_stats.name}. Max memory = {max_memory} GB.")
    print(f"{start_gpu_memory} GB of memory reserved.")

    trainer_stats = trainer.train()

# Saving
if args.save and not args.load:
    print(f"Saving model to {sft_model_path}_{args.target}_merged_16bit")
    model.save_pretrained_merged(
        f"{sft_model_path}_{args.target}_merged_16bit",
        tokenizer,
        save_method="merged_16bit",
    )
    model.save_pretrained_merged(
        f"{sft_model_path}_{args.target}_lora",
        tokenizer,
        save_method="lora",
    )
    model.save_pretrained_gguf(
        f"{sft_model_path}_{args.target}_GGUF",
        tokenizer,
        quantization_method=["q4_k_m"],
    )
if args.push and not args.load:
    model.push_to_hub_merged(
        f"phiwi/{sft_model_path.name}_{args.target}_lora",
        tokenizer,
        save_method="lora",
        token=hf_key,
    )

# Loading
if args.load:
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=f"{sft_model_path}_{args.target}_lora",
        max_seq_length=max_seq_length,
        dtype=dtype,
        load_in_4bit=load_in_4bit,
    )
    if args.save:
        model.save_pretrained_merged(
            f"{sft_model_path}_{args.target}_lora",
            tokenizer,
            save_method="lora",
        )
    if args.push:
        model.push_to_hub_merged(
            f"phiwi/{sft_model_path.name}_{args.target}_lora",
            tokenizer,
            save_method="lora",
            token=hf_key,
        )

# Generation
if True:
    FastLanguageModel.for_inference(model)

    inputs = tokenizer(test_dataset[0]["text"], return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=5_000, use_cache=True)
    print(tokenizer.batch_decode(outputs))

    # text_streamer = TextStreamer(tokenizer)
    # _ = model.generate(**inputs, streamer=text_streamer, max_new_tokens=5_000)
    # pass
